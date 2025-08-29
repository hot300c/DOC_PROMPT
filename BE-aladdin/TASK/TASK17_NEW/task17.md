# TASK 17: Thêm chức năng nhập liệu B2B

## Goal
Thêm chức năng quản lý B2B với đầy đủ CRUD, import/export, phân quyền theo user. Tài liệu này là chuẩn để tái sử dụng.

## Mô tả yêu cầu
Cần màn hình thêm chức năng nhập liệu B2B.
Bao gồm: Thêm/ Xóa/ Sửa/ Select/ import, export, Phân quyền theo user.
**Table**: `L_CompanyB2B`

## Tham thảo code file
- **Backend CRUD**: `ws_MDM_Patient_SaveV2.cs`
- **Frontend Search**: https://dev-genie.vnvc.info/quan-ly-tai-khoan/danh-sach-tai-khoan-qapay
- **Frontend Pagination**: https://dev-genie.vnvc.info/nha-thuoc/quan-li-ca
- **entity linq DB**: C:\PROJECTS\aladdin\Entities\QAHosGenericDB\LCompanyB2B.cs
- **code base front-end**: C:\PROJECTS\DOCS_PROMPT\FE-genie\GENIE_CODEBASE_OVERVIEW.md

Ví dụ gọi API:
API List:
curl -H "X-API-KEY: BKDfNANyHx4cQAMvM7yHr0Qyo0PtQebvBOBA5g0o+IY=" "http://localhost:5272/api/company-b2b/list?page=1&pageSize=20"

---

# BUSINESS RULES (User Requirements)

## 1. Chức năng cơ bản

### 1.1 Menu và Navigation
- Thêm submenu "Company Management" dưới menu "System"
- Menu hiển thị theo phân quyền của user

### 1.2 Phân quyền người dùng
- User access được kiểm soát qua "Action On Page" hoặc "Page" permissions
- Phân quyền chi tiết:
  - **View**: Xem danh sách và thông tin chi tiết
  - **Create**: Thêm mới công ty B2B
  - **Edit**: Sửa thông tin công ty B2B
  - **Delete**: Xóa mềm công ty B2B
  - **Import**: Nhập dữ liệu từ file Excel/CSV
  - **Export**: Xuất dữ liệu ra file Excel/CSV

## 2. Quy tắc nghiệp vụ

### 2.1 Thêm mới công ty B2B
- **Kiểm tra trùng lặp**: `CompanyCode` phải là duy nhất trong hệ thống
- **Validation bắt buộc**:
  - `CompanyCode`: Mã công ty (không được trống, tối đa 50 ký tự)
  - `CompanyTax`: Mã số thuế (không được trống, tối đa 50 ký tự)
  - `CompanyName`: Tên công ty (không được trống, tối đa 500 ký tự)
  - `CompanyAddress`: Địa chỉ công ty (không được trống, tối đa 500 ký tự)
  - `EffectiveFrom`: Ngày bắt đầu hiệu lực (bắt buộc)
  - `Hopdong`: Số hợp đồng/PO (không được trống, tối đa 100 ký tự)
- **Validation logic**:
  - `EffectiveFrom` phải <= `EffectiveTo` (nếu có)
  - `EffectiveFrom` không được trong quá khứ quá 1 năm
  - `EffectiveTo` (nếu có) không được trong quá khứ

### 2.2 Cập nhật thông tin
- **Kiểm tra tồn tại**: `CompanyB2BID` phải tồn tại trong hệ thống
- **Kiểm tra trùng lặp**: `CompanyCode` không được trùng với công ty khác (trừ chính nó)
- **Audit trail**: Tự động cập nhật `ModifiedOn` và `ModifiedBy`

### 2.3 Xóa công ty B2B
- **Xóa mềm**: Toggle trạng thái `IsActive` thay vì xóa vật lý
- **Audit trail**: Cập nhật `ModifiedOn` và `ModifiedBy`
- **Trạng thái hiển thị**: 
  - `IsActive = true` → "Kích hoạt"
  - `IsActive = false` → "Không kích hoạt"

