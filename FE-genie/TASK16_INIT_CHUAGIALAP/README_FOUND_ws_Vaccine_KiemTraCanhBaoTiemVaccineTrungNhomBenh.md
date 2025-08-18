# Kết quả tìm kiếm API Usage - Genie Frontend

## Thông tin tìm kiếm
- **API Name**: `ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh`
- **Ngày tìm kiếm**: `2024-12-19`
- **Người thực hiện**: `phucnnd`
- **Project**: `Genie Frontend (React/Next.js)`

## Tổng quan kết quả
- **Tổng số file tìm thấy**: `3 files`
- **Tổng số nơi sử dụng**: `3 nơi` (bao gồm cả các nơi gọi gián tiếp)
- **Loại usage**: Service Definition, Direct Usage, UI Components
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong

## Phân tích sử dụng

### Mục đích chính
1. ✅ **Validation**: Kiểm tra cảnh báo tiêm vaccine trùng nhóm bệnh trước khi chỉ định
2. ✅ **Safety Check**: Đảm bảo an toàn khi chỉ định vaccine cho bệnh nhân
3. ✅ **User Warning**: Hiển thị cảnh báo cho bác sĩ khi có nguy cơ trùng nhóm bệnh
4. ✅ **Decision Support**: Hỗ trợ bác sĩ đưa ra quyết định chỉ định vaccine
5. ✅ **Protocol Management**: Quản lý phác đồ vaccine và tránh xung đột

### Giải thích về "Trùng nhóm bệnh"
**Vấn đề y tế**: Khi tiêm 2 vaccine cùng nhóm bệnh trong thời gian ngắn có thể gây:
- **Tương tác thuốc**: Vaccine có thể "đánh nhau" với nhau
- **Tăng tác dụng phụ**: Cơ thể phải xử lý nhiều kháng nguyên cùng lúc  
- **Giảm hiệu quả**: Vaccine có thể không hoạt động tốt
- **Nguy hiểm sức khỏe**: Có thể gây sốc phản vệ hoặc phản ứng nặng

**Ví dụ thực tế**: 
- Bệnh nhân đã tiêm vaccine CÚM (nhóm bệnh đường hô hấp) hôm qua
- Hôm nay bác sĩ muốn tiêm thêm vaccine VIÊM PHỔI (cũng thuộc nhóm bệnh đường hô hấp)
- → Hệ thống cảnh báo: "Cảnh báo! Bệnh nhân vừa tiêm vaccine cùng nhóm bệnh"

### Pattern sử dụng
- **Service Layer Pattern**: API được wrap trong service function trong `keVaccinTabServices.ts`
- **Import Pattern**: Import từ service layer thông qua `KeVaccinTabServices`
- **Error Handling**: Sử dụng response structure với `errcode` và `errMsg`
- **Type Safety**: Có TypeScript interface `VaccineKiemTraCanhBaoTiemVaccineTrungNhomBenhParams`
- **Business Logic Pattern**: API được sử dụng trong business logic function `ChiDinhVaccine`
- **UI Component Pattern**: API được trigger từ UI checkbox "Chỉ định" trong bảng vaccine

### User Journey & Testing Scenarios

#### Scenario 1: Chỉ định vaccine cho bệnh nhân
1. **Login** vào hệ thống Genie
2. **Mở menu** "Ngoại trú" → "Khám bệnh" → Chọn bệnh nhân
3. **Chuyển sang tab "Chỉ định Vắc-xin"** → Chọn tab con **"Kê vaccine"**
4. **Chọn vaccine** từ danh sách vaccine trong phác đồ (bảng hiển thị các cột: Chỉ định, Mũi, Tên Vaccine, SL, Lịch tiêm, Ngày đã tiêm, v.v.)
5. **Bấm checkbox "Chỉ định"** (cột đầu tiên) → API `ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh` được gọi
6. **Kết quả**: 
   - Nếu không có cảnh báo → Chỉ định vaccine thành công
   - Nếu có cảnh báo → Hiển thị dialog cảnh báo với nội dung từ `errMsg`

   LINK VÍ DỤ:
   https://dev-genie.vnvc.info/ngoai-tru/kham-benh/4ea37bc4-410d-43e5-9f5f-012e6ec902c5?date=2025-08-18&deptID=5&roomID=1&doiTuongInPhieu=1&isPediatric=false

   curl 'https://dev-genie.vnvc.info/aladdin/DataAccess/ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'content-type: application/json' \
  -b 'qaaAnswered=true; s=fc93a0d4-c38d-4bf9-8f47-c89045ac10bb; u=e9a4dd0a-6b52-480e-8c15-a0f49f67b5fa; facId=8.1; customerId=8; sidebar:state=false' \
  -H 'origin: https://dev-genie.vnvc.info' \
  -H 'priority: u=1, i' \
  -H 'referer: https://dev-genie.vnvc.info/ngoai-tru/kham-benh/4ea37bc4-410d-43e5-9f5f-012e6ec902c5?date=2025-08-18&deptID=5&roomID=1&doiTuongInPhieu=1&isPediatric=false' \
  -H 'sec-ch-ua: "Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'source: genie' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36' \
  --data-raw '[{"category":"QAHosGenericDB","command":"ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh","parameters":{"MaChung":"7","PatientID":"4ea37bc4-410d-43e5-9f5f-012e6ec902c5","NgayChiDinh":"08/18/2025 11:24:12","PhacDoDangChiDinh":"51688bb6-7fc5-435a-a0f4-acf70c351af9","FacID":"8.1"}}]'

