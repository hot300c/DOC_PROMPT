# Hướng dẫn tìm kiếm API Usage trong Genie Frontend

## Mục đích
Tài liệu này hướng dẫn cách tìm kiếm và kiểm tra nơi gọi API trong dự án Genie Frontend (React/Next.js).

## ⚡ QUY TẮC QUAN TRỌNG: SỬ DỤNG TÀI LIỆU TỔNG QUAN

**TRƯỚC KHI BẮT ĐẦU TÌM KIẾM API, LUÔN ĐỌC TÀI LIỆU TỔNG QUAN:**
- **File**: `DOCS_PROMPT/FE-genie/GENIE_CODEBASE_OVERVIEW.md`
- **Mục đích**: Hiểu nhanh cấu trúc toàn bộ codebase để tìm kiếm hiệu quả
- **Lợi ích**: 
  - Không cần quét lại từ đầu mỗi lần
  - Biết chính xác nơi tìm kiếm
  - Hiểu pattern sử dụng chung
  - Tiết kiệm thời gian tìm kiếm

**QUY TRÌNH TÌM KIẾM TỐI ƯU:**
1. ✅ **Đọc GENIE_CODEBASE_OVERVIEW.md** (5 phút)
2. ✅ **Xác định API cần tìm** (1 phút)  
3. ✅ **Áp dụng search strategy** từ tài liệu tổng quan (10-15 phút)
4. ✅ **Tạo báo cáo README_FOUND.md** (5 phút)

**TỔNG THỜI GIAN**: ~25 phút thay vì 1-2 giờ như trước!

## Phạm vi tìm kiếm
**Chỉ tìm kiếm trong project Genie**: `C:\PROJECTS\genie`
- Không bao gồm các project khác như aladdin, qas-app, qas-db, etc.
- Tập trung vào codebase React/Next.js của Genie Frontend
- KHÔNG bỏ sót các nơi gọi gián tiếp gọi API đó
- Phân tích đầy đủ các UI components và buttons
- Để làm sao quét hết mọi trường hợp mà có thể hay nghi vấn gọi vào API đó.

## Các bước thực hiện

### Bước 0: ⚡ ĐỌC TÀI LIỆU TỔNG QUAN (BẮT BUỘC)
- **File**: `DOCS_PROMPT/FE-genie/GENIE_CODEBASE_OVERVIEW.md`
- **Thời gian**: 5 phút
- **Mục đích**: 
  - Hiểu cấu trúc toàn bộ codebase
  - Nắm vững service patterns và component patterns
  - Biết chính xác nơi tìm kiếm
  - Hiểu common import patterns và business logic locations

### Bước 1: Xác định tên API cần tìm
- Ghi nhớ chính xác tên API (ví dụ: `ws_MDM_Patient_CheckExists`)
- Xác định loại API: Backend procedure, Frontend service, hoặc cả hai

### Bước 2: Tìm kiếm trong toàn bộ codebase

#### 2.1. Tìm kiếm chính xác tên API
```bash
# Di chuyển vào thư mục Genie project
cd C:\PROJECTS\genie

# Tìm kiếm chính xác tên API
grep -r "ws_MDM_Patient_CheckExists" .

# Hoặc sử dụng ripgrep (nếu có)
rg "ws_MDM_Patient_CheckExists"
```

#### 2.2. Tìm kiếm function call trong Frontend
```bash
# Tìm kiếm function call (thường có prefix fetch_)
grep -r "fetch_ws_MDM_Patient_CheckExists" .

# Tìm kiếm trong TypeScript/TSX files
grep -r "fetch_ws_MDM_Patient_CheckExists" --include="*.ts" --include="*.tsx" .
```

#### 2.3. Tìm kiếm các biến thể và pattern khác
```bash
# Tìm kiếm các phần của tên API (để tránh bỏ sót)
grep -r "Patient_CheckExists" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các function wrapper có thể gọi API này
grep -r "checkPatientExists" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các UI elements có thể liên quan
grep -r "In mã vạch\|Print.*barcode\|Barcode" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các biến thể khác của tên API
grep -r "CheckExists\|check.*exists\|exists.*check" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các import statements có thể liên quan
grep -r "import.*Patient.*Check\|import.*check.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các destructuring assignments
grep -r "fetch_.*CheckExists\|CheckExists.*fetch_" --include="*.ts" --include="*.tsx" .
```

#### 2.4. Tìm kiếm các nơi gọi gián tiếp và business logic
```bash
# Tìm kiếm các business functions có thể gọi API
grep -r "SearchPatient\|loadDataFromExternalSources\|handleEventSaveData" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các event handlers có thể trigger API
grep -r "handlePrintBarcode\|handleSave\|handleSearch\|handleScan" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các useEffect và event listeners
grep -r "useEffect.*patient\|addEventListener.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các async functions có thể gọi API
grep -r "async.*patient\|await.*patient" --include="*.ts" --include="*.tsx" .
```