### 2.4 Tìm kiếm và lọc
- **Tiêu chí tìm kiếm**:
  - `CompanyCode`: Tìm chính xác
  - `CompanyName`: Tìm kiếm theo từ khóa (contains)
  - `CompanyTax`: Tìm chính xác
  - `IsActive`: Lọc theo trạng thái (true/false)
  - `EffectiveFrom/EffectiveTo`: Lọc theo khoảng thời gian
  - `Hopdong`: Tìm kiếm theo từ khóa (contains)
  - `CompanyAddress`: Tìm kiếm theo từ khóa (contains)
  - `CreatedBy/ModifiedBy`: Lọc theo người tạo/sửa
- **Tìm kiếm tổng hợp**: Tìm kiếm theo từ khóa chung (CompanyCode, CompanyName, CompanyTax, CompanyAddress, Hopdong)

### 2.5 Phân trang
- **Page size**: 10, 20, 50, 100 bản ghi/trang
- **Sắp xếp mặc định**: Theo `CreatedOn` giảm dần (mới nhất trước)
- **Tùy chọn sắp xếp**: 
  - Theo `CompanyCode` (ASC/DESC)
  - Theo `CompanyName` (ASC/DESC)
  - Theo `CreatedOn` (ASC/DESC)

## 3. Import dữ liệu

### 3.1 Quy tắc import
- **Format file**: Excel (.xlsx, .xls) hoặc CSV (.csv)
- **Kích thước file**: Tối thiểu 1KB, tối đa 10MB
- **Số lượng dòng**: Tối đa 10,000 dòng dữ liệu (không tính header)

### 3.2 Cấu trúc file import
**Cột bắt buộc**:
- `CompanyCode`: Mã công ty
- `CompanyName`: Tên công ty
- `EffectiveFrom`: Ngày bắt đầu hiệu lực
- `Hopdong`: Số hợp đồng/PO
- `IsActive`: Trạng thái kích hoạt

**Cột tùy chọn**:
- `CompanyTax`: Mã số thuế
- `CompanyAddress`: Địa chỉ
- `EffectiveTo`: Ngày kết thúc hiệu lực

### 3.3 Mapping header (hỗ trợ đa ngôn ngữ)
**CompanyCode**: "Mã công ty", "Ma cong ty", "Ma công ty"
**CompanyName**: "Tên công ty", "Ten cong ty"
**CompanyTax**: "MST", "Mã số thuế", "Ma so thue"
**CompanyAddress**: "Địa chỉ", "Dia chi"
**EffectiveFrom**: "Ngày bắt đầu", "Ngày bắt đầu tiêm", "Ngay bat dau", "Ngay bat dau tiem"
**EffectiveTo**: "Ngày kết thúc", "Ngay ket thuc"
**IsActive**: "Kích hoạt", "Active", "Trạng thái"
**Hopdong**: "Số PO-HĐ", "Số PO-HD", "So PO-HD", "PO", "Hợp đồng", "Hop dong"

### 3.4 Xử lý dữ liệu import
- **Upsert logic**: Cập nhật/thay thế dựa trên `CompanyCode`
- **Validation**: Kiểm tra toàn bộ file trước khi ghi database
- **Error handling**: 
  - Dòng lỗi: Trả về chi tiết lỗi (Line, CompanyCode, Error)
  - Dòng thiếu trường bắt buộc: Bỏ qua và đếm vào `Skipped`
  - File lỗi: Không ghi database, rollback toàn bộ
- **Date parsing**: Hỗ trợ nhiều format ngày tháng
- **Transaction**: Thực thi trong transaction, rollback nếu có lỗi

### 3.5 Kết quả import
- **Thành công**: Trả về số lượng `Created`, `Updated`, `Skipped`
- **Thất bại**: Trả về danh sách lỗi chi tiết

## 4. Export dữ liệu

### 4.1 Quy tắc export
- **Dữ liệu xuất**: Toàn bộ dữ liệu từ bảng `L_CompanyB2B` (không áp dụng filter)
- **Format xuất**: JSON được nén base64 (để client-side xử lý)
- **Sắp xếp**: 
  - Ưu tiên theo `ModifiedOn` giảm dần (mới nhất trước)
  - Nếu `ModifiedOn` null, sử dụng `CreatedOn` giảm dần
  - Tie-break theo `CreatedOn` giảm dần

