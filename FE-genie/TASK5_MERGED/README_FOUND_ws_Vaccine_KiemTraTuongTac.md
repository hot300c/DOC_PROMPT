## API: ws_Vaccine_KiemTraTuongTac

### Frontend Genie (React/Next.js)

### cURL Example

```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_Vaccine_KiemTraTuongTac",
      "parameters": {
        "FacID": "8.1",
        "MaChung": "1000014",
        "PatientID": "33333333-3333-3333-3333-333333333333",
        "Ngay": "01/01/2024 10:00:00"
      }
    }
  ]'
```

### User Journey & Testing Scenarios

#### Flow Chỉ định vaccine – Kiểm tra tương tác trước khi chỉ định
- Đường dẫn màn hình: Menu → Ngoại trú → Khám bệnh
- Tiền điều kiện: `PatientID`, `FacID` có giá trị hợp lệ; đã chọn `vaccine` có `maChung`
- Bước thao tác:
  1) Chọn bệnh nhân cần chỉ định vaccine
  2) Chọn vaccine trong danh mục chỉ định
  3) Bấm chỉ định/tiếp tục
  4) Hệ thống gọi `ws_Vaccine_KiemTraTuongTac`
- Trigger API: `useChiDinhVaccine.ts` → `ws_Vaccine_KiemTraTuongTac`
- Kỳ vọng UI:
  - Nếu `isError == "0"`: không hiển thị cảnh báo, tiếp tục luồng
  - Nếu `isError != "0"` và `return == "1"`: hiển thị alert với `msg`, dừng luồng
  - Nếu `isError != "0"` và `return != "1"`: hiển thị confirm với `msg`
- Nhánh quyết định:
  - A) User đồng ý: tiếp tục, lưu cảnh báo qua `ws_CN_VaccineTuongTac_CanhBao_Save`
  - B) User từ chối: dừng luồng
- Kết quả dữ liệu: sử dụng `table[0].isError`, `table[0].return`, `table[0].msg`
- Dữ liệu mẫu: `FacID=8.1`, `MaChung=1000014`, `PatientID=33333333-3333-3333-3333-333333333333`, `Ngay=MM/dd/yyyy HH:mm:ss`
- Mapping UI → Code: `app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts` → gọi service trong `app/lib/services/keVaccinTabServices.ts`

#### Flow Xử lý cảnh báo tương tác – Lưu lại quyết định
- Đường dẫn màn hình: Menu → Ngoại trú → Khám bệnh
- Tiền điều kiện: Flow trên trả về `isError != "0"` và user xác nhận tiếp tục
- Bước thao tác:
  1) Hệ thống hiển thị confirm dialog (nội dung từ `msg`)
  2) User chọn Đồng ý
  3) Hệ thống gọi `ws_CN_VaccineTuongTac_CanhBao_Save` để lưu cảnh báo
- Trigger API: `useChiDinhVaccine.ts` → `ws_CN_VaccineTuongTac_CanhBao_Save`
- Kỳ vọng UI: Đóng dialog, tiếp tục quy trình chỉ định
- Nhánh quyết định:
  - A) Đồng ý: lưu cảnh báo, tiếp tục
  - B) Hủy: dừng
- Kết quả dữ liệu: cảnh báo tương tác được log lại (server)
- Mapping UI → Code: `app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts`

### Negative cases (đề xuất test)
- Thiếu `PatientID`/`MaChung`/`FacID`: API có thể trả lỗi hoặc FE chặn trước khi gọi
- Sai định dạng `Ngay`: server có thể parse lỗi; FE dùng `format(new Date(), "MM/dd/yyyy HH:mm:ss")`
- Network/API error: hiển thị cảnh báo lỗi kết nối; dừng luồng
- API trả `isError != "0"` và `return == "1"`: hiển thị alert, dừng

### Tổng kết
- Đã xác định 1 service definition và 1 usage trực tiếp trong hook chỉ định vaccine.
- Params FE khớp với BE (ngoại trừ `SessionID` do backend/gateway gắn), response được xử lý theo `isError/return/msg` để quyết định dừng/confirm/tiếp tục.

