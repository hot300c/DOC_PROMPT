# Kết quả tìm kiếm API Usage - Genie Frontend

## Thông tin tìm kiếm
- **API Name**: `ws_BIL_InvoiceDetail_Save_Vaccine`
- **Ngày tìm kiếm**: `2025-08-21`
- **Project**: `Genie Frontend (React/Next.js)`

## Tổng quan kết quả
- **Tổng số file tìm thấy**: `2` files (mã nguồn FE gọi trực tiếp API)
- **Tổng số nơi sử dụng**: `6` nơi (các request trong 2 hooks chính)
- **Loại usage**: Direct Usage (qua executeTransaction), Indirect via flow hooks, UI-triggered flows
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong

## Phân tích sử dụng

### Mục đích chính
1. ✅ Ghi chi tiết hóa đơn (Invoice Detail) khi thu tạm ứng/hợp đồng trong màn hình thanh toán
2. ✅ Ghi chi tiết hóa đơn khi thao tác “Tiêm” tại phòng tiêm vaccine (vaccine và vật tư)

### Pattern sử dụng
- API được gọi trực tiếp trong các hook nghiệp vụ (không có wrapper `fetch_...` riêng), thông qua `SystemService.executeTransaction`/`executeTransaction`
- Tham số truyền theo SP backend, bao gồm các ID phát sinh từ `ws_Guid_NewSequential_Get`
- Được gọi theo chuỗi cùng các SP liên quan: `ws_BIL_Invoice_Save_Vaccine`, `ws_BIL_Invoice_Voucher_Save`, `ws_BIL_Invoice_Update_RealTotal_FromVNPAY`, `ws_BIL_AdvancedPayment_Save`, v.v.

## Thông tin API (Backend)

### Stored Procedure
- File: `qas-db/QAHosGenericDB/Procedures/ws_BIL_InvoiceDetail_Save_Vaccine.sql`
- Chữ ký tham số chính (rút gọn):
  - `@SessionID`, `@FacID`, `@InvoiceDetailID`, `@InvoiceID`, `@PatientID`, `@FacAdmissionID`, `@PhysicianAdmissionID`, `@ClinicalSessionID`, `@AdvancedPaymentID`, `@ApprovedOutID`, `@DoiTuongTinhTienID`, `@MaChung_Vaccine`, `@NoiDung`, `@ServiceID`, `@ProductID`, `@UnitID`, `@Batch`, `@ExpDate`, `@Qty`, `@DonGia`, `@PatientPay`, `@MedicarePay`, `@NguonKhac`, `@SoTienGiam`, `@IsComplete`, `@IsRefund`, `@IsNgoaiGio`, `@IsGoi`, `@IsTiem`.

### cURL Example (FE DataAccess)
```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_BIL_InvoiceDetail_Save_Vaccine",
      "parameters": {
        "FacID": "8.1",
        "InvoiceDetailID": "GUID-DETAIL",
        "InvoiceID": "GUID-INVOICE",
        "PatientID": "GUID-PATIENT",
        "FacAdmissionID": "GUID-FAC-ADMISSION",
        "ClinicalSessionID": "GUID-CLINICAL",
        "NoiDung": "Thu tạm ứng",
        "Qty": 1,
        "UnitID": 42,
        "DonGia": 100000,
        "PatientPay": 100000,
        "IsComplete": 1,
        "IsRefund": 0,
        "IsTiem": 1
      }
    }
  ]'
```

## Chi tiết kết quả

### 1) Direct Usage — Thanh toán hợp đồng (Contract Payment)
- File: `genie/app/(main)/thanh-toan/_hooks/use-contract-payment.ts`
- Mục đích: Lưu tạm ứng hợp đồng; phát sinh `Invoice` và `InvoiceDetail` tương ứng.
- Call chính đến `ws_BIL_InvoiceDetail_Save_Vaccine` (nhiều vị trí trong hook):
  - Thêm `InvoiceDetail` với các tham số: `FacID`, `InvoiceDetailID` (GUID mới), `InvoiceID` (nhóm bill), `PatientID`, `FacAdmissionID`, `AdvancedPaymentID` (GUID mới), `DoiTuongTinhTienID: 0`, `NoiDung: "Thu tạm ứng"`, `Qty: 1`, `UnitID: 42`, `DonGia`, `PatientPay`, `IsComplete: 1`, `IsRefund: 0`.
- Ngữ cảnh: Đi kèm các lệnh `ws_BIL_Invoice_Save_Vaccine`, `ws_BIL_Invoice_Voucher_Save`, `ws_BIL_Invoice_Update_RealTotal_FromVNPAY` ... trong một transaction.