### 4.2 Cấu trúc dữ liệu xuất
**Cột chính** (cho Excel):
1. **Mã công ty** (`CompanyCode`)
2. **Tên công ty** (`CompanyName`)
3. **Số PO-HĐ** (`Hopdong`)
4. **Ngày bắt đầu tiêm** (`EffectiveFrom` - format: yyyy-MM-dd)
5. **Ngày kết thúc** (`EffectiveTo` - format: yyyy-MM-dd, trống nếu null)
6. **Ghi chú** (trống - chưa có cột riêng trong DB)
7. **Trạng thái** (`IsActive` → "Kích hoạt"/"Không kích hoạt")

**Metadata bổ sung**:
- `CompanyB2BID`: ID duy nhất
- `CompanyTax`: Mã số thuế
- `CompanyAddress`: Địa chỉ
- `IsActive`: Trạng thái boolean
- `CreatedOn`: Ngày tạo (format: yyyy-MM-dd HH:mm:ss)
- `ModifiedOn`: Ngày sửa (format: yyyy-MM-dd HH:mm:ss, trống nếu null)

### 4.3 Format dữ liệu
```json
{
  "Data": [
    {
      "CompanyCode": "EXP1",
      "CompanyName": "Export Co 1",
      "Hopdong": "HD_EXP_1",
      "EffectiveFrom": "2025-01-01",
      "EffectiveTo": "",
      "GhiChu": "",
      "TrangThai": "Kích hoạt",
      "CompanyB2BID": "11111111-1111-1111-1111-111111111111",
      "CompanyTax": "1111111111",
      "CompanyAddress": "Export St 1",
      "IsActive": true,
      "CreatedOn": "2025-01-01 00:00:00",
      "ModifiedOn": "2025-01-01 00:00:00"
    }
  ],
  "Metadata": {
    "TotalCount": 123,
    "ExportDate": "2025-01-01 12:00:00",
    "ColumnHeaders": [
      "Mã công ty",
      "Tên công ty",
      "Số PO-HĐ",
      "Ngày bắt đầu tiêm",
      "Ngày kết thúc",
      "Ghi chú",
      "Trạng thái"
    ],
    "SuggestedFileName": "CompanyB2B_20250101120000.json",
    "SheetName": "CompanyB2B",
    "ColumnCount": 7,
    "DataFormat": "json"
  }
}
```

### 4.4 Response format
```json
{
  "Table1": [{
    "FileName": "CompanyB2B_20250101120000.json",
    "FileExtension": ".json",
    "FileData": "base64_encoded_json_string",
    "TotalCount": 123,
    "FileSizeBytes": 45678,
    "FileSizeKB": 44.61,
    "FileSizeMB": 0.04,
    "ExportDate": "2025-01-01 12:00:00",
    "DataFormat": "json",
    "ContentType": "application/json"
  }]
}
```

### 4.5 Xử lý client-side
- **Decode base64**: Chuyển đổi base64 thành JSON string
- **Tạo Excel**: Sử dụng thư viện Excel (ExcelJS, SheetJS, EPPlus)
- **Download**: Tự động tải file Excel về máy

## 5. Validation và ràng buộc

### 5.1 Validation dữ liệu
- **Null handling**: Tất cả null values được convert thành empty string `""`
- **Date validation**: 
  - `EffectiveFrom` không được null
  - `EffectiveFrom` <= `EffectiveTo` (nếu có)
  - Ngày không được trong quá khứ quá 1 năm
- **String validation**:
  - `CompanyCode`: Không được trống, tối đa 50 ký tự
  - `CompanyName`: Không được trống, tối đa 500 ký tự
  - `CompanyTax`: Không được trống, tối đa 50 ký tự
  - `CompanyAddress`: Không được trống, tối đa 500 ký tự
  - `Hopdong`: Không được trống, tối đa 100 ký tự

