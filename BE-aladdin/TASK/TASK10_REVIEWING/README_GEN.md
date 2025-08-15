# ws_BIL_Invoice_Save_Vaccine - Refactoring/Conversion Report

## Overview
Đã chuyển SP `dbo.ws_BIL_Invoice_Save_Vaccine` sang handler `.NET` theo kiến trúc Aladdin, đặt tại `aladdin/WebService.Handlers/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine.cs`.

## Changes Made
- Tạo handler với cấu trúc `GenericHandler<Parameters>`.
- Xác thực `SessionID` để lấy `UserID` từ `Security..Sessions`.
- Áp dụng logic:
  - Chuẩn hóa `CaseID`, `HopDongID` rỗng về `null`.
  - Tính `InvoiceNo` theo `L_Counter.OrderIndex` + yymmdd + sequence trong ngày (từ `BIL_Invoice_CurrentDay`).
  - Tính `Description` theo 5 ký tự không dấu đầu từ `Note`.
  - Tính `ReceiptNumber` từ `ReceiptDaily` (`SoKyHieu|padded(SoBienLai)`).
  - Tính `LanThu` khi `IsTamUng=1`.
  - Tính xấp xỉ `TotalContract` từ `Vaccine_HopDong_Detail`.
  - Insert `BIL_Invoice`, `BIL_Invoice_Live`, `BIL_Invoice_CurrentDay`.
- Thêm test tối thiểu và YAML dữ liệu để verify flow insert cơ bản (cần môi trường nuget đầy đủ để chạy test end-to-end).

## Files
- Handler: `aladdin/WebService.Handlers/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine.cs`
- Test: `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine_Test.cs`
- TestCase YAML: `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine/Test-01.yaml`

## Test Cases
- Test-01: Insert hóa đơn mới với session hợp lệ, tồn tại `L_Counter` và `ReceiptDaily`.
  - Kỳ vọng: Bản ghi mới trong `BIL_Invoice`, `BIL_Invoice_Live`, `BIL_Invoice_CurrentDay` được tạo, `Description`, `ReceiptNumber` đúng.

## Notes
- SP có gọi `History..sp_BIL_Invoice_LogUpdate`; hiện project chưa có `HistoryService` tương ứng cho `BIL_Invoice`, do đó phần này chưa tích hợp.
- Chuỗi xuất dùng kiểu mặc định, có thể điều chỉnh single-quote trong nơi cần thiết khác.
- Mọi truy vấn đều có `With(SqlServerHints.Table.NoLock)` để đảm bảo hiệu năng như guideline.

## Quick Links
- Handler: aladdin/WebService.Handlers/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine.cs
- Test: aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine_Test.cs
- YAML: aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine/Test-01.yaml

## Conclusion
Handler đã được implement theo yêu cầu, build thành công. Test YAML và test C# đã được tạo sẵn để kiểm thử trên môi trường đầy đủ.
