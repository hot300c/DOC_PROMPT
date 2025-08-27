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

## ⚠️ **THÔNG TIN QUAN TRỌNG - CẬP NHẬT MỚI**

**API `ws_BIL_Invoice_Save_Vaccine` KHÔNG được gọi riêng lẻ mà được gọi trong cùng một `executeTransaction` với nhiều API khác.**

### **Thực tế khi bấm nút "Tiêm":**
1. **Không gọi riêng** `ws_BIL_Invoice_Save_Vaccine`
2. **Gọi `executeTransaction`** với **12+ API** trong cùng một request
3. **`ws_BIL_Invoice_Save_Vaccine` chỉ là 1 trong số các API** được gọi

### **Danh sách đầy đủ các API được gọi:**
```typescript
// 1. API chính - Hoàn thành vaccine
ws_Vaccine_Completed_V2

// 2. API lưu vaccine sử dụng thực tế  
ws_Vaccine_VaccineSuDungThucTe_Save

// 3. API lưu vị trí tiêm
ws_CN_ClinicalSessions_BodyPart_Save

// 4. API xuất kho vaccine
ws_XuatVaccine

// 5. API xuất kho vật tư (nếu có)
ws_XuatVaccine (với IsVaccine: false)

// 6. API lưu hóa đơn vaccine (CHỈ KHI có hợp đồng)
ws_BIL_Invoice_Save_Vaccine

// 7. API lưu chi tiết hóa đơn vaccine
ws_BIL_InvoiceDetail_Save_Vaccine

// 8. API lưu hóa đơn vật tư (nếu có)
ws_BIL_Invoice_Save_Vaccine (với Reason: "đây là vật tư")

// 9. API lưu chi tiết hóa đơn vật tư
ws_BIL_InvoiceDetail_Save_Vaccine

// 10. API cập nhật ngày hẹn tiêm
ws_Vaccine_KiemTra_CapNhat_NgayHenTiem

// 11. API lưu danh sách đã tiêm
ws_Vaccine_DanhSachChoTiem_DaTiem_Save

// 12. API log vaccine perform
ws_CN_Data_Log_Vaccine_Perform_UpdateCompleted_Save
```

## Phân tích sử dụng

### Mục đích chính
1. ✅ **Vaccine Injection**: Lưu hóa đơn vaccine khi thực hiện tiêm vaccine tại phòng tiêm
2. ✅ **Contract Payment**: Lưu hóa đơn vaccine khi thanh toán hợp đồng vaccine
3. ✅ **Revenue Tracking**: Theo dõi doanh thu vaccine và vật tư
4. ✅ **Inventory Management**: Quản lý xuất kho vaccine và vật tư
5. ✅ **Patient Billing**: Tạo hóa đơn cho bệnh nhân sử dụng vaccine

### Pattern sử dụng
- **Batch Transaction Pattern**: API được gọi trong cùng một `executeTransaction` với nhiều API khác
- **Conditional Execution Pattern**: Chỉ được gọi khi có hợp đồng và không phải vaccine ngoài danh mục
- **Dual Purpose Pattern**: Được gọi 2 lần - một cho vaccine, một cho vật tư (nếu có)
- **Parameter Validation**: Kiểm tra và validate parameters trước khi gọi API
- **Error Handling**: Xử lý lỗi thông qua try-catch và notifyError

### User Journey & Testing Scenarios

#### Scenario 1: Tiêm vaccine tại phòng tiêm (CÓ HỢP ĐỒNG)
1. **Login** vào hệ thống Genie
2. **Mở menu** "Ngoại trú" → "Phòng tiêm vaccine" → "Chọn bệnh nhân"
3. **Chọn vaccine** cần tiêm từ danh sách vaccine được chỉ định (có hợp đồng)
4. **Nhập thông tin** vị trí tiêm, số lượng, vật tư kèm theo
5. **Bấm nút "Tiêm"** → Hệ thống gọi `executeTransaction` với **12+ API** bao gồm:
   - `ws_Vaccine_Completed_V2` (API chính)
   - `ws_BIL_Invoice_Save_Vaccine` (lưu hóa đơn vaccine)
   - `ws_BIL_Invoice_Save_Vaccine` (lưu hóa đơn vật tư nếu có)
   - Và 9+ API khác
6. **Kết quả**: 
   - Nếu thành công → Hiển thị thông báo "Đã tiêm", chuyển sang vaccine tiếp theo
   - Nếu thất bại → Hiển thị thông báo lỗi, không lưu dữ liệu