### 5.2 Ràng buộc hiệu suất
- **Export**: Không giới hạn số lượng bản ghi (có thể ảnh hưởng performance)
- **Import**: Giới hạn 10,000 dòng để tránh timeout
- **Search**: Sử dụng index để tối ưu tìm kiếm
- **Memory**: Cần monitoring memory usage cho export lớn

### 5.3 Ràng buộc bảo mật
- **Phân quyền**: Kiểm tra quyền truy cập trước khi thực hiện thao tác
- **Audit trail**: Ghi log tất cả thao tác CRUD
- **Data exposure**: Export toàn bộ dữ liệu - cần kiểm soát quyền truy cập

## 6. Response schemas chuẩn

### 6.1 Save (Create/Update)
```json
{
  "Table1": [{
    "Result": "Created|Updated",
    "CompanyB2BID": "guid"
  }]
}
```

### 6.2 Delete (Toggle)
```json
{
  "Table1": [{
    "Result": "Toggled",
    "CompanyB2BID": "guid",
    "IsActive": true|false
  }]
}
```

### 6.3 Get (có ID)
```json
{
  "Table1": [{
    "errorCode": 0,
    "errorMsg": "Success"
  }],
  "Table2": [{
    // Thông tin chi tiết công ty
  }]
}
```

### 6.4 Get (không có ID - list active)
```json
{
  "Table1": [
    {
      "CompanyId": "guid",
      "CompanyName": "string",
      "CompanyCode": "string",
      "CompanyContract": "string"
    }
  ]
}
```

### 6.5 List (search + pagination)
```json
{
  "Table1": [
    // Danh sách công ty
  ],
  "Table2": [{
    "Total": 123,
    "Page": 1,
    "PageSize": 20
  }]
}
```

### 6.6 Import
```json
{
  "Table1": [{
    "Result": "OK",
    "Created": 10,
    "Updated": 5,
    "Skipped": 2
  }]
}
```

### 6.7 Export
```json
{
  "Table1": [{
    "FileName": "string",
    "FileExtension": ".json",
    "FileData": "base64_string",
    "TotalCount": 123,
    "FileSizeBytes": 45678,
    "FileSizeKB": 44.61,
    "FileSizeMB": 0.04,
    "ExportDate": "2025-01-01 12:00:00",
    "DataFormat": "json",
    "ContentType": "application/json"
  }]
}
```

---

# TECHNICAL SPECIFICATIONS

## RULE
- **Project front-end**: `C:\PROJECTS\genie`
- **Project back-end**: `C:\PROJECTS\aladdin`

### Trước khi generate code, phải check nhánh GIT:
git checkout main
git pull
git checkout feat/ws_CompanyB2B

## Backend Architecture

### Framework và Technology
- Framework: .NET 8, C#
- Database: SQL Server (LinqToDB)
- Architecture: WebService.Handlers pattern

### File Structure
- **Handler file**: `aladdin/WebService.Handlers/QAHosGenericDB/ws_L_CompanyB2B_Save.cs`
- **Controller**: `aladdin/WebService/Api/CompanyB2BController.cs`
- **Entity**: `aladdin/Entities/QAHosGenericDB/LCompanyB2B.cs`

### Handlers (đều dùng `GenericHandler<Parameters>` và `record Parameters` mạnh kiểu)
- `ws_L_CompanyB2B_Save` (Create/Update, validate, check trùng mã)
- `ws_L_CompanyB2B_Get` (Get theo ID; nếu thiếu ID trả list active trong hiệu lực)
- `ws_L_CompanyB2B_List` (search + pagination + sort)
- `ws_L_CompanyB2B_Delete` (toggle `IsActive` + cập nhật audit)
- `ws_L_CompanyB2B_Import` (import CSV, upsert theo `CompanyCode`)
- `ws_L_CompanyB2B_Export` (xuất JSON base64, trả metadata)

### Service phụ trợ
- `DateTimeService` (DI) - cung cấp thời gian hiện tại

## API Endpoints

### CompanyB2BController
- POST `/api/company-b2b/save`
- POST `/api/company-b2b/delete`
- GET  `/api/company-b2b/get?companyB2BID={id}`
- GET  `/api/company-b2b/list` (đủ filter + sort + page)
- POST `/api/company-b2b/import`
- GET  `/api/company-b2b/export`

