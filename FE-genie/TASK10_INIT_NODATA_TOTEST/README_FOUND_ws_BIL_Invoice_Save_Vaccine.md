# Kết quả tìm kiếm API Usage - Genie Frontend

## Thông tin tìm kiếm
- **API Name**: `ws_BIL_Invoice_Save_Vaccine`
- **Ngày tìm kiếm**: `2024-01-15`
- **Người thực hiện**: `phucnnd`
- **Project**: `Genie Frontend (React/Next.js)`

## Tổng quan kết quả
- **Tổng số file tìm thấy**: `2 files`
- **Tổng số nơi sử dụng**: `5 nơi` (bao gồm cả các nơi gọi gián tiếp)
- **Loại usage**: Direct Usage trong hooks, UI Components
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong

## Phân tích sử dụng

### Mục đích chính
1. ✅ **Vaccine Injection**: Lưu hóa đơn vaccine khi thực hiện tiêm vaccine tại phòng tiêm
2. ✅ **Contract Payment**: Lưu hóa đơn vaccine khi thanh toán hợp đồng vaccine
3. ✅ **Revenue Tracking**: Theo dõi doanh thu vaccine và vật tư
4. ✅ **Inventory Management**: Quản lý xuất kho vaccine và vật tư
5. ✅ **Patient Billing**: Tạo hóa đơn cho bệnh nhân sử dụng vaccine

### Pattern sử dụng
- **Direct API Call Pattern**: API được gọi trực tiếp trong hooks thông qua `executeTransaction`
- **Batch Request Pattern**: Nhiều API calls được gộp thành một batch request
- **Transaction Pattern**: Sử dụng transaction để đảm bảo tính nhất quán dữ liệu
- **Parameter Validation**: Kiểm tra và validate parameters trước khi gọi API
- **Error Handling**: Xử lý lỗi thông qua try-catch và notifyError

### User Journey & Testing Scenarios

#### Scenario 1: Tiêm vaccine tại phòng tiêm
1. **Login** vào hệ thống Genie
2. **Mở menu** "Ngoại trú" → "Phòng tiêm vaccine" → "Chọn bệnh nhân"
3. **Chọn vaccine** cần tiêm từ danh sách vaccine được chỉ định
4. **Nhập thông tin** vị trí tiêm, số lượng, vật tư kèm theo
5. **Bấm nút "Tiêm"** → API `ws_BIL_Invoice_Save_Vaccine` được gọi để lưu hóa đơn
6. **Kết quả**: 
   - Nếu thành công → Hiển thị thông báo "Đã tiêm", chuyển sang vaccine tiếp theo
   - Nếu thất bại → Hiển thị thông báo lỗi, không lưu dữ liệu

#### Scenario 2: Thanh toán hợp đồng vaccine
1. **Login** vào hệ thống Genie
2. **Mở menu** "Thanh toán" → "Thanh toán vaccine"
3. **Chọn quầy** thanh toán
4. **Nhập thông tin** hợp đồng, số tiền, phương thức thanh toán
5. **Bấm nút "Thanh toán"** → API `ws_BIL_Invoice_Save_Vaccine` được gọi để lưu hóa đơn
6. **Kết quả**:
   - Nếu thành công → In biên lai, hoàn tất thanh toán
   - Nếu thất bại → Hiển thị thông báo lỗi, không lưu dữ liệu

#### Scenario 3: Lưu hóa đơn vật tư kèm theo
1. **Login** vào hệ thống Genie
2. **Mở menu** "Ngoại trú" → "Phòng tiêm vaccine" → "Chọn bệnh nhân"
3. **Chọn vaccine** và **vật tư kèm theo** (bơm kim, bông gòn, etc.)
4. **Nhập thông tin** số lượng vật tư
5. **Bấm nút "Tiêm"** → API `ws_BIL_Invoice_Save_Vaccine` được gọi cho cả vaccine và vật tư
6. **Kết quả**:
   - Nếu thành công → Lưu hóa đơn cho cả vaccine và vật tư
   - Nếu thất bại → Rollback toàn bộ transaction

## Thông tin API

