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



## Yêu cầu chức năng
- Thêm Menu màn hình tạo công ty B2B
- File mẫu: Tệp đính kèm
- Các chức năng: thêm, sửa, xóa, import, export, Phân quyền theo user

## Clarification

### Import
- Cập nhật/thay thế thông tin dựa trên `CompanyCode` (upsert theo mã công ty B2B).

### Delete
- Xóa mềm: Toggle `IsActive` thay vì xóa vật lý.

### Add New Company
- Kiểm tra trùng `CompanyCode` trước khi tạo mới.

### Menu
- Thêm submenu "Company Management" dưới menu "System".

## User Permissions
- User access to this page should be controlled via "Action On Page" or "Page" permissions.
- On the B2B Company Management page, users should be able to search for company information.

## RULE
- **Project front-end**: `C:\PROJECTS\genie`
- **Project back-end**: `C:\PROJECTS\aladdin`

### Validation
- Dựa vào thông tin của cột trong table (tham thảo: `C:\PROJECTS\qas-db\QAHosGenericDB\Tables\L_CompanyB2B.sql`)
- Để tạo validation check ở front-end và backend.

### Search & Pagination
- Phần Frontend và backend, có chức năng search với đầy đủ tiêu chí search như theo các cột của L_CompanyB2B hiện có.
- Có phân trang.

### Permission & CRUD
- Có định nghĩa permission trong table lưu permission.
- Có đầy đủ chức năng CRUD.
- `public record Parameters` thì sẽ có action xác định là thêm, xóa, sửa, import, export.
- Và tương ứng với action đó là có DTOs tương ứng.

## TECH SPECIFICATIONS

### Trước khi generate code, phải check nhánh GIT:
git checkout main
git pull
git checkout feat/ws_CompanyB2B



### Backend
- Framework: .NET 8, C#
- Database: SQL Server (LinqToDB)
- Architecture: WebService.Handlers pattern; toàn bộ handler của B2B nằm trong 1 file
  - File: `aladdin/WebService.Handlers/QAHosGenericDB/ws_L_CompanyB2B_Save.cs`
  - Handlers (đều dùng `GenericHandler<Parameters>` và `record Parameters` mạnh kiểu):
    - `ws_L_CompanyB2B_Save` (Create/Update, validate, check trùng mã)
    - `ws_L_CompanyB2B_Get` (Get theo ID; nếu thiếu ID trả list active trong hiệu lực)
    - `ws_L_CompanyB2B_List` (search + pagination + sort)
    - `ws_L_CompanyB2B_Delete` (toggle `IsActive` + cập nhật audit)
    - `ws_L_CompanyB2B_Import` (import CSV, upsert theo `CompanyCode`)
    - `ws_L_CompanyB2B_Export` (xuất CSV, trả Base64 meta)
  - Service phụ trợ: `DateTimeService` (DI)

- API Controller: `aladdin/WebService/Api/CompanyB2BController.cs`
  - Endpoints:
    - POST `/api/company-b2b/save`
    - POST `/api/company-b2b/delete`
    - GET  `/api/company-b2b/get?companyB2BID={id}`
    - GET  `/api/company-b2b/list` (đủ filter + sort + page)
    - POST `/api/company-b2b/import`
    - GET  `/api/company-b2b/export`
  - DTOs: `CompanySaveDto`, `CompanyDeleteDto`, `CompanyImportDto` (Required annotations)

- ### Frontend
- Framework: Next.js, React, TypeScript
- UI: Tailwind CSS
- Excel/CSV Utils: `C:\PROJECTS\genie\app\lib\utils`
- Reference: 
  - Search: https://dev-genie.vnvc.info/quan-ly-tai-khoan/danh-sach-tai-khoan-qapay
  - Pagination: https://dev-genie.vnvc.info/nha-thuoc/quan-li-ca


## Frontend và Backend Implementation
- file tạo mới chỉ 1 file gồm tất cả các tính năng trong file đó luôn nhé.

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