### DTOs (Required annotations)
- `CompanySaveDto`
- `CompanyDeleteDto`
- `CompanyImportDto`

## Frontend Architecture

### Framework và Technology
- Framework: Next.js, React, TypeScript
- UI: Tailwind CSS
- Excel/CSV Utils: `C:\PROJECTS\genie\app\lib\utils`

### Reference implementations
- Search: https://dev-genie.vnvc.info/quan-ly-tai-khoan/danh-sach-tai-khoan-qapay
- Pagination: https://dev-genie.vnvc.info/nha-thuoc/quan-li-ca

## Implementation Details

### Import file (Excel/CSV)
1. **Frontend**:
   - Utils đọc Excel/CSV, validate size > 1KB.
   - Chuyển nội dung thành Base64 hoặc text CSV và gửi về backend qua `Base64Data`.

2. **Backend**:
   - Nhận `Base64Data` và `FileName`.
   - Thử decode Base64, nếu fail sẽ xử lý như raw CSV text.
   - Parse CSV header với alias tiếng Việt/Anh (xem Mapping bên dưới), robust date parsing.
   - Giới hạn tối đa 10,000 dòng dữ liệu (không tính header). Nếu vượt, trả lỗi 400.
   - Tiền kiểm toàn bộ file trước khi ghi DB:
     - Bắt buộc: `CompanyCode`, `CompanyName`, `Hopdong`, `IsActive`, `EffectiveFrom`.
     - Kiểm tra ngày và quan hệ `EffectiveFrom <= EffectiveTo` (nếu có).
     - Nếu có lỗi: trả về bảng lỗi chi tiết gồm các cột: `Line`, `CompanyCode`, `Error`. Không ghi DB.
   - Upsert theo `CompanyCode`; cập nhật audit bằng `UserID`.
   - Thực thi trong transaction: dùng bulk insert cho bản ghi mới, update theo mã cho bản ghi cũ; rollback toàn bộ nếu bất kỳ bước nào lỗi.
   - Trả kết quả: `Result=OK`, `Created` (số bản ghi mới), `Updated` (số bản ghi cập nhật).

### Export file (JSON base64)
1. **Backend**:
   - Tạo JSON object từ `L_CompanyB2B` (toàn bộ dữ liệu, không filter).
   - Cấu trúc dữ liệu như định nghĩa trong Business Rules.
   - Sắp xếp: ưu tiên `ModifiedOn` mới nhất trước (nếu null dùng `CreatedOn`), sau đó tie-break theo `CreatedOn` giảm dần.
   - Encode Base64, trả về ở bảng meta `Table1` gồm: `FileName`, `FileExtension=.json`, `FileData`.

2. **Frontend**:
   - Nhận Base64 JSON, decode và tạo Excel file.
   - Sử dụng thư viện Excel để tạo file và download.

### CSV Header Mapping (Import)
- Bắt buộc: `CompanyCode` ("Mã công ty", "Ma cong ty"), `CompanyName` ("Tên công ty", "Ten cong ty"), `EffectiveFrom` ("Ngày bắt đầu"/"Ngày bắt đầu tiêm"/"Ngay bat dau"), `Hopdong` ("Số PO-HĐ"/"PO"/"Hợp đồng").
- Tùy chọn: `CompanyTax` ("MST"/"Mã số thuế"), `CompanyAddress` ("Địa chỉ"), `EffectiveTo` ("Ngày kết thúc"), `IsActive` ("Kích hoạt"/"Active").
- Date parsing hỗ trợ: `yyyy-MM-dd`, `yyyy/MM/dd`, `dd/MM/yyyy`, `d/M/yyyy`, `MM/dd/yyyy`, `M/d/yyyy`, `yyyy-MM-ddTHH:mm:ss[.fff][K]`.
- Dòng thiếu trường bắt buộc sẽ bị đếm `Skipped` (không fail file).

## Database Schema Reference
**File**: `C:\PROJECTS\qas-db\QAHosGenericDB\Tables\L_CompanyB2B.sql`