#### 2.5. Tìm kiếm các UI components và event triggers
```bash
# Tìm kiếm các buttons và inputs có thể trigger API
grep -r "onClick.*patient\|onSubmit.*patient\|onChange.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các keyboard shortcuts
grep -r "useKeyboardShortcut.*patient\|keyboard.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các form submissions
grep -r "form.*patient\|submit.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các modal và dialog triggers
grep -r "modal.*patient\|dialog.*patient\|popup.*patient" --include="*.ts" --include="*.tsx" .
```

#### 2.6. Tìm kiếm các Redux actions và state management
```bash
# Tìm kiếm các Redux actions có thể gọi API
grep -r "dispatch.*patient\|action.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các Redux selectors và state
grep -r "useSelector.*patient\|useState.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các Redux slices và reducers
grep -r "slice.*patient\|reducer.*patient" --include="*.ts" --include="*.tsx" .
```

#### 2.7. Tìm kiếm các service calls và HTTP requests
```bash
# Tìm kiếm các HTTP service calls
grep -r "httpService.*patient\|fetch.*patient\|axios.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các API endpoints
grep -r "/api.*patient\|/DataAccess.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các service imports
grep -r "import.*Service.*patient\|import.*service.*patient" --include="*.ts" --include="*.tsx" .
```

#### 2.8. Tìm kiếm các conditional logic và validation
```bash
# Tìm kiếm các conditional checks
grep -r "if.*patient.*exists\|if.*check.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các validation functions
grep -r "validate.*patient\|validation.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các error handling
grep -r "catch.*patient\|error.*patient\|try.*patient" --include="*.ts" --include="*.tsx" .
```

### Bước 3: Phân tích kết quả tìm kiếm

#### 3.1. Các file cần chú ý:
- **Service files**: `app/lib/services/*.ts`
- **Page components**: `app/(main)/*/page.tsx`
- **Component files**: `app/**/*.tsx`
- **Hook files**: `hooks/*.ts`
- **Business logic files**: `app/lib/services/admissionBusiness.ts`

#### 3.2. Các pattern thường gặp:

##### Pattern 1: Service Definition
```typescript
// app/lib/services/patient.ts
export const fetch_ws_MDM_Patient_CheckExists = async ({
  facID,
  patientID,
  // ... other params
}: {
  facID: string;
  patientID?: string;
  // ... other types
}): Promise<ResultResp> => {
  const response = await httpService.post("/DataAccess", [
    {
      category: "QAHosGenericDB",
      command: "ws_MDM_Patient_CheckExists",
      parameters: {
        // ... parameters
      },
    },
  ]);
  return checkResponse(response);
};
```

##### Pattern 2: Direct Usage in Components
```typescript
// app/(main)/tiep-nhan/tiep-nhan-moi/page.tsx
import { fetch_ws_MDM_Patient_CheckExists } from "@/app/lib/services/patient";

const handleSomeAction = async () => {
  const result = await fetch_ws_MDM_Patient_CheckExists({
    facID,
    patientID: selectedPatient.patientID,
  });
  // ... handle result
};
```

##### Pattern 3: Usage through Service Layer
```typescript
// app/lib/services/admissionBusiness.ts
import * as PatientService from "./patient";

const checkPatientExists = async (facID: string, patientHospital: string) => {
  return (
    await PatientService.fetch_ws_MDM_Patient_CheckExists({
      facID: facID,
      patientHospitalID: patientHospital,
      IsGETPatientInfor: false,
      IscheckFacID: false,
    })
  ).dataRsp.data.table?.[0]?.isTonTai;
};
```

##### Pattern 4: Indirect Usage through Business Functions
```typescript
// app/lib/services/admissionBusiness.ts
const loadDataFromExternalSources = async (facID, patientHospital, ...) => {
  if (dongbobenhnhantuNutri?.toUpperCase() === "Y" &&
      !(await checkPatientExists(facID, patientHospital))) {
    // Show confirmation dialog
  }
};

const SearchPatient = async ({ patientHospital, ... }) => {
  const isSuccess = await loadDataFromExternalSources(facID, patientHospital, ...);
  // ... rest of the function
};
```

### Bước 4: Kiểm tra chi tiết từng file

#### 4.1. Đọc file service để hiểu API signature
```bash
# Đọc file service
cat app/lib/services/patient.ts | grep -A 20 "fetch_ws_MDM_Patient_CheckExists"
```

#### 4.2. Đọc file component để hiểu context sử dụng
```bash
# Đọc file page/component
cat app/\(main\)/tiep-nhan/tiep-nhan-moi/page.tsx | grep -A 10 -B 5 "fetch_ws_MDM_Patient_CheckExists"
```

#### 4.3. Tìm kiếm các nơi gọi gián tiếp
```bash
# Tìm kiếm các function có thể gọi API này
grep -r "SearchPatient\|loadDataFromExternalSources" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các UI elements và buttons
grep -r "handlePrintBarcode\|PrintBarcode\|print.*barcode" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các business logic functions
grep -r "BusinessAdmission\|admissionBusiness\|BusinessLogic" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các service layer functions
grep -r "ServiceAdmission\|PatientService\|ServiceLayer" --include="*.ts" --include="*.tsx" .
```

