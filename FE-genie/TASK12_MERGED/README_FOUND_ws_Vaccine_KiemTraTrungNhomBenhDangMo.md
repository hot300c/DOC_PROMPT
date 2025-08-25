## Kết quả tìm kiếm API Usage - Genie Frontend

### Thông tin tìm kiếm
- **API Name**: `ws_Vaccine_KiemTraTrungNhomBenhDangMo`
- **Project**: Genie Frontend (React/Next.js)
- **Thư mục**: `C:\PROJECTS\genie`

### Tổng quan kết quả
- **Tổng số file tìm thấy**: 3
- **Loại usage**: Service Definition, Direct Usage (hooks)
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong

### Phân tích sử dụng

- **Service Definition**
  - **File**: `genie/app/lib/services/detailCheckup.ts`
  - **Function**: `ws_Vaccine_KiemTraTrungNhomBenhDangMo(params)`
  - **Command**: `"ws_Vaccine_KiemTraTrungNhomBenhDangMo"`
  - Trả về `data` với `table[0].column1` là số lượng phác đồ chung nhóm bệnh đang mở

- **Direct Usage 1**
  - **File**: `genie/app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts`
  - **Context**: Trong flow chỉ định vaccine, gọi API để kiểm tra trùng nhóm bệnh đang mở trước khi tiếp tục
  - **Điều kiện**: Nếu `table[0].column1 > 1` → hiển thị cảnh báo và dừng

- **Direct Usage 2**
  - **File**: `genie/app/(main)/ngoai-tru/kham-benh/hooks/useTiemNgoai.ts`
  - **Context**: Trong flow Tiêm Ngoài, gọi API để kiểm tra trùng nhóm bệnh trước khi cập nhật trạng thái tiêm ngoài
  - **Điều kiện**: Nếu `table[0]?.column1 > 1` → thông báo lỗi và dừng

### Thông tin API

#### Request
```typescript
// detailCheckup.ts
type VaccineCheckDuplicateParams = {
  PatientID: string;
  MaChung: string;
};
```

#### Response (được sử dụng thực tế)
```typescript
// response.data
{
  table: [
    { column1: number } // số lượng phác đồ chung nhóm bệnh đang mở
  ]
}
```

#### cURL Example
```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_Vaccine_KiemTraTrungNhomBenhDangMo",
      "parameters": {
        "PatientID": "<PATIENT_ID>",
        "MaChung": "<MA_CHUNG>"
      }
    }
  ]'
```

### User Journey & Testing Scenarios

#### Flow Chỉ định vaccine (Kiểm tra trùng nhóm bệnh đang mở)
- **Đường dẫn màn hình**: Menu → Ngoại trú → Khám bệnh
- **Tiền điều kiện**: Có `PatientID`, `FacID`; mở hồ sơ khám với phác đồ vaccine
- **Bước thao tác**:
  1) Chọn vaccine cần chỉ định trong danh sách gợi ý/chi tiết phác đồ
  2) Thực hiện thao tác chỉ định (nút tương ứng trong UI)
- **Trigger API**: `ws_Vaccine_KiemTraTrungNhomBenhDangMo`
- **Kỳ vọng UI**: Nếu có ≥ 2 phác đồ chung nhóm bệnh đang mở → Hiển thị cảnh báo và không tiếp tục chỉ định
- **Kết quả dữ liệu**: Đọc `data.table[0].column1`
- **Mapping UI → Code**: `app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts` → gọi `ws_Vaccine_KiemTraTrungNhomBenhDangMo`

#### Flow Tiêm ngoài (Kiểm tra trùng nhóm bệnh trước khi xác nhận)
- **Đường dẫn màn hình**: Menu → Ngoại trú → Khám bệnh
- **Tiền điều kiện**: Có mũi trong phác đồ, thao tác bật/tắt trạng thái Tiêm ngoài
- **Bước thao tác**:
  1) Chọn mũi vaccine trong phác đồ
  2) Thực hiện thao tác Tiêm ngoài
- **Trigger API**: `ws_Vaccine_KiemTraTrungNhomBenhDangMo`
- **Kỳ vọng UI**: Nếu `column1 > 1` → Thông báo lỗi và dừng cập nhật
- **Kết quả dữ liệu**: Đọc `data.table[0].column1`
- **Mapping UI → Code**: `app/(main)/ngoai-tru/kham-benh/hooks/useTiemNgoai.ts` → gọi `detailCheckup.ws_Vaccine_KiemTraTrungNhomBenhDangMo`



- TESTING CASE DATA DEV:
https://dev-genie.vnvc.info/ngoai-tru/kham-benh/80daad32-643b-42e0-9c3a-012ffcf2013b?date=2025-08-19&deptID=5&roomID=1&doiTuongInPhieu=1&isPediatric=false

https://dev-genie.vnvc.info/ngoai-tru/kham-benh/f8b23382-6b65-4b3e-850d-0131119201ff?date=2025-08-20&deptID=5&roomID=3&doiTuongInPhieu=1&isPediatric=false

FLOW 1:
Mô tả:
Điều kiện: Trùng nhóm bệnh tương ứng như : Bạch hầu, Ho gà, Uốn ván.
1) Khi chỉ định 1 vaccin --> popup bảng "Danh sách phác đồ sẽ đóng" (Còn giữ lại ít nhất 1 nhóm bệnh tương ứng) 
2) Sau đó thêm 1 vaccion mới số cùng nhóm bệnh  (Thì hệ thống sẽ sinh ra 3 phác đồ theo nhóm bệnh mới).
3) Sau đó chọn chỉ định cái mới vừa thêm --> Hệ thống báo lỗi.

FLOW 2:
Mô tả:
Điều kiện: Trùng nhóm bệnh tương ứng như : Bạch hầu, Ho gà, Uốn ván.
1) Khi chỉ định 1 vaccin --> popup bảng "Danh sách phác đồ sẽ đóng" (Còn giữ lại ít nhất 1 nhóm bệnh tương ứng) 
2) Sau đó thêm 1 vaccion mới số cùng nhóm bệnh  (Thì hệ thống sẽ sinh ra 3 phác đồ theo nhóm bệnh mới).
3) Sau đó chọn chỉ định cái mới vừa thêm --> Hệ thống báo lỗi.





### Chi tiết vị trí mã nguồn

- `genie/app/lib/services/detailCheckup.ts`
- `genie/app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts`
- `genie/app/(main)/ngoai-tru/kham-benh/hooks/useTiemNgoai.ts`

### Ghi chú
- API được wrap trực tiếp dưới dạng function trùng tên trong `detailCheckup.ts` (không dùng prefix `fetch_`)
- Các hook nghiệp vụ gọi API để chặn thao tác khi phát hiện trùng nhóm bệnh đang mở


