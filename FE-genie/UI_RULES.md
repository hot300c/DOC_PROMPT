# UI Rules & Standards

## Table Components

### 1. Table Implementation
- **Sử dụng**: `DataTable` component từ `@/components/ui/dataTable` với sorting và filtering
- **Không sử dụng**: Custom table với `<table>`, `<th>`, `<td>` tự tạo
- **Không sử dụng**: `DeprecatedTable` components (đã lỗi thời)

```tsx
// ✅ ĐÚNG
import {
  DataTable,
  DataTableColumnHeaderSort,
} from "@/components/ui/dataTable";
import { ColumnDef } from "@tanstack/react-table";

const columns: ColumnDef<any>[] = useMemo(() => [
  {
    id: "field1",
    accessorKey: "field1",
    header: ({ column }) => (
      <DataTableColumnHeaderSort column={column} title="Header" />
    ),
    cell: ({ row }) => (
      <div className="text-center">{row.original.field1}</div>
    ),
  },
], []);

<DataTable
  className="w-full"
  data={rows}
  columns={columns}
  enablePaging={false}
  enableColumnFilter={true}
  isLoading={loading}
/>
```

// ❌ SAI
<table className="w-full">
  <thead>
    <tr>
      <th>Header</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Content</td>
    </tr>
  </tbody>
</table>
```

### 2. Table Styling
- **Header**: Tự động có `bg-blue-base text-white` từ DataTableColumnHeaderSort
- **Rows**: Tự động có alternating rows và hover effects
- **Sorting**: Click vào header để sort (asc/desc)
- **Filtering**: Icon filter trên header để lọc dữ liệu

## Layout Patterns

### 1. Search & Actions Layout
- **Container**: `bg-muted p-4`
- **Layout**: `flex gap-2 items-end justify-between flex-wrap`
- **Search Section**: Bên trái với input và button tìm kiếm
- **Actions Section**: Bên phải với các button actions

```tsx
// ✅ ĐÚNG
<div className="w-full bg-muted p-4">
  <div className="flex gap-2 items-end justify-between flex-wrap">
    <div className="flex gap-2 items-end">
      <div className="flex flex-col">
        <label className="text-sm">Từ khóa</label>
        <Input className="w-[300px]" />
      </div>
      <Button variant="outline">Tìm kiếm</Button>
    </div>
    <div className="flex gap-2 items-end">
      <Button variant="default">Thêm mới</Button>
      <Button variant="secondary">Export CSV</Button>
      <Button variant="outline">Import CSV</Button>
    </div>
  </div>
</div>
```

### 2. Page Structure (Chuẩn từ tiep-nhan/quan-ly-hop-dong)
- **FacilityInfo**: Đứng riêng biệt ở trên cùng
- **Form Filter**: `bg-muted p-4` với search và actions
- **Table Container**: `bg-white rounded-md border`
- **Footer**: `bg-muted py-2 px-4` với pagination

```tsx
// ✅ Cấu trúc chuẩn
<>
  <CenterInfo page={PageName.XXX} />
  
  <div className="w-full bg-muted p-4">
    {/* Search & Actions */}
  </div>

  <div className="bg-white rounded-md border">
    <DataTable
      data={rows}
      columns={columns}
      enablePaging={false}
      enableColumnFilter={true}
    />
  </div>

  <div className="w-full bg-muted py-2 px-4">
    {/* Footer pagination */}
  </div>
