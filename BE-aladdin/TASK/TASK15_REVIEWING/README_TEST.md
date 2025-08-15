# Test Cases cho ws_Vaccine_ThongBaoKhongchan

## 📋 Tổng quan
Đã tạo thành công 8 test cases cho handler `ws_Vaccine_ThongBaoKhongchan` để kiểm tra các trường hợp khác nhau của logic thông báo thanh toán vaccine.

## 🧪 Test Cases đã tạo

### 1. Test-01.yaml - Test cơ bản
- **Mô tả**: SessionID và ClinicalSessionID hợp lệ, không có điều kiện đặt trước
- **Input**: 
  - SessionID: "test_session_01"
  - ClinicalSessionID: "11111111-1111-1111-1111-111111111111"
- **Điều kiện**: IsDatTruoc = false
- **Expected**: Trả về Mess = "" (không có thông báo)

### 2. Test-02.yaml - Không có thanh toán chưa hoàn tất
- **Mô tả**: Có điều kiện đặt trước nhưng không có thanh toán chưa hoàn tất
- **Input**: 
  - SessionID: "test_session_02"
  - ClinicalSessionID: "11111111-1111-1111-1111-111111111112"
- **Điều kiện**: IsDatTruoc = true, nhưng BIL_InvoiceDetail có ClinicalSessionId
- **Expected**: Trả về Mess = "" (không có thông báo)

### 3. Test-03.yaml - Đủ tiền thanh toán
- **Mô tả**: Có điều kiện đặt trước và thanh toán chưa hoàn tất, đủ tiền thanh toán
- **Input**: 
  - SessionID: "test_session_03"
  - ClinicalSessionID: "11111111-1111-1111-1111-111111111113"
- **Điều kiện**: 
  - IsDatTruoc = true
  - DonGia = 100,000, SoTienGiam = 0
  - ConLai = 150,000 (đủ tiền)
- **Expected**: Trả về Mess = "" (không có thông báo)

### 4. Test-04.yaml - Thiếu tiền thanh toán
- **Mô tả**: Có điều kiện đặt trước và thanh toán chưa hoàn tất, thiếu tiền thanh toán
- **Input**: 
  - SessionID: "test_session_04"
  - ClinicalSessionID: "11111111-1111-1111-1111-111111111114"
- **Điều kiện**: 
  - IsDatTruoc = true
  - DonGia = 100,000, SoTienGiam = 0
  - ConLai = 50,000 (thiếu tiền)
- **Expected**: Trả về Mess = "Vui lòng đi thanh toán đủ tiền mũi tiêm"

### 5. Test-05.yaml - Không có vaccine payment log
- **Mô tả**: Có điều kiện đặt trước và thanh toán chưa hoàn tất, không có vaccine payment log (cần tạo mới)
- **Input**: 
  - SessionID: "test_session_05"
  - ClinicalSessionID: "11111111-1111-1111-1111-111111111115"
- **Điều kiện**: 
  - IsDatTruoc = true
  - Không có CN_Data_Log_Vaccine_Payment
- **Expected**: Trả về Mess = "Vui lòng đi thanh toán đủ tiền mũi tiêm"

### 6. Test-06.yaml - SessionID không hợp lệ
- **Mô tả**: Test lỗi - SessionID không tồn tại trong database
- **Input**: 
  - SessionID: "invalid_session_06"
  - ClinicalSessionID: "11111111-1111-1111-1111-111111111116"
- **Expected**: Trả về DataSet rỗng (không có kết quả)

### 7. Test-07.yaml - ClinicalSessionID không tồn tại
- **Mô tả**: Test lỗi - ClinicalSessionID không tồn tại trong database
- **Input**: 
  - SessionID: "test_session_07"
  - ClinicalSessionID: "99999999-9999-9999-9999-999999999999"
- **Expected**: Trả về Mess = "" (không có thông báo)

### 8. Test-08.yaml - Có giảm giá
- **Mô tả**: Có điều kiện đặt trước và thanh toán chưa hoàn tất, có giảm giá
- **Input**: 
  - SessionID: "test_session_08"
  - ClinicalSessionID: "11111111-1111-1111-1111-111111111118"
- **Điều kiện**: 
  - IsDatTruoc = true
  - DonGia = 100,000, SoTienGiam = 20,000 (giảm giá)
  - ConLai = 70,000 (đủ tiền sau giảm giá)
- **Expected**: Trả về Mess = "" (không có thông báo)

## 📁 Files đã tạo

### 1. Test Class
- **File**: `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_Vaccine_ThongBaoKhongchan_Test.cs`
- **Mô tả**: Class test chính sử dụng BaseHandlerTest và MemberData để chạy các test cases

### 2. Test Cases Directory
- **Directory**: `aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_Vaccine_ThongBaoKhongchan/`
- **Files**: 8 file YAML (Test-01.yaml đến Test-08.yaml)

## 🔧 Cấu trúc Test Case

Mỗi test case YAML có cấu trúc:
```yaml
# Mô tả test case
initialData:
  - database: Security
    table: Sessions
    rows:
      - SessionID: "test_session"
        UserID: "00000000-0000-0000-0000-000000000001"
  - database: QAHosGenericDB
    table: CN_ClinicalSessions
    rows:
      - ClinicalSessionID: "11111111-1111-1111-1111-111111111111"
        IsDatTruoc: true

input:
  SessionID: "test_session"
  ClinicalSessionID: "11111111-1111-1111-1111-111111111111"

expectedOutput:
  - table: 0
    rows:
      - Mess: "Vui lòng đi thanh toán đủ tiền mũi tiêm"
```

## 🎯 Các trường hợp được test

1. **Happy Path**: Các trường hợp bình thường hoạt động đúng
2. **Edge Cases**: Các trường hợp biên như giảm giá, đủ tiền chính xác
3. **Error Cases**: Các trường hợp lỗi như SessionID không hợp lệ
4. **Business Logic**: Kiểm tra logic nghiệp vụ chính xác

## 🚀 Cách chạy test

```bash
# Chạy tất cả test cases
dotnet test WebService.Handlers.Tests --filter "ws_Vaccine_ThongBaoKhongchan_Test"

# Chạy test cụ thể
dotnet test WebService.Handlers.Tests --filter "ws_Vaccine_ThongBaoKhongchan_Test.Handle_ShouldReturnExpected"
```

## ✅ Kết quả

- **Build Status**: ✅ Thành công (0 errors, 113 warnings)
- **Test Coverage**: 8 test cases bao phủ các trường hợp chính
- **Code Quality**: Tuân thủ cấu trúc test chuẩn của project
- **Documentation**: Đầy đủ mô tả cho từng test case

## 📝 Ghi chú

- Các test cases được thiết kế để kiểm tra logic nghiệp vụ chính xác
- Sử dụng GUID cố định để đảm bảo tính nhất quán
- Các giá trị tiền tệ được sử dụng để dễ hiểu (100,000 VND, 50,000 VND, etc.)
- Test cases bao phủ cả trường hợp thành công và thất bại
