-- Script kiểm tra quan hệ giữa ROLE, Permission và các bảng liên quan
-- Chạy từng phần để hiểu rõ cấu trúc

-- ========================================
-- PHẦN 1: KIỂM TRA CẤU TRÚC CÁC BẢNG
-- ========================================

-- 1.1. Cấu trúc bảng Roles
SELECT '=== CẤU TRÚC BẢNG ROLES ===' as Info;
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'Roles'
ORDER BY ORDINAL_POSITION;

-- 1.2. Cấu trúc bảng Permissions
SELECT '=== CẤU TRÚC BẢNG PERMISSIONS ===' as Info;
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'Permissions'
ORDER BY ORDINAL_POSITION;

-- 1.3. Cấu trúc bảng RolePermissions (bảng trung gian)
SELECT '=== CẤU TRÚC BẢNG ROLEPERMISSIONS ===' as Info;
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'RolePermissions'
ORDER BY ORDINAL_POSITION;

-- ========================================
-- PHẦN 2: KIỂM TRA DỮ LIỆU CÁC BẢNG
-- ========================================

-- 2.1. Xem tất cả Roles
SELECT '=== TẤT CẢ ROLES ===' as Info;
SELECT TOP 10 ID, Name, FacID, Description, CreatedOn, CreatedBy
FROM Security.dbo.Roles
ORDER BY CreatedOn DESC;

-- 2.2. Xem tất cả Permissions
SELECT '=== TẤT CẢ PERMISSIONS ===' as Info;
SELECT TOP 10 ID, Name, PermissionKey, Category, Description
FROM Security.dbo.Permissions
ORDER BY Category, Name;

-- 2.3. Xem tất cả RolePermissions
SELECT '=== TẤT CẢ ROLEPERMISSIONS ===' as Info;
SELECT TOP 10 rp.RoleID, rp.PermissionID, 
       r.Name as RoleName, 
       p.Name as PermissionName,
       p.PermissionKey
FROM Security.dbo.RolePermissions rp
JOIN Security.dbo.Roles r ON rp.RoleID = r.ID
JOIN Security.dbo.Permissions p ON rp.PermissionID = p.ID
ORDER BY r.Name, p.Category, p.Name;

-- ========================================
-- PHẦN 3: TÌM PERMISSIONS B2B
-- ========================================

-- 3.1. Tìm tất cả permissions có chữ B2B
SELECT '=== PERMISSIONS B2B ===' as Info;
SELECT ID, Name, PermissionKey, Category, Description
FROM Security.dbo.Permissions
WHERE Name LIKE '%B2B%' 
   OR PermissionKey LIKE '%B2B%'
   OR Name LIKE '%CÔNG TY%'
   OR Name LIKE '%CHỈNH SỬA%'
ORDER BY Category, Name;

-- 3.2. Kiểm tra permission ID đã biết
SELECT '=== PERMISSION ID ĐÃ BIẾT ===' as Info;
SELECT ID, Name, PermissionKey, Category, Description
FROM Security.dbo.Permissions
WHERE ID = '3128C1B7-D495-4EA8-A248-D3EB985F6B7C';

-- ========================================
-- PHẦN 4: KIỂM TRA ROLE CỤ THỂ
-- ========================================

-- 4.1. Tìm role theo FacID
SELECT '=== ROLES THEO FACID ===' as Info;
SELECT ID, Name, FacID, Description
FROM Security.dbo.Roles
WHERE FacID = '8.1'  -- Thay đổi FacID nếu cần
ORDER BY Name;

-- 4.2. Xem permissions của một role cụ thể
SELECT '=== PERMISSIONS CỦA ROLE ===' as Info;
-- Thay đổi RoleID dưới đây
DECLARE @TargetRoleID UNIQUEIDENTIFIER = 'YOUR_ROLE_ID_HERE'; -- Thay đổi thành RoleID thực tế

SELECT r.Name as RoleName, 
       p.Name as PermissionName,
       p.PermissionKey,
       p.Category
FROM Security.dbo.RolePermissions rp
JOIN Security.dbo.Roles r ON rp.RoleID = r.ID
JOIN Security.dbo.Permissions p ON rp.PermissionID = p.ID
WHERE r.ID = @TargetRoleID
ORDER BY p.Category, p.Name;

-- ========================================
-- PHẦN 5: TỔNG HỢP QUAN HỆ
-- ========================================

-- 5.1. Sơ đồ quan hệ tổng quát
SELECT '=== SƠ ĐỒ QUAN HỆ ===' as Info;
SELECT 'Users -> UserRoles -> Roles -> RolePermissions -> Permissions' as Relationship;

-- 5.2. Kiểm tra xem có permission nào bị orphan không
SELECT '=== PERMISSIONS ORPHAN ===' as Info;
SELECT p.ID, p.Name, p.PermissionKey
FROM Security.dbo.Permissions p
LEFT JOIN Security.dbo.RolePermissions rp ON p.ID = rp.PermissionID
WHERE rp.PermissionID IS NULL;
