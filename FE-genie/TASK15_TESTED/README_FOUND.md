# Kết quả tìm kiếm API Usage - Genie Frontend

## Thông tin tìm kiếm
- **API Name**: `ws_Vaccine_ThongBaoKhongchan`
- **Ngày tìm kiếm**: `2025-08-18`
- **Người thực hiện**: `phucnnd`
- **Project**: `Genie Frontend (React/Next.js)`

## Tổng quan kết quả
- **Tổng số file tìm thấy**: `2 files`
- **Tổng số nơi sử dụng**: `1 nơi` (Direct Usage)
- **Loại usage**: Service Definition, Direct Usage
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong (chỉ trong Genie, theo hướng dẫn)

## Phân tích sử dụng

### Mục đích chính
1. ✅ Hiển thị cảnh báo không chặn (nếu có) trước/đang khi chỉ định vaccine
2. ✅ Xác nhận tiếp tục hoặc đồng ý chỉ định qua `ws_Vaccine_DongY_ChiDinh`

### Pattern sử dụng
- **Service Layer Pattern**: API được wrap trực tiếp trong `keVaccinTabServices.ts`
- **Import Pattern**: Import từ `@/app/lib/services/keVaccinTabServices`
- **Response Handling**: Đọc `result.table[0].mess` để hiển thị cảnh báo

### User Journey & Testing Scenarios (đi từng bước cụ thể trên màn hình)

#### Flow A: Chỉ định vaccine tại màn hình Khám bệnh (Ngoại trú)
- **Đường dẫn màn hình**: Menu → Ngoại trú → Khám bệnh (`app/(main)/ngoai-tru/kham-benh`)
- **Tiền điều kiện**:
  - Đang ở phiên khám có `PatientID`, `FacAdmissionID`, `PhysicianAdmissionID`, `ClinicalSessionID` (lấy từ context `useMedicalCheckup`).
  - Trạng thái hồ sơ không phải: “Được tiêm”, “Bỏ về”, “Không được tiêm”.
- **Các bước thao tác**:
  1) Tại khu vực danh sách phác đồ/mũi tiêm, chọn 1 dòng vaccine cần chỉ định.
  2) Nhấn nút “Chỉ định” của dòng đó.
  3) Hệ thống thực hiện chuỗi kiểm tra; tới bước gọi `ws_Vaccine_ThongBaoKhongchan` với `ClinicalSessionID` hiện tại.
  4) Nếu API trả về `table[0].mess` → hiển thị dialog Cảnh báo với nội dung trả về.
  5) Hệ thống hiển thị dialog xác nhận “Bạn đồng ý tiếp tục chỉ định ?”.
     - Chọn “Đồng ý” → gọi `ws_Vaccine_DongY_ChiDinh` (`Type: "0"` khi chỉ định mới, hoặc `"1"` nếu đang ở trạng thái đã chỉ định) rồi tiếp tục lưu chỉ định.
     - Chọn “Hủy/Không” → dừng, không tiếp tục.
  6) Hoàn tất: nếu thành công, hiện “Đã lưu” và refresh các danh sách liên quan.
- **Kỳ vọng hiển thị**:
  - 01 dialog Cảnh báo (nếu có `mess`).
  - 01 dialog Xác nhận tiếp tục.
- **Lưu ý**: API này chỉ chạy ở nhánh “chưa chỉ định” (`!vaccine.isChiDinh`).

#### Flow B: Kiểm thử nhanh (QA checklist trên UI)
1) Mở Ngoại trú → Khám bệnh, chọn khách hàng có phác đồ vaccine.
2) Chọn dòng vaccine “chưa chỉ định”, bấm “Chỉ định”.
3) Kiểm tra popup cảnh báo (nếu API trả về `mess`).
4) Bấm “Đồng ý” để tiếp tục → xác nhận hệ thống lưu thành công và refresh.
5) Thử thêm trường hợp khác để so sánh có/không cảnh báo.

#### Flow C: Kiểm thử qua API (Postman/cURL)
- Gọi `POST /api/DataAccess` theo cURL phía dưới với một `ClinicalSessionID` hợp lệ → kiểm tra `table[0].mess`.
- Đối chiếu lại UX trong Flow A.

## Thông tin API

### Request
```typescript
{
  ClinicalSessionID: string; // GUID phiên khám hiện tại
}
```

### Response (quan sát từ usage)
```typescript
{
  table?: Array<{
    mess?: string; // Nội dung cảnh báo không chặn để hiển thị
  }>
}
```

### cURL Example
```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_Vaccine_ThongBaoKhongchan",
      "parameters": {
        "ClinicalSessionID": "<GUID>"
      }
    }
  ]'
```

## Chi tiết kết quả

### 1. Service Definition
- **File**: `genie/app/lib/services/keVaccinTabServices.ts`
- **Line**: `964-980`
- **Function**: `ws_Vaccine_ThongBaoKhongchan`
- **Mục đích**: Gọi API backend để lấy thông báo không chặn theo `ClinicalSessionID`

```964:980:genie/app/lib/services/keVaccinTabServices.ts
export interface VaccineThongBaoKhongchanParams {
  ClinicalSessionID: string;
}

export const ws_Vaccine_ThongBaoKhongchan = async (
  params: VaccineThongBaoKhongchanParams,
) => {
  const response = await httpService.post("/DataAccess", [
    {
      category: "QAHosGenericDB",
      command: "ws_Vaccine_ThongBaoKhongchan",
      parameters: params,
    },
  ]);
  return response.data;
};
```

### 2. Direct Usage
- **File**: `genie/app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts`
- **Line**: `590-600`
- **Context**: Trong luồng `ChiDinhVaccine`, gọi API để lấy cảnh báo; nếu có `mess` thì hiển thị, sau đó hỏi xác nhận tiếp tục và có thể gọi `ws_Vaccine_DongY_ChiDinh`

```590:600:genie/app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts
const thongBaoKhongChanResult =
  await KeVaccinTabServices.ws_Vaccine_ThongBaoKhongchan({
    ClinicalSessionID: text2,
  });
if (thongBaoKhongChanResult.table?.length > 0) {
  if (thongBaoKhongChanResult.table[0].mess)
    await alert({
      title: ETitleConfirm.CANH_BAO,
      content: thongBaoKhongChanResult.table[0].mess,
    });
```

## Kết luận
API `ws_Vaccine_ThongBaoKhongchan` trong Genie được sử dụng tại:
1. **Service Definition** (1 nơi): `genie/app/lib/services/keVaccinTabServices.ts`
2. **Direct Usage** (1 nơi): `genie/app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts`

API đóng vai trò cảnh báo không chặn trong luồng chỉ định vaccine, giúp bác sĩ cân nhắc tiếp tục thao tác.

## Ghi chú
- Báo cáo này chỉ bao gồm tìm kiếm trong Genie Frontend theo hướng dẫn `API_SEARCH_GUIDE.md`.
- Tham số `ClinicalSessionID` được truyền từ ngữ cảnh khám bệnh; không thêm các tham số khác ngoài scope FE.

