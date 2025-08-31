# README_TODO_BEFORE_GEN.md - ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc

## 📋 Thông tin chung
- **Stored Procedure**: `ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc`
- **Mục tiêu**: Convert stored procedure sang C# handler
- **Tên file handler**: `ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc.cs`

## 🔍 Phân tích Stored Procedure

### Input Parameters:
1. `@SessionID VARCHAR(MAX)` - Session ID để xác thực user
2. `@FacID VARCHAR(10)` - Facility ID
3. `@HopDongID UNIQUEIDENTIFIER` - Contract ID
4. `@IDPhacDo INT` - Protocol ID

### Business Logic:
1. **Lấy dữ liệu cơ bản** từ `Vaccine_HopDong_Detail_Root` theo `HopDongID` và `IDPhacDo`
2. **Tính toán ThanhTien** dựa trên logic phức tạp:
   - Nếu `IsMuiNgoaiDanhMuc = 1` hoặc `IsTiemNgoai = 1` thì `ThanhTien = 0`
   - Ngược lại tính theo công thức phức tạp với `GiaChenhLechChuaGiam`, `GiaChenhLechTiemNgoai`, `TienGiam`, `PhanTramGiam`
3. **Cập nhật STTMuiTiem** từ `L_Vaccine_Phacdo_Detail`
4. **Cập nhật SoHopDong** từ `Vaccine_HopDong`
5. **Cập nhật DoiTuongSuDungID** từ `L_Vaccine_Phacdo`
6. **Sắp xếp kết quả** theo `STTMuiTiem`

### Output Fields:
- `STTMuiTiem`: Thứ tự mũi tiêm
- `Gia`: Giá mũi tiêm
- `TienGiam`: Tiền giảm
- `PhanTramGiam`: Phần trăm giảm
- `ThanhTien`: Thành tiền (đã tính toán)
- `NgayDung`: Ngày dùng
- `IsTiemNgoai`: Có phải tiêm ngoài không
- `ID_Detail`: Mã mũi tiêm
- `IDPhacDo`: ID phác đồ
- `ThoiGian_GianCach`: Thời gian giãn cách
- `HopDongID`: ID hợp đồng
- `SoHopDong`: Số hợp đồng
- `HopDongDetailID`: ID chi tiết hợp đồng
- `IsMuiNgoaiDanhMuc`: Có phải mũi ngoài danh mục không
- `GiaChenhLechTiemNgoai`: Giá chênh lệch tiêm ngoài
- `DoiTuongSuDungID`: ID đối tượng sử dụng
- `LoaiGianCach`: Loại giãn cách
- `MuiThanhToan`: Mũi thanh toán
- `IsKhongDuocBoCheckThanhToan`: Có được bỏ check thanh toán không
- `HopDongID_Goc`: ID hợp đồng gốc
- `GiaChenhLechChuaGiam`: Giá chênh lệch chưa giảm
- `IsDaTiem`: Đã tiêm chưa

## 🏗️ Cấu trúc Code Handler

### Class Parameters:
```csharp
public class Parameters
{
    [Required]
    public string SessionID { get; set; } = string.Empty;
    
    [Required]
    public string FacID { get; set; } = string.Empty;
    
    [Required]
    public Guid HopDongID { get; set; }
    
    [Required]
    public int IDPhacDo { get; set; }
}
```

### Các Function cần tạo:
1. **`AuthenticateUser(string sessionID)`** - Xác thực user
2. **`ValidateInput(Parameters @params)`** - Validate input parameters
3. **`GetContractDetailData(Parameters @params)`** - Lấy dữ liệu chi tiết hợp đồng
4. **`CalculatePaymentAmount(DataTable resultData)`** - Tính toán thành tiền
5. **`UpdateSequenceNumber(DataTable resultData)`** - Cập nhật số thứ tự mũi tiêm
6. **`UpdateContractNumber(DataTable resultData)`** - Cập nhật số hợp đồng
7. **`UpdateUsageObjectID(DataTable resultData)`** - Cập nhật ID đối tượng sử dụng
8. **`CreateResultDataSet(DataTable resultData)`** - Tạo DataSet kết quả

## 📁 Đường dẫn file cần tạo:
- **Handler**: `C:\PROJECTS\aladdin\WebService.Handlers\QAHosGenericDB\ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc.cs`
- **Test**: `C:\PROJECTS\aladdin\WebService.Handlers.Tests\QAHosGenericDB\ws_LayDanhSachMuiTiemTheoHopDongDaDatTruocTests.cs`
- **Test Cases YAML**: `C:\PROJECTS\aladdin\WebService.Handlers.Tests\TestCases\QAHosGenericDB\ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc.yaml`

## 🔧 Các bước thực hiện:
1. Tạo file handler với cấu trúc đã phân tích
2. Implement các function theo business logic
3. Test compile để đảm bảo không có lỗi
4. Tạo test cases
5. Tạo file README_GEN.md
6. Commit và push code

## ⚠️ Lưu ý quan trọng:
- Sử dụng `With(SqlServerHints.Table.NoLock)` cho tất cả queries
- Thêm try-catch và logging cẩn thận
- Giữ nguyên business logic như stored procedure gốc
- Code phải dễ đọc, dễ test, dễ maintain
