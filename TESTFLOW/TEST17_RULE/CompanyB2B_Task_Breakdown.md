# CompanyB2B Management System - Task Breakdown

## Tổng quan dự án
**Mục tiêu**: Xây dựng hệ thống quản lý CompanyB2B với đầy đủ chức năng CRUD, import/export dữ liệu, và chuẩn hóa xử lý dữ liệu. Hệ thống đảm bảo tính nhất quán trong validation, null-handling, audit trail và hỗ trợ đa ngôn ngữ (tiếng Việt/Anh).

**Phạm vi**: Entity CompanyB2B với các thao tác Create/Update (Save), List, Export, Import (XLSX). Không thay đổi cấu trúc DB, chỉ chuẩn hóa xử lý logic và format dữ liệu.

**Yêu cầu đặc biệt**: 
- Tất cả thông báo lỗi phải bằng tiếng Việt
- Hỗ trợ import tối đa 10,000 records
- Chuẩn hóa null values thành empty string ("")
- Audit trail đầy đủ (CreatedBy, ModifiedBy, timestamps)

---

## 📁 Project Structure & File Paths

### 🏗️ **Backend Project (Aladdin)**
- **Repository**: `aladdin` (main project)
- **Git Branch**: `feat/ws_CompanyB2B`
- **Solution File**: [`Aladdin.sln`](/c:/PROJECTS/aladdin/Aladdin.sln)
- **Project Path**: [`/c:/PROJECTS/aladdin/`](/c:/PROJECTS/aladdin/)

#### **Key Directories & Files:**
```
aladdin/
├── [WebService/](/c:/PROJECTS/aladdin/WebService/)                    ← Main API project
│   ├── [Controllers/](/c:/PROJECTS/aladdin/WebService/Controllers/)
│   │   └── [CompanyB2BController.cs](/c:/PROJECTS/aladdin/WebService/Controllers/CompanyB2BController.cs)      ← API endpoints
│   ├── [Program.cs](/c:/PROJECTS/aladdin/WebService/Program.cs)                        ← Startup configuration
│   └── [appsettings.json](/c:/PROJECTS/aladdin/WebService/appsettings.json)                 ← Configuration
├── [WebService.Handlers/](/c:/PROJECTS/aladdin/WebService.Handlers/)                  ← Business logic handlers
│   ├── [CompanyB2B/](/c:/PROJECTS/aladdin/WebService.Handlers/CompanyB2B/)                      ← CompanyB2B handlers
│   │   ├── [ws_L_CompanyB2B_Save.cs](/c:/PROJECTS/aladdin/WebService.Handlers/CompanyB2B/ws_L_CompanyB2B_Save.cs)      ← Save operation handler
│   │   ├── [ws_L_CompanyB2B_Get.cs](/c:/PROJECTS/aladdin/WebService.Handlers/CompanyB2B/ws_L_CompanyB2B_Get.cs)       ← List operation handler
│   │   ├── [ws_L_CompanyB2B_Import.cs](/c:/PROJECTS/aladdin/WebService.Handlers/CompanyB2B/ws_L_CompanyB2B_Import.cs)    ← Import operation handler
│   │   └── [ws_L_CompanyB2B_Export.cs](/c:/PROJECTS/aladdin/WebService.Handlers/CompanyB2B/ws_L_CompanyB2B_Export.cs)    ← Export operation handler
│   └── [WebService.Handlers.csproj](/c:/PROJECTS/aladdin/WebService.Handlers/WebService.Handlers.csproj)
├── [Entities/](/c:/PROJECTS/aladdin/Entities/)                             ← Data models
│   ├── [CompanyB2B/](/c:/PROJECTS/aladdin/Entities/CompanyB2B/)                      ← CompanyB2B entity
│   │   └── [CompanyB2B.cs](/c:/PROJECTS/aladdin/Entities/CompanyB2B/CompanyB2B.cs)                ← Domain model
│   └── [Entities.csproj](/c:/PROJECTS/aladdin/Entities/Entities.csproj)
├── [Services/](/c:/PROJECTS/aladdin/Services/)                             ← Business services
│   ├── [CompanyB2B/](/c:/PROJECTS/aladdin/Services/CompanyB2B/)                      ← CompanyB2B services
│   │   ├── [ICompanyB2BService.cs](/c:/PROJECTS/aladdin/Services/CompanyB2B/ICompanyB2BService.cs)        ← Service interface
│   │   ├── [CompanyB2BService.cs](/c:/PROJECTS/aladdin/Services/CompanyB2B/CompanyB2BService.cs)         ← Service implementation
│   │   └── [ExcelProcessingService.cs](/c:/PROJECTS/aladdin/Services/CompanyB2B/ExcelProcessingService.cs)    ← Excel import/export
│   └── [Services.csproj](/c:/PROJECTS/aladdin/Services/Services.csproj)
└── [TestHelpers/](/c:/PROJECTS/aladdin/TestHelpers/)                          ← Testing utilities
    ├── [CompanyB2B/](/c:/PROJECTS/aladdin/TestHelpers/CompanyB2B/)                       ← CompanyB2B test helpers
    └── [TestHelpers.csproj](/c:/PROJECTS/aladdin/TestHelpers/TestHelpers.csproj)
```