### Table Structure
```sql
CREATE TABLE [dbo].[L_CompanyB2B](
    [CompanyB2BID] [uniqueidentifier] NOT NULL PRIMARY KEY,
    [CompanyTax] [varchar](50) NOT NULL,
    [CompanyCode] [varchar](50) NOT NULL,
    [CompanyName] [nvarchar](500) NOT NULL,
    [CompanyAddress] [nvarchar](500) NOT NULL,
    [EffectiveFrom] [datetime] NOT NULL,
    [EffectiveTo] [datetime] NULL,
    [IsActive] [bit] NOT NULL,
    [CreatedOn] [datetime] NOT NULL,
    [CreatedBy] [uniqueidentifier] NULL,
    [ModifiedOn] [datetime] NULL,
    [ModifiedBy] [uniqueidentifier] NULL,
    [Hopdong] [varchar](100) NOT NULL
)
```

## Validation Rules (Technical)
Backend:
1. Save: bắt buộc `CompanyCode`, `CompanyTax`, `CompanyName`, `CompanyAddress`, `EffectiveFrom`; `EffectiveFrom <= EffectiveTo`; `CompanyCode` không trùng.
2. Delete: bắt buộc `CompanyB2BID`, `UserID`.
3. List: hỗ trợ toàn bộ filter theo cột; bắt buộc `SortBy`, `SortDir` (mặc định `CreatedOn/DESC`).
4. Import: bắt buộc header tối thiểu (nêu trên); bỏ qua dòng thiếu; parse ngày theo list formats.
5. Export: trả 1 bảng dữ liệu + meta file.

## Permission Structure
```csharp
public enum CompanyB2BPermission
{
    View = 1,
    Create = 2,
    Edit = 3,
    Delete = 4,
    Import = 5,
    Export = 6
}
```

## Search Criteria (Technical)
- CompanyCode (exact)
- CompanyName (contains)
- CompanyTax (exact)
- IsActive (bool)
- EffectiveFrom/EffectiveTo (range)
- Hopdong (contains)
- CompanyAddress (contains)
- CreatedBy/ModifiedBy (exact)

## Pagination (Technical)
- Page size: 10, 20, 50, 100
- Sort by: CompanyCode, CompanyName, CreatedOn
- Sort direction: ASC, DESC

## Testing
- Unit tests (xUnit + YAML):
  - Save/Get/List/Delete/Import/Export trong `aladdin/WebService.Handlers.Tests/QAHosGenericDB`.
  - Test cases YAML tại `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/...`.
  - Chạy nhóm CompanyB2B: `dotnet test -c Debug --filter FullyQualifiedName~ws_L_CompanyB2B_`.

- k6 API test:
  - File: `DOCS_PROMPT/BE-aladdin/TASK/TASK17_NEW/company-b2b.k6.js`
  - Biến môi trường: `BASE_URL`, `SESSION_ID`, `USER_ID`, `K6_VUS`, `K6_ITERS`.
  - Run: `k6 run DOCS_PROMPT/BE-aladdin/TASK/TASK17_NEW/company-b2b.k6.js -e BASE_URL=http://localhost:5000 -e USER_ID=00000000-0000-0000-0000-000000000000`.

## Auth và cách gọi API (CompanyB2BController)

Các endpoint trong `CompanyB2BController` kế thừa `ApiBaseController` nên bắt buộc xác thực bằng API Key qua header `X-API-KEY`.

- Yêu cầu header: `X-API-KEY: <raw_api_key>`
- Hệ thống sẽ băm SHA256 key này và so khớp với `Security.ApiKeys.KeyHash` trong DB. Role trích từ bảng API key sẽ được map quyền theo `Configs/api-roles.json`. Để thử nhanh, tạo key với role `FullAccess`.

Tham khảo cấu hình:

```12:20:aladdin/WebService/Api/ApiBaseController.cs
[Authorize(AuthenticationSchemes = ApiKeyAuthenticationHandler.SchemeName)]
```

```1:16:aladdin/WebService/Configs/api-roles.json
{
  "RoleActions": {
    "FullAccess": [{ "Path": ".*", "Method": ".*" }]
  }
}
```

### Đăng nhập (tham chiếu)

