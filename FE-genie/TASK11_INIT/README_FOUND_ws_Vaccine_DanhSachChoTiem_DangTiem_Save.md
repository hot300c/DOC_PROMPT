## Kết quả tìm kiếm API Usage - Genie Frontend

### Thông tin tìm kiếm
- **API Name**: `ws_Vaccine_DanhSachChoTiem_DangTiem_Save`
- **Ngày tìm kiếm**: `2025-08-21`
- **Project**: `Genie Frontend (React/Next.js)`

### Tổng quan kết quả
- **Tổng số file gọi trực tiếp**: 1
- **Tổng số nơi sử dụng (gián tiếp + UI trigger)**: 3
- **Loại usage**: Server Action, Hook điều phối, UI Component trigger
- **Trạng thái**: ✅ Hoàn tất phân tích

### Vị trí sử dụng
- **Direct call (Server Action)**: `genie/app/(main)/ngoai-tru/(nurse)/phong-tiem-vaccine/_actions/perform-injection.ts`
- **Indirect (Hook)**: `genie/app/(main)/ngoai-tru/(nurse)/phong-tiem-vaccine/_hooks/use-procedure-room.ts`
- **UI trigger**: `genie/app/(main)/ngoai-tru/(nurse)/phong-tiem-vaccine/_components/patient-data-container/patient-data-table.tsx`

### Mục đích sử dụng
- Khởi tạo/tracking trạng thái Đang Tiêm cho bệnh nhân tại phòng tiêm trước khi mở UI tiêm.
- Gate/validation: chỉ mở popup UI tiêm nếu API trả về `result === "Ok"`.

### Chi tiết kỹ thuật (FE)
- Server action `performInjection(patientId, roomId)` gọi `/DataAccess` với:
  - category: `QAHosGenericDB`
  - command: `ws_Vaccine_DanhSachChoTiem_DangTiem_Save`
  - parameters: `{ PatientID, RoomID, FacID, UserID }` (lấy `FacID`, `UserID` từ session)
- Hook `useProcedureRoom.goToVaccineUi(patientId)`:
  - Gọi `performInjection` trước; nếu `false` thì không mở popup và tắt overlay.
  - Nếu thành công, mở popup `.../phong-tiem-vaccine/[patientId]?roomId=...&date=...&dept=...`.
- Component `patient-data-table.tsx`:
  - Dùng `useProcedureRoom` để gọi `goToVaccineUi` và theo dõi `isVaccineOpen` để `router.refresh()` khi popup đóng.

### User Journeys (Flows)
#### Flow 1: Mở UI tiêm từ danh sách phòng tiêm
- **Đường dẫn**: Menu → Ngoại trú → Phòng tiêm Vaccine
- **Tiền điều kiện**: Có `PatientID`, URL có `?room=...`, session hợp lệ (`FacID`, `UserID`).
- **Bước**:
  1) Chọn bệnh nhân trong danh sách
  2) Trigger mở tiêm → `goToVaccineUi(patientId)`
  3) Gọi API `ws_Vaccine_DanhSachChoTiem_DangTiem_Save`
- **Kỳ vọng**: API Ok → popup mở; lỗi → không mở, overlay tắt, trang refresh.
- **Mapping**: `patient-data-table.tsx` → `useProcedureRoom.goToVaccineUi` → `performInjection` → `/DataAccess`.

#### Flow 2: Mở popup kèm tham số phòng/ngày/khoa
- **Đường dẫn**: Menu → Ngoại trú → Phòng tiêm Vaccine
- **Tiền điều kiện**: URL có `?room=...&date=...&dept=...`
- **Bước**:
  1) Chọn bệnh nhân → `goToVaccineUi`
  2) Hook build query, gọi API trước khi `window.open`
- **Kỳ vọng**: Popup mở trung tâm; nếu đóng → overlay tắt, context reset.
- **Mapping**: `useProcedureRoom.ts` → `perform-injection.ts`.

### Thông tin API (theo usage FE)
- **Request**:
  - `PatientID: string (GUID)`
  - `RoomID: string`
  - `FacID: string`
  - `UserID: string`
- **Response tối thiểu FE dùng**: `data.table[0].result === "Ok"`

### cURL minh hoạ
```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_Vaccine_DanhSachChoTiem_DangTiem_Save",
      "parameters": {
        "PatientID": "11111111-1111-1111-1111-111111111111",
        "RoomID": "101",
        "FacID": "FAC001",
        "UserID": "22222222-2222-2222-2222-222222222222"
      }
    }
  ]'
```

### Backend liên quan
- **Handler**: `aladdin/WebService.Handlers/QAHosGenericDB/ws_Vaccine_DanhSachChoTiem_DangTiem_Save.cs`
- **Tests**: `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_Vaccine_DanhSachChoTiem_DangTiem_Save_Test.cs`
