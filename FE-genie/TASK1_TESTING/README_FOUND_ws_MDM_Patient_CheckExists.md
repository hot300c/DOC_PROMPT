# Kết quả tìm kiếm API Usage - Genie Frontend

## Thông tin tìm kiếm
- **API Name**: `ws_MDM_Patient_CheckExists`
- **Ngày tìm kiếm**: `2024-12-19`
- **Người thực hiện**: `phucnnd`
- **Project**: `Genie Frontend (React/Next.js)`

## Tổng quan kết quả
- **Tổng số file tìm thấy**: `3 files`
- **Tổng số nơi sử dụng**: `5-6 nơi` (bao gồm cả các nơi gọi gián tiếp)
- **Loại usage**: Service Definition, Direct Usage, Service Layer, Indirect Usage
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong

## Phân tích sử dụng

### Mục đích chính
1. ✅ **Validation**: Kiểm tra bệnh nhân tồn tại trước khi thực hiện các thao tác
2. ✅ **Data Loading**: Quyết định có tải dữ liệu từ nguồn bên ngoài hay không
3. ✅ **Barcode Printing**: Validate trước khi in mã vạch bệnh nhân
4. ✅ **Patient Search**: Validate trong quá trình tìm kiếm bệnh nhân
5. ✅ **External Data Sync**: Kiểm tra trước khi đồng bộ dữ liệu từ Nutri

### Pattern sử dụng
- **Service Layer Pattern**: API được wrap trong service function với prefix `fetch_`
- **Import Pattern**: Import từ service layer thay vì gọi trực tiếp
- **Error Handling**: Sử dụng `checkResponse` utility để xử lý lỗi
- **Type Safety**: Có TypeScript types và interfaces đầy đủ

### User Journey & Testing Scenarios

#### Scenario 1: In mã vạch bệnh nhân
1. **Login** vào hệ thống Genie
2. **Mở menu** "Tiếp nhận" → "Tiếp nhận mới"
3. **Tìm kiếm** bệnh nhân bằng mã bệnh nhân hoặc thông tin cá nhân
4. **Chọn bệnh nhân** từ danh sách kết quả
5. **Bấm nút "In mã vạch"** → API `ws_MDM_Patient_CheckExists` được gọi để validate
6. **Kết quả**: 
   - Nếu bệnh nhân tồn tại → In mã vạch thành công
   - Nếu không tồn tại → Hiển thị thông báo lỗi

#### Scenario 2: Load dữ liệu từ nguồn bên ngoài (Nutri)
1. **Login** vào hệ thống Genie
2. **Mở menu** "Tiếp nhận" → "Tiếp nhận mới"
3. **Nhập thông tin** bệnh nhân từ nguồn bên ngoài (Nutri, etc.)
4. **Hệ thống tự động** gọi API `ws_MDM_Patient_CheckExists` để kiểm tra
5. **Kết quả**:
   - Nếu bệnh nhân tồn tại → Load dữ liệu từ hệ thống nội bộ
   - Nếu không tồn tại → Tạo bệnh nhân mới và load dữ liệu từ nguồn bên ngoài

#### Scenario 3: Tìm kiếm bệnh nhân (Search Patient)
1. **Login** vào hệ thống Genie
2. **Mở menu** "Tiếp nhận" → "Tiếp nhận mới"
3. **Nhập mã bệnh nhân** vào ô tìm kiếm
4. **Hệ thống tự động** gọi API `ws_MDM_Patient_CheckExists` để validate
5. **Kết quả**:
   - Nếu bệnh nhân tồn tại → Load thông tin bệnh nhân
   - Nếu không tồn tại → Hiển thị thông báo không tìm thấy

#### Scenario 4: Scan mã vạch bệnh nhân
1. **Login** vào hệ thống Genie
2. **Mở menu** "Tiếp nhận" → "Tiếp nhận mới"
3. **Scan mã vạch** bệnh nhân bằng máy quét
4. **Hệ thống tự động** gọi API `ws_MDM_Patient_CheckExists` để validate
5. **Kết quả**:
   - Nếu bệnh nhân tồn tại → Load thông tin bệnh nhân
   - Nếu không tồn tại → Hiển thị thông báo lỗi

#### Scenario 5: Lưu thông tin bệnh nhân (Save Patient)
1. **Login** vào hệ thống Genie
2. **Mở menu** "Tiếp nhận" → "Tiếp nhận mới"
3. **Nhập thông tin** bệnh nhân mới
4. **Bấm nút "Lưu"** → Hệ thống có thể gọi API `ws_MDM_Patient_CheckExists` để validate
5. **Kết quả**:
   - Nếu bệnh nhân chưa tồn tại → Lưu thông tin mới
   - Nếu đã tồn tại → Hiển thị thông báo trùng lặp

## Thông tin API

### Request
```typescript
{
  facID: string;                    // Mã cơ sở y tế
  patientID?: string;              // Mã bệnh nhân (optional)
  patientHospitalID?: string;      // Mã bệnh nhân tại bệnh viện (optional)
  IsGETPatientInfor?: boolean;     // Có lấy thông tin bệnh nhân không (optional)
  IscheckFacID?: boolean;          // Có kiểm tra facID không (optional)
}
```

### Response
```typescript
{
  dataRsp: {
    data: {
      table: [
        {
          isTonTai: boolean;        // true/false - bệnh nhân có tồn tại không
          patientID?: string;       // Mã bệnh nhân (nếu có)
          patientName?: string;     // Tên bệnh nhân (nếu có)
          // ... other patient fields if IsGETPatientInfor = true
        }
      ]
    }
  }
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
      "command": "ws_MDM_Patient_CheckExists",
      "parameters": {
        "FacID": "FAC001",
        "PatientID": "PAT123456",
        "PatientHospitalID": "HOSP789",
        "IsGETPatientInfor": false,
        "IscheckFacID": false
      }
    }
  ]'
```