### 2) Direct Usage — Phòng tiêm vaccine (Nurse)
- File: `genie/app/(main)/ngoai-tru/(nurse)/phong-tiem-vaccine/[patientId]/_hooks/use-tiem.ts`
- Mục đích: Khi bấm “Tiêm”, tạo `Invoice` và `InvoiceDetail` cho vaccine và vật tư lẻ.
- Các vị trí gọi tiêu biểu:
  - Vaccine: Ghi `InvoiceDetail` với `IsTiem: true`, `ClinicalSessionID`, `ProductID`, `Batch`, `ExpDate`, `MaChung_Vaccine`, `Qty` (số mũi), `DonGia` (đơn giá vaccine), `ApprovedOutID` (phiếu xuất), `NoiDung` (tên vaccine chuẩn hoá, ví dụ "Qdenga").
  - Vật tư: Ghi `InvoiceDetail` với `DoiTuongTinhTienID: 99`, tương tự vaccine nhưng thuộc hóa đơn vật tư.
- Ngữ cảnh: Chạy cùng chuỗi SP như `ws_BIL_Invoice_Save_Vaccine`, `ws_BIL_InvoiceDetail_UpdateApprovedOutID`, `ws_CN_Data_Log_Vaccine_Perform_UpdateCompleted_Save`, `ws_Vaccine_KiemTra_CapNhat_NgayHenTiem`, v.v.

### 3) Tài liệu nội bộ tham chiếu
- File: `genie/app/(main)/ngoai-tru/(nurse)/phong-tiem-vaccine/[patientId]/README.md`
- Ghi nhận API được gọi trong flow tiêm (liệt kê rõ `ws_BIL_InvoiceDetail_Save_Vaccine`).

## User Journey & Testing Scenarios

### Flow 1: Thanh toán hợp đồng với tạm ứng
- Đường dẫn màn hình: Menu → Thanh toán → Hợp đồng
- Tiền điều kiện: `PatientID`, `HopDongID`, `FacID`, cấu hình in/thu; user có quyền thanh toán
- Bước thao tác:
  1) Chọn hợp đồng cần thu
  2) Nhập số tiền cần thu và hình thức thanh toán
  3) Bấm lưu/thu
  4) Hệ thống thực hiện transaction, trong đó gọi `ws_BIL_InvoiceDetail_Save_Vaccine`
- Trigger API: Trong `use-contract-payment.ts` khi xử lý `saveRequests`
- Kỳ vọng UI: Thông báo thành công; hoá đơn tạm ứng được tạo; có thể in biên lai
- Nhánh quyết định: Nếu thanh toán qua VNPAY, bổ sung map voucher và cập nhật RealTotal
- Kết quả dữ liệu: Thêm dòng `BIL_InvoiceDetail` với số tiền và nội dung “Thu tạm ứng”
- Dữ liệu mẫu: `DonGia = PatientPay = 200000`, `Qty=1`, `UnitID=42`
- Mapping UI → Code: `app/(main)/thanh-toan/_hooks/use-contract-payment.ts` → `saveRequests`

### Flow 2: Tiêm vaccine tại phòng tiêm
- Đường dẫn màn hình: Menu → Ngoại trú → (Nurse) Phòng tiêm vaccine → [patientId]
- Tiền điều kiện: `PatientID`, `ClinicalSessionID`, `FacID`, vaccine/vật tư đã chuẩn bị; user có quyền tiêm
- Bước thao tác:
  1) Chọn vaccine/vật tư thực tế và số lượng
  2) Bấm nút “Tiêm”
  3) Hệ thống tạo hoá đơn và chi tiết tương ứng (vaccine/vật tư)
  4) Gọi `ws_BIL_InvoiceDetail_Save_Vaccine` cho từng mục
- Trigger API: Trong `use-tiem.ts` khi build `requests` gửi vào `executeTransaction`
- Kỳ vọng UI: Thông báo “Đã tiêm”; cập nhật theo dõi sau tiêm; có thể in chứng từ
- Nhánh quyết định: Nếu không thuộc hợp đồng → chỉ cập nhật ApprovedOutID cho vaccine; nếu có vật tư → tạo hoá đơn riêng vật tư
- Kết quả dữ liệu: Thêm dòng `BIL_InvoiceDetail` cho từng vaccine/vật tư; trường `IsTiem=true`
- Dữ liệu mẫu: `Qty=1`, `DonGia=prescribedVaccineDonGia`, `ProductID`, `Batch`, `ExpDate`
- Mapping UI → Code: `app/(main)/ngoai-tru/(nurse)/phong-tiem-vaccine/[patientId]/_hooks/use-tiem.ts` → `requests.push({...})`

### Negative cases (đề xuất kiểm thử)
1. Thiếu `PatientID` hoặc `InvoiceID` → Trả lỗi/không lưu `InvoiceDetail`
2. `DonGia` hoặc `PatientPay` âm/không hợp lệ → Từ chối lưu
3. `ExpDate` không đúng định dạng hoặc nhỏ hơn ngày hợp lệ → Từ chối lưu

## Kết luận
`ws_BIL_InvoiceDetail_Save_Vaccine` là API quan trọng trong 2 luồng chính:
- Thanh toán hợp đồng (tạm ứng, voucher, cập nhật real total)
- Thao tác tiêm tại phòng tiêm (vaccine và vật tư)

Việc gọi API luôn nằm trong transaction cùng các SP liên quan, đảm bảo tính toàn vẹn dữ liệu khi ghi hoá đơn và các chi tiết kèm theo.


