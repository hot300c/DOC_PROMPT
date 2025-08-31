# Task 15: Convert Stored Procedure ws_Vaccine_ThongBaoKhongchan

## 📋 Thông tin chung
- **Stored Procedure**: `ws_Vaccine_ThongBaoKhongchan`
- **Handler Name**: `ws_Vaccine_ThongBaoKhongchan`
- **Mục đích**: Thông báo không chặn - kiểm tra thanh toán cho mũi tiêm đã thanh toán một phần

## 🔍 Phân tích Stored Procedure

### Parameters:
- `@SessionID VARCHAR(MAX)`: Session ID của user
- `@ClinicalSessionID UNIQUEIDENTIFIER`: ID của clinical session

### Logic chính:
1. **Kiểm tra điều kiện đặt trước**: Kiểm tra `CN_ClinicalSessions` có `IsDatTruoc = 1`
2. **Kiểm tra thanh toán chưa hoàn tất**: Tìm các invoice detail chưa được liên kết với clinical session
3. **Tính toán số tiền còn lại**: So sánh đơn giá với số tiền còn lại
4. **Trả về thông báo**: Nếu đơn giá > số tiền còn lại thì thông báo cần thanh toán đủ

### Các bảng liên quan:
- `CN_ClinicalSessions`: Thông tin clinical session
- `BIL_InvoiceDetail_TempForHinhThucThanhToan`: Chi tiết hóa đơn tạm
- `BIL_Invoice_TempForHinhThucThanhToan`: Hóa đơn tạm
- `BIL_InvoiceDetail`: Chi tiết hóa đơn
- `BIL_Invoice_PTTT_Link`: Liên kết phương thức thanh toán
- `CN_Data_Log_Vaccine_Payment`: Log thanh toán vaccine
- `CN_Data_Log_Vaccine_Perform`: Log thực hiện vaccine

## 🏗️ Cấu trúc Handler

### Class Parameters:
```csharp
public class Parameters
{
    [Required]
    public string SessionID { get; set; }
    
    [Required]
    public Guid ClinicalSessionID { get; set; }
}
```

### Các Function cần tạo:
1. **AuthenticateUser()**: Xác thực user từ SessionID
2. **ValidateInput()**: Validate input parameters
3. **CheckDatTruocCondition()**: Kiểm tra điều kiện đặt trước
4. **CheckIncompletePayment()**: Kiểm tra thanh toán chưa hoàn tất
5. **GetInvoiceGroupInfo()**: Lấy thông tin invoice group
6. **SaveVaccinePaymentLog()**: Lưu log thanh toán vaccine
7. **CalculateRemainingAmount()**: Tính số tiền còn lại
8. **CheckPaymentSufficiency()**: Kiểm tra đủ tiền thanh toán
9. **CreateResultDataSet()**: Tạo kết quả trả về

## 📁 File cần tạo:
1. **Handler**: `aladdin/WebService.Handlers/QAHosGenericDB/ws_Vaccine_ThongBaoKhongchan.cs`
2. **Test Cases**: `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_Vaccine_ThongBaoKhongchanTests.cs`
3. **YAML Test Cases**: `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_Vaccine_ThongBaoKhongchan.yaml`

## 🧪 Test Cases cần tạo:
1. **Test cơ bản**: SessionID và ClinicalSessionID hợp lệ
2. **Test không đặt trước**: ClinicalSession không có IsDatTruoc = 1
3. **Test thanh toán đủ**: Không có invoice detail chưa hoàn tất
4. **Test thanh toán thiếu**: Có invoice detail chưa hoàn tất và đơn giá > số tiền còn lại
5. **Test thanh toán đủ tiền**: Có invoice detail chưa hoàn tất nhưng đơn giá <= số tiền còn lại
6. **Test lỗi**: SessionID không hợp lệ, ClinicalSessionID không tồn tại

## 🔧 Business Logic:
- Chỉ kiểm tra khi `IsDatTruoc = 1`
- Chỉ kiểm tra các invoice có `IsRefund = 0`
- Chỉ kiểm tra các invoice có liên kết PTTT
- So sánh `DonGia - SoTienGiam` với số tiền còn lại
- Trả về thông báo "Vui lòng đi thanh toán đủ tiền mũi tiêm" nếu thiếu tiền
