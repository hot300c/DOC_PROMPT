# ws_BIL_Invoice_Save_Vaccine - Test Cases Report

## Overview
Handler `ws_BIL_Invoice_Save_Vaccine` đã được kiểm tra và cập nhật test cases để phù hợp với response pattern mới với errorCode và errorMsg.

## Changes Made

### 1. Handler Code Fixes
- **Fixed compilation errors**: Sửa lỗi trùng tên biến `dataSet` trong handler
- **Updated response pattern**: Chuyển từ pattern cũ sang pattern mới với `errorCode` và `errorMsg`
- **Maintained functionality**: Tất cả business logic gốc được giữ nguyên

### 2. Test Cases Created/Updated

#### Test-01.yaml: Happy Path - Insert New Invoice
- **Scenario**: Tạo hóa đơn mới khi chưa tồn tại
- **Expected Result**: 
  - `errorCode: 0` (success)
  - `errorMsg: "Invoice saved successfully"`
  - Trả về `InvoiceID` và `InvoiceNo`
- **Data Validation**: Kiểm tra dữ liệu được insert vào 3 bảng: `BIL_Invoice`, `BIL_Invoice_Live`, `BIL_Invoice_CurrentDay`

#### Test-02.yaml: Authentication Failure
- **Scenario**: Session ID không hợp lệ
- **Expected Result**: 
  - `errorCode: 1` (authentication failure)
  - `errorMsg: "Session ID is not valid"`
- **Data Validation**: Không có dữ liệu nào được tạo

#### Test-03.yaml: Invoice Already Exists
- **Scenario**: Hóa đơn đã tồn tại trong database
- **Expected Result**: 
  - `errorCode: 3` (no data found - invoice exists)
  - `errorMsg: "Invoice already exists"`
- **Data Validation**: Không có dữ liệu mới nào được tạo

#### Test-04.yaml: Temporary Advance Payment
- **Scenario**: Tạo hóa đơn tạm ứng với `IsTamUng = true`
- **Expected Result**: 
  - `errorCode: 0` (success)
  - `errorMsg: "Invoice saved successfully"`
  - Trả về `InvoiceID` và `InvoiceNo`
- **Data Validation**: 
  - Kiểm tra `LanThu` được tính đúng (tăng dần)
  - Kiểm tra dữ liệu được insert vào 3 bảng
  - Kiểm tra `Description` được map đúng từ `Note`

#### Test-05.yaml: CalculateTotalContractApprox - Valid Contract
- **Scenario**: Test hàm `CalculateTotalContractApprox` với `HopDongID` hợp lệ
- **Expected Result**: 
  - `errorCode: 0` (success)
  - `TotalContract = 160000` (tính từ 3 records hợp lệ)
- **Logic Tested**: 
  - Tính tổng `GiaMuiTiem + GiaChenhLechChuaGiam` (hoặc `GiaChenhLechTiemNgoai` nếu `GiaChenhLechChuaGiam = 0`)
  - Chỉ tính các records với `IsTiemNgoai=false`, `IsMuiNgoaiDanhMuc=false`, `IsHuyMui=false`, `IsDoiMui=false`

#### Test-06.yaml: CalculateTotalContractApprox - No Contract
- **Scenario**: Test hàm `CalculateTotalContractApprox` với `HopDongID = null`
- **Expected Result**: 
  - `errorCode: 0` (success)
  - `TotalContract = null` (không có contract)
- **Logic Tested**: 
  - Trả về `null` khi `HopDongID` là `null` hoặc `Guid.Empty`

#### Test-07.yaml: CalculateTotalContractApprox - Complex Filtering
- **Scenario**: Test logic filtering phức tạp trong `CalculateTotalContractApprox`
- **Expected Result**: 
  - `errorCode: 0` (success)
  - `TotalContract = 250000` (chỉ tính 2 records hợp lệ)
- **Logic Tested**: 
  - **Included**: Records với tất cả flags = false
  - **Excluded**: Records với `IsTiemNgoai=true`, `IsMuiNgoaiDanhMuc=true`, `IsHuyMui=true`, `IsDoiMui=true`
  - Logic tính toán: `GiaMuiTiem + (GiaChenhLechChuaGiam == 0 ? GiaChenhLechTiemNgoai : GiaChenhLechChuaGiam)`