#### 4.4. Phân tích function call chains
```bash
# Tìm kiếm các function calls trong business logic
grep -r "await.*SearchPatient\|await.*loadDataFromExternalSources" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các function exports và imports
grep -r "export.*SearchPatient\|import.*SearchPatient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các function assignments
grep -r "const.*SearchPatient\|let.*SearchPatient\|var.*SearchPatient" --include="*.ts" --include="*.tsx" .
```

#### 4.5. Kiểm tra các hooks và custom hooks
```bash
# Tìm kiếm các custom hooks có thể gọi API
grep -r "use.*Patient\|use.*Check\|use.*Exists" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các useEffect dependencies
grep -r "useEffect.*\[\].*patient\|useEffect.*dependencies.*patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các useCallback và useMemo
grep -r "useCallback.*patient\|useMemo.*patient" --include="*.ts" --include="*.tsx" .
```

#### 4.6. Kiểm tra các context providers và consumers
```bash
# Tìm kiếm các context providers
grep -r "PatientContext\|PatientProvider\|Context.*Patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các context consumers
grep -r "useContext.*Patient\|Consumer.*Patient" --include="*.ts" --include="*.tsx" .

# Tìm kiếm các context values
grep -r "value.*patient\|context.*patient" --include="*.ts" --include="*.tsx" .
```

### Bước 5: Tạo báo cáo tổng hợp

#### 5.1. Cấu trúc báo cáo:
```markdown
## API: ws_MDM_Patient_CheckExists

### Frontend Genie (React/Next.js):

1. **Service Definition**
   - File: `app/lib/services/patient.ts`
   - Function: `fetch_ws_MDM_Patient_CheckExists`
   - Purpose: API wrapper function

2. **Direct Usage**
   - File: `app/(main)/tiep-nhan/tiep-nhan-moi/page.tsx`
   - Line: 737
   - Purpose: Check patient exists before printing barcode

3. **Service Layer Usage**
   - File: `app/lib/services/admissionBusiness.ts`
   - Line: 211
   - Purpose: Check patient exists for external data loading

4. **Indirect Usage**
   - File: `app/lib/services/admissionBusiness.ts`
   - Line: 316, 242
   - Purpose: Called from SearchPatient and loadDataFromExternalSources

5. **UI Components**
   - Buttons, inputs, and other UI elements that trigger API calls

### Backend (.NET):
- Handler: `aladdin/WebService.Handlers/QAHosGenericDB/ws_MDM_Patient_CheckExists.cs`
- Tests: `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_MDM_Patient_CheckExists_Test.cs`
- Database: `qas-db/QAHosGenericDB/Procedures/ws_MDM_Patient_CheckExists.sql`
```

## Công cụ hỗ trợ

### 1. IDE Search Tools
- **VS Code**: Ctrl+Shift+F (Find in Files)
- **WebStorm**: Ctrl+Shift+F (Find in Files)
- **Vim/Neovim**: `:grep` command

### 2. Command Line Tools
```bash
# Di chuyển vào thư mục Genie project trước
cd C:\PROJECTS\genie

# Grep với context
grep -r -A 5 -B 5 "API_NAME" .

# Tìm kiếm trong specific file types
find . -name "*.ts" -o -name "*.tsx" | xargs grep "API_NAME"

# Tìm kiếm với regex
grep -r -E "fetch_.*API_NAME" .

# Tìm kiếm các biến thể
grep -r "API_NAME_PART" --include="*.ts" --include="*.tsx" .
```

### 3. Git Search
```bash
# Di chuyển vào thư mục Genie project trước
cd C:\PROJECTS\genie

# Tìm kiếm trong git history
git grep "API_NAME"

# Tìm kiếm với context
git grep -A 5 -B 5 "API_NAME"
```

## Best Practices

### 0. ⚡ SỬ DỤNG TÀI LIỆU TỔNG QUAN (BẮT BUỘC)
- **LUÔN ĐỌC**: `GENIE_CODEBASE_OVERVIEW.md` trước khi bắt đầu
- **Hiểu cấu trúc**: App directory, service patterns, component patterns
- **Nắm vững**: Common import patterns, business logic locations
- **Tiết kiệm thời gian**: Không cần quét lại từ đầu mỗi lần

### 1. Tìm kiếm có hệ thống
- Bắt đầu với tên chính xác của API
- Tìm kiếm function wrapper (thường có prefix `fetch_`)
- Kiểm tra import statements
- Tìm kiếm trong service layer
- **QUAN TRỌNG**: Tìm kiếm các nơi gọi gián tiếp thông qua business functions
- **QUAN TRỌNG**: Tìm kiếm các UI elements và buttons có thể trigger API calls

### 2. Ghi chép kết quả
- Lưu lại đường dẫn file
- Ghi chú line number
- Mô tả mục đích sử dụng
- Phân loại theo loại usage (direct, service layer, indirect, UI components)
- **QUAN TRỌNG**: Ghi chép cả các nơi gọi gián tiếp

