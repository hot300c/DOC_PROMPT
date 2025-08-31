# ws_BIL_InvoiceDetail_Save_Vaccine - Refactoring Report

## Overview
Handler `ws_BIL_InvoiceDetail_Save_Vaccine` đã được convert từ stored procedure và tách thành các function nhỏ, dễ đọc, dễ test.

## Changes Made

### 1. Code Refactoring
- `AuthenticateUser()`: Xác thực người dùng từ `SessionID` hoặc `UserId` đã được test harness bơm vào.
- `GetClinicalSession()`: Lấy context của `CN_ClinicalSessions` với NoLock.
- `ApplyVaccineContractPricing()`: Map logic 1.1.2.1 và 1.1.4.1 của store: lấy `UserID` từ hóa đơn tạm ứng gần nhất; tính `DonGia`, `PatientPay`, `SoTienGiam`, `ChenhLech` từ `Vaccine_HopDong_Detail` và phụ lục khi cần.
- `ValidateBusinessRules()`: Map 1.0.0.9 và 1.0.0.12 – kiểm tra thay đổi DVKT và số lượng thuốc.
- `InsertBilInvoiceDetail()`: Insert bản ghi chính vào `BIL_InvoiceDetail` với `With(SqlServerHints.Table.NoLock)` trong truy vấn nguồn và set các trường audit.
- `InsertBilInvoiceDetailLive()`: Ghi đồng bộ vào `BIL_InvoiceDetail_Live`.
- `CallCurrentDayHandler()`: Gọi handler đã có `ws_BIL_InvoiceDetail_CurrentDay_ByInvoiceDetail_Save` để tạo bản ghi current-day.
- `InsertAdvancedPaymentIfAny()`: Thêm vào `BIL_Invoice_AdvancedPayment` khi có `AdvancedPaymentID`.

### 2. Benefits of Refactoring
- Dễ đọc: phân rã function, tên rõ ràng.
- Dễ test: mỗi function có thể test riêng.
- Dễ maintain: tách rõ retrieval/logic/update.
- Giữ hiệu năng: dùng `NoLock` theo chuẩn codebase.

### 3. Test Cases Updated
- Tạo class test `ws_BIL_InvoiceDetail_Save_Vaccine_Test` và 3 test case YAML:
  - Test-01: Happy path insert, IsTiem=1, có AdvancedPayment.
  - Test-02: Lỗi DVKT thay đổi khi không có session + ServiceID != 0.
  - Test-03: Lỗi số lượng thuốc thay đổi so với session.

Liên kết nhanh:
- `aladdin/WebService.Handlers/QAHosGenericDB/ws_BIL_InvoiceDetail_Save_Vaccine.cs`
- `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_BIL_InvoiceDetail_Save_Vaccine_Test.cs`
- `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_BIL_InvoiceDetail_Save_Vaccine/Test-01.yaml`
- `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_BIL_InvoiceDetail_Save_Vaccine/Test-02.yaml`
- `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_BIL_InvoiceDetail_Save_Vaccine/Test-03.yaml`

### 4. Business Logic Preserved
- Ánh xạ đầy đủ block tính giá và kiểm tra phụ lục hợp đồng (1.1.2.1, 1.1.4.1, 1.0.0.9, 1.0.0.12) của store.

### 5. Performance Considerations
- Sử dụng `With(SqlServerHints.Table.NoLock)` cho các SELECT.

## Conclusion
Việc convert và refactor hoàn tất, logic chính được giữ nguyên, có test tự động và tài liệu kèm theo.


