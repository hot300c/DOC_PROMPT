# Hướng dẫn Phân quyền (Permission System)

## Tổng quan

Hệ thống phân quyền trong Genie sử dụng **Permission-based Access Control** với các permission key được định nghĩa trong `PermissionEnum` và được quản lý thông qua `AppPermissionsProvider`.

## Cấu trúc hệ thống

### 1. Permission Provider
```tsx
// app/(main)/layout.tsx
<AppPermissionsProvider
  permissions={permissions}        // Tất cả permissions của facility
  userPermissions={userPermissions} // Permissions của user hiện tại
  baseSettings={baseSettings}
  vaccineTooltips={vaccineTooltips}
>
  {children}
</AppPermissionsProvider>
```

### 2. Permission Hook
```tsx
// components/app-permissions/app-permissions.tsx
export const useAppPermissions = () => {
  const context = use(AppPermissionsContext);
  if (!context) {
    throw new Error("useAppPermissions must be used within a AppPermissionsProvider");
  }
  return context;
};
```

### 3. Permission Functions
```tsx
interface AppPermissionsContextProps {
  hasPermission: (name: string) => boolean;           // Kiểm tra 1 permission
  hasAnyOfPermissions: (names: string[]) => boolean;  // Kiểm tra 1 trong nhiều permissions
}
```

## Cách sử dụng

### 1. Import và sử dụng hook
```tsx
import { useAppPermissions } from "@/components/app-permissions/app-permissions";
import { PermissionEnum } from "@/app/lib/enums";

export default function MyComponent() {
  const { hasPermission, hasAnyOfPermissions } = useAppPermissions();
  
  // Kiểm tra 1 permission
  const canEdit = hasPermission(PermissionEnum.RECEPTION_EDIT_ADMIN_INFO);
  
  // Kiểm tra 1 trong nhiều permissions
  const canExport = hasAnyOfPermissions([
    PermissionEnum.RECEPTION_EXPORT_EXCEL_PATIENT_LIST,
    PermissionEnum.PAYMENT_EXPORT_DATA
  ]);
  
  return (
    <div>
      {canEdit && <Button>Chỉnh sửa</Button>}
      {canExport && <Button>Export</Button>}
    </div>
  );
}
```

### 2. Conditional Rendering
```tsx
// Hiển thị/ẩn component dựa trên permission
{hasPermission(PermissionEnum.RECEPTION_SHOW_VACCINE_TAB) && (
  <TabsTrigger value="vaccine">Vaccine</TabsTrigger>
)}

// Hiển thị/ẩn button dựa trên permission
{hasPermission(PermissionEnum.RECEPTION_CHANGE_APPOINTMENT_ORDER) && (
  <Button onClick={() => setIsOpenEditTNNModal(true)}>
    Chỉnh sửa thứ tự KH đi cùng
  </Button>
)}
```

### 3. Disable button dựa trên permission
```tsx
<Button 
  disabled={!hasPermission(PermissionEnum.HANGDOIDOC_CAUHINHFILEXML)}
  onClick={handleAction}
>
  Thực hiện
</Button>
```

## Định nghĩa Permission

### 1. Thêm Permission vào PermissionEnum
```tsx
// app/lib/enums.ts
export enum PermissionEnum {
  // Existing permissions...
  B2B_COMPANY_VIEW = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.XEM",
  B2B_COMPANY_CREATE = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.TẠO MỚI",
  B2B_COMPANY_EDIT = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.CHỈNH SỬA",
  B2B_COMPANY_DELETE = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.XÓA",
  B2B_COMPANY_EXPORT = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.XUẤT EXCEL",
  B2B_COMPANY_IMPORT = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.NHẬP EXCEL",
}
```

### 2. Naming Convention
- **Format**: `MODULE.FEATURE.ACTION`
- **Ví dụ**: `HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.XEM`
- **Actions phổ biến**: `XEM`, `TẠO MỚI`, `CHỈNH SỬA`, `XÓA`, `XUẤT EXCEL`, `NHẬP EXCEL`

## Implementation cho B2B Company Management

### 1. Import permissions
```tsx
import { useAppPermissions } from "@/components/app-permissions/app-permissions";
import { PermissionEnum } from "@/app/lib/enums";

export default function CompanyB2BPage() {
  const { hasPermission } = useAppPermissions();
  
  // Define permissions
  const canView = hasPermission(PermissionEnum.B2B_COMPANY_VIEW);
  const canCreate = hasPermission(PermissionEnum.B2B_COMPANY_CREATE);
  const canEdit = hasPermission(PermissionEnum.B2B_COMPANY_EDIT);
  const canDelete = hasPermission(PermissionEnum.B2B_COMPANY_DELETE);
  const canExport = hasPermission(PermissionEnum.B2B_COMPANY_EXPORT);
  const canImport = hasPermission(PermissionEnum.B2B_COMPANY_IMPORT);
  
  // Early return nếu không có quyền xem
  if (!canView) {
    return <div>Bạn không có quyền truy cập trang này</div>;
  }
  
  return (
    <>
      <CenterInfo page={PageName.B2B_COMPANY_MANAGEMENT} />
      
      <div className="w-full bg-muted p-4">
        <div className="flex gap-2 items-end justify-between flex-wrap">
          <div className="flex gap-2 items-end">
            <div className="flex flex-col">
              <label className="text-sm">Từ khóa</label>
              <Input
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="Mã / Tên / MST / Địa chỉ / HĐ"
                className="w-[300px]"
              />
            </div>
            <Button variant="outline">Tìm kiếm</Button>
          </div>
          <div className="flex gap-2 items-end">
            {canCreate && (
              <Button
                onClick={() => {
                  onReset();
                  setIsModalOpen(true);
                }}
                variant="default"
              >
                Thêm mới
              </Button>
            )}
            {canExport && (
              <Button onClick={() => onExport()} variant="secondary">
                Export CSV
              </Button>
            )}
            {canImport && (
              <Button
                variant="outline"
                onClick={() => setIsImportModalOpen(true)}
              >
                Import Excel
              </Button>
            )}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-md border">
        <DataTable
          className="w-full"
          data={rows}
          columns={columns}
          enablePaging={false}
          enableColumnFilter={true}
          isLoading={loading}
        />
      </div>

      {/* Actions trong table */}
      <DeprecatedTableCell className="text-center">
        <div className="flex gap-2 justify-center">
          {canEdit && (
            <Button size="sm" onClick={() => onEdit(r)}>
              Sửa
            </Button>
          )}
          {canDelete && (
            <Button 
              size="sm" 
              variant="outline" 
              onClick={() => onToggle(r.CompanyB2Bid || r.CompanyB2BID)}
            >
              Toggle
            </Button>
          )}
        </div>
      </DeprecatedTableCell>
    </>
  );
}
```