#### Scenario 2: Kiểm tra cảnh báo trùng nhóm bệnh
1. **Login** vào hệ thống Genie
2. **Mở menu** "Ngoại trú" → "Khám bệnh" → Chọn bệnh nhân
3. **Chuyển sang tab "Chỉ định Vắc-xin"** → Chọn tab con **"Kê vaccine"**
4. **Chọn vaccine** có cùng nhóm bệnh với vaccine đã chỉ định trước đó
5. **Bấm checkbox "Chỉ định"** → API được gọi để kiểm tra
6. **Kết quả**:
   - Nếu có trùng nhóm bệnh → Hiển thị cảnh báo và cho phép bác sĩ quyết định
   - Nếu không trùng → Tiếp tục chỉ định bình thường

#### Scenario 3: Quản lý phác đồ vaccine
1. **Login** vào hệ thống Genie
2. **Mở menu** "Ngoại trú" → "Khám bệnh" → Chọn bệnh nhân
3. **Chuyển sang tab "Chỉ định Vắc-xin"** → Chọn tab con **"Kê vaccine"**
4. **Thêm vaccine mới** vào phác đồ hiện có
5. **Hệ thống tự động** gọi API để kiểm tra xung đột
6. **Kết quả**:
   - Nếu có xung đột → Hiển thị cảnh báo và hướng dẫn xử lý
   - Nếu không có xung đột → Thêm vaccine thành công

## Cấu trúc Tabs thực tế trong Genie

### Tab Structure
- **Tab chính**: "Chỉ định Vắc-xin" (`vaccineIndication`)
- **Tab con bên trong**:
  - **"Kê vaccine"** (`keVaccine`) - Đây chính là tab xử lý vaccine (tương đương với "Kế hoạch vaccine" trong tài liệu cũ)
  - **"Phác đồ đã đóng"** (`phacDoDaDong`) - Xem phác đồ đã hoàn thành

### File Location
- **Tab chính**: `app/(main)/ngoai-tru/kham-benh/[patientId]/tabs/VaccineIndicationTab.tsx`
- **Tab con "Kê vaccine"**: `app/(main)/ngoai-tru/kham-benh/[patientId]/tabs/KeVaccinTab.tsx`

### Lưu ý
- Tài liệu cũ gọi là "Kế hoạch vaccine" nhưng thực tế trong code là tab con "Kê vaccine" bên trong tab "Chỉ định Vắc-xin"
- API `ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh` được sử dụng trong tab con "Kê vaccine"

### Các API Kiểm tra Vaccine trong ChiDinhVaccine
Khi chỉ định vaccine, hệ thống sẽ gọi **nhiều API kiểm tra** theo thứ tự:
1. **`ws_Vaccine_KiemTraTrungNhomBenhDangMo`** (dòng 192) - Kiểm tra có 2 phác đồ cùng nhóm bệnh đang mở không
   - **Cảnh báo cụ thể**: "Khách hàng đang có 2 phác đồ chung nhóm bệnh đang mở, vui lòng kiểm tra lại"
2. **`ws_Vaccine_KiemTraTuongTac`** - Kiểm tra tương tác vaccine
3. **`ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh`** (dòng 509) - **API chính** kiểm tra cảnh báo trùng nhóm bệnh
   - **Cảnh báo cụ thể**: Nội dung từ `errMsg` của API response