#### Test-08.yaml: CalculateLanThu - With Existing Records
- **Scenario**: Test hàm `CalculateLanThu` với `IsTamUng = true` và có `LanThu` trước đó
- **Expected Result**: 
  - `errorCode: 0` (success)
  - `LanThu = 3` (tăng từ max LanThu hiện tại + 1)
- **Logic Tested**: 
  - Chỉ tính các records với `IsTamUng = true` và `RefundType = null`
  - Loại trừ records với `RefundType != null` (đã hoàn tiền)
  - Tìm `Max(LanThu)` và tăng lên 1

#### Test-09.yaml: CalculateLanThu - IsTamUng = false
- **Scenario**: Test hàm `CalculateLanThu` với `IsTamUng = false`
- **Expected Result**: 
  - `errorCode: 0` (success)
  - `LanThu = null` (không tính LanThu khi không phải tạm ứng)
- **Logic Tested**: 
  - Trả về `null` khi `IsTamUng = false`
  - Không query database để tính LanThu

#### Test-10.yaml: BuildInvoiceNo - Sequence Increment
- **Scenario**: Test hàm `BuildInvoiceNo` với sequence tăng dần
- **Expected Result**: 
  - `errorCode: 0` (success)
  - `InvoiceNo = '007250816-00004'` (sequence tiếp theo sau 3 invoices hiện có)
- **Logic Tested**: 
  - Chỉ tính sequence từ invoices cùng ngày, cùng counter, cùng facility
  - Loại trừ invoices khác counter, khác facility, khác ngày
  - Format: `MaQuay + yymmdd + '-' + sequence`

#### Test-11.yaml: BuildInvoiceNo - Different Counter OrderIndex
- **Scenario**: Test hàm `BuildInvoiceNo` với các counter có `OrderIndex` khác nhau
- **Expected Result**: 
  - `errorCode: 0` (success)
  - `InvoiceNo = '001250816-00001'` (OrderIndex = 1 → MaQuay = "001")
- **Logic Tested**: 
  - `OrderIndex = 1` → `MaQuay = "001"`
  - `OrderIndex = 15` → `MaQuay = "015"`
  - `OrderIndex = 99` → `MaQuay = "099"`
  - Format: `MaQuay + yymmdd + '-' + sequence`

## Response Pattern Summary

| Scenario | Error Code | Error Message | Description |
|----------|------------|---------------|-------------|
| Success | 0 | "Invoice saved successfully" | Hóa đơn được tạo thành công |
| Auth Failure | 1 | "Session ID is not valid" | Session ID không hợp lệ |
| Invoice Exists | 3 | "Invoice already exists" | Hóa đơn đã tồn tại |

## Business Logic Preserved
- **Invoice Number Generation**: Tự động tạo `InvoiceNo` theo format `MaQuay + yymmdd + sequence`
- **Description Mapping**: Map `Note` thành `Description` theo quy tắc:
  - "tien " → "Tiền viện phí"
  - "dong " → "Tiền chênh lệch"  
  - "tam u" → "Tiền tạm ứng"
  - Default → "Đồng chi trả"
- **Receipt Number**: Tạo từ `ReceiptDaily` theo format `SoKyHieu|SoBienLai`
- **LanThu Calculation**: Tính số lần tạm ứng khi `IsTamUng = true`
- **TotalContract Calculation**: Tính tổng giá trị contract từ `Vaccine_HopDong_Detail` với logic filtering phức tạp
- **LanThu Calculation**: Tính số lần tạm ứng khi `IsTamUng = true`, loại trừ records đã hoàn tiền (`RefundType != null`)
- **Invoice Number Generation**: Tự động tạo `InvoiceNo` theo format `MaQuay + yymmdd + sequence` với logic sequence tăng dần
- **Multi-table Insert**: Insert vào 3 bảng: `BIL_Invoice`, `BIL_Invoice_Live`, `BIL_Invoice_CurrentDay`

## File Links
- **Handler**: `aladdin/WebService.Handlers/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine.cs`
- **Test Class**: `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine_Test.cs`
- **Test Cases**: `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_BIL_Invoice_Save_Vaccine/`

## Conclusion
Việc kiểm tra và cập nhật test cases đã hoàn tất. Handler hoạt động đúng với response pattern mới và tất cả test cases đều pass. Business logic gốc được bảo toàn hoàn toàn.
