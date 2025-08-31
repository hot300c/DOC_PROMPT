-- Script lấy SessionID từ username và gọi SP ws_UserPermissions_List
-- ========================================

-- PHẦN 1: LẤY SESSIONID TỪ USERNAME
-- ========================================

DECLARE @UserName VARCHAR(50) = 'phucnnd'; -- Thay đổi username của bạn
DECLARE @FacID VARCHAR(10) = '8.1'; -- Thay đổi FacID nếu cần

-- 1.1. Tìm UserID từ username
DECLARE @UserID UNIQUEIDENTIFIER;
SELECT @UserID = ID FROM [Security].dbo.Users WHERE UserName = @UserName;

IF @UserID IS NULL
BEGIN
    PRINT 'Không tìm thấy user: ' + @UserName;
    RETURN;
END

PRINT 'User: ' + @UserName + ' (ID: ' + CAST(@UserID AS VARCHAR(50)) + ')';

-- 1.2. Tìm SessionID từ UserID
DECLARE @SessionID VARCHAR(MAX);
SELECT @SessionID = SessionID 
FROM [Security].dbo.Sessions 
WHERE UserID = @UserID 
ORDER BY CreatedOn DESC;

IF @SessionID IS NULL
BEGIN
    PRINT 'Không tìm thấy session cho user: ' + @UserName;
    PRINT 'Có thể user chưa login hoặc session đã hết hạn.';
    RETURN;
END

PRINT 'SessionID: ' + @SessionID;
PRINT 'FacID: ' + @FacID;
PRINT '';

-- ========================================
-- PHẦN 2: GỌI STORED PROCEDURE
-- ========================================

-- 2.1. Gọi SP để lấy permissions
PRINT '=== GỌI STORED PROCEDURE ws_UserPermissions_List ===';
EXEC [dbo].[ws_UserPermissions_List] 
    @SessionID = @SessionID,
    @FacID = @FacID;

-- ========================================
-- PHẦN 3: KIỂM TRA CHI TIẾT
-- ========================================

-- 3.1. Kiểm tra user có role gì
PRINT '';
PRINT '=== KIỂM TRA ROLE CỦA USER ===';
SELECT ur.UserID, ur.RoleID, ur.FacID,
       u.UserName,
       r.Name as RoleName,
       r.Active as RoleActive
FROM [Security].dbo.UserRoles ur
JOIN [Security].dbo.Users u ON ur.UserID = u.ID
JOIN [Security].dbo.Roles r ON ur.RoleID = r.ID
WHERE ur.UserID = @UserID;

-- 3.2. Kiểm tra role có permissions gì
PRINT '';
PRINT '=== KIỂM TRA PERMISSIONS CỦA ROLE ===';
SELECT r.Name as RoleName,
       p.[Key] as PermissionKey,
       p.Name as PermissionName,
       p.Category
FROM [Security].dbo.UserRoles ur
JOIN [Security].dbo.Roles r ON ur.RoleID = r.ID
JOIN [Security].dbo.RolePermissions rp ON r.ID = rp.RoleID
JOIN [Security].dbo.Permissions p ON rp.PermissionID = p.ID
WHERE ur.UserID = @UserID
ORDER BY p.Category, p.[Key];

-- 3.3. Kiểm tra xem có phải Administrator không
PRINT '';
PRINT '=== KIỂM TRA CÓ PHẢI ADMINISTRATOR KHÔNG ===';
DECLARE @IsAdmin BIT = 0;
SELECT @IsAdmin = CASE WHEN EXISTS (
    SELECT 1 FROM [Security].dbo.UserRoles ur
    JOIN [Security].dbo.Roles r ON ur.RoleID = r.ID
    WHERE ur.UserID = @UserID AND r.Name = 'Administrators' AND r.FacID = @FacID
) THEN 1 ELSE 0 END;

IF @IsAdmin = 1
    PRINT 'User ' + @UserName + ' là Administrator tại FacID ' + @FacID + ' (có tất cả permissions)';
ELSE
    PRINT 'User ' + @UserName + ' KHÔNG phải Administrator tại FacID ' + @FacID + ' (chỉ có permissions được gán)';

-- ========================================
-- PHẦN 4: TẠO SCRIPT TEST
-- ========================================

-- 4.1. Script để test với SessionID cụ thể
PRINT '';
PRINT '=== SCRIPT TEST VỚI SESSIONID ===';
PRINT '-- Copy và paste script này để test:';
PRINT 'EXEC [dbo].[ws_UserPermissions_List] @SessionID = ''' + @SessionID + ''', @FacID = ''' + @FacID + ''';';

-- 4.2. Script để tìm session mới nhất của user
PRINT '';
PRINT '=== SCRIPT TÌM SESSION MỚI NHẤT ===';
PRINT '-- Copy và paste script này để tìm session:';
PRINT 'SELECT TOP 5 SessionID, UserID, CreatedOn, IPAddress';
PRINT 'FROM [Security].dbo.Sessions';
PRINT 'WHERE UserID = ''' + CAST(@UserID AS VARCHAR(50)) + '''';
PRINT 'ORDER BY CreatedOn DESC;';
