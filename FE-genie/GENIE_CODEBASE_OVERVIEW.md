# Genie Frontend Codebase Overview

## 📋 Thông tin chung
- **Project**: Genie Frontend (React/Next.js)
- **Path**: `C:\PROJECTS\genie`
- **Framework**: Next.js 13+ với App Router
- **Language**: TypeScript
- **State Management**: Redux Toolkit + SWR
- **UI Library**: Shadcn/ui + Tailwind CSS
- **Date**: 2024-12-19

## 🏗️ Cấu trúc thư mục chính

### 1. App Directory Structure (Next.js 13+)
```
app/
├── (main)/                    # Main layout routes
│   ├── tiep-nhan/            # Tiếp nhận bệnh nhân
│   ├── ngoai-tru/            # Ngoại trú
│   │   ├── kham-benh/        # Khám bệnh
│   │   ├── do-chi-so-co-the/ # Đo chỉ số cơ thể
│   │   └── theo-doi-phac-do/ # Theo dõi phác đồ
│   ├── noi-tru/              # Nội trú
│   └── bao-cao/              # Báo cáo
├── lib/                       # Shared libraries
│   ├── services/             # API services
│   ├── definitions/          # TypeScript types
│   ├── enums/                # Enums và constants
│   ├── utils/                # Utility functions
│   └── hooks/                # Custom hooks
├── components/                # Shared components
└── redux/                     # Redux store
```

### 2. Service Layer Architecture
```
app/lib/services/
├── patient.ts                 # Patient-related APIs
├── admissionBusiness.ts       # Business logic for admission
├── keVaccinTabServices.ts    # Vaccine-related APIs
├── vaccineService.ts          # Vaccine business logic
├── khamTruocTiemApi.ts       # Pre-vaccination APIs
├── system.ts                  # System utilities
└── saveError.ts              # Error handling
```

### 3. Component Structure
```
app/components/
├── ui/                        # Shadcn/ui components
├── app-permissions/           # Permission components
├── input-date-picker/         # Date picker components
├── select/                    # Select components
└── loading/                   # Loading components
```

## 🔍 API Service Patterns

### 1. Service Function Naming Convention
- **Prefix**: `ws_` (Web Service)
- **Wrapper**: `fetch_ws_` (không phổ biến trong Genie)
- **Direct**: Gọi trực tiếp từ service object

### 2. Common Service Import Patterns
```typescript
// Pattern 1: Import entire service
import * as KeVaccinTabServices from "@/app/lib/services/keVaccinTabServices";

// Pattern 2: Import specific functions
import { ws_Vaccine_KiemTraTuongTac } from "@/app/lib/services/keVaccinTabServices";

// Pattern 3: Import from business logic
import { checkPatientExists } from "@/app/lib/services/admissionBusiness";
```

### 3. API Call Structure
```typescript
const response = await httpService.post("/DataAccess", [
  {
    category: "QAHosGenericDB",           // Database category
    command: "ws_API_NAME",               // Stored procedure name
    parameters: {                          // API parameters
      // ... parameters
    },
  },
]);
return response.data;
```

## 📱 UI Component Patterns

### 1. Page Components
- **Location**: `app/(main)/*/page.tsx`
- **Pattern**: Server components với client components
- **Data Fetching**: SWR hooks

### 2. Tab Components
- **Location**: `app/(main)/*/[patientId]/tabs/*.tsx`
- **Pattern**: TabsContent với DataTable
- **State Management**: Local state + SWR

### 3. Modal/Dialog Components
- **Location**: `app/(main)/*/[patientId]/components/*.tsx`
- **Pattern**: Controlled open/close state
- **Forms**: React Hook Form + validation

### 4. Common UI Elements
```typescript
// Buttons
<Button onClick={handleAction}>Action</Button>

// Checkboxes
<Checkbox onChange={handleChange} />

// Data Tables
<DataTable columns={columns} data={data} />

// Forms
<form onSubmit={handleSubmit}>
  <InputDatePicker />
  <TableSelect />
</form>
```

## 🎣 Hook Patterns

### 1. Custom Hooks Location
```
app/(main)/*/hooks/
├── useChiDinhVaccine.ts      # Vaccine prescription logic
├── useThemPhacDo.ts          # Add protocol logic
├── useEditVaccinRow.ts       # Edit vaccine row logic
└── useTiemNgoai.ts           # External injection logic
```

### 2. Hook Usage Pattern
```typescript
export const useCustomHook = (facId: string) => {
  const { data, mutate } = useSWR(key, fetcher);
  
  const handleAction = async (params) => {
    // Business logic
    await serviceCall(params);
    mutate(); // Refresh data
  };
  
  return { handleAction, data };
};
```

### 3. Context Usage
```typescript
// Medical checkup context
const { parentInfo, isDisabled } = useMedicalCheckup();

// Feedback dialog context
const { alert, confirm, decision } = useFeedbackDialog();
```

## 🔄 State Management

### 1. Redux Store Structure
```
redux/
├── store.ts                   # Store configuration
├── slices/                    # Redux slices
└── selectors/                 # Redux selectors
```

### 2. SWR Usage Patterns
```typescript
// Basic usage
const { data, error, mutate } = useSWR(key, fetcher);

// Conditional fetching
const { data } = useSWR(
  condition ? key : null,
  fetcher
);

// Optimistic updates
await mutate(newData, false);
await serviceCall();
await mutate(); // Refresh from server
```

## 🚀 Business Logic Patterns

