# README_TODO_BEFORE_GEN.md - ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh

## 📋 Thông tin chung

- **Ticket**: 
- **Mục tiêu**: Convert stored procedure `ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh`
- **Tên file handler**: `ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh.cs`
- **Mô tả**: Kiểm tra cảnh báo tiêm vaccine trùng nhóm bệnh

## 🔍 Phân tích Stored Procedure

### Input Parameters:
- `@SessionID VARCHAR(MAX)` - Session ID của user
- `@PatientID UNIQUEIDENTIFIER` - ID của bệnh nhân
- `@MaChung VARCHAR(100)` - Mã chung của vaccine
- `@NgayChiDinh DATE` - Ngày chỉ định tiêm
- `@PhacDoDangChiDinh UNIQUEIDENTIFIER` - ID phác đồ đang chỉ định
- `@FacID VARCHAR(10)` - ID của facility

### Output:
- `Errcode`: 0 nếu không có cảnh báo, 1 nếu có cảnh báo
- `ErrMsg`: Thông báo cảnh báo (nếu có)

### Logic chính:

1. **Lấy thông tin phác đồ đang chỉ định:**
   - Từ `Vaccine_PhacDoBenhNhan` lấy `IDPhacDo`
   - Từ `L_Vaccine_Phacdo` lấy `DoiTuongSuDungID`

2. **Lấy danh sách nhóm bệnh của vaccine đang chỉ định:**
   - Từ `L_NhomBenhVaccineDetail` lấy `NhomBenhID` theo `MaChung`

3. **Lấy danh sách vaccine cùng nhóm bệnh:**
   - Tìm các `MaChung` khác có cùng `NhomBenhID`
   - Loại trừ vaccine đang chỉ định

4. **Kiểm tra phác đồ bệnh nhân đã có:**
   - Tìm các phác đồ của bệnh nhân có vaccine cùng nhóm bệnh
   - Chỉ xét phác đồ cùng đối tượng sử dụng và chưa đóng

5. **Kiểm tra lịch sử tiêm:**
   - Tìm các mũi tiêm đã hoàn thành của vaccine cùng nhóm bệnh
   - Loại trừ ngày chỉ định hiện tại

6. **Tạo thông báo cảnh báo:**
   - Nếu có mũi tiêm trùng nhóm bệnh, tạo thông báo cảnh báo
   - Format: "Bệnh [TenNhomBenh] đã được tiêm bởi vaccine [HospitalName] vào ngày [CompleteOn]. Bạn có muốn cập nhật lại lịch tiêm cho vaccine này không?"

## 🏗️ Cấu trúc Handler

### Class Parameters:
```csharp
public class Parameters
{
    public string SessionID { get; set; }
    public Guid PatientID { get; set; }
    public string MaChung { get; set; }
    public DateTime NgayChiDinh { get; set; }
    public Guid PhacDoDangChiDinh { get; set; }
    public string FacID { get; set; }
}
```

### Các Function cần tách:

1. **`GetPhacDoInfo()`** - Lấy thông tin phác đồ đang chỉ định
2. **`GetNhomBenhList()`** - Lấy danh sách nhóm bệnh của vaccine
3. **`GetVaccineCungNhomBenh()`** - Lấy danh sách vaccine cùng nhóm bệnh
4. **`GetPhacDoBenhNhanTrung()`** - Lấy phác đồ bệnh nhân trùng nhóm bệnh
5. **`GetLichSuTiemTrung()`** - Lấy lịch sử tiêm trùng nhóm bệnh
6. **`CreateCanhBaoMessage()`** - Tạo thông báo cảnh báo
7. **`Handle()`** - Function chính

## 🗄️ Entities sử dụng:

1. **`VaccinePhacDoBenhNhan`** - Phác đồ vaccine của bệnh nhân
2. **`LVaccinePhacdo`** - Danh mục phác đồ vaccine
3. **`LNhomBenhVaccineDetail`** - Chi tiết nhóm bệnh vaccine
4. **`LNhomBenhVaccine`** - Danh mục nhóm bệnh vaccine
5. **`VaccinePhacDoBenhNhanDetail`** - Chi tiết phác đồ vaccine bệnh nhân
6. **`LProduct`** - Danh mục sản phẩm (để lấy HospitalName)

## 📁 Đường dẫn file:

- **Handler**: `C:\PROJECTS\aladdin\WebService.Handlers\QAHosGenericDB\ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh.cs`
- **Test**: `C:\PROJECTS\aladdin\WebService.Handlers.Tests\QAHosGenericDB\ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh_Test.cs`
- **TestCases**: `C:\PROJECTS\aladdin\WebService.Handlers.Tests\TestCases\QAHosGenericDB\ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh\`

## 🔧 Yêu cầu kỹ thuật:

- Sử dụng `With(SqlServerHints.Table.NoLock)` cho tất cả queries
- Có try-catch và logging cẩn thận
- Tách code thành các function nhỏ, dễ đọc, dễ test
- Tuân thủ naming convention PascalCase
- Có XML documentation cho mỗi function
- Tạo test cases đầy đủ

## 📝 Ghi chú từ SQL:

- Sử dụng comment tiếng Anh tương ứng với logic SQL
- Giữ nguyên business logic gốc
- Chỉ tách thành function để code dễ đọc và maintain