### 3. Verify kết quả
- Đọc code context để hiểu rõ cách sử dụng
- Kiểm tra parameters được truyền vào
- Xác nhận mục đích sử dụng
- **QUAN TRỌNG**: Kiểm tra các function chain để tìm nơi gọi gián tiếp

### 4. Phân tích toàn diện
- **QUAN TRỌNG**: Không chỉ tìm kiếm direct calls mà còn indirect calls
- **QUAN TRỌNG**: Tìm kiếm các UI components và buttons
- **QUAN TRỌNG**: Phân tích business logic functions
- **QUAN TRỌNG**: Kiểm tra các pattern sử dụng khác nhau
- **QUAN TRỌNG**: Phân tích function call chains
- **QUAN TRỌNG**: Kiểm tra các hooks và custom hooks
- **QUAN TRỌNG**: Tìm kiếm các context providers và consumers
- **QUAN TRỌNG**: Kiểm tra các Redux actions và state management
- **QUAN TRỌNG**: Tìm kiếm các conditional logic và validation
- **QUAN TRỌNG**: Phân tích các event handlers và triggers

## Ví dụ thực tế: ws_MDM_Patient_CheckExists

### Kết quả tìm kiếm:
1. **Service Definition**: `app/lib/services/patient.ts:1022`
2. **Direct Usage**: `app/(main)/tiep-nhan/tiep-nhan-moi/page.tsx:737`
3. **Service Layer**: `app/lib/services/admissionBusiness.ts:211`
4. **Indirect Usage**: `app/lib/services/admissionBusiness.ts:316, 242`
5. **UI Components**: Multiple buttons and inputs

### Mục đích sử dụng:
- ✅ Kiểm tra bệnh nhân tồn tại trước khi in mã vạch
- ✅ Validation trong quá trình load dữ liệu từ nguồn bên ngoài
- ✅ Quyết định có tải dữ liệu từ Nutri hay không
- ✅ Validate trong quá trình tìm kiếm bệnh nhân
- ✅ Validate khi scan barcode

### Bài học rút ra:
- **QUAN TRỌNG**: API có thể được gọi từ nhiều nơi khác nhau (5-6 nơi)
- **QUAN TRỌNG**: Cần tìm kiếm cả direct và indirect usage
- **QUAN TRỌNG**: UI components cũng có thể trigger API calls
- **QUAN TRỌNG**: Business logic functions có thể wrap API calls

## Lưu ý quan trọng

1. **Naming Convention**: API trong Genie thường có prefix `fetch_` khi được wrap thành service function
2. **File Structure**: Services thường nằm trong `app/lib/services/`
3. **Import Pattern**: Thường import từ service layer thay vì gọi trực tiếp
4. **Error Handling**: Kiểm tra cách xử lý lỗi trong từng usage
5. **Type Safety**: Chú ý TypeScript types và interfaces
6. **QUAN TRỌNG**: Business logic thường được tách riêng trong `admissionBusiness.ts`
7. **QUAN TRỌNG**: UI components có thể trigger API calls thông qua event handlers
8. **QUAN TRỌNG**: Cần phân tích function chain để tìm tất cả usage points

## Troubleshooting

### Nếu không tìm thấy kết quả:
1. Đảm bảo đang ở đúng thư mục `C:\PROJECTS\genie`
2. Kiểm tra spelling của API name
3. Tìm kiếm với pattern khác (ví dụ: không có prefix `fetch_`)
4. Tìm kiếm trong git history
5. Kiểm tra trong các file config hoặc constants
6. **QUAN TRỌNG**: Tìm kiếm các biến thể của tên API
7. **QUAN TRỌNG**: Tìm kiếm trong business logic files

### Nếu có quá nhiều kết quả:
1. Filter theo file type cụ thể
2. Tìm kiếm với context lớn hơn
3. Phân loại theo directory structure
4. Sử dụng regex để filter chính xác hơn
5. **QUAN TRỌNG**: Phân loại theo loại usage (direct, indirect, UI)

### Nếu thiếu kết quả:
1. **QUAN TRỌNG**: Kiểm tra các function wrapper
2. **QUAN TRỌNG**: Tìm kiếm trong business logic files
3. **QUAN TRỌNG**: Kiểm tra UI components và event handlers
4. **QUAN TRỌNG**: Phân tích function call chain
5. **QUAN TRỌNG**: Tìm kiếm các pattern sử dụng khác nhau
6. **QUAN TRỌNG**: Kiểm tra các hooks và custom hooks
7. **QUAN TRỌNG**: Tìm kiếm các context providers và consumers
8. **QUAN TRỌNG**: Kiểm tra các Redux actions và state management
9. **QUAN TRỌNG**: Tìm kiếm các conditional logic và validation
10. **QUAN TRỌNG**: Phân tích các event handlers và triggers
11. **QUAN TRỌNG**: Kiểm tra các service layer functions
12. **QUAN TRỌNG**: Tìm kiếm các HTTP service calls
13. **QUAN TRỌNG**: Kiểm tra các keyboard shortcuts và form submissions
14. **QUAN TRỌNG**: Tìm kiếm các modal và dialog triggers
15. **QUAN TRỌNG**: Phân tích các useEffect dependencies