#### **Database Scripts:**
```
aladdin/
├── [Database/](/c:/PROJECTS/aladdin/Database/)
│   ├── [Scripts/](/c:/PROJECTS/aladdin/Database/Scripts/)
│   │   ├── [CompanyB2B/](/c:/PROJECTS/aladdin/Database/Scripts/CompanyB2B/)
│   │   │   ├── [Create_CompanyB2B_Table.sql](/c:/PROJECTS/aladdin/Database/Scripts/CompanyB2B/Create_CompanyB2B_Table.sql)
│   │   │   ├── [Create_Indexes.sql](/c:/PROJECTS/aladdin/Database/Scripts/CompanyB2B/Create_Indexes.sql)
│   │   │   └── [StoredProcedures/](/c:/PROJECTS/aladdin/Database/Scripts/CompanyB2B/StoredProcedures/)
│   │   │       ├── [ws_L_CompanyB2B_Save.sql](/c:/PROJECTS/aladdin/Database/Scripts/CompanyB2B/StoredProcedures/ws_L_CompanyB2B_Save.sql)
│   │   │       ├── [ws_L_CompanyB2B_Get.sql](/c:/PROJECTS/aladdin/Database/Scripts/CompanyB2B/StoredProcedures/ws_L_CompanyB2B_Get.sql)
│   │   │       ├── [ws_L_CompanyB2B_Import.sql](/c:/PROJECTS/aladdin/Database/Scripts/CompanyB2B/StoredProcedures/ws_L_CompanyB2B_Import.sql)
│   │   │       └── [ws_L_CompanyB2B_Export.sql](/c:/PROJECTS/aladdin/Database/Scripts/CompanyB2B/StoredProcedures/ws_L_CompanyB2B_Export.sql)
│   │   └── [Migrations/](/c:/PROJECTS/aladdin/Database/Scripts/Migrations/)
│   └── [Database.csproj](/c:/PROJECTS/aladdin/Database/Database.csproj)
```

### 🎨 **Frontend Project (genie)**
- **Repository**: `genie` (frontend app)
- **Git Branch**: `feat/ws_CompanyB2B`
- **Project Path**: [`/c:/PROJECTS/genie/`](/c:/PROJECTS/genie/)

