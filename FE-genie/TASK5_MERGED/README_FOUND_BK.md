# Kết quả tìm kiếm API Usage - Genie Frontend

## Thông tin tìm kiếm
- **API Name**: `ws_Vaccine_KiemTraTuongTac`
- **Ngày tìm kiếm**: `2025-08-18`
- **Project**: `Genie Frontend (React/Next.js)`

## Tổng quan kết quả
- **Tổng số file tìm thấy**: 2 files
- **Tổng số nơi sử dụng**: 2 nơi
- **Loại usage**: Service Definition, Direct Usage (qua service function)
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong

## Phân tích sử dụng

- **Service Definition**
  - File: `genie/app/lib/services/keVaccinTabServices.ts`
  - Interfaces:
```288:296:genie/app/lib/services/keVaccinTabServices.ts
export interface VaccineKiemTraTuongTacParams {
  FacID: string;
  MaChung: string;
  PatientID: string;
  Ngay: string;
}

export interface VaccineKiemTraTuongTacResult {
  table: [
    {
```
  - Function:
```640:650:genie/app/lib/services/keVaccinTabServices.ts
export const ws_Vaccine_KiemTraTuongTac = async (
  params: VaccineKiemTraTuongTacParams,
): Promise<VaccineKiemTraTuongTacResult> => {
  const response = await httpService.post("/DataAccess", [
    {
      category: "QAHosGenericDB",
      command: "ws_Vaccine_KiemTraTuongTac",
      parameters: params,
    },
  ]);
  return response.data;
};
```

- **Direct Usage (qua service)**
  - File: `genie/app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts`
  - Vị trí: gọi trong flow chỉ định vaccine trước khi lưu chỉ định
```478:485:genie/app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts
const tuongTacResult = await KeVaccinTabServices.ws_Vaccine_KiemTraTuongTac(
  {
    FacID: facId,
    MaChung: vaccine.maChung,
    PatientID: patientId,
    Ngay: format(new Date(), "MM/dd/yyyy HH:mm:ss"),
  },
);
```
  - Xử lý kết quả:
```489:507:genie/app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts
if (tuongTacResult.table[0].isError != "0") {
  if (tuongTacResult.table[0].return == "1") {
    utils.notifyWarning(tuongTacResult.table[0].msg);
    return;
  }
  const dialogResult = await confirm({
    content: tuongTacResult.table[0].msg,
    title: "Thông báo",
  });
  if (!dialogResult) {
    return;
  }

  await KeVaccinTabServices.ws_CN_VaccineTuongTac_CanhBao_Save({
    PatientID: patientId,
    ClinicalSessionID: text2,
    FacAdmissionID: facAdmissionId,
    FacID: facId,
  });
}
```

## Mục đích chính
- ✅ Kiểm tra tương tác vaccine trước khi chỉ định
- ✅ Hiển thị cảnh báo/confirm cho người dùng khi có tương tác
- ✅ Ghi nhận cảnh báo tương tác (save) khi người dùng chấp nhận tiếp tục

## Pattern sử dụng
- **Service wrapper**: `ws_Vaccine_KiemTraTuongTac` gọi `httpService.post("/DataAccess", [...])`
- **Hook**: `useChiDinhVaccine` gọi service và xử lý kết quả (`notifyWarning`, `confirm`, và `ws_CN_VaccineTuongTac_CanhBao_Save`)

## User Journey & Testing Scenarios

### Flow Chỉ định vaccine tại khám bệnh
- **Đường dẫn màn hình**: Menu → Ngoại trú → Khám bệnh → Chỉ định vaccine
- **Tiền điều kiện**: `FacID`, `patientId`, `phacDo`, `vaccine` hợp lệ
- **Bước thao tác**:
  1) Chọn vaccine trong danh sách chỉ định
  2) Hệ thống kiểm tra các điều kiện khác (trùng nhóm bệnh, điều kiện chỉ định, hạn chế...) và sau đó gọi `ws_Vaccine_KiemTraTuongTac`
  3) Nếu có tương tác: hiển thị cảnh báo/confirm
  4) Nếu người dùng đồng ý, ghi nhận cảnh báo tương tác và tiếp tục quy trình chỉ định
- **Trigger API**: `ws_Vaccine_KiemTraTuongTac` (tại `useChiDinhVaccine → ChiDinhVaccine`)
- **Kỳ vọng UI**: Hiển thị cảnh báo hoặc confirm khi có tương tác; nếu chọn tiếp tục, flow chỉ định tiếp tục
- **Nhánh quyết định**:
  - `return == "1"` → chỉ cảnh báo (toast) và dừng
  - Confirm từ người dùng → nếu hủy thì dừng; nếu đồng ý thì lưu cảnh báo và tiếp tục
- **Kết quả dữ liệu**: Có thể phát sinh bản ghi cảnh báo tương tác qua `ws_CN_VaccineTuongTac_CanhBao_Save`
- **Dữ liệu mẫu**: `{ FacID, MaChung, PatientID, Ngay }`
- **Mapping UI → Code**: `genie/app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts` → `ChiDinhVaccine`

## Negative cases
- Response `table[0].isError == "0"` → không cảnh báo, tiếp tục bình thường
- `return == "1"` → chỉ cảnh báo dạng warning và dừng
- Người dùng chọn Cancel ở confirm → dừng flow
- Lỗi mạng/timeout khi gọi service → hiển thị lỗi tổng quát (qua handler chung nếu có)

## Thông tin API

### Request (FE)
```typescript
{
  FacID: string;
  MaChung: string;
  PatientID: string;
  Ngay: string; // MM/dd/yyyy HH:mm:ss
}
```

### Response (FE)
```typescript
{
  table: [
    {
      isError: string;  // "0" hoặc khác "0" khi có cảnh báo/ lỗi logic
      return: string;   // "1" → cảnh báo nhẹ; các trường hợp khác cần confirm
      msg: string;      // nội dung cảnh báo/ghi chú
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
        "FacID": "FAC001",
        "MaChung": "VAC001",
        "PatientID": "PAT123",
        "Ngay": "08/18/2025 10:00:00"
      }
    }
  ]'
```

## Kết luận
- API `ws_Vaccine_KiemTraTuongTac` được wrap trong `keVaccinTabServices` và được sử dụng tại `useChiDinhVaccine` để cảnh báo tương tác trước khi chỉ định.
- Flow UI có confirm và ghi nhận cảnh báo khi người dùng vẫn tiếp tục.
