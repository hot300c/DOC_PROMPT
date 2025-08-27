# TODO: Company B2B Management - Pre-Generation Analysis

## Handler Information
- **Handler Name**: Company B2B Management Handlers
- **Original SP**: N/A (New functionality)
- **Purpose**: CRUD operations for B2B Company management with import/export Excel functionality

## Analysis Results

### Business Logic
- **Create Company**: Add new B2B company with validation for unique CompanyCode
- **Update Company**: Modify existing company information
- **Delete Company**: Soft delete by toggling IsActive status
- **Search & List**: Search companies with pagination and filtering
- **Import Excel**: Import company data from Excel file with update/replace logic
- **Export Excel**: Export company data to Excel format

### Required Functions
- [ ] `AuthenticateUser()` - User authentication
- [ ] `ValidateInput()` - Input parameter validation
- [ ] `ValidateBusinessRules()` - Business logic validation
- [ ] `GetCompanyB2B()` - Get single company by ID
- [ ] `SearchCompanyB2B()` - Search companies with filters and pagination
- [ ] `CreateCompanyB2B()` - Create new company
- [ ] `UpdateCompanyB2B()` - Update existing company
- [ ] `DeleteCompanyB2B()` - Soft delete company (toggle IsActive)
- [ ] `ImportExcelData()` - Process Excel import
- [ ] `ExportExcelData()` - Generate Excel export
- [ ] `ValidateCompanyCodeUnique()` - Check unique CompanyCode
- [ ] `ValidateCompanyData()` - Validate company information

### Required Entities
- **LCompanyB2B**: Main company entity
- **ReportOutput**: For Excel export functionality
- **Sessions**: For user authentication

### Test Scenarios
- [ ] Happy path - Create company
- [ ] Happy path - Update company
- [ ] Happy path - Delete company (soft delete)
- [ ] Happy path - Search companies
- [ ] Happy path - Import Excel
- [ ] Happy path - Export Excel
- [ ] Authentication failure
- [ ] Validation error - Duplicate CompanyCode
- [ ] Validation error - Invalid data
- [ ] Business logic error - Invalid date range
- [ ] No data found
- [ ] System error

## API Endpoints to Implement

### 1. CRUD Operations
```
POST   /api/company-b2b/create
PUT    /api/company-b2b/update
DELETE /api/company-b2b/delete (soft delete - toggle IsActive)
GET    /api/company-b2b/get/{id}
GET    /api/company-b2b/list (with search, pagination)
```

### 2. Import/Export Operations
```
POST   /api/company-b2b/import-excel
GET    /api/company-b2b/export-excel
```

## DTOs Structure

### Import Excel DTO
```csharp
public record ImportExcelDto
{
    public string Base64Data { get; init; }
    public string FileName { get; init; }
    public Guid UserId { get; init; }
}
```

### Export Excel DTO
```csharp
public record ExportExcelDto
{
    public string ReportName { get; init; }
    public string ReportParams { get; init; }
    public Guid UserId { get; init; }
}
```

## Validation Rules
1. **CompanyCode**: Unique, không được trùng
2. **CompanyTax**: Format mã số thuế hợp lệ
3. **EffectiveFrom**: Phải <= EffectiveTo (nếu có)
4. **CompanyName**: Không được để trống
5. **CompanyAddress**: Không được để trống

## Search Criteria
- CompanyCode (exact match)
- CompanyName (contains)
- CompanyTax (exact match)
- IsActive (boolean)
- EffectiveFrom/EffectiveTo (date range)
- Hopdong (contains)

## Pagination
- Page size: 10, 20, 50, 100
- Sort by: CompanyCode, CompanyName, CreatedOn
- Sort direction: ASC, DESC

## Notes
- Import will update/replace existing companies based on CompanyCode
- Delete is implemented as soft delete (toggle IsActive)
- Excel export follows the same pattern as existing report system
- All operations require user authentication
- CompanyCode must be unique across all companies