#### **Key Directories & Files:**
```
genie/
├── [app/](/c:/PROJECTS/genie/app/)                                  ← Main application
│   ├── [company-b2b/](/c:/PROJECTS/genie/app/company-b2b/)                      ← CompanyB2B module
│   │   ├── [page.tsx](/c:/PROJECTS/genie/app/company-b2b/page.tsx)                      ← Main page component
│   │   ├── [components/](/c:/PROJECTS/genie/app/company-b2b/components/)                   ← UI components
│   │   │   ├── [CompanyB2BForm.tsx](/c:/PROJECTS/genie/app/company-b2b/components/CompanyB2BForm.tsx)       ← Add/Edit form
│   │   │   ├── [CompanyB2BList.tsx](/c:/PROJECTS/genie/app/company-b2b/components/CompanyB2BList.tsx)       ← Data table
│   │   │   ├── [CompanyB2BImport.tsx](/c:/PROJECTS/genie/app/company-b2b/components/CompanyB2BImport.tsx)     ← Import component
│   │   │   └── [CompanyB2BExport.tsx](/c:/PROJECTS/genie/app/company-b2b/components/CompanyB2BExport.tsx)     ← Export component
│   │   ├── [services/](/c:/PROJECTS/genie/app/company-b2b/services/)                     ← API services
│   │   │   └── [companyB2BService.ts](/c:/PROJECTS/genie/app/company-b2b/services/companyB2BService.ts)     ← API integration
│   │   ├── [types/](/c:/PROJECTS/genie/app/company-b2b/types/)                        ← TypeScript types
│   │   │   └── [companyB2B.types.ts](/c:/PROJECTS/genie/app/company-b2b/types/companyB2B.types.ts)      ← Data models
│   │   └── [utils/](/c:/PROJECTS/genie/app/company-b2b/utils/)                        ← Utility functions
│   │       └── [dataNormalizer.ts](/c:/PROJECTS/genie/app/company-b2b/utils/dataNormalizer.ts)         ← Data processing
│   ├── [globals.css](/c:/PROJECTS/genie/app/globals.css)                       ← Global styles
│   └── [layout.tsx](/c:/PROJECTS/genie/app/layout.tsx)                        ← App layout
├── [components/](/c:/PROJECTS/genie/components/)                            ← Shared components
│   ├── [ui/](/c:/PROJECTS/genie/components/ui/)                               ← UI components
│   │   ├── [button.tsx](/c:/PROJECTS/genie/components/ui/button.tsx)                    ← Button component
│   │   ├── [input.tsx](/c:/PROJECTS/genie/components/ui/input.tsx)                     ← Input component
│   │   ├── [table.tsx](/c:/PROJECTS/genie/components/ui/table.tsx)                     ← Table component
│   │   └── [dialog.tsx](/c:/PROJECTS/genie/components/ui/dialog.tsx)                    ← Modal component
│   └── [forms/](/c:/PROJECTS/genie/components/forms/)                            ← Form components
├── [lib/](/c:/PROJECTS/genie/lib/)                                   ← Utility libraries
│   ├── [api.ts](/c:/PROJECTS/genie/lib/api.ts)                            ← API utilities
│   ├── [utils.ts](/c:/PROJECTS/genie/lib/utils.ts)                          ← General utilities
│   └── [validations.ts](/c:/PROJECTS/genie/lib/validations.ts)                    ← Validation schemas
├── [package.json](/c:/PROJECTS/genie/package.json)                           ← Dependencies
├── [tailwind.config.ts](/c:/PROJECTS/genie/tailwind.config.ts)                     ← Styling configuration
└── [tsconfig.json](/c:/PROJECTS/genie/tsconfig.json)                         ← TypeScript configuration
```

### 🗄️ **Database Project (qas-db)**
- **Repository**: `qas-db` (database scripts)
- **Git Branch**: `main` (or relevant feature branch)
- **Project Path**: [`/c:/PROJECTS/qas-db/`](/c:/PROJECTS/qas-db/)

