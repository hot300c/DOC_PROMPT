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

#### 2.1. Quy tắc hiển thị lỗi chuẩn hóa (API)
- **Không gọi được API (không có `error.response`)**: hiển thị
  - "Không thể kết nối tới máy chủ. Vui lòng kiểm tra mạng hoặc thử lại sau."
- **HTTP 500 / Internal Server Error**: hiển thị
  - "Hệ thống đang gặp sự cố. Vui lòng thử lại sau hoặc liên hệ hỗ trợ."
- **Có `response.data.message`**: hiển thị đúng thông báo từ backend
  - Ví dụ: "EffectiveFrom must be less than or equal to EffectiveTo"
- **Có `response.data.errors` theo field**: flatten, hiển thị lỗi đầu tiên
- **Fallback**: nếu không có thông tin cụ thể, hiển thị
  - "Có lỗi xảy ra!" hoặc thông báo lỗi chung theo ngữ cảnh (lưu/tải/xử lý)

```tsx
try {
  await apiCall();
  toast.success("Thành công!");
} catch (error) {
  // @ts-ignore
  const errResp = error?.response;
  if (!errResp) {
    notifyError("Không thể kết nối tới máy chủ. Vui lòng kiểm tra mạng hoặc thử lại sau.");
  } else if (errResp?.status === 500 || String(errResp?.statusText || "").toLowerCase().includes("internal server error")) {
    notifyError("Hệ thống đang gặp sự cố. Vui lòng thử lại sau hoặc liên hệ hỗ trợ.");
  } else if (errResp?.data?.message) {
    toast.error(errResp.data.message);
  } else if (errResp?.data?.errors && typeof errResp.data.errors === "object") {
    const first = Object.entries(errResp.data.errors)
      .flatMap(([field, msgs]) => Array.isArray(msgs) ? msgs.map((m) => `${field}: ${m}`) : typeof msgs === "string" ? [`${field}: ${msgs}`] : [])
      .at(0);
    if (first) toast.error(first);
    else notifyError("Có lỗi xảy ra!");
  } else {
    notifyError("Có lỗi xảy ra!");
  }
}
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
  let toastId: string | number | undefined;
  try {
    toastId = notifyLoading("Đang xử lý...");
    await someAsyncOperation();
    toast.success("Thành công!");
  } catch (error) {
    notifyError("Có lỗi xảy ra!");
  } finally {
    // Luôn tắt loading toast sau khi hoàn thành hoặc lỗi
    if (toastId) {
      toast.dismiss(toastId);
    }
  }
};
```

**Lưu ý quan trọng**: 
- **Luôn sử dụng `finally` block** để đảm bảo loading toast được tắt trong mọi trường hợp
- **Không gọi `toast.dismiss()` trong `try` hoặc `catch`** vì có thể bị bỏ qua nếu có lỗi
- **Kiểm tra `toastId` tồn tại** trước khi gọi `toast.dismiss()` để tránh lỗi

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

**Lưu ý**: 
- Mã số thuế (CompanyTax) không bắt buộc khi thêm mới hoặc sửa đổi công ty B2B.
- Địa chỉ (CompanyAddress) không bắt buộc khi thêm mới hoặc sửa đổi công ty B2B.
- Số PO-HĐ (Hopdong) không bắt buộc khi thêm mới hoặc sửa đổi công ty B2B.

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

### ✅ Đồng bộ với trang thanh-toan/danh-sach (Finalized)
- **Phân trang (footer trên cùng)**:
  - Cố định dưới cùng (fixed) với `bg-muted border-t`.
  - Hàng 1 (căn phải): hiển thị `Tổng: {meta.Total} công ty` bên trái cụm phân trang; cụm phân trang gồm các nút: về đầu, trước, “Trang X trên Y”, sau, về cuối, và selector “Số dòng mỗi trang”.
  - Hàng 2 (căn phải): cụm nút hành động theo thứ tự từ trái qua phải: `Thêm mới` (default) → `Nhập Excel` (outline) → `Xuất Excel` (secondary).
  - Spacer nội dung: thêm khoảng trống tương đương chiều cao footer để tránh đè nội dung.
- **Nhãn tiếng Việt**:
  - Trạng thái: “Hoạt động”/“Ngưng hoạt động”.
  - Nút: “Nhập Excel”, “Xuất Excel”, “Thêm mới”.
- **Cột Trạng thái**:
  - Tiêu đề cột: “Trạng thái”.
  - Cell là ô checkbox: tick = “Hoạt động”, bỏ tick = “Ngưng hoạt động”.
  - Click checkbox gọi API toggle trạng thái (stopPropagation để không mở popup sửa).
  - Loại bỏ nút toggle trong cột Hành động; click nguyên dòng mở popup sửa.
