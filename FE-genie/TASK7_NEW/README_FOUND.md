## API: ws_INV_ProductTemp_Proccessing_Vaccine

### Kết quả tìm kiếm (Genie Frontend)

- **Ghi chú quan trọng**: Không tìm thấy usage trực tiếp của `ws_INV_ProductTemp_Proccessing_Vaccine` (không có hậu tố). Frontend đang sử dụng biến thể mới: **`ws_INV_ProductTemp_Proccessing_Vaccine_V2`**.

### Tổng quan
- **Tổng số file tìm thấy**: 3
- **Tổng số nơi sử dụng**: 3 (đều là gọi trực tiếp trong mảng `SequenceRequest` gửi qua `SystemService.executeTransaction`)
- **Loại usage**: Direct usage (không qua service wrapper), trong các hook xử lý thanh toán
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong
- **Ngày tìm kiếm**: 2025-08-18

### Chi tiết usage theo file

1) Direct usage (Pre-order Payment)
   - File: `genie/app/(main)/thanh-toan/_hooks/use-pre-order-payment.ts`
   - Vị trí: khoảng dòng 629–639
   - Ngữ cảnh: Trong hàm `generateExecuteRequests`, khi tạo `saveRequests` cho từng dịch vụ vaccine, push câu lệnh:
   ```629:639:genie/app/(main)/thanh-toan/_hooks/use-pre-order-payment.ts
            {
              category: "QAHosGenericDB",
              command: "ws_INV_ProductTemp_Proccessing_Vaccine_V2",
              parameters: {
                FacID: faculty.facId,
                RoomID: originVaccine.roomID,
                Qty: qty,
                MaChung: originVaccine.maChung,
                PatientID: patient?.patientID,
                ClinicalSessionID: originVaccine.clinicalSessionID,
              },
            },
   ```

2) Direct usage (Retail - nhiều phương thức thanh toán)
   - File: `genie/app/(main)/thanh-toan/_hooks/use-save-data-mutiple-payment-method-retail.ts`
   - Vị trí: khoảng dòng 181–193
   - Ngữ cảnh: Trong `handleLuuBienLaiPhuongThucThanhToanMuiLe`, push câu lệnh V2 vào `query` khi là lần thanh toán cuối cùng và đã chọn phòng tiêm:
   ```181:193:genie/app/(main)/thanh-toan/_hooks/use-save-data-mutiple-payment-method-retail.ts
               {
                 category: QAHOSGENERICDB,
                 command: "ws_INV_ProductTemp_Proccessing_Vaccine_V2",
                 parameters: {
                   FacID: faculty.facId,
                   RoomID: ktChiDinhChoBienLaiTTDPT
                     ? selectedDepartment?.roomID || 0
                     : 0,
                   Qty: item.qty || 0,
                   MaChung: item.maChung,
                   PatientID: paymentStore?.patient.patientID,
                   ClinicalSessionID: item.clinicalSessionID,
                 },
               },
   ```

3) Direct usage (Pre-order - nhiều phương thức thanh toán)
   - File: `genie/app/(main)/thanh-toan/_hooks/use-save-data-mutiple-payment-method-pre-order.ts`
   - Vị trí: khoảng dòng 178–186
   - Ngữ cảnh: Trong `handleLuuBienLaiPhuongThucThanhToanDatTruoc`, push câu lệnh V2 vào `query`:
   ```178:186:genie/app/(main)/thanh-toan/_hooks/use-save-data-mutiple-payment-method-pre-order.ts
           query.push({
             category: QAHOSGENERICDB,
             command: "ws_INV_ProductTemp_Proccessing_Vaccine_V2",
             parameters: {
               FacID: faculty.facId,
               RoomID: selectedDepartment?.roomID || 0,
               Qty: item.qty || 0,
               MaChung: item.maChung,
               PatientID: paymentStore?.patient.patientID,
               ClinicalSessionID: item.clinicalSessionID,
             },
           });
   ```

### Mục đích chính khi gọi API (suy ra từ ngữ cảnh)
- **Trừ/Cộng kho tạm vaccine** tương ứng với các chi định vaccine đã thanh toán/đặt trước
- Thực hiện sau khi đã lưu chi tiết hóa đơn, cập nhật phòng/phác đồ, và/hoặc trước in biên lai tùy flow

### Pattern sử dụng
- Gọi trực tiếp qua `SystemService.executeTransaction` bằng cách push phần tử vào mảng `SequenceRequest`
- Không có service wrapper riêng trong `app/lib/services/*` cho API này (FE dùng trực tiếp tên command `ws_INV_ProductTemp_Proccessing_Vaccine_V2`)

### User Journey & Testing Scenarios