#### Scenario 2: Tiêm vaccine tại phòng tiêm (KHÔNG CÓ HỢP ĐỒNG)
1. **Login** vào hệ thống Genie
2. **Mở menu** "Ngoại trú" → "Phòng tiêm vaccine" → "Chọn bệnh nhân"
3. **Chọn vaccine** cần tiêm từ danh sách vaccine được chỉ định (không có hợp đồng)
4. **Nhập thông tin** vị trí tiêm, số lượng, vật tư kèm theo
5. **Bấm nút "Tiêm"** → Hệ thống gọi `executeTransaction` với **9+ API** (KHÔNG BAO GỒM `ws_BIL_Invoice_Save_Vaccine`):
   - `ws_Vaccine_Completed_V2` (API chính)
   - `ws_XuatVaccine` (xuất kho)
   - Và 7+ API khác
6. **Kết quả**:
   - Nếu thành công → Hiển thị thông báo "Đã tiêm", chuyển sang vaccine tiếp theo
   - Nếu thất bại → Hiển thị thông báo lỗi, không lưu dữ liệu

#### Scenario 3: Thanh toán hợp đồng vaccine
1. **Login** vào hệ thống Genie
2. **Mở menu** "Thanh toán" → "Thanh toán vaccine"
3. **Chọn quầy** thanh toán
4. **Nhập thông tin** hợp đồng, số tiền, phương thức thanh toán
5. **Bấm nút "Thanh toán"** → API `ws_BIL_Invoice_Save_Vaccine` được gọi để lưu hóa đơn
6. **Kết quả**:
   - Nếu thành công → In biên lai, hoàn tất thanh toán
   - Nếu thất bại → Hiển thị thông báo lỗi, không lưu dữ liệu

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
// Response sẽ chứa kết quả của TẤT CẢ các API trong batch request
```

### cURL Example
```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_Vaccine_Completed_V2",
      "parameters": {
        "FacID": "FAC001",
        "ClinicalSessionID": "CLINICAL123",
        "ProductID": "PROD456",
        "PatientID": "PAT123456",
        "IPUser": "192.168.1.100",
        "MacAddressUser": "00:11:22:33:44:55"
      }
    },
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
    // ... và 10+ API khác
  ]'
```

## Chi tiết kết quả

### 1. Direct Usage trong Vaccine Injection Hook
- **File**: `app/(main)/ngoai-tru/(nurse)/phong-tiem-vaccine/[patientId]/_hooks/use-tiem.ts`
- **Line**: `278, 327, 386`
- **Function**: `tiem` function
- **Context**: Lưu hóa đơn vaccine khi thực hiện tiêm vaccine
- **Trigger**: Nút "Tiêm" trong form tiêm vaccine
- **Điều kiện**: Chỉ được gọi khi có hợp đồng và không phải vaccine ngoài danh mục
- **Parameters**: 
  - Line 278: Lưu hóa đơn vaccine chính
  - Line 327: Lưu hóa đơn vật tư kèm theo (nếu có)
  - Line 386: Lưu hóa đơn vật tư kèm theo (trường hợp khác)
- **Code snippet**: 
```typescript
// CHỈ KHI có hợp đồng và không phải ngoài danh mục
if (
  selectedPrescribedVaccine.hopDongID !== DEFAULT_GUID &&
  !selectedPrescribedVaccine.isNgoaiDanhMuc
) {
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
      HopDongID: prescribedPrescribedVaccineHopDongId,
      IsTiem: true,
    },
  });
}
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
  - Function: `onSubmitTiem` → `tiem` → `executeTransaction` với 12+ API
- **Nút "Thanh toán"**: Trong form thanh toán hợp đồng vaccine
  - File: `app/(main)/thanh-toan/_components/collect/payment-contract/payment-contract.tsx`
  - Line: 153
  - Function: `handleTamUng` → `contractPayment` → API call

### 4. Function Call Chains
- **Vaccine Injection Flow**:
  ```
  onSubmitTiem (UI Button) → tiem (hook) → executeTransaction → 12+ API bao gồm ws_BIL_Invoice_Save_Vaccine
  ```
- **Contract Payment Flow**:
  ```
  handleTamUng (UI Button) → contractPayment (hook) → processDataForPrint → ws_BIL_Invoice_Save_Vaccine
  ```