</>
```

### 3. Footer Layout
- **Container**: `bg-muted py-2 px-4`
- **Layout**: `flex justify-between items-center`
- **Left**: Thông tin tổng hợp
- **Right**: Pagination controls

```tsx
// ✅ ĐÚNG
<div className="w-full bg-muted py-2 px-4 flex justify-between items-center">
  <div className="text-sm">
    Tổng: {meta.Total} công ty
  </div>
  <div className="flex items-center space-x-2">
    <Button variant="outline" size="sm" disabled={loading || meta.Page <= 1}>
      Trước
    </Button>
    <span className="text-sm font-medium">
      Trang {meta.Page}
    </span>
    <Button variant="outline" size="sm" disabled={loading || meta.Page * meta.PageSize >= meta.Total}>
      Sau
    </Button>
    <select
      value={meta.PageSize}
      onChange={(e) => load(1, Number(e.target.value))}
      className="border rounded px-2 py-1 text-sm"
    >
      {pageSizeOptions.map((p) => (
        <option key={p} value={p}>{p}/trang</option>
      ))}
    </select>
  </div>
</div>
```

## Button Variants

### 1. Button Types
- **Primary Actions**: `variant="default"` (Thêm mới, Lưu, Tìm kiếm)
- **Secondary Actions**: `variant="secondary"` (Export, Xuất Excel)
- **Utility Actions**: `variant="outline"` (Import, Hủy, Toggle)
- **Small Buttons**: `size="sm"` (trong table cells, footer)

### 2. Button Order
1. **Thêm mới** (variant="default")
2. **Export/Import** (variant="secondary"/"outline")
3. **Utility actions** (variant="outline")

## Form Components

### 1. Input Layout
```tsx
function LabeledInput({ label, children }: { label: string; children: any }) {
  return (
    <label className="flex flex-col">
      <span className="text-sm">{label}</span>
      {children}
    </label>
  );
}
```

### 2. Modal Structure
```tsx
function Modal({ title, children, onClose }: { title: string; children: any; onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <div className="relative bg-white rounded shadow-lg w-[95vw] max-w-5xl p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="text-lg font-semibold">{title}</div>
          <button 
            onClick={onClose} 
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            aria-label="Đóng"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}
```

## Spacing & Typography

### 1. Text Sizes
- **Labels**: `text-sm`
- **Body text**: `text-sm`
- **Headers**: `text-lg font-semibold`
- **Table headers**: Tự động từ DeprecatedTableHead

### 2. Spacing
- **Gap between elements**: `gap-2`
- **Space between items**: `space-x-2`
- **Padding**: `p-2` cho containers, `px-2 py-1` cho small elements

## Color Classes

### 1. Background Colors
- **Muted background**: `bg-muted` (footers, alternating rows)
- **Muted with opacity**: `bg-muted/20` (alternating table rows)
- **Hover states**: `hover:bg-sky-blue` (table rows)

### 2. Text Colors
- **Primary text**: Default (no class needed)
- **Muted text**: `text-muted-foreground`
- **White text**: `text-white` (on colored backgrounds)

## Responsive Design

### 1. Grid Layouts
```tsx
// Form grid
<div className="grid grid-cols-1 md:grid-cols-3 gap-3">
  <LabeledInput label="Field 1">
    <Input />
  </LabeledInput>
  <LabeledInput label="Field 2">
    <Input />
  </LabeledInput>
</div>
```

### 2. Flexbox Layouts
```tsx
// Responsive flex
<div className="flex gap-2 items-end flex-wrap">
  {/* Content */}
</div>
```

## Import Statements

### 1. Required Imports
```tsx
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  DataTable,
  DataTableColumnHeaderSort,
} from "@/components/ui/dataTable";
import { ColumnDef } from "@tanstack/react-table";
```

## Common Patterns

### 1. Loading States
```tsx
const [loading, setLoading] = useState(false);

<Button disabled={loading} onClick={handleAction}>
  {loading ? "Đang xử lý..." : "Thực hiện"}
</Button>
```

### 2. Error Handling & Toast Notifications
```tsx
import { toast } from "sonner";
import { notifyError } from "@/app/lib/utils";

