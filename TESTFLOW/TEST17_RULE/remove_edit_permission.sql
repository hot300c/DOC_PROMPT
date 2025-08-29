-- Script để xóa quyền EDIT khỏi role (test)
-- Thay thế các giá trị sau:
-- @UserName: tên user của bạn (ví dụ: 'phucnnd')
-- @FacID: ID của facility (ví dụ: '8.1')

DECLARE @UserName VARCHAR(50) = 'phucnnd'; -- Thay đổi thành username của bạn
DECLARE @FacID VARCHAR(10) = '8.1'; -- Thay đổi thành FacID của bạn

-- Tìm UserID
DECLARE @UserID UNIQUEIDENTIFIER;
SELECT @UserID = ID FROM Users WHERE UserName = @UserName;

IF @UserID IS NULL
BEGIN
    PRINT 'Không tìm thấy user: ' + @UserName;
    RETURN;
END

-- Tìm RoleID mà user đang có
DECLARE @RoleID UNIQUEIDENTIFIER;
SELECT @RoleID = ur.RoleID 
FROM UserRoles ur
JOIN Roles r ON ur.RoleID = r.ID
WHERE ur.UserID = @UserID AND r.FacID = @FacID;

IF @RoleID IS NULL
BEGIN
    PRINT 'Không tìm thấy role cho user ' + @UserName + ' tại FacID ' + @FacID;
    RETURN;
END

-- Tìm PermissionID của quyền EDIT
DECLARE @PermissionID UNIQUEIDENTIFIER;
SELECT @PermissionID = ID 
FROM Permissions 
WHERE PermissionKey = 'HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.CHỈNH SỬA';

IF @PermissionID IS NULL
BEGIN
    PRINT 'Không tìm thấy permission: HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.CHỈNH SỬA';
    RETURN;
END

-- Hiển thị thông tin trước khi xóa
PRINT 'Thông tin trước khi xóa:';
PRINT 'User: ' + @UserName + ' (ID: ' + CAST(@UserID AS VARCHAR(50)) + ')';
PRINT 'Role ID: ' + CAST(@RoleID AS VARCHAR(50));
PRINT 'Permission ID: ' + CAST(@PermissionID AS VARCHAR(50));

-- Kiểm tra xem role có quyền EDIT không
IF EXISTS (SELECT 1 FROM RolePermissions WHERE RoleID = @RoleID AND PermissionID = @PermissionID)
BEGIN
    -- Xóa quyền EDIT khỏi role
    DELETE FROM RolePermissions 
    WHERE RoleID = @RoleID 
    AND PermissionID = @PermissionID;
    
    PRINT 'Đã xóa quyền EDIT thành công!';
    PRINT 'Bây giờ user ' + @UserName + ' sẽ không thể chỉnh sửa công ty B2B.';
    PRINT '';
    PRINT 'Để khôi phục quyền, chạy script sau:';
    PRINT 'INSERT INTO RolePermissions (RoleID, PermissionID) VALUES (''' + CAST(@RoleID AS VARCHAR(50)) + ''', ''' + CAST(@PermissionID AS VARCHAR(50)) + ''');';
END
ELSE
BEGIN
    PRINT 'Role này không có quyền EDIT để xóa.';
END