Endpoint đăng nhập: `POST /Login` nhận `Username`, `PasswordHash` (MD5), `FacId`. Đăng nhập sẽ set cookie `s` (session id) dùng cho các controller xác thực theo SessionScheme. Riêng nhóm API `/api/company-b2b/*` dùng API Key nên không dùng cookie này.

Ví dụ PowerShell (Windows):

```powershell
$password = "Phuc*1234"
$hash = ([System.Security.Cryptography.MD5]::Create().ComputeHash([Text.Encoding]::UTF8.GetBytes($password)) | ForEach-Object { $_.ToString("x2") }) -join ''
$body = @{ Username='phucnnd'; PasswordHash=$hash; FacId='8.1' } | ConvertTo-Json -Compress
Invoke-RestMethod -Method Post -Uri http://localhost:5272/Login -ContentType 'application/json' -Body $body
```

### Session cookie (s)

- Sau khi `POST /Login` thành công, server set cookie phiên tên `s` (HttpOnly, Secure, SameSite phụ thuộc môi trường) hết hạn cuối ngày.
- Swagger UI khi gọi `/Login` cũng sẽ lưu cookie này trong trình duyệt, nên các endpoint xác thực theo SessionScheme có thể gọi tiếp ngay trong Swagger.
- Lưu ý: Nhóm API `CompanyB2BController` dùng `X-API-KEY` (ApiKeyScheme), nên cookie `s` không áp dụng để gọi các endpoint `/api/company-b2b/*`.

### Gọi thử List qua Swagger

1. Mở `http://localhost:5272/swagger/index.html`.
2. Bấm "Authorize" → nhập `X-API-KEY` với giá trị API key thô (không băm).
3. Mở `GET /api/company-b2b/list` → nhập tham số, Execute.

### Gọi thử List qua PowerShell

```powershell
# Thay bằng API key thực tế của bạn (raw string, không phải SHA256)
$API_KEY = "<YOUR_API_KEY>"

Invoke-RestMethod `
  -Method Get `
  -Uri "http://localhost:5272/api/company-b2b/list?page=1&pageSize=20" `
  -Headers @{ "X-API-KEY" = $API_KEY }
```

Nếu thiếu hoặc sai API key:

- Thiếu header: trả Unauthorized
- Key sai: trả thông báo "Invalid API Key."

### Tạo API key mới (gợi ý)

1. Chọn chuỗi bí mật làm key thô (ví dụ: `my-dev-key-123`).
2. Băm SHA256 chuỗi này và lưu vào `Security.ApiKeys.KeyHash` với `Role='FullAccess'` (hoặc role phù hợp).
3. Khi gọi API, gửi đúng chuỗi thô qua `X-API-KEY`.

Lưu ý: Không commit key thô vào repo.

## DTOs Structure

### Import Excel DTO
```csharp
public record ImportExcelDto
{
    public string Base64Data { get; init; }
    public string FileName { get; init; }
    public Guid UserId { get; init; }
}
```

### Export Excel DTO
```csharp
public record ExportExcelDto
{
    public string ReportName { get; init; }
    public string ReportParams { get; init; }
    public Guid UserId { get; init; }
}
```

### Excel Export Response DTO
```csharp
public record ExcelExportResponseDto
{
    // Thông tin cơ bản của báo cáo Excel
    public long QueueSeq { get; init; }
    public Guid ReportId { get; init; }
    public string ReportName { get; init; }
    public string ReportParams { get; init; }
    public string ReportType { get; init; }
    public string FileData { get; init; }  // Base64 Excel data
    public string FileExtension { get; init; }
    public DateTime CreatedOn { get; init; }
    public string Name { get; init; }
}
```

## Ghi chú triển khai
- Tất cả handler B2B gom trong 1 file; dùng `GenericHandler<Parameters>` để map YAML/API -> tham số mạnh kiểu.
- `ws_L_CompanyB2B_Get` không có ID sẽ trả danh sách active trong hiệu lực, phục vụ dropdown/list nhanh.
- Import chấp nhận Base64 hoặc CSV raw text.
- Export trả về JSON base64 để client-side xử lý thành Excel.