const onSave = async () => {
  try {
    const res = await saveData(payload);
    if (res?.message === "Success") {
      toast.success("Lưu dữ liệu thành công!");
      // Handle success
    } else {
      notifyError("Có lỗi xảy ra khi lưu dữ liệu!");
    }
  } catch (error) {
    notifyError("Có lỗi xảy ra khi lưu dữ liệu!");
    console.error('Save error:', error);
  }
};
```

### 3. Toast Notification Types
- **Success**: `toast.success("Thành công!")`
- **Error**: `notifyError("Có lỗi xảy ra!")` (từ utils)
- **Loading**: `notifyLoading("Đang xử lý...")` (từ utils)
- **Info**: `toast.info("Thông tin")`
- **Warning**: `toast.warning("Cảnh báo")`

### 4. Loading States with Toast
```tsx
// Tất cả async operations phải có loading toast
const handleAction = async () => {
  const toastId = notifyLoading("Đang xử lý...");
  try {
    await someAsyncOperation();
    toast.dismiss(toastId);
    toast.success("Thành công!");
  } catch (error) {
    toast.dismiss(toastId);
    notifyError("Có lỗi xảy ra!");
  }
};
```

### 5. Form Validation
```tsx
// Validation trước khi submit
const onSave = async () => {
  // Kiểm tra từng field cụ thể
  if (!form.field1?.trim()) {
    notifyError("Vui lòng nhập Field 1!");
    return;
  }
  if (!form.field2?.trim()) {
    notifyError("Vui lòng nhập Field 2!");
    return;
  }
  
  // Tiếp tục xử lý
  const toastId = notifyLoading("Đang lưu dữ liệu...");
  // ...
};
```

### 6. Export Validation
```tsx
// Kiểm tra dữ liệu trước khi export
const onExport = async () => {
  const toastId = notifyLoading("Đang export dữ liệu...");
  const data = await exportData();
  toast.dismiss(toastId);
  
  if (!data?.FileData) {
    notifyError("Không có dữ liệu để export! Vui lòng tải dữ liệu trước.");
    return;
  }
  // Tiếp tục xử lý export
};
```

### 4. File Upload with Validation
```tsx
// Import Modal với validation
const onImport = async (file: File) => {
  // Kiểm tra dữ liệu hiện có
  if (rows.length === 0) {
    alert("Không có dữ liệu để import! Vui lòng tải dữ liệu trước.");
    return;
  }

  // Kiểm tra kích thước file (5MB)
  const maxSize = 5 * 1024 * 1024;
  if (file.size > maxSize) {
    alert("File quá lớn! Kích thước tối đa cho phép là 5MB.");
    return;
  }

  // Kiểm tra extension
  const allowedExtensions = ['.xlsx', '.xls'];
  const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
  if (!allowedExtensions.includes(fileExtension)) {
    alert("Chỉ chấp nhận file Excel (.xlsx, .xls)!");
    return;
  }

  try {
    // Xử lý import
    const buf = await file.arrayBuffer();
    const base64 = btoa(String.fromCharCode(...new Uint8Array(buf)));
    await importData({ Base64Data: base64, FileName: file.name, UserID: userId });
    await loadData();
  } catch (error) {
    alert("Có lỗi xảy ra khi import file!");
    console.error('Import error:', error);
  }
};
```

### 5. Search Validation
```tsx
// Kiểm tra từ khóa trước khi tìm kiếm
<Button 
  onClick={() => {
    const trimmedKeyword = keyword.trim();
    if (!trimmedKeyword) {
      alert("Vui lòng nhập từ khóa tìm kiếm!");
      return;
    }
    setKeyword(trimmedKeyword);
    load(1, meta.PageSize);
  }} 
  variant="outline"
>
  Tìm kiếm