## Chi tiết kết quả

### 1. Service Definition
- **File**: `app/lib/services/patient.ts`
- **Line**: `1022`
- **Function**: `fetch_ws_MDM_Patient_CheckExists`
- **Mục đích**: API wrapper function cho backend procedure
- **Parameters**:
  ```typescript
  {
    facID: string;
    patientID?: string;
    patientHospitalID?: string | true;
    IsGETPatientInfor?: boolean | true;
    IscheckFacID?: boolean;
  }
  ```

### 2. Direct Usage - Print Barcode
- **File**: `app/(main)/tiep-nhan/tiep-nhan-moi/page.tsx`
- **Line**: `737`
- **Function**: `handlePrintBarcode`
- **Context**: Check patient exists before printing barcode
- **Trigger**: Nút "In mã vạch" hoặc phím tắt F3
- **Code snippet**:
  ```typescript
  const rspCheckPatient = await fetch_ws_MDM_Patient_CheckExists({
    facID,
    patientID: selectedPatient.patientID,
  });
  ```

### 3. Service Layer Usage - External Data Loading
- **File**: `app/lib/services/admissionBusiness.ts`
- **Line**: `211`
- **Function**: `checkPatientExists`
- **Mục đích**: Check patient exists for external data loading
- **Code snippet**:
  ```typescript
  const checkPatientExists = async (
    facID: string,
    patientHospital: string,
  ): Promise<boolean> => {
    try {
      return (
        await PatientService.fetch_ws_MDM_Patient_CheckExists({
          facID: facID,
          patientHospitalID: patientHospital,
          IsGETPatientInfor: false,
          IscheckFacID: false,
        })
      ).dataRsp.data.table?.[0]?.isTonTai;
    } catch {
      return false;
    }
  };
  ```

### 4. Indirect Usage - Search Patient (Multiple Locations)
- **File**: `app/lib/services/admissionBusiness.ts`
- **Line**: `316`
- **Function**: `SearchPatient`
- **Context**: Called from multiple places in the application
- **Trigger**: Tìm kiếm bệnh nhân, scan barcode, load patient data
- **Usage Locations**:
  - **Line 640**: Direct search by patient hospital ID
  - **Line 924**: Search from external source (Nutri, etc.)
  - **Multiple UI components**: Search modals, patient information forms

### 5. Indirect Usage - Load Data from External Sources
- **File**: `app/lib/services/admissionBusiness.ts`
- **Line**: `242`
- **Function**: `loadDataFromExternalSources`
- **Context**: Called from SearchPatient function
- **Trigger**: Khi load dữ liệu từ nguồn bên ngoài (Nutri)
- **Logic**: 
  ```typescript
  if (
    dongbobenhnhantuNutri?.toUpperCase() === "Y" &&
    !(await checkPatientExists(facID, patientHospital))
  ) {
    // Show confirmation dialog to load from Nutri
  }
  ```

### 6. UI Components và Buttons liên quan

#### Nút "In mã vạch"
- **File**: `app/(main)/tiep-nhan/tiep-nhan-moi/page.tsx`
- **Line**: `1531`
- **Trigger**: Click button hoặc phím tắt F3
- **Action**: Gọi `handlePrintBarcode` → API `ws_MDM_Patient_CheckExists`

#### Checkbox "In mã vạch"
- **File**: `app/(main)/tiep-nhan/tiep-nhan-moi/floorSettingUI.tsx`
- **Line**: `118`
- **Trigger**: Tự động in mã vạch khi lưu
- **Action**: Gọi `handlePrintBarcode` → API `ws_MDM_Patient_CheckExists`

#### Search Patient Input
- **File**: `app/(main)/tiep-nhan/tiep-nhan-moi/patient-information.tsx`
- **Line**: `580, 637`
- **Trigger**: Nhập mã bệnh nhân để tìm kiếm
- **Action**: Gọi `SearchPatient` → `loadDataFromExternalSources` → API `ws_MDM_Patient_CheckExists`

#### Scan Barcode Input
- **File**: `app/(main)/tiep-nhan/tiep-nhan-moi/patient-information.tsx`
- **Line**: `1024`
- **Trigger**: Scan mã vạch bệnh nhân
- **Action**: Gọi `SearchPatient` → `loadDataFromExternalSources` → API `ws_MDM_Patient_CheckExists`

## Kết luận
API `ws_MDM_Patient_CheckExists` được sử dụng rộng rãi trong hệ thống Genie với **5-6 nơi sử dụng chính**:

1. **Service Definition** (1 nơi)
2. **Direct Usage - Print Barcode** (1 nơi)
3. **Service Layer - External Data Loading** (1 nơi)
4. **Indirect Usage - Search Patient** (2-3 nơi thông qua SearchPatient function)
5. **UI Components** (nhiều nút và input fields)

API này đóng vai trò quan trọng trong việc validation bệnh nhân trước khi thực hiện các thao tác như in mã vạch, load dữ liệu từ nguồn bên ngoài, và tìm kiếm bệnh nhân.

## Ghi chú
- API này là backend procedure được wrap thành frontend service
- Có sử dụng TypeScript types để đảm bảo type safety
- Error handling được implement thông qua `checkResponse` utility
- Pattern sử dụng nhất quán trong toàn bộ codebase
- File README_FOUND.md được tạo trong cùng thư mục với file API documentation
- **Lý do thiếu trong báo cáo ban đầu**: Chỉ tập trung vào 3 nơi gọi trực tiếp, bỏ sót các nơi gọi gián tiếp thông qua SearchPatient function và các UI components

---
*Tài liệu được tạo tự động từ kết quả tìm kiếm API Usage*