### 2. Cập nhật columns definition
```tsx
const columns: ColumnDef<any>[] = useMemo(() => [
  // ... other columns
  {
    id: "actions",
    header: "Hành động",
    cell: ({ row }) => (
      <div className="flex gap-2 justify-center">
        {canEdit && (
          <Button size="sm" onClick={() => onEdit(row.original)}>
            Sửa
          </Button>
        )}
        {canDelete && (
          <Button 
            size="sm" 
            variant="outline" 
            onClick={() => onToggle(row.original.CompanyB2Bid || row.original.CompanyB2BID)}
          >
            Toggle
          </Button>
        )}
      </div>
    ),
  },
], [canEdit, canDelete]);
```

## Các bước thực hiện

### 1. Định nghĩa Permissions
- [ ] Thêm permission keys vào `PermissionEnum`
- [ ] Đặt tên theo convention: `MODULE.FEATURE.ACTION`

### 2. Setup Permission Provider
- [ ] Đảm bảo `AppPermissionsProvider` đã được wrap trong layout
- [ ] Kiểm tra permissions được load từ server

### 3. Implement trong Component
- [ ] Import `useAppPermissions` và `PermissionEnum`
- [ ] Define permission variables
- [ ] Thêm early return nếu không có quyền xem
- [ ] Wrap buttons/actions với permission checks

### 4. Test Permissions
- [ ] Test với user có đầy đủ quyền
- [ ] Test với user thiếu quyền
- [ ] Test với user không có quyền nào

## Best Practices

### 1. Permission Naming
```tsx
// ✅ Tốt
B2B_COMPANY_VIEW = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.XEM"
B2B_COMPANY_CREATE = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.TẠO MỚI"

// ❌ Không tốt
B2B_VIEW = "B2B_VIEW"
COMPANY_MANAGEMENT = "COMPANY_MANAGEMENT"
```

### 2. Permission Granularity
```tsx
// ✅ Tốt - Chi tiết từng action
B2B_COMPANY_VIEW = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.XEM"
B2B_COMPANY_CREATE = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.TẠO MỚI"
B2B_COMPANY_EDIT = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B.CHỈNH SỬA"

// ❌ Không tốt - Quá rộng
B2B_COMPANY_ALL = "HỆ THỐNG.QUẢN LÝ CÔNG TY B2B"
```

### 3. Error Handling
```tsx
// ✅ Tốt - Hiển thị thông báo rõ ràng
if (!canView) {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="text-center">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Không có quyền truy cập
        </h3>
        <p className="text-gray-600">
          Bạn không có quyền xem trang Quản lý công ty B2B
        </p>
      </div>
    </div>
  );
}
```

### 4. Loading States
```tsx
// ✅ Tốt - Hiển thị loading khi check permissions
const { hasPermission } = useAppPermissions();
const [permissionsLoaded, setPermissionsLoaded] = useState(false);

useEffect(() => {
  // Simulate permission loading
  setPermissionsLoaded(true);
}, []);

if (!permissionsLoaded) {
  return <div>Đang tải...</div>;
}
```

## Troubleshooting

### 1. Permission không hoạt động
- Kiểm tra permission key có đúng format không
- Kiểm tra permission đã được assign cho user chưa
- Kiểm tra `AppPermissionsProvider` đã được wrap chưa

### 2. Permission cache
- Permissions được cache 1 giờ
- User cần logout/login để apply changes ngay lập tức
- Hoặc đợi 1 giờ để cache expire

### 3. Debug permissions
```tsx
// Thêm debug để kiểm tra permissions
console.log('User permissions:', userPermissions);
console.log('Can edit:', hasPermission(PermissionEnum.B2B_COMPANY_EDIT));
```

## Checklist Implementation

### Trước khi commit
- [ ] Đã định nghĩa đầy đủ permissions trong `PermissionEnum`
- [ ] Đã implement permission checks cho tất cả actions
- [ ] Đã test với user có/không có quyền
- [ ] Đã handle error cases (không có quyền xem)
- [ ] Đã follow naming convention
- [ ] Đã có loading states
- [ ] Đã có error messages rõ ràng