### 1. Business Functions Location
- **Primary**: `app/lib/services/admissionBusiness.ts`
- **Vaccine**: `app/lib/services/vaccineService.ts`
- **Patient**: `app/lib/services/patient.ts`

### 2. Business Logic Structure
```typescript
const businessFunction = async (params) => {
  // 1. Validation
  if (!isValid(params)) return;
  
  // 2. API calls
  const result1 = await service1(params);
  const result2 = await service2(params);
  
  // 3. Business logic
  if (result1.success && result2.success) {
    // Process success
  }
  
  // 4. Update UI
  mutate();
};
```

### 3. Transaction Pattern
```typescript
await executeTransaction({
  request: [
    {
      category: "QAHosGenericDB",
      command: "ws_Command1",
      parameters: params1,
    },
    {
      category: "QAHosGenericDB", 
      command: "ws_Command2",
      parameters: params2,
    },
  ],
});
```

## 📊 Data Flow Patterns

### 1. User Action Flow
```
UI Component → Event Handler → Custom Hook → Service Call → API → Response → UI Update
```

### 2. Data Fetching Flow
```
Component Mount → SWR Hook → Service Function → HTTP Request → Response → State Update → Re-render
```

### 3. Error Handling Flow
```
API Call → Error → Error Handler → User Notification → Logging → Recovery
```

## 🎯 Common API Categories

### 1. QAHosGenericDB (Primary Database)
- **Patient APIs**: `ws_MDM_Patient_*`
- **Vaccine APIs**: `ws_Vaccine_*`
- **Admission APIs**: `ws_CN_*`
- **Generic APIs**: `ws_*`

### 2. API Response Patterns
```typescript
// Success response
{
  table: [
    {
      // Data fields
    }
  ]
}

// Error response
{
  table: [
    {
      errcode: "1",
      errMsg: "Error message"
    }
  ]
}
```

## 🔧 Development Tools & Patterns

### 1. TypeScript Interfaces
```typescript
export interface ApiParams {
  FacID: string;
  PatientID: string;
  // ... other fields
}

export interface ApiResponse {
  table: Array<{
    // Response fields
  }>;
}
```

### 2. Utility Functions
```typescript
// Date formatting
format(new Date(), "MM/dd/yyyy HH:mm:ss")

// UUID generation
utils.UuidCreateSequential()

// Error handling
getErrorMessage(error)

// Notifications
utils.notifySuccess("Message")
utils.notifyError("Error")
```

### 3. Permission System
```typescript
const { hasPermission } = useAppPermissions();
const canEdit = hasPermission(PermissionEnum.EDIT_VACCINE);
```

## 📍 Key File Locations

### 1. Core Services
- **Patient**: `app/lib/services/patient.ts`
- **Vaccine**: `app/lib/services/keVaccinTabServices.ts`
- **Admission**: `app/lib/services/admissionBusiness.ts`
- **System**: `app/lib/services/system.ts`

### 2. Main Pages
- **Tiếp nhận**: `app/(main)/tiep-nhan/tiep-nhan-moi/page.tsx`
- **Khám bệnh**: `app/(main)/ngoai-tru/kham-benh/[patientId]/page.tsx`
- **Vaccine**: `app/(main)/ngoai-tru/kham-benh/[patientId]/tabs/KeVaccinTab.tsx`

### 3. Business Logic
- **Admission**: `app/(main)/tiep-nhan/hooks/useAdmission.ts`
- **Vaccine**: `app/(main)/ngoai-tru/kham-benh/hooks/useChiDinhVaccine.ts`
- **Protocol**: `app/(main)/ngoai-tru/kham-benh/hooks/useThemPhacDo.ts`

## 🚨 Common Patterns to Watch

### 1. API Call Patterns
- **Direct service calls**: `KeVaccinTabServices.ws_API_NAME()`
- **Business logic calls**: `checkPatientExists()`
- **Transaction calls**: `executeTransaction()`

### 2. UI Trigger Patterns
- **Checkbox changes**: `onChange` events
- **Button clicks**: `onClick` handlers
- **Form submissions**: `onSubmit` handlers
- **Row actions**: `onRowClick`, `onRowDoubleClick`

### 3. Data Update Patterns
- **Optimistic updates**: Update UI first, then API
- **SWR mutations**: `mutate()` calls after API success
- **Conditional fetching**: Fetch only when needed

## 💡 Search Strategy Tips

### 1. Start with Service Files
- Look in `app/lib/services/*.ts` first
- Find the API wrapper function
- Check import statements

### 2. Follow the Chain
- Find where service is imported
- Look for function calls
- Check UI components that trigger functions

### 3. Look for Patterns
- **Service imports**: `import * as ServiceName`
- **Function calls**: `await ServiceName.ws_API_NAME()`
- **UI triggers**: `onClick`, `onChange`, `onSubmit`

### 4. Check Business Logic
- Look in `admissionBusiness.ts` and similar files
- Find wrapper functions
- Check for indirect usage

## 🔍 Quick Reference Commands

### 1. Find API Definition
```bash
cd C:\PROJECTS\genie
grep -r "ws_API_NAME" app/lib/services/
```

### 2. Find Usage
```bash
grep -r "ServiceName.ws_API_NAME" app/
grep -r "ws_API_NAME" app/
```

### 3. Find UI Components
```bash
grep -r "onClick.*function" app/
grep -r "Button.*onClick" app/
```

### 4. Find Business Logic
```bash
grep -r "function.*async" app/lib/services/
grep -r "const.*=.*async" app/
```

---

*Tài liệu này giúp hiểu nhanh cấu trúc Genie Frontend để tìm kiếm API hiệu quả hơn*
