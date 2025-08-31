-- Script kiểm tra cấu trúc bảng Permissions và tìm permission EDIT
-- Chạy script này trước để xem cấu trúc bảng

-- 1. Kiểm tra cấu trúc bảng Permissions
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'Permissions'
ORDER BY ORDINAL_POSITION;

-- 2. Tìm permission EDIT theo các cột có thể có
SELECT 'Theo Name:' as SearchType, ID, Name, PermissionKey, Category
FROM Security.dbo.Permissions 
WHERE Name LIKE '%B2B%' OR Name LIKE '%CÔNG TY%' OR Name LIKE '%CHỈNH SỬA%';

SELECT 'Theo PermissionKey:' as SearchType, ID, Name, PermissionKey, Category
FROM Security.dbo.Permissions 
WHERE PermissionKey LIKE '%B2B%' OR PermissionKey LIKE '%CÔNG TY%' OR PermissionKey LIKE '%CHỈNH SỬA%';

-- 3. Tìm tất cả permissions có chữ B2B
SELECT 'Tất cả B2B:' as SearchType, ID, Name, PermissionKey, Category
FROM Security.dbo.Permissions 
WHERE Name LIKE '%B2B%' OR PermissionKey LIKE '%B2B%';

-- 4. Kiểm tra xem permission ID đã biết có tồn tại không
SELECT 'Permission ID đã biết:' as SearchType, ID, Name, PermissionKey, Category
FROM Security.dbo.Permissions 
WHERE ID = '3128C1B7-D495-4EA8-A248-D3EB985F6B7C';