</Button>
```

## Checklist

### Before Committing
- [ ] Sử dụng DataTable component với sorting và filtering
- [ ] Layout cân đối với justify-between
- [ ] Button variants đúng loại
- [ ] Page structure theo chuẩn tiep-nhan/quan-ly-hop-dong
- [ ] Footer có bg-muted và pagination đúng format
- [ ] Search & Actions có container bg-muted p-4
- [ ] Table có container bg-white rounded-md border
- [ ] Search validation: kiểm tra từ khóa không rỗng và trim
- [ ] Import validation: kiểm tra file size, extension, và dữ liệu hiện có
- [ ] Error handling cho tất cả các actions
- [ ] Modal với hướng dẫn chi tiết cho import
- [ ] Sử dụng toast notifications thay vì alert()
- [ ] Success/Error messages cho tất cả các actions
- [ ] Loading toast cho tất cả async operations
- [ ] Form validation với thông báo cụ thể cho từng field
- [ ] Export validation với thông báo rõ ràng khi không có dữ liệu
- [ ] Modal close button sử dụng icon X thay vì text "Đóng"

## Recent Updates (B2B Company Management)

### ✅ Đã cải thiện:
1. **Table Components**: Thay thế custom table bằng DataTable với sorting và filtering
2. **Layout Structure**: Áp dụng chuẩn từ tiep-nhan/quan-ly-hop-dong
3. **Search & Actions**: Container bg-muted p-4 với layout cân đối
4. **Footer Pagination**: bg-muted py-2 px-4 với controls đầy đủ
5. **Button Organization**: 
   - Tìm kiếm: variant="outline" (bên cạnh input)
   - Thêm mới: variant="default" (đầu tiên bên phải)
   - Export: variant="secondary"
   - Import: variant="outline"
6. **Responsive Design**: flex-wrap cho mobile compatibility
7. **Search Validation**: Kiểm tra từ khóa không rỗng và trim khoảng trắng
8. **Import Modal**: Popup với hướng dẫn chi tiết và validation
9. **File Validation**: Kiểm tra kích thước (5MB), extension (.xlsx, .xls), và dữ liệu hiện có
10. **Error Handling**: Thông báo lỗi rõ ràng cho từng trường hợp
11. **Toast Notifications**: Thay thế alert() bằng toast.success() và notifyError()
12. **Success Messages**: Thông báo thành công cho tất cả các actions
13. **Loading States**: Toast loading cho tất cả async operations (load, save, toggle, export, import)
14. **Form Validation**: Kiểm tra từng field cụ thể với thông báo rõ ràng
15. **Export Validation**: Thông báo tường minh khi không có dữ liệu để export
16. **Modal UI**: Close button sử dụng icon X với hover effect

### 📋 Template cho trang mới:
```tsx
export default function NewPage() {
  return (
    <>
      <CenterInfo page={PageName.XXX} />
      
      <div className="w-full bg-muted p-4">
        <div className="flex gap-2 items-end justify-between flex-wrap">
          {/* Search Section */}
          <div className="flex gap-2 items-end">
            <div className="flex flex-col">
              <label className="text-sm">Từ khóa</label>
              <Input className="w-[300px]" />
            </div>
            <Button variant="outline">Tìm kiếm</Button>
          </div>
          
          {/* Actions Section */}
          <div className="flex gap-2 items-end">
            <Button variant="default">Thêm mới</Button>
            <Button variant="secondary">Export</Button>
            <Button variant="outline">Import</Button>
          </div>
        </div>
      </div>

             <div className="bg-white rounded-md border">
         <DataTable
           data={rows}
           columns={columns}
           enablePaging={false}
           enableColumnFilter={true}
         />
       </div>

      <div className="w-full bg-muted py-2 px-4 flex justify-between items-center">
        {/* Footer pagination */}
      </div>
    </>
  );
}
```
- [ ] Footer có bg-muted
- [ ] Alternating rows có bg-muted/20
- [ ] Responsive design
- [ ] Consistent spacing
- [ ] Proper imports

### Code Review
- [ ] Tuân thủ UI patterns
- [ ] Consistent styling
- [ ] Proper component structure
- [ ] Error handling
- [ ] Loading states
- [ ] Accessibility considerations