### ⚡ NẾU VẪN KHÔNG TÌM THẤY:
1. **ĐỌC LẠI**: `GENIE_CODEBASE_OVERVIEW.md` để hiểu sâu hơn
2. **Kiểm tra**: Có bỏ sót pattern nào không
3. **Tìm kiếm**: Trong các file tương tự (ví dụ: cùng module)
4. **Phân tích**: Business logic flow để tìm nơi gọi gián tiếp

## Bước 6: Tạo tài liệu README_FOUND.md

Sau khi hoàn thành việc tìm kiếm và phân tích, tạo file `README_FOUND.md` để lưu trữ kết quả tìm kiếm.

### 6.1. Tạo file README_FOUND.md
```bash
# Di chuyển vào thư mục chứa file API documentation
# Ví dụ: nếu có file ws_MDM_Patient_CheckExists.md trong thư mục DOCS_PROMPT/FE-genie/
cd C:\PROJECTS\DOCS_PROMPT\FE-genie

# Tạo file README_FOUND.md trong cùng thư mục
touch README_FOUND.md
# Hoặc tạo file với tên cụ thể: README_FOUND_ws_MDM_Patient_CheckExists.md
```

### 6.2. Cấu trúc nội dung README_FOUND.md

```markdown
# Kết quả tìm kiếm API Usage - Genie Frontend

## Thông tin tìm kiếm
- **API Name**: `ws_MDM_Patient_CheckExists`
- **Ngày tìm kiếm**: `2024-01-15`
- **Người thực hiện**: `phucnnd`
- **Project**: `Genie Frontend (React/Next.js)`

## Tổng quan kết quả
- **Tổng số file tìm thấy**: `[SỐ] files`
- **Tổng số nơi sử dụng**: `[SỐ] nơi` (bao gồm cả các nơi gọi gián tiếp)
- **Loại usage**: Service Definition, Direct Usage, Service Layer, Indirect Usage, UI Components
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong

## Phân tích sử dụng

### Mục đích chính
1. ✅ **Validation**: Kiểm tra bệnh nhân tồn tại trước khi thực hiện các thao tác
2. ✅ **Data Loading**: Quyết định có tải dữ liệu từ nguồn bên ngoài hay không
3. ✅ **Barcode Printing**: Validate trước khi in mã vạch bệnh nhân
4. ✅ **Patient Search**: Validate trong quá trình tìm kiếm bệnh nhân
5. ✅ **External Data Sync**: Kiểm tra trước khi đồng bộ dữ liệu từ nguồn bên ngoài

### Pattern sử dụng
- **Service Layer Pattern**: API được wrap trong service function với prefix `fetch_`
- **Import Pattern**: Import từ service layer thay vì gọi trực tiếp
- **Error Handling**: Sử dụng `checkResponse` utility để xử lý lỗi
- **Type Safety**: Có TypeScript types và interfaces đầy đủ
- **Business Logic Pattern**: API được sử dụng trong business logic functions
- **UI Component Pattern**: API được trigger từ UI components và event handlers

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

#### Scenario 2: Load dữ liệu từ nguồn bên ngoài
1. **Login** vào hệ thống Genie
2. **Mở menu** "Tiếp nhận" → "Tiếp nhận mới"
3. **Nhập thông tin** bệnh nhân từ nguồn bên ngoài (Nutri, etc.)
4. **Hệ thống tự động** gọi API `ws_MDM_Patient_CheckExists` để kiểm tra
5. **Kết quả**:
   - Nếu bệnh nhân tồn tại → Load dữ liệu từ hệ thống nội bộ
   - Nếu không tồn tại → Tạo bệnh nhân mới và load dữ liệu từ nguồn bên ngoài

#### Scenario 3: Tìm kiếm bệnh nhân
1. **Login** vào hệ thống Genie
2. **Mở menu** "Tiếp nhận" → "Tiếp nhận mới"
3. **Nhập mã bệnh nhân** vào ô tìm kiếm
4. **Hệ thống tự động** gọi API `ws_MDM_Patient_CheckExists` để validate
5. **Kết quả**:
   - Nếu bệnh nhân tồn tại → Load thông tin bệnh nhân
   - Nếu không tồn tại → Hiển thị thông báo không tìm thấy

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
- **Parameters**: [Chi tiết parameters]

### 2. Direct Usage
- **File**: `app/(main)/tiep-nhan/tiep-nhan-moi/page.tsx`
- **Line**: `737`
- **Function**: `handlePrintBarcode`
- **Context**: Check patient exists before printing barcode
- **Trigger**: Nút "In mã vạch" hoặc phím tắt F3
- **Code snippet**: [Code snippet]

### 3. Service Layer Usage
- **File**: `app/lib/services/admissionBusiness.ts`
- **Line**: `211`
- **Function**: `checkPatientExists`
- **Mục đích**: Check patient exists for external data loading
- **Code snippet**: [Code snippet]

### 4. Indirect Usage
- **File**: `app/lib/services/admissionBusiness.ts`
- **Line**: `316, 242`
- **Function**: `SearchPatient`, `loadDataFromExternalSources`
- **Context**: Called from multiple places in the application
- **Trigger**: Tìm kiếm bệnh nhân, scan barcode, load patient data
- **Usage Locations**: [Chi tiết các nơi gọi]

### 5. UI Components và Buttons liên quan
- **Nút "In mã vạch"**: [Chi tiết]
- **Checkbox "In mã vạch"**: [Chi tiết]
- **Search Patient Input**: [Chi tiết]
- **Scan Barcode Input**: [Chi tiết]

## Kết luận
API `[TÊN_API]` được sử dụng rộng rãi trong hệ thống Genie với **[SỐ] nơi sử dụng chính**:

1. **Service Definition** (1 nơi)
2. **Direct Usage** (X nơi)
3. **Service Layer** (X nơi)
4. **Indirect Usage** (X nơi thông qua business functions)
5. **UI Components** (nhiều nút và input fields)

API này đóng vai trò quan trọng trong việc [mô tả vai trò].

## Ghi chú
- API này là backend procedure được wrap thành frontend service
- Có sử dụng TypeScript types để đảm bảo type safety
- Error handling được implement thông qua `checkResponse` utility
- Pattern sử dụng nhất quán trong toàn bộ codebase
- File README_FOUND.md được tạo trong cùng thư mục với file API documentation
- **Lý do thiếu trong báo cáo ban đầu**: [Giải thích nếu có thiếu sót]

---
*Tài liệu được tạo tự động từ kết quả tìm kiếm API Usage*
```