4. **`ws_Vaccine_KTChiDinhVaccineCungNhomBenh`** - Kiểm tra vaccine cùng nhóm bệnh
5. **`ws_Vaccine_ChiDinhVaccine`** - Thực hiện chỉ định vaccine

### Cấu trúc Bảng Vaccine
Bảng vaccine trong tab "Kê vaccine" có các cột chính:
- **Chỉ định** (cột đầu tiên): Checkbox để chỉ định vaccine
- **Mũi**: Số thứ tự mũi tiêm
- **Tên Vaccine**: Tên vaccine với tooltip chi tiết
- **SL**: Số lượng
- **Lịch tiêm**: Date picker để chọn ngày hẹn
- **Ngày đã tiêm**: Date picker để chọn ngày đã tiêm
- **Trung tâm**: Tên trung tâm tiêm chủng

## Thông tin API
```typescript
{
  MaChung: string;                    // Mã chung của vaccine
  PatientID: string;                  // ID của bệnh nhân
  NgayChiDinh: string;                // Ngày chỉ định (format: MM/dd/yyyy HH:mm:ss)
  PhacDoDangChiDinh: string;          // ID phác đồ đang chỉ định
  FacID: string;                      // ID của cơ sở y tế
}
```

### Response
```typescript
{
  table: [
    {
      errcode: string;                 // "0" = không có cảnh báo, "1" = có cảnh báo
      errMsg: string;                  // Nội dung thông báo cảnh báo (nếu có)
    }
  ]
}
```

### cURL Example
```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh",
      "parameters": {
        "MaChung": "S00000003",
        "PatientID": "b87020e4-9fa0-4cb5-bab5-0071f56501fd",
        "NgayChiDinh": "12/19/2024 10:30:00",
        "PhacDoDangChiDinh": "f51e5bb8-ec02-11ee-b780-8cec4b9f2b93",
        "FacID": "8.1"
      }
    }
  ]'
```

## Chi tiết kết quả

### 1. Service Definition
- **File**: `app/lib/services/keVaccinTabServices.ts`
- **Line**: `856-868`
- **Function**: `ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh`
- **Mục đích**: API wrapper function cho backend procedure
- **Parameters**: Interface `VaccineKiemTraCanhBaoTiemVaccineTrungNhomBenhParams`
- **Response Type**: Promise với structure `{ table: [{ errcode: string; errMsg: string }] }`

### 2. Direct Usage
- **File**: `app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts`
- **Line**: `509-518`
- **Function**: `ChiDinhVaccine` (trong hook `useChiDinhVaccine`)
- **Context**: Kiểm tra cảnh báo trước khi chỉ định vaccine
- **Trigger**: Được gọi từ UI component khi bấm checkbox "Chỉ định"
- **Code snippet**: 
```typescript
const canhBaoTiemVaccineTrungNhomBenhResult =
  await KeVaccinTabServices.ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh({
    MaChung: vaccine.maChung,
    PatientID: patientId,
    NgayChiDinh: format(new Date(), "MM/dd/yyyy HH:mm:ss"),
    PhacDoDangChiDinh: phacDo.idPhacDoBenhNhan,
    FacID: facId,
  });
```

### 3. UI Components và Buttons liên quan
- **File**: `app/(main)/ngoai-tru/kham-benh/[patientId]/tabs/KeVaccinTab.tsx`
- **Line**: `706-780` (trong `columnsVaccinceChiDinh`)
- **Component**: Checkbox "Chỉ định" trong bảng vaccine (cột đầu tiên)
- **Header**: "Chỉ định" 
- **Trigger**: `onClick` event của checkbox
- **Action**: Gọi function `ChiDinhVaccine` với các tham số vaccine, muiTruoc, muiSau, phacDo
- **UI Flow**: 
  1. User click checkbox "Chỉ định" (cột đầu tiên của bảng)
  2. Hàm `ChiDinhVaccine` được gọi
  3. API `ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh` được gọi
  4. Nếu có cảnh báo → Hiển thị dialog cảnh báo
  5. Nếu không có cảnh báo → Tiếp tục chỉ định vaccine