- **Sorting/Filtering**:
  - Cột “Hiệu lực” sort theo `EffectiveFrom` với `sortingFn = "datetime"`.
  - Tắt filter inputs ở header: `enableColumnFilter={false}` toàn bảng (và `enableColumnFilter: false` cho cột “Hiệu lực”).
- **Định dạng ngày trong bảng**:
  - Cột “Hiệu lực” hiển thị theo định dạng `dd/MM/yyyy - dd/MM/yyyy`.
  - Vẫn dùng giá trị ISO `yyyy-MM-dd` trong state và khi gọi API.

### 🧱 Bố cục trang (đã hoàn tất)
- **Header thông tin**: `CenterInfo` đứng trên cùng (không cố định).
- **Khu vực tìm kiếm**: khối `bg-muted p-4`, chứa input từ khóa và nút “Tìm kiếm” (variant="outline"), căn trái; không có nút hành động ở khu vực này.
- **Bảng dữ liệu**: khối `bg-white rounded-md border overflow-auto max-h-[calc(100vh-220px)]` để hỗ trợ scroll khi xem 100 dòng trở lên; dùng `DataTable` với sorting, tắt filter header.
- **Footer cố định (2 hàng)**: `fixed bottom-0 left-0 w-full bg-muted border-t z-50`
  - Hàng 1 (căn phải): “Tổng: X công ty” nằm ngay bên trái cụm phân trang, cùng một hàng với cụm phân trang.
  - Hàng 2 (căn phải): cụm hành động theo thứ tự từ trái qua phải: `Thêm mới` → `Nhập Excel` → `Xuất Excel`.
- **Khoảng đệm dưới nội dung**: thêm spacer tương đương chiều cao footer để tránh che nội dung (ví dụ `h-16`).

Ghi chú triển khai:
- `onRowClick={(row) => onEdit(row)}` để mở popup sửa.
- Cột “Trạng thái” là checkbox, click gọi API toggle; dừng nổi bọt để không mở popup.
- Phân trang do client-side điều khiển (số trang tính từ `Total/PageSize` hiện tại), kết hợp gọi lại `load(page, pageSize)`.

