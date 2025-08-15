# Task 14: Convert Stored Procedure ws_CN_ClinicalSessions_GetByNgayChiDinh

## 📋 Thông tin chung
- **Stored Procedure**: `ws_CN_ClinicalSessions_GetByNgayChiDinh`
- **Mục tiêu**: Convert stored procedure thành C# handler
- **Tên file handler**: `ws_CN_ClinicalSessions_GetByNgayChiDinh.cs`

## 🔍 Phân tích Stored Procedure

### Parameters:
1. `@SessionID VARCHAR(MAX)` - Session ID của user
2. `@NgayChiDinh DATETIME` - Ngày chỉ định dịch vụ
3. `@FacID VARCHAR(10)` - Facility ID
4. `@PatientID UNIQUEIDENTIFIER` - Patient ID

### Logic chính:
1. **Kiểm tra cấu hình quản lý bệnh nhân theo chuỗi**:
   - Lấy setting `QuanLiBenhNhanTheoChuoi` từ bảng `Application..Settings` với ID = 90000
   - Nếu không tìm thấy theo FacID, tìm theo FacID = '0'
   - Nếu vẫn không tìm thấy, mặc định = 'N'

2. **Xử lý theo 2 trường hợp**:
   - **Trường hợp 1**: `QuanLiBenhNhanTheoChuoi = 'Y'`
     - Lấy `CustomerID` từ bảng `L_Customer` theo `FacID`
     - Join với `CN_FacAdmissions` để lấy `FacID`
     - Cập nhật `ServiceName` từ bảng `L_Service` theo `ServiceID` và `FacID`
   
   - **Trường hợp 2**: `QuanLiBenhNhanTheoChuoi = 'N'`
     - Không cần lấy `CustomerID`
     - Cập nhật `ServiceName` từ bảng `L_Service` theo `ServiceID` và `FacID` cố định

3. **Điều kiện lọc**:
   - `cs.PatientID = @PatientID`
   - `UserCreatedDate = CAST(@NgayChiDinh AS DATE)`
   - `ServiceID != 0`
   - `fa.FacAdmissionType != 'IP'`

4. **Kết quả trả về**:
   - `ServiceID`, `ServiceName`, `Qty`, `DonGia`, `ThanhTien`
   - Group by `ServiceID`, `ServiceName`, `DonGia`
   - Sum `Qty` và `ThanhTien`

## 🏗️ Cấu trúc Handler cần tạo

### 1. Parameters Class:
```csharp
public class Parameters
{
    [Required]
    public string SessionID { get; set; }
    
    [Required]
    public DateTime NgayChiDinh { get; set; }
    
    [Required]
    public string FacID { get; set; }
    
    [Required]
    public Guid PatientID { get; set; }
}
```

### 2. Các Function cần tách:
1. **`AuthenticateUser(string sessionId)`** - Xác thực user
2. **`GetApplicationSettings(string facId)`** - Lấy cấu hình quản lý bệnh nhân theo chuỗi
3. **`GetCustomerId(string facId)`** - Lấy CustomerID nếu cần
4. **`GetClinicalSessions(Parameters @params, bool quanLiBenhNhanTheoChuoi)`** - Lấy danh sách clinical sessions
5. **`UpdateServiceNames(List<ResultDto> results, bool quanLiBenhNhanTheoChuoi, string facId)`** - Cập nhật tên dịch vụ
6. **`CalculateTotalAmount(List<ResultDto> results)`** - Tính toán tổng tiền
7. **`GroupAndFormatResults(List<ResultDto> results)`** - Nhóm và format kết quả

### 3. Entities cần sử dụng:
- `CN_ClinicalSessions`
- `CN_FacAdmissions`
- `L_Service`
- `L_Customer`
- `Application.Settings`

### 4. Test Cases cần tạo:
1. **Test cơ bản**: Authentication, validation
2. **Test QuanLiBenhNhanTheoChuoi = 'Y'**: Trường hợp quản lý theo chuỗi
3. **Test QuanLiBenhNhanTheoChuoi = 'N'**: Trường hợp không quản lý theo chuỗi
4. **Test edge cases**: Không có dữ liệu, dữ liệu null
5. **Test error cases**: Invalid input, exceptions

## 📁 Đường dẫn file cần tạo:
- **Handler**: `aladdin/WebService.Handlers/QAHosGenericDB/ws_CN_ClinicalSessions_GetByNgayChiDinh.cs`
- **Test Cases**: `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_CN_ClinicalSessions_GetByNgayChiDinhTests.cs`
- **Test Data**: `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_CN_ClinicalSessions_GetByNgayChiDinh/`

## ⚠️ Lưu ý quan trọng:
1. File handler đã tồn tại nhưng cần refactor theo template
2. Cần thêm Parameters class và tách thành các function nhỏ
3. Cần thêm try-catch và logging
4. Cần tạo test cases đầy đủ
5. Sử dụng `With(SqlServerHints.Table.NoLock)` cho performance
6. Đảm bảo logic giống hệt stored procedure gốc