### 4. Business Logic Integration
- **File**: `app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts`
- **Line**: `95-953`
- **Function**: `ChiDinhVaccine` (async function)
- **Logic Flow**:
  1. Kiểm tra vaccine và phác đồ hợp lệ
  2. **Kiểm tra trùng nhóm bệnh đang mở** (`ws_Vaccine_KiemTraTrungNhomBenhDangMo`) - dòng 192
  3. Kiểm tra tương tác vaccine (`ws_Vaccine_KiemTraTuongTac`)
  4. **Kiểm tra cảnh báo tiêm vaccine trùng nhóm bệnh** (`ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh`) - dòng 509
  5. Nếu có cảnh báo → Hiển thị dialog decision cho user
  6. Kiểm tra vaccine cùng nhóm bệnh (`ws_Vaccine_KTChiDinhVaccineCungNhomBenh`)
  7. Thực hiện chỉ định vaccine (`ws_Vaccine_ChiDinhVaccine`)
  8. Cập nhật trạng thái và refresh data

## Kết luận
API `ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh` được sử dụng trong hệ thống Genie với **3 nơi sử dụng chính**:

1. **Service Definition** (1 nơi) - `keVaccinTabServices.ts`
2. **Direct Usage** (1 nơi) - `useChiDinhVaccine.ts` hook
3. **UI Components** (1 nơi) - Checkbox "Chỉ định" trong `KeVaccinTab.tsx` (tab con "Kê vaccine")

API này đóng vai trò **QUAN TRỌNG** trong việc đảm bảo an toàn khi chỉ định vaccine, kiểm tra xung đột nhóm bệnh và hỗ trợ bác sĩ đưa ra quyết định chính xác.

**Lưu ý quan trọng**: 
- API được sử dụng trong tab con **"Kê vaccine"** bên trong tab chính **"Chỉ định Vắc-xin"**, không phải trong tab riêng biệt "Kế hoạch vaccine" như tài liệu cũ đã ghi
- **API này là một trong nhiều API kiểm tra** được gọi khi chỉ định vaccine, cùng với `ws_Vaccine_KiemTraTrungNhomBenhDangMo` và các API khác

## Ghi chú
- API này là backend procedure được wrap thành frontend service
- Có sử dụng TypeScript types để đảm bảo type safety
- Error handling được implement thông qua response structure với `errcode` và `errMsg`
- Pattern sử dụng nhất quán trong toàn bộ codebase
- API được tích hợp chặt chẽ vào workflow chỉ định vaccine
- **Mục đích chính**: Kiểm tra cảnh báo trùng nhóm bệnh trước khi chỉ định vaccine
- **User Experience**: Hiển thị cảnh báo rõ ràng và cho phép user quyết định có tiếp tục hay không

## ❓ FAQ - Câu hỏi thường gặp

### **Q: Tại sao cần kiểm tra trùng nhóm bệnh?**
**A**: Để đảm bảo an toàn cho bệnh nhân. Tiêm 2 vaccine cùng nhóm bệnh trong thời gian ngắn có thể gây tương tác thuốc, tăng tác dụng phụ, giảm hiệu quả hoặc thậm chí nguy hiểm đến sức khỏe.

### **Q: "Nhóm bệnh" là gì?**
**A**: Là tập hợp các bệnh có liên quan đến nhau. Ví dụ:
- **Nhóm bệnh đường hô hấp**: Cúm, Viêm phổi, Viêm phế quản
- **Nhóm bệnh đường tiêu hóa**: Tiêu chảy, Viêm dạ dày, Viêm ruột
- **Nhóm bệnh truyền nhiễm**: Sởi, Quai bị, Rubella

### **Q: Hệ thống xử lý cảnh báo như thế nào?**
**A**: 
1. Hiển thị dialog cảnh báo với nội dung từ `errMsg`
2. Cho phép bác sĩ quyết định: Tiếp tục hoặc Hủy
3. Nếu tiếp tục → Ghi nhận quyết định và tiêm vaccine
4. Nếu hủy → Không tiêm vaccine này

### **Q: Có bao nhiêu loại kiểm tra vaccine?**
**A**: Hệ thống thực hiện **5 bước kiểm tra** theo thứ tự:
1. Kiểm tra trùng nhóm bệnh đang mở
2. Kiểm tra tương tác vaccine  
3. **Kiểm tra cảnh báo trùng nhóm bệnh** (API chính)
4. Kiểm tra vaccine cùng nhóm bệnh
5. Thực hiện chỉ định vaccine

---

*Tài liệu được tạo tự động từ kết quả tìm kiếm API Usage*