### 🔗 Trang tham chiếu và trang đã triển khai (đường dẫn tuyệt đối)
- Trang triển khai quản lý công ty B2B: [http://localhost:3000/he-thong/quan-ly-cong-ty-b2b](http://localhost:3000/he-thong/quan-ly-cong-ty-b2b)
- Trang tham chiếu bố cục: [http://localhost:3000/thanh-toan/danh-sach](http://localhost:3000/thanh-toan/danh-sach)
- **Date inputs (popup)**:
  - Dùng `InputDatePicker` cho “Ngày hiệu lực từ/đến”.
  - Lưu vào state dạng ISO `yyyy-MM-dd`; “đến” cho phép bỏ trống (clearable).
- **Sự kiện dòng**:
  - `onRowClick={(row) => onEdit(row)}` (DataTable trả thẳng object row).

Checklist nhanh (B2B align thanh-toan/danh-sach):
- [ ] Footer 2 hàng, cố định, có spacer.
- [ ] Tổng nằm bên trái cụm phân trang (cùng hàng trên).
- [ ] Thứ tự nút phải: Thêm → Nhập → Xuất (hàng dưới, bên phải).
- [ ] Cột “Trạng thái” là checkbox, toggle bằng API.
- [ ] Cột “Hiệu lực” sort theo `EffectiveFrom`, không filter row.
- [ ] Popup ngày dùng `InputDatePicker`, lưu ISO.

## B2B Company Management - Integration Rules

### 1. List loading (khi mở page)
- **Auto-load**: Gọi `b2bList()` khi mount trang, chỉ gửi `page` và `pageSize` nếu không có filter; không gửi các field rỗng.
- **Stripping filters**: Service phải loại bỏ `undefined/null/""` trước khi gọi API (đảm bảo lấy tất cả mặc định).
- **Response shapes**: Hỗ trợ nhiều cấu trúc dữ liệu trả về:
  - `data.data.Tables` hoặc `data.Tables`
  - `Table1` (rows), `Table2[0]` (meta)
  - Ưu tiên đọc `Table1` làm dữ liệu bảng và `Table2[0]` cho `Total/Page/PageSize`.
- **Normalize keys**: Chuẩn hóa keys để khớp `accessorKey` cột của DataTable:
  - `CompanyB2BID`, `CompanyCode`, `CompanyName`, `CompanyTax`, `CompanyAddress`, `Hopdong`, `EffectiveFrom`, `EffectiveTo`, `IsActive`.

### 2. DataTable
- **Columns**: `accessorKey` phải khớp với keys đã normalize.
- **Loading state**: Truyền `isLoading` vào `DataTable`.
- **Toggle label**: Nhãn nút Toggle hiển thị theo trạng thái: `IsActive=true` → “Ngưng kích hoạt”, ngược lại → “Kích hoạt”.

### 3. Modal (Thêm/Sửa)
- **Thứ tự input**: Mã công ty → Tên công ty → Mã số thuế → Địa chỉ → (các field còn lại).
- **Khóa mã**: Khi sửa (`editingId != null`), disable ô “Mã công ty”.
- **Validation trước lưu**: 
  - **Bắt buộc**: Mã công ty, Tên công ty, Ngày hiệu lực từ, Số PO-HĐ
  - **Không bắt buộc**: Mã số thuế, Địa chỉ, Ngày hiệu lực đến, Trạng thái
  - Dùng `notifyError` cho thông báo validation

### 4. Save flow
- **Payload cleaning**: Trước khi gọi API:
  - Trim tất cả chuỗi.
  - Bỏ các field optional rỗng (`""`) hoặc `null/undefined`.
  - Đảm bảo `IsActive` là boolean.
  - Gửi `UserID` theo ngữ cảnh.
- **Error handling**:
  - Nếu backend trả `400` với `data.errors`, flatten và hiển thị message đầu tiên bằng toast; log đầy đủ để debug.
- **Reload**: Sau khi save "Success", reset form, đóng modal, gọi lại list với `Page/PageSize` hiện tại.

### 5. Export flow
- **Server response format**: Server trả về `Table1[0]` chứa metadata export:
  ```json
  {
    "FileName": "CompanyB2B_20250108143022.json",
    "FileExtension": ".json", 
    "FileData": "base64_encoded_json_string",
    "TotalCount": 2762,
    "FileSizeBytes": 1324983
  }
  ```
- **Data extraction**: 
  - Decode base64: `atob(exportData.FileData)`
  - Parse JSON: `JSON.parse(jsonString)`
  - Extract data: `exportObject.Data` (array các công ty)
- **Client-side Excel generation**: Sử dụng `exportToExcel()` với `TableConfig`:
  - **Columns (6 cột)**: Mã công ty → Tên công ty → Số PO-HĐ → Ngày bắt đầu → Ngày kết thúc → Trạng thái
  - **Data mapping**: Map từ server data sang Excel rows (bỏ cột Ghi chú)
  - **Status mapping**: `IsActive ? "Kích hoạt" : "Ngưng kích hoạt"`
- **Error handling**: Kiểm tra `FileData` và `Data` trước khi tạo Excel
- **File naming**: `CompanyB2B_${Date.now()}.xlsx`

### 6. Import flow
- **File validation**: 
  - Kiểm tra dữ liệu hiện có trong bảng trước khi import
  - Kích thước file tối đa: 5MB
  - Chỉ chấp nhận file Excel (.xlsx, .xls)
- **Modal hướng dẫn**: Hiển thị hướng dẫn chi tiết về cấu trúc file và format dữ liệu
- **Processing**: Convert file thành base64 và gửi qua `b2bImport` API

#### 6.1. Import result handling (response từ server)
- Khi response có `data.Table1` dạng lỗi từng dòng (các phần tử có `Error`, `Line`, `CompanyCode`):
  - Hiển thị toast lỗi dùng `notifyError` với tiền tố: “Lỗi khi nhập Excel: …” (màu đỏ, đồng nhất validation).
  - Mở popup “Lỗi khi nhập Excel” liệt kê toàn bộ lỗi; popup cao tối đa ~60vh, có scroll.
  - Mỗi dòng: “Dòng {Line} - {CompanyCode}: {Error}”.
- Khi response có `data.Table1[0] = { Result: "OK", Created, Updated }`:
  - Mở popup tổng kết “Nhập Excel thành công”.
  - Hiển thị: “Thêm mới thành công: {Created} dòng”, “Cập nhật thành công: {Updated} dòng”.
- Khi không có `Error` và không có `Result` rõ ràng:
  - Mở popup thành công với Created=0, Updated=0 (fallback), sau đó reload danh sách.

### 7. Local API setup (Dev)
- **Base URL**: Client axios dùng `baseURL = "/aladdin"` kèm header `Source: genie`.
- **API Key (dev-only)**: Gắn `X-API-KEY` qua env:
  - Client: `NEXT_PUBLIC_ALADDIN_API_KEY`
  - Server: `ALADDIN_API_KEY`
- **Rewrites**: Trong dev, proxy `"/aladdin/api/:path*"` → `${ALADDIN_API_URL}/api/:path*`.
- **Interceptor an toàn**: Chỉ `JSON.parse(config.data)` khi là chuỗi hợp lệ (GET không có body).

### 8. UTF-8 Encoding (Export)
- **Server-side**: Server trả về base64 encoded JSON với UTF-8 encoding đúng
- **Client-side**: Decode base64 và parse JSON trực tiếp, không cần `fixEncoding` function
- **Excel generation**: Sử dụng ExcelJS với encoding mặc định (không cần BOM cho .xlsx files)

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
