# README_TODO_BEFORE_GEN.md - ws_Vaccine_KiemTraTrungNhomBenhDangMo

## 📋 Thông tin chung
- **Ticket**: 
- **Mục tiêu**: Convert stored procedure `ws_Vaccine_KiemTraTrungNhomBenhDangMo`
- **Tên file handler**: `ws_Vaccine_KiemTraTrungNhomBenhDangMo.cs`

## 🔍 Phân tích Stored Procedure

### Chức năng
Kiểm tra phác đồ nhóm bệnh trùng đang mở (NgayDong IS NULL)

### Parameters
- `@SessionID VARCHAR(max)` - Session ID
- `@MaChung VARCHAR(100)` - Mã chung vaccine
- `@PatientID UNIQUEIDENTIFIER` - ID bệnh nhân

### Logic chính
1. Tìm số lượng phác đồ trùng nhau cho cùng một nhóm bệnh
2. Điều kiện: PatientID, MaChung, và NgayDong IS NULL (đang mở)
3. Trả về số lượng phác đồ trùng (MAX của count)

### SQL Query gốc
```sql
SELECT @SoPhacDo = MAX(SLPD) FROM (
    SELECT pd.NhomBenhID, Count(pd.NhomBenhID) SLPD 
    FROM QAHosGenericDB..Vaccine_PhacDoBenhNhan_NhomBenh pd WITH(NOLOCK)
    JOIN QAHosGenericDB..L_NhomBenhVaccineDetail lb WITH(NOLOCK)
    ON lb.NhomBenhID= pd.NhomBenhID
    WHERE PatientID = @PatientID 
    AND lb.MaChung=@MaChung 
    AND pd.NgayDong IS NULL
    Group By pd.NhomBenhID
    Having count(pd.NhomBenhID)>1
) as p
```

## 🏗️ Cấu trúc Handler

### Class Parameters
```csharp
public class Parameters
{
    public string SessionID { get; set; }
    public string MaChung { get; set; }
    public Guid PatientID { get; set; }
}
```

### Các Function cần tách
1. **ValidateInput()** - Validate input parameters
2. **GetDuplicateProtocolCount()** - Lấy số lượng phác đồ trùng
3. **CreateResultDataSet()** - Tạo kết quả trả về

### Entities sử dụng
- `VaccinePhacDoBenhNhanNhomBenh` - Bảng chính
- `LNhomBenhVaccineDetail` - Bảng lookup để join với MaChung

## 📁 Đường dẫn file
- **Handler**: `aladdin/WebService.Handlers/QAHosGenericDB/ws_Vaccine_KiemTraTrungNhomBenhDangMo.cs`
- **Test**: `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_Vaccine_KiemTraTrungNhomBenhDangMo_Test.cs`
- **Test Cases**: `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_Vaccine_KiemTraTrungNhomBenhDangMo/`

## 🧪 Test Cases cần tạo
1. **Test-01.yaml**: Trường hợp có phác đồ trùng (count > 1)
2. **Test-02.yaml**: Trường hợp không có phác đồ trùng (count <= 1)
3. **Test-03.yaml**: Trường hợp không có dữ liệu
4. **Test-04.yaml**: Trường hợp PatientID không tồn tại
5. **Test-05.yaml**: Trường hợp MaChung không tồn tại

## ⚠️ Lưu ý kỹ thuật
- Sử dụng `With(SqlServerHints.Table.NoLock)` cho performance
- Có try-catch và logging cẩn thận
- Code phải đảm bảo đúng logic như stored procedure gốc
- Tách code thành các function nhỏ, dễ đọc, dễ test
- Cần có XML documentation cho mỗi function
