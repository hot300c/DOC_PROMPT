# TODO before code generation for ws_BIL_Invoice_Save_Vaccine

## Nguồn đầu vào
- File SQL: `store.md` chứa SP `dbo.ws_BIL_Invoice_Save_Vaccine`
- Yêu cầu chung: `README_TASK_TEMPLATE.md`

## Mục tiêu
- Convert SP `ws_BIL_Invoice_Save_Vaccine` sang handler `.cs` trong `aladdin/WebService.Handlers/QAHosGenericDB`.
- Logic chính: Insert `BIL_Invoice` (và `BIL_Invoice_Live`, `BIL_Invoice_CurrentDay`) khi chưa tồn tại, theo các quy tắc sinh `InvoiceNo`, `ReceiptNumber`, `Description`, `LanThu`, `TotalContract`, xác thực `SessionID` để lấy `UserID`.

## Mapping tham số
- Input (theo SP):
  - `SessionID`, `InvoiceID`, `FacID`, `PatientID`, `CaseID`, `FacAdmissionID`, `PhysicianAdmissionID`, `HopDongID`, `CounterID`, `InvoiceNo`, `DoiTuongID`, `Total`, `RealTotal`, `IsPaid`, `IsTamUng`, `PatientType`, `Reason`, `Note`, `ReceiptNumber`, `SoKyHieu`, `ShiftID`, `HinhThucThanhToan`, `IsVAT`, `IsNgoaiGio`, `IsChenhLech`, `IsThuPhi`, `TongTienGiam`, `PhanTramMienGiam`, `LiDoMienGiam`, `SoTK`, `SoTKNhan`, `ApprovedInID`, `ApprovedOutID`, `IsTiem`, `IPUser`, `MacAddressUser`, `TypeID_LoaiThu`.
- Output: DataSet rỗng (nếu user chưa auth hoặc invoice đã tồn tại), hoặc DataSet có `{ Result = 1, InvoiceID, InvoiceNo }`.

## Logic chi tiết (áp dụng vào code)
1. Xác thực Session
   - Lấy `UserID` từ `Security..Sessions` theo `SessionID`. Không có thì return.
   - Nếu `IsTiem = 1` và có `PatientID`, override `UserID` bằng `CreatedByUser` của `BIL_Invoice` tạm ứng gần nhất (`IsTamUng=1`) của `PatientID` (theo SP).

2. Chuẩn hóa input
   - `CaseID = NULL` khi `0000-...-0000`.
   - `HopDongID = NULL` khi `0000-...-0000`.

3. Kiểm tra tồn tại
   - Nếu đã có `BIL_Invoice` với `InvoiceID` thì dừng (SP nhánh insert mới khi không tồn tại).

4. Sinh `InvoiceNo`
   - Lấy `OrderIndex` từ `L_Counter` để tạo `MaQuay` (3 chữ số pad-left).
   - Tạo prefix `MaQuay + yyMMDD + '-'`.
   - Lấy `BIL_Invoice_CurrentDay` trong ngày hiện tại theo `FacID` (bỏ qua `InvoiceNo` bắt đầu `HDNG`, match theo prefix) -> tăng sequence 5 chữ số.

5. Tạo `Description` từ `Note`
   - Chuyển `Note` về không dấu, lấy 5 ký tự đầu -> map:
     - `"tien "` -> "Tiền viện phí"
     - `"dong "` -> "Tiền chênh lệch"
     - `"tam u"` -> "Tiền tạm ứng"
     - mặc định -> "Đồng chi trả"

6. Tạo `ReceiptNumber`
   - Chọn 1 dòng `ReceiptDaily` theo `FacID`, `CounterID`, `IsVAT`, `IsActive=1`.
   - `ReceiptNumber = SoKyHieu + '|' + zeroPad(SoBienLai, len(SoCuoi))`.

7. Tính `LanThu`
   - Khi `IsTamUng=1`: `LanThu = Max(LanThu) + 1` của các invoice cùng `PatientID`, `HopDongID` và `IsTamUng=1`, `RefundType IS NULL`. Nếu chưa có -> `1`.

8. Tính `TotalContract` (xấp xỉ)
   - Theo nhóm chi tiết `Vaccine_HopDong_Detail`: cộng `GiaMuiTiem + (GiaChenhLechChuaGiam == 0 ? GiaChenhLechTiemNgoai : GiaChenhLechChuaGiam)` và `Round` -> lưu vào `BIL_Invoice.TotalContract`.
   - Ghi chú: logic SP gốc rất dài, handler thực hiện bản rút gọn phù hợp với hiện trạng entity.

9. Insert dữ liệu
   - `BIL_Invoice`: đầy đủ các trường theo SP (CreatedDateAsInt = yyyyMMddHHmmss, CreatedByUser = UserID, ...).
   - `BIL_Invoice_Live`: set `CheckSum_FacID`, `CreatedDateAsInt = yyyyMMdd`, `CreatedOnAsInt = yyyyMMddHHmmss`, các trường còn lại mirror từ `BIL_Invoice`.
   - `BIL_Invoice_CurrentDay`: lưu `InvoiceID`, `InvoiceNo`, `FacID`, `CreatedDateAsInt = yyyyMMddHHmmss`, `CreatedOn`.

10. Lịch sử/History
   - SP gọi `History..sp_BIL_Invoice_LogUpdate`. Hiện tại codebase chưa có `HistoryService` tương ứng cho `BIL_Invoice`; chưa thực hiện phần này.

## Kiểm thử
- Tạo test case YAML: insert mới với session hợp lệ, có `L_Counter` và `ReceiptDaily` -> mong đợi 3 bảng được insert.
- Tạo test C#: `ws_BIL_Invoice_Save_Vaccine_Test`.
- Lưu ý: Test runner hiện gặp lỗi dependency (`Azure.Core`) trong môi trường, cần môi trường đầy đủ nuget để chạy test.

## Đầu ra cần tạo
- Handler: `aladdin/WebService.Handlers/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine.cs`
- Test: `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine_Test.cs`
- YAML: `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine/Test-01.yaml`