### Request
```typescript
{
  InvoiceID: string;                    // Mã hóa đơn (GUID mới)
  FacID: string;                        // Mã cơ sở y tế
  PatientID: string;                    // Mã bệnh nhân
  FacAdmissionID: string;               // Mã tiếp nhận
  PhysicianAdmissionID: string;         // Mã bác sĩ tiếp nhận
  Reason: string;                       // Lý do lưu hóa đơn
  ApprovedOutID: string;                // Mã phiếu xuất kho
  IPUser: string;                       // IP của user
  MacAddressUser: string;               // MAC address của user
  HopDongID: string;                    // Mã hợp đồng (nếu có)
  IsTiem: boolean;                      // Có phải tiêm vaccine không
  // Các field khác tùy theo context sử dụng
  DoiTuongID?: number;                  // Mã đối tượng tính tiền
  CounterID?: string;                   // Mã quầy thanh toán
  InvoiceNo?: string;                   // Số hóa đơn
  Total?: number;                       // Tổng tiền
  RealTotal?: number;                   // Số tiền thực thu
  IsPaid?: string;                      // Trạng thái thanh toán
  PatientType?: number;                 // Loại bệnh nhân
  Note?: string;                        // Ghi chú
  IsTamUng?: number;                    // Có phải tạm ứng không
  SoTK?: string;                        // Số tài khoản
  LiDoMienGiam?: string;                // Lý do miễn giảm
  HinhThucThanhToan?: string;           // Hình thức thanh toán
  TypeID_LoaiThu?: number;              // Loại thu
}
```

### Response
```typescript
// API này là backend procedure, response được xử lý thông qua executeTransaction
// Không có response structure cụ thể trong frontend
```

### cURL Example
```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_BIL_Invoice_Save_Vaccine",
      "parameters": {
        "InvoiceID": "GUID_NEW_SEQUENTIAL",
        "FacID": "FAC001",
        "PatientID": "PAT123456",
        "FacAdmissionID": "ADM789",
        "PhysicianAdmissionID": "DOC456",
        "Reason": "Lưu doanh thu vaccine lúc bấm tiêm tại phòng tiêm vaccine",
        "ApprovedOutID": "OUT123",
        "IPUser": "192.168.1.100",
        "MacAddressUser": "00:11:22:33:44:55",
        "HopDongID": "CONTRACT001",
        "IsTiem": true
      }
    }
  ]'
```

## Chi tiết kết quả

### 1. Direct Usage trong Vaccine Injection Hook
- **File**: `app/(main)/ngoai-tru/(nurse)/phong-tiem-vaccine/[patientId]/_hooks/use-tiem.ts`
- **Line**: `278, 327, 386`
- **Function**: `tiem` function
- **Context**: Lưu hóa đơn vaccine khi thực hiện tiêm vaccine
- **Trigger**: Nút "Tiêm" trong form tiêm vaccine
- **Parameters**: 
  - Line 278: Lưu hóa đơn vaccine chính
  - Line 327: Lưu hóa đơn vật tư kèm theo (nếu có)
  - Line 386: Lưu hóa đơn vật tư kèm theo (trường hợp khác)
- **Code snippet**: 
```typescript
requests.push({
  category: "QAHosGenericDB",
  command: "ws_BIL_Invoice_Save_Vaccine",
  parameters: {
    InvoiceID: invoiceIdVaccine,
    FacID: facId,
    PatientID: patientIdParam,
    FacAdmissionID: prescribedVaccineFacAdmissionId,
    PhysicianAdmissionID: prescribedVaccinePhysicianAdmissionId,
    Reason: "Lưu doanh thu vaccine lúc bấm tiêm tại phòng tiêm vaccine",
    ApprovedOutID: phieuXuatIdVaccine,
    IPUser: localIpAddress,
    MacAddressUser: localMacAddress,
    HopDongID: prescribedVaccineHopDongId,
    IsTiem: true,
  },
});
```

### 2. Direct Usage trong Contract Payment Hook
- **File**: `app/(main)/thanh-toan/_hooks/use-contract-payment.ts`
- **Line**: `185, 503`
- **Function**: `processDataForPrint` và `contractPayment`
- **Context**: Lưu hóa đơn vaccine khi thanh toán hợp đồng
- **Trigger**: Nút "Thanh toán" trong form thanh toán hợp đồng
- **Parameters**:
  - Line 185: Lưu hóa đơn tạm ứng cho chương trình khuyến mãi VNPAY
  - Line 503: Lưu hóa đơn tạm ứng cho hợp đồng vaccine