#### **Key Directories & Files:**
```
qas-db/
├── [QAHosGenericDB/](/c:/PROJECTS/qas-db/QAHosGenericDB/)                       ← Main database schema
│   ├── [Tables/](/c:/PROJECTS/qas-db/QAHosGenericDB/Tables/)
│   │   └── [CompanyB2B.sql](/c:/PROJECTS/qas-db/QAHosGenericDB/Tables/CompanyB2B.sql)               ← Table definition
│   ├── [StoredProcedures/](/c:/PROJECTS/qas-db/QAHosGenericDB/StoredProcedures/)
│   │   └── [ws_L_CompanyB2B_*.sql](/c:/PROJECTS/qas-db/QAHosGenericDB/StoredProcedures/)        ← Stored procedures
│   ├── [Indexes/](/c:/PROJECTS/qas-db/QAHosGenericDB/Indexes/)
│   │   └── [CompanyB2B_Indexes.sql](/c:/PROJECTS/qas-db/QAHosGenericDB/Indexes/CompanyB2B_Indexes.sql)       ← Index definitions
│   └── [Constraints/](/c:/PROJECTS/qas-db/QAHosGenericDB/Constraints/)
│       └── [CompanyB2B_Constraints.sql](/c:/PROJECTS/qas-db/QAHosGenericDB/Constraints/CompanyB2B_Constraints.sql)    ← Constraint definitions
├── [QA_API/](/c:/PROJECTS/qas-db/QA_API/)                               ← API database objects
├── [QA_Pay/](/c:/PROJECTS/qas-db/QA_Pay/)                               ← Payment related objects
└── [qas-db.sqlproj](/c:/PROJECTS/qas-db/qas-db.sqlproj)                        ← Database project file
```

---

## 🔗 **Git Repository Information**

### **Backend (Aladdin)**
```bash
# Clone repository
git clone <aladdin-repo-url>
cd aladdin

# Switch to feature branch
git checkout feat/ws_CompanyB2B

# Check current branch
git branch

# View recent commits
git log --oneline -10

# View file changes
git status
```

### **Frontend (genie)**
```bash
# Clone repository
git clone <genie-repo-url>
cd genie

# Switch to feature branch
git checkout feat/ws_CompanyB2B

# Install dependencies
npm install
# or
yarn install

# Start development server
npm run dev
# or
yarn dev
```

### **Database (qas-db)**
```bash
# Clone repository
git clone <qas-db-repo-url>
cd qas-db

# Check current branch
git branch

# View database changes
git log --oneline --grep="CompanyB2B"
```

---

## 📋 **Development Environment Setup**

### **Prerequisites**
- **.NET 8.0** (Backend)
- **Node.js 18+** (Frontend)
- **SQL Server** (Database)
- **Visual Studio 2022** or **VS Code**
- **Git** for version control

### **Backend Setup (Aladdin)**
```bash
# Navigate to project
cd /c:/PROJECTS/aladdin/

# Restore NuGet packages
dotnet restore

# Build solution
dotnet build

# Run tests
dotnet test

# Start API
cd WebService
dotnet run
```

### **Frontend Setup (genie)**
```bash
# Navigate to project
cd /c:/PROJECTS/genie/

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### **Database Setup (qas-db)**
```bash
# Open in SQL Server Management Studio
# Or use Azure Data Studio

# Deploy database project
# Run scripts in order:
# 1. Create_CompanyB2B_Table.sql
# 2. Create_Indexes.sql
# 3. StoredProcedures/*.sql
```

---

## 🔍 **Code Review & Maintenance**

### **Key Files to Review**
1. **`CompanyB2BController.cs`** - API endpoints and routing
2. **`ws_L_CompanyB2B_*.cs`** - Business logic handlers
3. **`CompanyB2B.cs`** - Domain model and validation
4. **`CompanyB2BForm.tsx`** - Frontend form component
5. **`companyB2BService.ts`** - API integration service
6. **Stored Procedures** - Database operations

### **Testing Files**
```
aladdin/
├── WebService.Handlers.Tests/
│   └── CompanyB2B/
│       ├── CompanyB2BHandlerTests.cs
│       ├── CompanyB2BValidationTests.cs
│       └── CompanyB2BImportExportTests.cs
└── TestHelpers/
    └── CompanyB2B/
        └── CompanyB2BTestData.cs