### Export file CSV
1. **Backend**:
   - Tạo CSV từ `L_CompanyB2B` (đã filter theo tham số).
   - Cột xuất ra (tiêu đề tiếng Việt, theo thứ tự):
     - Mã công ty, Tên công ty, Số PO-HĐ, Ngày bắt đầu tiêm, Ngày kết thúc, Ghi chú, Trạng thái
     - Ghi chú hiện để trống (chưa có cột riêng trong DB)
     - Trạng thái: "Kích hoạt"/"Không kích hoạt" theo `IsActive`
   - Sắp xếp: ưu tiên `ModifiedOn` mới nhất trước (nếu null dùng `CreatedOn`), sau đó tie-break theo `CreatedOn` giảm dần.
   - Encode Base64, trả về ở bảng meta `Table2` gồm: `FileName`, `FileExtension=.csv`, `FileData`.

2. **Frontend**:
   - Nhận Base64 CSV, decode và trigger download.

3. **Reference**: `ws_ReportOutput_Get.cs` (tham khảo kiến trúc meta file)

### CSV Header Mapping (Import)
- Bắt buộc: `CompanyCode` ("Mã công ty", "Ma cong ty"), `CompanyName` ("Tên công ty", "Ten cong ty"), `EffectiveFrom` ("Ngày bắt đầu"/"Ngày bắt đầu tiêm"/"Ngay bat dau"), `Hopdong` ("Số PO-HĐ"/"PO"/"Hợp đồng").
- Tùy chọn: `CompanyTax` ("MST"/"Mã số thuế"), `CompanyAddress` ("Địa chỉ"), `EffectiveTo` ("Ngày kết thúc"), `IsActive` ("Kích hoạt"/"Active").
- Date parsing hỗ trợ: `yyyy-MM-dd`, `yyyy/MM/dd`, `dd/MM/yyyy`, `d/M/yyyy`, `MM/dd/yyyy`, `M/d/yyyy`, `yyyy-MM-ddTHH:mm:ss[.fff][K]`.
- Dòng thiếu trường bắt buộc sẽ bị đếm `Skipped` (không fail file).

### Response Schemas (chuẩn hóa)
- Save (create): `Table1[0] = { Result: "Created", CompanyB2BID }`
- Save (update): `Table1[0] = { Result: "Updated", CompanyB2BID }`
- Delete: `Table1[0] = { Result: "Toggled", CompanyB2BID, IsActive }`
- Get (ID có giá trị): `Table1[0] = { errorCode: 0, errorMsg: "Success" }`, `Table2[0] = row`
- Get (không có ID): `Table1 = list active trong hiệu lực` với cột: `CompanyId, CompanyName, CompanyCode, CompanyContract`
- List: `Table1 = rows`, `Table2[0] = { Total, Page, PageSize }`
- Import: `Table1[0] = { Result: "OK", Created, Updated, Skipped }`
- Export: `Table1 = rows`, `Table2[0] = { FileName, FileExtension: ".csv", FileData }`

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

## Validation Rules
Backend:
1. Save: bắt buộc `CompanyCode`, `CompanyTax`, `CompanyName`, `CompanyAddress`, `EffectiveFrom`; `EffectiveFrom <= EffectiveTo`; `CompanyCode` không trùng.
2. Delete: bắt buộc `CompanyB2BID`, `UserID`.
3. List: hỗ trợ toàn bộ filter theo cột; bắt buộc `SortBy`, `SortDir` (mặc định `CreatedOn/DESC`).
4. Import: bắt buộc header tối thiểu (nêu trên); bỏ qua dòng thiếu; parse ngày theo list formats.
5. Export: trả 2 bảng dữ liệu + meta file.

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

## Search Criteria
- CompanyCode (exact)
- CompanyName (contains)
- CompanyTax (exact)
- IsActive (bool)
- EffectiveFrom/EffectiveTo (range)
- Hopdong (contains)
- CompanyAddress (contains)
- CreatedBy/ModifiedBy (exact)

## Pagination
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

## Ghi chú triển khai
- Tất cả handler B2B gom trong 1 file; dùng `GenericHandler<Parameters>` để map YAML/API -> tham số mạnh kiểu.
- `ws_L_CompanyB2B_Get` không có ID sẽ trả danh sách active trong hiệu lực, phục vụ dropdown/list nhanh.
- Import chấp nhận Base64 hoặc CSV raw text.