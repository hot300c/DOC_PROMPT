## API: ws_Vaccine_KiemTraTuongTac

### Frontend Genie (React/Next.js)

- **Service Definition**
  - File: `genie/app/lib/services/keVaccinTabServices.ts`
  - Export: `ws_Vaccine_KiemTraTuongTac(params: VaccineKiemTraTuongTacParams): Promise<VaccineKiemTraTuongTacResult>`
  - Params interface:
    - `VaccineKiemTraTuongTacParams { FacID: string; MaChung: string; PatientID: string; Ngay: string; }`
  - Response interface:
    - `VaccineKiemTraTuongTacResult { table: [{ isError: string; return: string; msg: string; }] }`

- **Direct Usage (Hook)**
  - File: `genie/app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts`
  - Context: Trong luồng chỉ định vaccine, trước khi lưu/tiếp tục, hệ thống gọi API để kiểm tra tương tác vaccine.
  - Call example:
    ```ts
    const tuongTacResult = await KeVaccinTabServices.ws_Vaccine_KiemTraTuongTac({
      FacID: facId,
      MaChung: vaccine.maChung,
      PatientID: patientId,
      Ngay: format(new Date(), "MM/dd/yyyy HH:mm:ss"),
    });
    if (tuongTacResult == null) return;
    if (tuongTacResult.table[0].isError != "0") {
      if (tuongTacResult.table[0].return == "1") {
        await alert({ title: tuongTacResult.table[0].msg });
        return;
      }
      const dialogResult = await confirm({ content: tuongTacResult.table[0].msg, title: "Thông báo" });
      if (!dialogResult) return;
      await KeVaccinTabServices.ws_CN_VaccineTuongTac_CanhBao_Save({ PatientID: patientId, ClinicalSessionID: text2, FacAdmissionID: facAdmissionId, FacID: facId });
    }
    ```

### Backend (SQL Procedure)

- File: `qas-db/QAHosGenericDB/Procedures/ws_Vaccine_KiemTraTuongTac.sql`
- Params: `@SessionID VARCHAR(MAX), @MaChung VARCHAR(100), @PatientID UNIQUEIDENTIFIER, @FacID VARCHAR(10), @Ngay DATETIME = NULL`
- Ghi chú: Frontend không truyền `SessionID`; gateway/backend có thể gắn tự động. Các tham số còn lại đã khớp FE.

### Request

```typescript
{
  FacID: string;      // Mã cơ sở
  MaChung: string;    // Mã chung vaccine
  PatientID: string;  // GUID bệnh nhân
  Ngay: string;       // MM/dd/yyyy HH:mm:ss
}
```

### Response

```typescript
{
  table: [
    {
      isError: string; // "0" = không chặn, khác "0" = có cảnh báo/chặn
      return: string;  // "1" = chặn (alert, dừng); giá trị khác = confirm (tiếp tục nếu user đồng ý)
      msg: string;     // Nội dung cảnh báo/khuyến cáo
    }
  ];
}
```

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