#### Flow Thanh toán đặt trước (Pre-order Payment)
- Đường dẫn màn hình: Menu → Thanh toán
- Tiền điều kiện: có danh sách `clinicalSessions` vaccine, đã chọn bệnh nhân (`PatientID`), `FacID` hợp lệ
- Bước thao tác:
  1) Chọn các dịch vụ vaccine cần thanh toán
  2) Thực hiện in biên lai tạm/preview → xác nhận in
  3) Hệ thống lần lượt lưu chi tiết hóa đơn, cập nhật phác đồ/phòng
- Trigger API: `ws_INV_ProductTemp_Proccessing_Vaccine_V2` (tại `use-pre-order-payment.ts → generateExecuteRequests`)
- Kỳ vọng UI: In biên lai thành công; nếu lỗi hiển thị dialog cảnh báo
- Nhánh quyết định: Tùy theo xác nhận in biên lai (modal) mà tiếp tục lưu các request còn lại
- Kết quả dữ liệu: Kho tạm vaccine được cập nhật theo `Qty`, `MaChung`, `RoomID`
- Dữ liệu mẫu: `FacID`, `PatientID`, `ClinicalSessionID`, `RoomID`, `Qty`, `MaChung`
- Mapping UI → Code: `genie/app/(main)/thanh-toan/_hooks/use-pre-order-payment.ts` → `generateExecuteRequests`

#### Flow Thanh toán lẻ nhiều phương thức (Retail - Multi Methods)
- Đường dẫn màn hình: Menu → Thanh toán
- Tiền điều kiện: chọn phòng tiêm cho lần thanh toán cuối cùng; có `PatientID`, `FacID`
- Bước thao tác:
  1) Chọn nhiều phương thức thanh toán cho hóa đơn lẻ
  2) Với lần thanh toán cuối cùng, bắt buộc chọn phòng tiêm
  3) Lưu biên lai cho từng phương thức
- Trigger API: `ws_INV_ProductTemp_Proccessing_Vaccine_V2` (tại `use-save-data-mutiple-payment-method-retail.ts → handleLuuBienLaiPhuongThucThanhToanMuiLe`)
- Kỳ vọng UI: Lưu thành công và thông báo; lỗi hiển thị cảnh báo khi thiếu phòng cuối
- Nhánh quyết định: Nếu chưa chọn phòng cho lần cuối → cảnh báo và dừng lưu
- Kết quả dữ liệu: Kho tạm vaccine cập nhật theo chi tiết dịch vụ lẻ đã thanh toán
- Dữ liệu mẫu: `FacID`, `RoomID`, `Qty`, `MaChung`, `PatientID`, `ClinicalSessionID`
- Mapping UI → Code: `genie/app/(main)/thanh-toan/_hooks/use-save-data-mutiple-payment-method-retail.ts`

### Negative cases (đọc từ logic kiểm tra và bối cảnh)
- Thiếu `RoomID` ở lần thanh toán cuối → cảnh báo “Vui lòng chọn phòng tiêm...”, không gọi API
- Thiếu `PatientID` hoặc `FacID` → các bước trước đó sẽ dừng và/hoặc cảnh báo, không tiến tới gọi API V2
- `Qty` không hợp lệ (0 hoặc undefined) → theo code vẫn push nhưng backend có thể trả lỗi; cần xác thực dữ liệu đầu vào trước khi gọi
- Lỗi mạng/timeout khi `executeTransaction` → hiện dialog cảnh báo nội dung lỗi

### Thông tin API (theo usage thực tế FE)

Request (tham số truyền từ FE):
```typescript
{
  FacID: string;
  RoomID: number;              // 0 hoặc ID phòng tiêm
  Qty: number;                 // số lượng vaccine
  MaChung: string;             // mã chung vaccine
  PatientID: string;           // mã bệnh nhân
  ClinicalSessionID: string;   // phiên khám/chi định
}
```

cURL (qua endpoint DataAccess):
```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_INV_ProductTemp_Proccessing_Vaccine_V2",
      "parameters": {
        "FacID": "FAC001",
        "RoomID": 123,
        "Qty": 1,
        "MaChung": "MC_ABC",
        "PatientID": "PAT123",
        "ClinicalSessionID": "CS456"
      }
    }
  ]'
```

### Kết luận
- Frontend Genie KHÔNG dùng `ws_INV_ProductTemp_Proccessing_Vaccine` bản cũ, mà dùng `ws_INV_ProductTemp_Proccessing_Vaccine_V2` tại 3 vị trí trong module Thanh toán.
- API được gọi theo pattern `SequenceRequest` gửi qua `SystemService.executeTransaction`, không có service wrapper riêng.