### 5. Related APIs
- **ws_Vaccine_Completed_V2**: API chính hoàn thành vaccine
- **ws_Vaccine_VaccineSuDungThucTe_Save**: Lưu vaccine sử dụng thực tế
- **ws_CN_ClinicalSessions_BodyPart_Save**: Lưu vị trí tiêm
- **ws_XuatVaccine**: Xuất kho vaccine và vật tư
- **ws_BIL_InvoiceDetail_Save_Vaccine**: Lưu chi tiết hóa đơn vaccine
- **ws_BIL_InvoiceDetail_UpdateApprovedOutID**: Cập nhật mã phiếu xuất kho
- **ws_CN_Data_Log_Vaccine_Perform_UpdateCompleted_Save**: Lưu log hoàn thành tiêm vaccine
- **ws_Vaccine_KiemTra_CapNhat_NgayHenTiem**: Cập nhật ngày hẹn tiêm
- **ws_Vaccine_DanhSachChoTiem_DaTiem_Save**: Lưu danh sách đã tiêm

## ⚠️ **ĐIỀU KIỆN QUAN TRỌNG ĐỂ API HOẠT ĐỘNG**

### **Điều kiện để `ws_BIL_Invoice_Save_Vaccine` được gọi khi tiêm vaccine:**
```typescript
if (
  selectedPrescribedVaccine.hopDongID !== DEFAULT_GUID &&  // ✅ Có hợp đồng
  !selectedPrescribedVaccine.isNgoaiDanhMuc               // ✅ Không phải ngoài danh mục
) {
  // API ws_BIL_Invoice_Save_Vaccine sẽ được gọi
}
```

### **Điều kiện để nút "Tiêm" hoạt động:**
```typescript
<Button disabled={isCompletedVaccine || isPendingTiem}>
  Tiêm
</Button>
```
- `isCompletedVaccine = !!selectedPrescribedVaccine?.completedOn;`
- Nếu `completedOn` có giá trị → nút bị disabled

### **Checklist để API hoạt động:**
- [ ] **Vaccine có hợp đồng**: `hopDongID !== DEFAULT_GUID`
- [ ] **Vaccine trong danh mục**: `isNgoaiDanhMuc = false`
- [ ] **Vaccine chưa hoàn thành**: `completedOn = null/undefined`
- [ ] **Có vaccine được chọn**: `vaccinesThucTe.length > 0`
- [ ] **Có vaccine thực tế**: `vaccinesThucTe.some(v => v.isVaccine)`
- [ ] **Đã nhập vị trí tiêm**: `viTriTiemId` có giá trị
- [ ] **Đã nhập số lượng**: `soLuong` có giá trị
- [ ] **Nút "Tiêm" không bị disabled**: `isCompletedVaccine = false`

## Kết luận
API `ws_BIL_Invoice_Save_Vaccine` được sử dụng rộng rãi trong hệ thống Genie với **5 nơi sử dụng chính**:

1. **Vaccine Injection** (3 nơi) - Lưu hóa đơn vaccine và vật tư khi tiêm (CHỈ KHI có hợp đồng)
2. **Contract Payment** (2 nơi) - Lưu hóa đơn khi thanh toán hợp đồng vaccine
3. **UI Components** (2 nút) - Nút "Tiêm" và nút "Thanh toán"
4. **Function Chains** (2 flows) - Vaccine injection flow và contract payment flow

**⚠️ QUAN TRỌNG**: API này **KHÔNG được gọi riêng lẻ** mà được gọi trong cùng một `executeTransaction` với **12+ API khác** khi bấm nút "Tiêm".

## Ghi chú
- API này là backend procedure được gọi trực tiếp thông qua `executeTransaction`
- Không có service wrapper function với prefix `fetch_`
- Sử dụng transaction pattern để đảm bảo tính nhất quán dữ liệu
- Có 2 context sử dụng chính: tiêm vaccine và thanh toán hợp đồng
- **Điều kiện quan trọng**: Chỉ được gọi khi có hợp đồng và không phải vaccine ngoài danh mục
- Parameters khác nhau tùy theo context sử dụng
- Error handling được implement thông qua try-catch và notifyError
- UI components trigger API calls thông qua form submissions
- **Cập nhật mới**: API được gọi trong batch request với 12+ API khác, không phải gọi riêng lẻ

---
*Tài liệu được cập nhật để phản ánh chính xác thực tế: API ws_BIL_Invoice_Save_Vaccine được gọi trong cùng một executeTransaction với nhiều API khác*