- **Code snippet**:
```typescript
saveRequests.push({
  category: "QAHosGenericDB",
  command: "ws_BIL_Invoice_Save_Vaccine",
  parameters: {
    InvoiceID: invoiceGroupId,
    PatientID: patient?.patientID,
    FacID: faculty.facId,
    FacAdmissionID: patient?.facAdmissionID,
    HopDongID: invoiceId,
    DoiTuongID: 0,
    CounterID: counter?.counterID,
    InvoiceNo: "",
    Total: amount,
    RealTotal: amount,
    IsPaid: "1",
    PatientType: 0,
    Reason: "Thu tạm ứng",
    Note: "Bill phát sinh Chương trình khuyến mãi VNPAY",
    IsTamUng: 1,
    SoTK: "",
    LiDoMienGiam: "",
    HinhThucThanhToan: "Mã khuyến mãi",
    TypeID_LoaiThu: 2,
    IPUser: utils.getLocalIPv4(),
    MacAddressUser: utils.getMacAddresses(),
  },
});
```

### 3. UI Components và Buttons liên quan
- **Nút "Tiêm"**: Trong form tiêm vaccine tại phòng tiêm vaccine
  - File: `app/(main)/ngoai-tru/(nurse)/phong-tiem-vaccine/[patientId]/_components/vaccination/vaccination.tsx`
  - Line: 430
  - Function: `onSubmitTiem` → `tiem` → API call
- **Nút "Thanh toán"**: Trong form thanh toán hợp đồng vaccine
  - File: `app/(main)/thanh-toan/_components/collect/payment-contract/payment-contract.tsx`
  - Line: 153
  - Function: `handleTamUng` → `contractPayment` → API call

### 4. Function Call Chains
- **Vaccine Injection Flow**:
  ```
  onSubmitTiem (UI Button) → tiem (hook) → executeTransaction → ws_BIL_Invoice_Save_Vaccine
  ```
- **Contract Payment Flow**:
  ```
  handleTamUng (UI Button) → contractPayment (hook) → processDataForPrint → ws_BIL_Invoice_Save_Vaccine
  ```

### 5. Related APIs
- **ws_BIL_InvoiceDetail_Save_Vaccine**: Lưu chi tiết hóa đơn vaccine
- **ws_BIL_InvoiceDetail_UpdateApprovedOutID**: Cập nhật mã phiếu xuất kho
- **ws_CN_Data_Log_Vaccine_Perform_UpdateCompleted_Save**: Lưu log hoàn thành tiêm vaccine
- **ws_Vaccine_KiemTra_CapNhat_NgayHenTiem**: Cập nhật ngày hẹn tiêm
- **ws_Vaccine_DanhSachChoTiem_DaTiem_Save**: Lưu danh sách đã tiêm

## Kết luận
API `ws_BIL_Invoice_Save_Vaccine` được sử dụng rộng rãi trong hệ thống Genie với **5 nơi sử dụng chính**:

1. **Vaccine Injection** (3 nơi) - Lưu hóa đơn vaccine và vật tư khi tiêm
2. **Contract Payment** (2 nơi) - Lưu hóa đơn khi thanh toán hợp đồng vaccine
3. **UI Components** (2 nút) - Nút "Tiêm" và nút "Thanh toán"
4. **Function Chains** (2 flows) - Vaccine injection flow và contract payment flow

API này đóng vai trò quan trọng trong việc quản lý doanh thu vaccine, theo dõi xuất kho, và tạo hóa đơn cho bệnh nhân sử dụng vaccine.

## Ghi chú
- API này là backend procedure được gọi trực tiếp thông qua `executeTransaction`
- Không có service wrapper function với prefix `fetch_`
- Sử dụng transaction pattern để đảm bảo tính nhất quán dữ liệu
- Có 2 context sử dụng chính: tiêm vaccine và thanh toán hợp đồng
- Parameters khác nhau tùy theo context sử dụng
- Error handling được implement thông qua try-catch và notifyError
- UI components trigger API calls thông qua form submissions

---
*Tài liệu được tạo tự động từ kết quả tìm kiếm API Usage*
