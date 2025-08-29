-- Script kiểm tra và tạo role-permission cho B2B Company Management
-- ========================================

-- PHẦN 1: KIỂM TRA HIỆN TRẠNG
-- ========================================

-- 1.1. Kiểm tra role hiện tại
SELECT '=== ROLE HIỆN TẠI ===' as Info;
SELECT ID, Name, FacID, Active, Description
FROM [Security].dbo.Roles 
WHERE ID = '021E2E86-D577-47DA-97D5-F42DB71EDB27';

-- 1.2. Kiểm tra tất cả permissions B2B
SELECT '=== PERMISSIONS B2B ===' as Info;
SELECT ID, [Key], Name, Category, Description
FROM [Security].dbo.Permissions 
WHERE [Key] LIKE N'%HỆ THỐNG.QUẢN LÝ CÔNG TY B2B%'
ORDER BY [Key];

-- 1.3. Kiểm tra role-permissions hiện tại
SELECT '=== ROLE-PERMISSIONS HIỆN TẠI ===' as Info;
SELECT rp.RoleID, rp.PermissionID, rp.FacID,
       r.Name as RoleName,
       p.[Key] as PermissionKey,
       p.Name as PermissionName
FROM [Security].dbo.RolePermissions rp
JOIN [Security].dbo.Roles r ON r.ID = rp.RoleID
JOIN [Security].dbo.Permissions p ON p.ID = rp.PermissionID
WHERE r.ID = '021E2E86-D577-47DA-97D5-F42DB71EDB27';

-- ========================================
-- PHẦN 2: TẠO ROLE-PERMISSIONS
-- ========================================

-- 2.1. Tìm tất cả permissions B2B cần thiết
DECLARE @RoleID UNIQUEIDENTIFIER = '021E2E86-D577-47DA-97D5-F42DB71EDB27';
DECLARE @FacID VARCHAR(10) = '8.1'; -- Thay đổi nếu cần

-- 2.2. Tạo role-permissions cho tất cả quyền B2B
INSERT INTO [Security].dbo.RolePermissions (RoleID, PermissionID, FacID, CreatedOn, CreatedBy)
SELECT 
    @RoleID as RoleID,
    p.ID as PermissionID,
    @FacID as FacID,
    GETDATE() as CreatedOn,
    NULL as CreatedBy -- Thay đổi thành UserID nếu cần
FROM [Security].dbo.Permissions p
WHERE p.[Key] LIKE N'%HỆ THỐNG.QUẢN LÝ CÔNG TY B2B%'
AND NOT EXISTS (
    SELECT 1 FROM [Security].dbo.RolePermissions rp 
    WHERE rp.RoleID = @RoleID AND rp.PermissionID = p.ID
);

-- 2.3. Hiển thị kết quả sau khi insert
SELECT '=== ROLE-PERMISSIONS SAU KHI TẠO ===' as Info;
SELECT rp.RoleID, rp.PermissionID, rp.FacID,
       r.Name as RoleName,
       p.[Key] as PermissionKey,
       p.Name as PermissionName
FROM [Security].dbo.RolePermissions rp
JOIN [Security].dbo.Roles r ON r.ID = rp.RoleID
JOIN [Security].dbo.Permissions p ON p.ID = rp.PermissionID
WHERE r.ID = @RoleID
ORDER BY p.[Key];

-- ========================================
-- PHẦN 3: KIỂM TRA QUYỀN CỦA USER
-- ========================================

-- 3.1. Kiểm tra user có role này không
SELECT '=== USER-ROLE ===' as Info;
SELECT ur.UserID, ur.RoleID, ur.FacID,
       u.UserName,
       r.Name as RoleName
FROM [Security].dbo.UserRoles ur
JOIN [Security].dbo.Users u ON ur.UserID = u.ID
JOIN [Security].dbo.Roles r ON ur.RoleID = r.ID
WHERE ur.RoleID = @RoleID;

-- 3.2. Kiểm tra quyền của user thông qua stored procedure
SELECT '=== QUYỀN CỦA USER ===' as Info;
-- Chạy stored procedure ws_UserPermissions_List với SessionID và FacID
-- EXEC ws_UserPermissions_List @SessionID = 'YOUR_SESSION_ID', @FacID = @FacID;

-- ========================================
-- PHẦN 4: SCRIPT XÓA QUYỀN (TEST)
-- ========================================

-- 4.1. Script để xóa quyền EDIT (test)
SELECT '=== SCRIPT XÓA QUYỀN EDIT ===' as Info;
SELECT 
    'DELETE FROM [Security].dbo.RolePermissions WHERE RoleID = ''' + CAST(@RoleID AS VARCHAR(50)) + ''' AND PermissionID = ''' + 
    CAST(p.ID AS VARCHAR(50)) + '; -- ' + p.[Key] as DeleteScript
FROM [Security].dbo.Permissions p
WHERE p.[Key] LIKE N'%HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.CHỈNH SỬA%';

-- 4.2. Script để khôi phục quyền EDIT
SELECT '=== SCRIPT KHÔI PHỤC QUYỀN EDIT ===' as Info;
SELECT 
    'INSERT INTO [Security].dbo.RolePermissions (RoleID, PermissionID, FacID, CreatedOn, CreatedBy) VALUES (''' + 
    CAST(@RoleID AS VARCHAR(50)) + ''', ''' + CAST(p.ID AS VARCHAR(50)) + ''', ''' + @FacID + ''', GETDATE(), NULL);' as RestoreScript
FROM [Security].dbo.Permissions p
WHERE p.[Key] LIKE N'%HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.CHỈNH SỬA%';
