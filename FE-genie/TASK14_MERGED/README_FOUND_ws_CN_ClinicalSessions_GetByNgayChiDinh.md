## Kết quả tìm kiếm API Usage - Genie Frontend

### Thông tin tìm kiếm
- **API Name**: `ws_CN_ClinicalSessions_GetByNgayChiDinh`
- **Ngày tìm kiếm**: `2025-08-18`
- **Người thực hiện**: `phucnnd`
- **Project**: `Genie Frontend (React/Next.js)`

### Tổng quan kết quả
- **Tổng số file tìm thấy**: 2 files
- **Tổng số nơi sử dụng**: 2 nơi (1 service wrapper, 1 component sử dụng trực tiếp)
- **Loại usage**: Service Definition, Direct Usage
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong

### Phân tích sử dụng

#### Mục đích chính
1. ✅ Liệt kê dịch vụ đã được chỉ định theo ngày cho bệnh nhân (để hiển thị trong modal lịch sử khám/CLS)


### User Journey & Testing Scenarios

#### Flow 1: Xem dịch vụ đã chỉ định trong ngày tại “Danh sách khách hàng” (Tiếp nhận mới)
- **Đường dẫn màn hình**: Menu → Ngoại trú → Tiếp nhận → Tiếp nhận mới → mở modal “Danh sách khách hàng”
- **Tiền điều kiện**: Có bệnh nhân trong danh sách hôm nay (`PatientListToday`), trường `admitOn` có giá trị; user đã chọn cơ sở (`facId`)
- **Bước thao tác**:
  1) Mở modal “Danh sách khách hàng” từ màn hình Tiếp nhận mới
  2) Chọn bệnh nhân trong danh sách hôm nay
  3) Mở/hiển thị phần “Thông tin lịch sử khám bệnh” của bệnh nhân → hệ thống nạp “Dịch vụ đã được chỉ định”
- **Trigger API**: `ws_CN_ClinicalSessions_GetByNgayChiDinh` (qua `PatientService.fetchPatientClinicalSession`)
- **Kỳ vọng UI**: Bảng hiển thị các cột: Tên (serviceName), Số lượng (qty), Đơn giá (donGia), Thành tiền (thanhTien)
- **Nhánh quyết định**: Không
- **Kết quả dữ liệu**: Dữ liệu từ `response.data.table` ánh xạ `PatientClinicalSession[]`
- **Dữ liệu mẫu**: `facId: "8.1"`, `patientId: "24ff1575-d6dd-49f5-9d0b-012c203301fa"`, `ngayChiDinh: patient.admitOn`
- **Mapping UI → Code**: `admissionExaminationHistoryModal.tsx` → SWR block; `app/lib/services/patient.ts` → `fetchPatientClinicalSession`

#### Flow 2: Đổi bệnh nhân trong modal → re-fetch danh sách dịch vụ chỉ định
- **Đường dẫn màn hình**: Trong modal “Danh sách khách hàng” (Tiếp nhận mới)
- **Tiền điều kiện**: Modal đang mở, thay đổi bệnh nhân được chọn
- **Bước thao tác**:
  1) Chọn bệnh nhân khác trong danh sách
  2) SWR key thay đổi theo `payload` → tự động gọi lại API
- **Trigger API**: `ws_CN_ClinicalSessions_GetByNgayChiDinh`
- **Kỳ vọng UI**: Bảng dịch vụ cập nhật theo bệnh nhân mới
- **Nhánh quyết định**: Không
- **Kết quả dữ liệu**: Cùng cấu trúc như Flow 1
- **Dữ liệu mẫu**: Như trên, thay `patientId`
- **Mapping UI → Code**: `admissionExaminationHistoryModal.tsx` → SWR dependency `patient`

### cURL Example (tham khảo nhanh)
```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_CN_ClinicalSessions_GetByNgayChiDinh",
      "parameters": {
        "FacID": "8.1",
        "PatientID": "24ff1575-d6dd-49f5-9d0b-012c203301fa",
        "NgayChiDinh": "08/18/2025"
      }
    }
  ]'
```



