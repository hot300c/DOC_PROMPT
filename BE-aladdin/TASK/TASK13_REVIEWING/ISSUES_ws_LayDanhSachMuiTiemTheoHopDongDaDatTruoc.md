# Issues Summary - ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc

## Tổng quan vấn đề
Test case đang fail với lỗi: **"Expected 1 tables, but actual 0"** - nghĩa là handler trả về DataSet rỗng thay vì DataSet có 1 table như mong đợi.

## Các vấn đề đã phát hiện

### 1. Vấn đề chính: Handler trả về DataSet rỗng
- **Lỗi**: `Xunit.Sdk.TrueException: Expected 1 tables, but actual 0`
- **Nguyên nhân**: Handler không tìm thấy dữ liệu phù hợp trong database
- **Trạng thái**: Đã thêm debug logging để xác định nguyên nhân

### 2. Vấn đề với DateTime overflow
- **Lỗi**: `SqlDateTime overflow. Must be between 1/1/1753 12:00:00 AM and 12/31/9999 11:59:59 PM`
- **Nguyên nhân**: Sử dụng `DateTime.MinValue` (1/1/0001) nằm ngoài phạm vi SQL Server
- **Giải pháp**: Đã thay thế bằng `new DateTime(1753, 1, 1)`
- **Trạng thái**: ✅ Đã sửa

### 3. Vấn đề với property name
- **Lỗi**: `VaccineHopDong` không có property `FacID`
- **Nguyên nhân**: Property name là `FacId` (không phải `FacID`)
- **Giải pháp**: Đã sửa thành `FacId`
- **Trạng thái**: ✅ Đã sửa

### 4. Vấn đề với việc query dữ liệu từ L_Vaccine_Phacdo
- **Lỗi**: `Phacdo found: False` - không tìm thấy dữ liệu trong bảng `L_Vaccine_Phacdo`
- **Nguyên nhân**: Query với điều kiện `IdPhacDo == idPhacDo && FacId == facId` không trả về kết quả
- **Trạng thái**: 🔍 Đang debug

### 5. Vấn đề với việc update các field quan trọng
- **Lỗi**: `DoiTuongSuDungID` expected '1' nhưng actual '0'
- **Lỗi**: `ThoiGian_GianCach` expected '30' nhưng actual '0'
- **Lỗi**: `LoaiGianCach` expected '1' nhưng actual '0'
- **Nguyên nhân**: Các method `UpdateUsageObjectID` và `UpdateThoiGianGianCach` không lấy được dữ liệu
- **Trạng thái**: 🔍 Đang debug

### 6. Vấn đề với số lượng rows
- **Lỗi**: Test-03 expected 2 rows nhưng actual 1 row
- **Nguyên nhân**: Handler chỉ trả về 1 row thay vì 2 rows như mong đợi
- **Trạng thái**: 🔍 Đang debug

## Các method đã thêm để debug

### 1. `DebugDatabaseData()`
- Kiểm tra tổng số rows trong các bảng
- Kiểm tra dữ liệu phù hợp với điều kiện query
- Log chi tiết về dữ liệu tìm thấy

### 2. Debug logging trong các method update
- `UpdateUsageObjectID()`: Log điều kiện query và kết quả
- `UpdateThoiGianGianCach()`: Log điều kiện query và kết quả

## Cấu trúc dữ liệu test case

### Bảng Vaccine_HopDong_Detail_Root
- `HopDongID: '11111111-1111-1111-1111-111111111111'`
- `FacID: '8.1'`
- `IDPhacDo: 1`

### Bảng L_Vaccine_Phacdo
- `FacID: '8.1'`
- `DoiTuongSuDungID: 1`
- `LoaiGianCach: 1`
- **Lưu ý**: Không có field `IDPhacDo` trong test case!

### Bảng L_Vaccine_Phacdo_Detail
- `FacID: '8.1'`
- `IDPhacDo: 1`
- `ThoiGian_GianCach: 30`

## Các vấn đề cần kiểm tra

### 1. Mapping dữ liệu test case
- Kiểm tra xem test data có được load đúng cách không
- Kiểm tra mapping giữa các bảng có chính xác không

### 2. Logic query trong handler
- Kiểm tra điều kiện query trong `GetContractDetailData()`
- Kiểm tra điều kiện query trong `UpdateUsageObjectID()` và `UpdateThoiGianGianCach()`

### 3. Kiểu dữ liệu
- Kiểm tra kiểu dữ liệu của `FacId` trong các bảng
- Kiểm tra việc so sánh string có chính xác không

### 4. Cấu trúc database
- Kiểm tra xem các bảng có đúng cấu trúc như mong đợi không
- Kiểm tra xem có thiếu field nào không

## Hướng dẫn debug

### 1. Chạy test với debug output
```bash
dotnet test WebService.Handlers.Tests --filter "ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc_Test" --verbosity normal
```

### 2. Kiểm tra debug output
- Tìm các dòng bắt đầu với "DEBUG:"
- Đặc biệt chú ý các dòng "Phacdo found:", "UpdateUsageObjectID - Found", "UpdateThoiGianGianCach - Found"

### 3. So sánh với test case
- Kiểm tra xem dữ liệu trong database có khớp với test case không
- Kiểm tra xem có thiếu field nào trong test case không

## Các file liên quan

### 1. Handler
- `aladdin/WebService.Handlers/QAHosGenericDB/ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc.cs`

### 2. Test case
- `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc_Test.cs`
- `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc/Test-01.yaml`

### 3. Entities
- `aladdin/Entities/QAHosGenericDB/VaccineHopDongDetailRoot.cs`
- `aladdin/Entities/QAHosGenericDB/LVaccinePhacdo.cs`
- `aladdin/Entities/QAHosGenericDB/LVaccinePhacdoDetail.cs`

## Trạng thái hiện tại
- ✅ Build thành công
- ✅ Không còn lỗi compile
- 🔍 Test vẫn fail, cần debug thêm
- 🔍 Đã thêm logging để xác định nguyên nhân

## Hành động cần thực hiện

### Ngắn hạn (ngày mai)
1. Chạy test để xem debug output
2. Phân tích debug output để xác định nguyên nhân chính xác
3. Kiểm tra mapping dữ liệu giữa các bảng

### Dài hạn
1. Sửa logic query nếu cần
2. Cập nhật test case nếu có vấn đề về dữ liệu
3. Thêm unit test cho các method riêng lẻ
4. Cải thiện error handling và logging

---
*File này được tạo tự động để ghi chú các vấn đề đã phát hiện. Vui lòng cập nhật khi có thông tin mới.*