### 6.3. Template cho các API khác

Để tái sử dụng, có thể tạo template:

```markdown
# Kết quả tìm kiếm API Usage - Genie Frontend

## Thông tin tìm kiếm
- **API Name**: `[TÊN_API]`
- **Ngày tìm kiếm**: `[YYYY-MM-DD]`
- **Người thực hiện**: `[TÊN]`
- **Project**: `Genie Frontend (React/Next.js)`

## Tổng quan kết quả
- **Tổng số file tìm thấy**: `[SỐ] files`
- **Tổng số nơi sử dụng**: `[SỐ] nơi` (bao gồm cả các nơi gọi gián tiếp)
- **Loại usage**: [Liệt kê các loại]
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong

## Phân tích sử dụng

### Mục đích chính
1. [Mục đích 1]
2. [Mục đích 2]
3. [Mục đích 3]
4. [Mục đích 4]
5. [Mục đích 5]

### Pattern sử dụng
- [Mô tả pattern]

### User Journey & Testing Scenarios

#### Scenario 1: [Tên scenario]
1. **Login** vào hệ thống Genie
2. **Mở menu** [đường dẫn menu]
3. **[Hành động]** [mô tả hành động]
4. **[Hành động]** [mô tả hành động]
5. **[Hành động]** → API `[TÊN_API]` được gọi
6. **Kết quả**: 
   - [Kết quả thành công]
   - [Kết quả thất bại]

#### Scenario 2: [Tên scenario]
1. **Login** vào hệ thống Genie
2. **Mở menu** [đường dẫn menu]
3. **[Hành động]** [mô tả hành động]
4. **[Hành động]** [mô tả hành động]
5. **Kết quả**:
   - [Kết quả 1]
   - [Kết quả 2]

#### Scenario 3: [Tên scenario]
1. **Login** vào hệ thống Genie
2. **Mở menu** [đường dẫn menu]
3. **[Hành động]** [mô tả hành động]
4. **[Hành động]** [mô tả hành động]
5. **Kết quả**:
   - [Kết quả 1]
   - [Kết quả 2]

## Thông tin API

### Request
```typescript
{
  [field1]: [type];                 // [Mô tả field1]
  [field2]?: [type];               // [Mô tả field2] (optional)
  [field3]?: [type];               // [Mô tả field3] (optional)
  // ... other fields
}
```

### Response
```typescript
{
  [responseStructure]: {
    [data]: {
      [table]: [
        {
          [field1]: [type];         // [Mô tả field1]
          [field2]?: [type];        // [Mô tả field2] (optional)
          // ... other response fields
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
      "category": "[CATEGORY]",
      "command": "[TÊN_API]",
      "parameters": {
        "[param1]": "[value1]",
        "[param2]": "[value2]",
        "[param3]": [value3]
      }
    }
  ]'
```

## Chi tiết kết quả

### 1. [Loại Usage 1]
- **File**: `[đường dẫn file]`
- **Line**: `[số dòng]`
- **Function**: `[tên function]`
- **Mục đích**: [mô tả mục đích]
- **Parameters**: [nếu có]

### 2. [Loại Usage 2]
- **File**: `[đường dẫn file]`
- **Line**: `[số dòng]`
- **Context**: [mô tả context]
- **Code snippet**: [code nếu cần]

### 3. [Loại Usage 3]
- **File**: `[đường dẫn file]`
- **Line**: `[số dòng]`
- **Function**: `[tên function]`
- **Context**: [mô tả context]
- **Trigger**: [mô tả trigger]

### 4. [Loại Usage 4]
- **File**: `[đường dẫn file]`
- **Line**: `[số dòng]`
- **Function**: `[tên function]`
- **Context**: [mô tả context]
- **Logic**: [mô tả logic]

### 5. UI Components và Buttons liên quan
- **[Tên component]**: [Chi tiết]
- **[Tên component]**: [Chi tiết]
- **[Tên component]**: [Chi tiết]

## Kết luận
API `[TÊN_API]` được sử dụng rộng rãi trong hệ thống Genie với **[SỐ] nơi sử dụng chính**:

1. **Service Definition** (1 nơi)
2. **Direct Usage** (X nơi)
3. **Service Layer** (X nơi)
4. **Indirect Usage** (X nơi thông qua business functions)
5. **UI Components** (nhiều nút và input fields)

API này đóng vai trò quan trọng trong việc [mô tả vai trò].

## Ghi chú
- [Ghi chú quan trọng]
- File README_FOUND.md được tạo trong cùng thư mục với file API documentation
- **Lý do thiếu trong báo cáo ban đầu**: [Giải thích nếu có thiếu sót]

---
*Tài liệu được tạo tự động từ kết quả tìm kiếm API Usage*
```

### 6.4. Lưu ý khi tạo README_FOUND.md

1. **Vị trí file**: Tạo file README_FOUND.md trong cùng thư mục với file API documentation
2. **Cập nhật thông tin chính xác**: Đảm bảo tên API, đường dẫn file, line number chính xác
3. **Mô tả rõ ràng**: Giải thích mục đích sử dụng của từng usage
4. **Code snippet**: Chỉ include code quan trọng, không copy toàn bộ file
5. **Phân loại**: Phân loại rõ ràng theo loại usage (Service Definition, Direct Usage, Service Layer, Indirect Usage, UI Components)
6. **User Journey**: Mô tả chi tiết các bước thao tác của người dùng để tester có thể testing
7. **API Information**: Bao gồm đầy đủ Request/Response fields và cURL example để dễ dàng test với Postman
8. **Kết luận**: Tóm tắt ngắn gọn kết quả tìm kiếm
9. **Ghi chú**: Thêm các thông tin quan trọng khác nếu có
10. **QUAN TRỌNG**: Bao gồm cả các nơi gọi gián tiếp và UI components
11. **QUAN TRỌNG**: Ghi chú lý do thiếu sót nếu có trong báo cáo ban đầu
12. **QUAN TRỌNG**: Phân tích toàn diện tất cả các pattern sử dụng

### 6.5. Rule BẮT BUỘC cho User Journey & Testing Scenarios

- **Mức chi tiết yêu cầu cho MỖI flow**:
  - **Đường dẫn màn hình**: Ghi rõ menu → module → màn hình (ví dụ: `Menu → Ngoại trú → Khám bệnh`).
  - **Tiền điều kiện**: ID/Session/Role/Config cần thiết (ví dụ: `PatientID`, `ClinicalSessionID`, quyền User, cơ sở `FacID`).
  - **Bước thao tác UI cụ thể**: Liệt kê theo thứ tự từng click/nhập/chọn, nêu rõ tên nút/label trường nhập, và phím tắt (nếu có).
  - **Thời điểm API được gọi**: Nêu rõ hành động nào trigger API, và (nếu xác định) function/hook gọi (ví dụ: `useChiDinhVaccine → ws_Vaccine_ThongBaoKhongchan`).
  - **Kỳ vọng hiển thị**: Modal/Dialog/Toast nào xuất hiện, nội dung message chính, icon trạng thái, và hành vi khi đóng.
  - **Nhánh quyết định**: Nếu có confirm, mô tả nhánh A/B (Đồng ý/Từ chối) và luồng tiếp theo (API phụ được gọi gì).
  - **Kết quả dữ liệu**: Ghi rõ field chính trong response được sử dụng (ví dụ: `data.table[0].mess`, `IsBlock`...).
  - **Dữ liệu mẫu**: Cung cấp input mẫu để tester tái hiện (ID, mã bệnh nhân, thông số form...).
  - **Negative cases**: Thiếu dữ liệu, quyền không đủ, timeout/network error, 4xx/5xx, dữ liệu biên; nêu kỳ vọng UI tương ứng.
  - **Mapping UI → Code**: Đường dẫn component/hook/service và handler (nếu xác định được).

- **Số lượng flow tối thiểu**: 2–3 flow đại diện các màn hình chính có liên quan đến API (ví dụ: flow tại màn hình A, flow tại dialog B, flow thao tác bằng hotkey).

- **Mini-template bắt buộc cho mỗi flow**:
```markdown
#### Flow [Tên flow/ngữ cảnh]
- **Đường dẫn màn hình**: [Menu → Module → Màn hình]
- **Tiền điều kiện**: [IDs/Role/Config/...]
- **Bước thao tác**:
  1) [Click nút "..."]
  2) [Nhập trường "...": giá trị]
  3) [Chọn dropdown "..."]
  4) [Phím tắt nếu có]
- **Trigger API**: `[TÊN_API]` (tại [tên function/hook] nếu biết)
- **Kỳ vọng UI**: [Dialog/Toast/Message], [nội dung chính], [hành vi]
- **Nhánh quyết định**:
  - A) [Hành động], tiếp tục → [API phụ/luồng tiếp]
  - B) [Hành động], dừng → [trạng thái]
- **Kết quả dữ liệu**: [field chính từ response và cách sử dụng]
- **Dữ liệu mẫu**: [ví dụ input]
- **Mapping UI → Code**: [`app/.../Component.tsx` → `handleXxx`; `app/lib/services/...ts` → `fetch_ws_...`]
```

### 6.6. Definition of Done (DoD) cho README_FOUND.md

- **Bắt buộc đạt tất cả**:
  - Có tối thiểu 2 flow User Journey theo mini-template ở trên, mỗi flow đầy đủ 10 mục.
  - Chỉ rõ ít nhất 1 vị trí Mapping UI → Code cho mỗi flow (nếu không xác định được, phải nêu lý do và hướng dẫn tìm tiếp).
  - Liệt kê Negative cases tối thiểu 3 tình huống và kỳ vọng UI tương ứng.
  - Có cURL mẫu và Request/Response mẫu để test nhanh.
  - Tổng hợp “Mục đích chính” và “Pattern sử dụng” ngắn gọn, bám sát usage thực tế.
  - Checklist cuối tài liệu được tick đủ cho API đang xét.

## Kết luận

Hướng dẫn này đã được cập nhật với những kinh nghiệm thực tế từ việc tìm kiếm API `ws_MDM_Patient_CheckExists`. Những điểm quan trọng cần lưu ý:

1. **Tìm kiếm toàn diện**: Không chỉ tìm direct calls mà còn indirect calls
2. **Phân tích business logic**: Kiểm tra các business functions
3. **UI Components**: Tìm kiếm các buttons và inputs có thể trigger API
4. **Function chains**: Phân tích chuỗi gọi function
5. **Pattern variations**: Tìm kiếm các biến thể của tên API
6. **Documentation**: Ghi chép đầy đủ tất cả các nơi sử dụng
7. **Hooks và Context**: Kiểm tra các React hooks và context providers
8. **Redux và State Management**: Tìm kiếm trong Redux actions và state
9. **Event Handlers**: Phân tích các event handlers và triggers
10. **Service Layer**: Kiểm tra các service layer functions
11. **Conditional Logic**: Tìm kiếm các conditional checks và validation
12. **HTTP Requests**: Phân tích các HTTP service calls
13. **Form Submissions**: Kiểm tra các form submissions và keyboard shortcuts
14. **Modal và Dialog**: Tìm kiếm các modal và dialog triggers
15. **useEffect Dependencies**: Phân tích các useEffect dependencies

### Checklist hoàn chỉnh để quét hết mọi trường hợp:

#### ✅ **Direct API Calls**
- [ ] Tìm kiếm chính xác tên API
- [ ] Tìm kiếm function wrapper với prefix `fetch_`
- [ ] Kiểm tra import statements
- [ ] Tìm kiếm destructuring assignments

#### ✅ **Indirect API Calls**
- [ ] Phân tích business logic functions
- [ ] Kiểm tra service layer functions
- [ ] Tìm kiếm function call chains
- [ ] Phân tích async/await patterns

#### ✅ **UI Components và Event Triggers**
- [ ] Tìm kiếm buttons và inputs
- [ ] Kiểm tra event handlers (onClick, onSubmit, onChange)
- [ ] Tìm kiếm keyboard shortcuts
- [ ] Phân tích form submissions
- [ ] Kiểm tra modal và dialog triggers

#### ✅ **React Patterns**
- [ ] Kiểm tra các hooks (useEffect, useCallback, useMemo)
- [ ] Tìm kiếm custom hooks
- [ ] Phân tích context providers và consumers
- [ ] Kiểm tra useEffect dependencies

#### ✅ **State Management**
- [ ] Tìm kiếm Redux actions và dispatches
- [ ] Kiểm tra Redux selectors và state
- [ ] Phân tích Redux slices và reducers
- [ ] Tìm kiếm state updates

#### ✅ **Service và HTTP**
- [ ] Kiểm tra HTTP service calls
- [ ] Tìm kiếm API endpoints
- [ ] Phân tích service imports
- [ ] Kiểm tra error handling

#### ✅ **Validation và Logic**
- [ ] Tìm kiếm conditional checks
- [ ] Kiểm tra validation functions
- [ ] Phân tích error handling patterns
- [ ] Tìm kiếm try-catch blocks

Với checklist này và hướng dẫn chi tiết, việc tìm kiếm API usage sẽ **QUÉT HẾT MỌI TRƯỜNG HỢP** có thể gọi vào API đó.