```

### **Configuration Files**
- **`appsettings.json`** - Backend configuration
- **`tailwind.config.ts`** - Frontend styling
- **`tsconfig.json`** - TypeScript configuration
- **`package.json`** - Frontend dependencies

---

## 📚 **Documentation Files**

### **Current Location**
```
DOCS_PROMPT/TESTFLOW/TEST17_RULE/
├── [CompanyB2B_Task_Breakdown.md](/c:/PROJECTS/DOCS_PROMPT/TESTFLOW/TEST17_RULE/CompanyB2B_Task_Breakdown.md)          ← This file (HOW to implement)
├── [CompanyB2B_Functional_Specification.md](/c:/PROJECTS/DOCS_PROMPT/TESTFLOW/TEST17_RULE/CompanyB2B_Functional_Specification.md) ← WHAT the system does
├── [UI_RULES.md](/c:/PROJECTS/DOCS_PROMPT/TESTFLOW/TEST17_RULE/UI_RULES.md)                            ← UI design guidelines
└── [SQL Scripts]                          ← Database scripts (to be updated)
```

### **Documentation Purpose**
- **Task Breakdown**: Implementation guide for developers
- **Functional Spec**: Business requirements and system behavior
- **UI Rules**: Design standards and component guidelines

---

## Database Layer

- [ ] Task 1: Verify existing CompanyB2B table structure and indexes
    - [ ] Check CompanyCode unique constraint
    - [ ] Verify CreatedOn, ModifiedOn indexes for sorting optimization
    - [ ] Confirm all required fields exist with correct data types
    - [ ] Validate Vietnamese character support in database

---

## Backend Application Layer

### API Controller

- [ ] Task 2: Create/Update CompanyB2BController
    - [ ] Implement POST /api/company-b2b/save endpoint
    - [ ] Implement GET /api/company-b2b/list endpoint  
    - [ ] Implement POST /api/company-b2b/import endpoint
    - [ ] Implement GET /api/company-b2b/export endpoint
    - [ ] Add JWT authentication attributes
    - [ ] Implement UserID extraction from session/claims (NameIdentifier claim → cookie 's' → UserService.GetUserIdFromSessionId)

### Request/Response Models

- [ ] Task 3: Create DTOs and models
    - [ ] Create CompanyB2BSaveRequest record (Id?, CompanyCode, CompanyName, CompanyTax?, CompanyAddress?, EffectiveFrom, EffectiveTo?, IsActive, Hopdong, UserID?)
    - [ ] Create CompanyB2BResponse record (Id, CompanyCode, CompanyName, CompanyTax, CompanyAddress, EffectiveFrom, EffectiveTo, IsActive, Hopdong, CreatedOn, ModifiedOn)
    - [ ] Create ImportResult and ImportError records
    - [ ] Create ExportResponse and ExportFile records
    - [ ] Add validation attributes and custom validators

### Business Logic Handlers

- [ ] Task 4: Implement Save operation handler
    - [ ] Create ws_L_CompanyB2B_Save stored procedure handler
    - [ ] Implement CompanyCode uniqueness validation (Create: unique toàn bảng; Update: không trùng với record khác)
    - [ ] Add EffectiveFrom ≤ EffectiveTo validation
    - [ ] Implement audit trail (CreatedBy, ModifiedBy, timestamps)
    - [ ] Handle null values normalization (null → "" for CompanyTax, CompanyAddress)
    - [ ] Auto-set UserID from session if not provided in request

- [ ] Task 5: Implement List operation handler
    - [ ] Create ws_L_CompanyB2B_Get stored procedure handler
    - [ ] Implement sorting by ModifiedOn DESC, CreatedOn DESC (fallback to CreatedOn if ModifiedOn is null)
    - [ ] Add data normalization (null → "", date formatting, boolean labels)
    - [ ] Ensure Vietnamese character support
    - [ ] Format dates: EffectiveFrom/EffectiveTo as "yyyy-MM-dd", CreatedOn/ModifiedOn as "yyyy-MM-dd HH:mm:ss"

- [ ] Task 6: Implement Import operation handler
    - [ ] Create ws_L_CompanyB2B_Import stored procedure handler
    - [ ] Add Excel file parsing (support .xlsx format, CSV fallback)
    - [ ] Implement header mapping (Vietnamese/English support: CompanyCode/Mã công ty, CompanyName/Tên công ty, CompanyTax/MST, CompanyAddress/Địa chỉ, EffectiveFrom/Ngày bắt đầu, EffectiveTo/Ngày kết thúc, IsActive/Trạng thái, Hopdong/Số PO-HĐ)
    - [ ] Add validation rules per row (required fields, data types, constraints)
    - [ ] Implement duplicate CompanyCode detection within file
    - [ ] Add row limit validation (max 10,000 records)
    - [ ] Implement transaction rollback on validation errors
    - [ ] Return detailed error messages in Vietnamese
    - [ ] Support upsert by CompanyCode in single transaction

- [ ] Task 7: Implement Export operation handler
    - [ ] Create ws_L_CompanyB2B_Export stored procedure handler
    - [ ] Retrieve all CompanyB2B records
    - [ ] Normalize data for export (null → "", format dates, boolean labels)
    - [ ] Convert to JSON with UTF-8 encoding
    - [ ] Encode to Base64
    - [ ] Calculate file sizes and metadata
    - [ ] Generate filename with timestamp (CompanyB2B_yyyyMMddHHmmss.json)

### Validation

- [ ] Task 8: Implement comprehensive validation
    - [ ] Create CompanyB2BSaveRequestValidator
    - [ ] Add CompanyCode required and length validation (max 50 chars)
    - [ ] Add CompanyName required and length validation (max 500 chars)
    - [ ] Add CompanyTax length validation (max 50 chars)
    - [ ] Add CompanyAddress length validation (max 500 chars)
    - [ ] Add EffectiveFrom required and valid date validation
    - [ ] Add EffectiveTo date range validation (≥ EffectiveFrom)
    - [ ] Add Hopdong required and length validation (max 100 chars)
    - [ ] Add IsActive boolean validation
    - [ ] Ensure all error messages are in Vietnamese
    - [ ] Add CompanyCode uniqueness validation

### Data Processing

- [ ] Task 9: Implement Excel file processing
    - [ ] Add EPPlus or ClosedXML NuGet package
    - [ ] Create ExcelParser service for .xlsx files
    - [ ] Implement header detection and mapping (Vietnamese/English)
    - [ ] Add row-by-row data extraction
    - [ ] Handle Vietnamese character encoding
    - [ ] Implement file size and row count validation (max 10,000 rows)
    - [ ] Support CSV format as fallback

- [ ] Task 10: Implement data normalization
    - [ ] Create DataNormalizer service
    - [ ] Implement null → "" conversion for text fields (CompanyTax, CompanyAddress)
    - [ ] Add date formatting (yyyy-MM-dd for dates, yyyy-MM-dd HH:mm:ss for timestamps)
    - [ ] Add boolean to Vietnamese label conversion ("Kích hoạt"/"Không kích hoạt")
    - [ ] Ensure UTF-8 encoding consistency
    - [ ] Handle audit trail fields (CreatedBy, ModifiedBy)

---

## Frontend Layer (genie app)

### Components

- [ ] Task 11: Create CompanyB2B form component
    - [ ] Implement create/edit form with all required fields
    - [ ] Add client-side validation (CompanyCode, CompanyName, EffectiveFrom, Hopdong required)
    - [ ] Handle form submission to save endpoint
    - [ ] Display success/error messages in Vietnamese
    - [ ] Implement EffectiveFrom ≤ EffectiveTo validation
    - [ ] Show field validation errors in Vietnamese

- [ ] Task 12: Create CompanyB2B list component
    - [ ] Implement data table with sorting (ModifiedOn DESC, CreatedOn DESC)
    - [ ] Display normalized data (formatted dates, boolean labels, empty strings)
    - [ ] Add pagination for future scalability (10, 20, 50, 100 rows per page)
    - [ ] Handle API calls to list endpoint
    - [ ] Show total record count
    - [ ] Implement search functionality (CompanyCode, CompanyName, MST, Address, PO-HĐ)

- [ ] Task 13: Create import component
    - [ ] Implement file upload with drag & drop
    - [ ] Add file type validation (.xlsx only, .csv fallback)
    - [ ] Display validation errors in Vietnamese
    - [ ] Show import progress and results
    - [ ] Display detailed error list by row number
    - [ ] Show import summary (total processed, total imported, error count)

- [ ] Task 14: Create export component
    - [ ] Implement export button and functionality
    - [ ] Handle Base64 decoding of response
    - [ ] Convert JSON to Excel file download
    - [ ] Ensure Vietnamese characters display correctly
    - [ ] Show export progress and completion status

### API Integration

- [ ] Task 15: Implement API service layer
    - [ ] Create CompanyB2B API service
    - [ ] Add authentication token handling (Bearer Token)
    - [ ] Implement error handling and Vietnamese message display
    - [ ] Add request/response type definitions
    - [ ] Handle session-based authentication
    - [ ] Implement proper error handling for network issues

---

## Testing

### Unit Tests

- [ ] Task 16: Write backend unit tests
    - [ ] Test CompanyB2BSaveRequest validation
    - [ ] Test data normalization logic (null → "")
    - [ ] Test audit trail creation (CreatedBy, ModifiedBy, timestamps)
    - [ ] Test Excel parsing functionality
    - [ ] Test Base64 encoding/decoding
    - [ ] Test CompanyCode uniqueness validation
    - [ ] Test date range validation (EffectiveFrom ≤ EffectiveTo)

- [ ] Task 17: Write frontend unit tests
    - [ ] Test form validation (required fields, date validation)
    - [ ] Test component rendering
    - [ ] Test API service methods
    - [ ] Test data transformation logic
    - [ ] Test Vietnamese language display
    - [ ] Test file upload validation

### Integration Tests

- [ ] Task 18: Write integration tests
    - [ ] Test complete save → list → export workflow
    - [ ] Test import validation and error handling
    - [ ] Test authentication and authorization
    - [ ] Test Vietnamese character handling throughout the system
    - [ ] Test audit trail creation and updates
    - [ ] Test transaction rollback on import errors

### Performance Tests

- [ ] Task 19: Write performance tests
    - [ ] Test import with maximum records (10,000)
    - [ ] Test export performance with large datasets
    - [ ] Test memory usage during file operations
    - [ ] Test API response times under load
    - [ ] Test Base64 encoding performance impact

---

## Documentation

- [ ] Task 20: Update API documentation
    - [ ] Document all endpoints with request/response examples
    - [ ] Add validation rules and error codes
    - [ ] Include Vietnamese error message examples
    - [ ] Document import/export file formats
    - [ ] Add authentication requirements
    - [ ] Document data normalization rules

- [ ] Task 21: Create user documentation
    - [ ] Write import/export user guide
    - [ ] Document validation rules and error messages
    - [ ] Create troubleshooting guide for common issues
    - [ ] Add screenshots and examples
    - [ ] Document Vietnamese language support
    - [ ] Create quick start guide for testing

---

## Deployment & Configuration

- [ ] Task 22: Update configuration files
    - [ ] Add Excel processing library dependencies (EPPlus/ClosedXML)
    - [ ] Configure JSON serialization for UTF-8 support
    - [ ] Set file upload size limits (max 10MB)
    - [ ] Configure authentication settings
    - [ ] Set import row limits (max 10,000)
    - [ ] Configure Vietnamese language support

- [ ] Task 23: Database deployment
    - [ ] Verify stored procedures are deployed (ws_L_CompanyB2B_Save, ws_L_CompanyB2B_Get, ws_L_CompanyB2B_Import, ws_L_CompanyB2B_Export)
    - [ ] Check indexes and constraints (CompanyCode unique, CreatedOn/ModifiedOn indexes)
    - [ ] Test data access performance
    - [ ] Validate Vietnamese character support
    - [ ] Test audit trail functionality

---

## Final Validation

- [ ] Task 24: End-to-end testing
    - [ ] Test complete user workflows (create → list → export)
    - [ ] Test import with various file formats and error scenarios
    - [ ] Verify Vietnamese character display in all components
    - [ ] Test error handling and user experience
    - [ ] Validate performance with realistic data volumes
    - [ ] Test authentication and authorization flows

- [ ] Task 25: User acceptance testing
    - [ ] Test with actual business users
    - [ ] Validate Vietnamese language support
    - [ ] Confirm import/export functionality meets requirements
    - [ ] Test with real Excel files containing Vietnamese data
    - [ ] Gather feedback and make final adjustments
    - [ ] Validate audit trail accuracy

---

## Quick Testing Guide

### Backend Testing (Swagger)
1. **Login**: POST /api/auth/login with credentials (phucnnd/Phuc*1234)
2. **Get Token**: Extract Bearer token from response
3. **Authorize**: Click Authorize in Swagger, paste "Bearer <token>"
4. **Test Endpoints**:
   - POST /api/company-b2b/save (create new record)
   - GET /api/company-b2b/list (view all records)
   - POST /api/company-b2b/import (upload Excel file)
   - GET /api/company-b2b/export (download data)

### Frontend Testing (genie app)
1. **Navigate** to CompanyB2B management page
2. **Test CRUD operations** with Vietnamese data
3. **Test import** with sample Excel files
4. **Test export** and verify downloaded data
5. **Verify Vietnamese language** support throughout

---

## Dependencies & Technical Notes

### Required NuGet Packages
- EPPlus or ClosedXML (Excel processing)
- System.Text.Encoding (UTF-8 support)
- Newtonsoft.Json (JSON serialization)

### Database Requirements
- CompanyCode unique constraint
- CreatedOn, ModifiedOn indexes for sorting
- Vietnamese character support (NVARCHAR fields)

### Performance Considerations
- Base64 encoding increases file size by ~33%
- Import limit: 10,000 records maximum
- File size limit: 10MB maximum
- Memory usage optimization for large imports

### Security Requirements
- JWT authentication for all endpoints
- Session-based UserID extraction
- Input validation to prevent injection attacks
- File upload security (type and size validation)

---

**Lưu ý**: Tất cả các task phải tuân thủ yêu cầu về tiếng Việt, null-handling, và audit trail như đã định nghĩa trong Technical Design Document. Mỗi task cần được test kỹ lưỡng trước khi mark as completed.

---

## ⚠️ **HIGH PRIORITY FIXES IN PROGRESS** 🚧

### ✅ **COMPLETED: CSV Injection Vulnerability**
- **Status**: Method `SanitizeCsvField` has been implemented and applied to all imported fields
- **Fix Applied**: Added CSV injection protection method and applied it to companyTax, companyCode, companyName, companyAddress, effectiveFrom, effectiveTo, isActive, and hopdong fields
- **Result**: Prevents malicious Excel formulas from being imported and executed when exported data is opened in Excel

### 🚧 **TO BE COMPLETED: Mass Assignment Risk**
- **Status**: Need to create separate API DTOs
- **Required**: Implement `CompanyB2BSaveRequest` DTO with restricted fields
- **Next Step**: Update controller to use separate request/response models
