# CompanyB2B Management System - Task Breakdown

## Database Layer

- [ ] Task 1: Verify existing CompanyB2B table structure and indexes
    - [ ] Check CompanyCode unique constraint
    - [ ] Verify CreatedOn, ModifiedOn indexes for sorting optimization
    - [ ] Confirm all required fields exist with correct data types

## Backend Application Layer

### API Controller

- [ ] Task 2: Create/Update CompanyB2BController
    - [ ] Implement POST /api/company-b2b/save endpoint
    - [ ] Implement GET /api/company-b2b/list endpoint  
    - [ ] Implement POST /api/company-b2b/import endpoint
    - [ ] Implement GET /api/company-b2b/export endpoint
    - [ ] Add JWT authentication attributes
    - [ ] Implement UserID extraction from session/claims

### Request/Response Models

- [ ] Task 3: Create DTOs and models
    - [ ] Create CompanyB2BSaveRequest record
    - [ ] Create CompanyB2BResponse record
    - [ ] Create ImportResult and ImportError records
    - [ ] Create ExportResponse and ExportFile records
    - [ ] Add validation attributes and custom validators

### Business Logic Handlers

- [ ] Task 4: Implement Save operation handler
    - [ ] Create ws_L_CompanyB2B_Save stored procedure handler
    - [ ] Implement CompanyCode uniqueness validation
    - [ ] Add EffectiveFrom ≤ EffectiveTo validation
    - [ ] Implement audit trail (CreatedBy, ModifiedBy, timestamps)
    - [ ] Handle null values normalization (null → "")

- [ ] Task 5: Implement List operation handler
    - [ ] Create ws_L_CompanyB2B_Get stored procedure handler
    - [ ] Implement sorting by ModifiedOn DESC, CreatedOn DESC
    - [ ] Add data normalization (null → "", date formatting, boolean labels)
    - [ ] Ensure Vietnamese character support

- [ ] Task 6: Implement Import operation handler
    - [ ] Create ws_L_CompanyB2B_Import stored procedure handler
    - [ ] Add Excel file parsing (support .xlsx format)
    - [ ] Implement header mapping (Vietnamese/English support)
    - [ ] Add validation rules per row (required fields, data types, constraints)
    - [ ] Implement duplicate CompanyCode detection within file
    - [ ] Add row limit validation (max 10,000 records)
    - [ ] Implement transaction rollback on validation errors
    - [ ] Return detailed error messages in Vietnamese

- [ ] Task 7: Implement Export operation handler
    - [ ] Create ws_L_CompanyB2B_Export stored procedure handler
    - [ ] Retrieve all CompanyB2B records
    - [ ] Normalize data for export (null → "", format dates, boolean labels)
    - [ ] Convert to JSON with UTF-8 encoding
    - [ ] Encode to Base64
    - [ ] Calculate file sizes and metadata
    - [ ] Generate filename with timestamp

### Validation

- [ ] Task 8: Implement comprehensive validation
    - [ ] Create CompanyB2BSaveRequestValidator
    - [ ] Add CompanyCode required and length validation (max 50)
    - [ ] Add CompanyName required and length validation (max 500)
    - [ ] Add CompanyTax length validation (max 50)
    - [ ] Add CompanyAddress length validation (max 500)
    - [ ] Add EffectiveFrom required and valid date validation
    - [ ] Add EffectiveTo date range validation (≥ EffectiveFrom)
    - [ ] Add Hopdong required and length validation (max 100)
    - [ ] Add IsActive boolean validation
    - [ ] Ensure all error messages are in Vietnamese

### Data Processing

- [ ] Task 9: Implement Excel file processing
    - [ ] Add EPPlus or ClosedXML NuGet package
    - [ ] Create ExcelParser service for .xlsx files
    - [ ] Implement header detection and mapping
    - [ ] Add row-by-row data extraction
    - [ ] Handle Vietnamese character encoding
    - [ ] Implement file size and row count validation

- [ ] Task 10: Implement data normalization
    - [ ] Create DataNormalizer service
    - [ ] Implement null → "" conversion for text fields
    - [ ] Add date formatting (yyyy-MM-dd for dates, yyyy-MM-dd HH:mm:ss for timestamps)
    - [ ] Add boolean to Vietnamese label conversion ("Kích hoạt"/"Không kích hoạt")
    - [ ] Ensure UTF-8 encoding consistency

## Frontend Layer (genie app)

### Components

- [ ] Task 11: Create CompanyB2B form component
    - [ ] Implement create/edit form with all required fields
    - [ ] Add client-side validation
    - [ ] Handle form submission to save endpoint
    - [ ] Display success/error messages in Vietnamese

- [ ] Task 12: Create CompanyB2B list component
    - [ ] Implement data table with sorting
    - [ ] Display normalized data (formatted dates, boolean labels, empty strings)
    - [ ] Add pagination for future scalability
    - [ ] Handle API calls to list endpoint

- [ ] Task 13: Create import component
    - [ ] Implement file upload with drag & drop
    - [ ] Add file type validation (.xlsx only)
    - [ ] Display validation errors in Vietnamese
    - [ ] Show import progress and results

- [ ] Task 14: Create export component
    - [ ] Implement export button and functionality
    - [ ] Handle Base64 decoding of response
    - [ ] Convert JSON to Excel file download
    - [ ] Ensure Vietnamese characters display correctly

### API Integration

- [ ] Task 15: Implement API service layer
    - [ ] Create CompanyB2B API service
    - [ ] Add authentication token handling
    - [ ] Implement error handling and Vietnamese message display
    - [ ] Add request/response type definitions

## Testing

### Unit Tests

- [ ] Task 16: Write backend unit tests
    - [ ] Test CompanyB2BSaveRequest validation
    - [ ] Test data normalization logic
    - [ ] Test audit trail creation
    - [ ] Test Excel parsing functionality
    - [ ] Test Base64 encoding/decoding

- [ ] Task 17: Write frontend unit tests
    - [ ] Test form validation
    - [ ] Test component rendering
    - [ ] Test API service methods
    - [ ] Test data transformation logic

### Integration Tests

- [ ] Task 18: Write integration tests
    - [ ] Test complete save → list → export workflow
    - [ ] Test import validation and error handling
    - [ ] Test authentication and authorization
    - [ ] Test Vietnamese character handling throughout the system

### Performance Tests

- [ ] Task 19: Write performance tests
    - [ ] Test import with maximum records (10,000)
    - [ ] Test export performance with large datasets
    - [ ] Test memory usage during file operations
    - [ ] Test API response times under load

## Documentation

- [ ] Task 20: Update API documentation
    - [ ] Document all endpoints with request/response examples
    - [ ] Add validation rules and error codes
    - [ ] Include Vietnamese error message examples
    - [ ] Document import/export file formats

- [ ] Task 21: Create user documentation
    - [ ] Write import/export user guide
    - [ ] Document validation rules and error messages
    - [ ] Create troubleshooting guide for common issues
    - [ ] Add screenshots and examples

## Deployment & Configuration

- [ ] Task 22: Update configuration files
    - [ ] Add Excel processing library dependencies
    - [ ] Configure JSON serialization for UTF-8 support
    - [ ] Set file upload size limits
    - [ ] Configure authentication settings

- [ ] Task 23: Database deployment
    - [ ] Verify stored procedures are deployed
    - [ ] Check indexes and constraints
    - [ ] Test data access performance
    - [ ] Validate Vietnamese character support

## Final Validation

- [ ] Task 24: End-to-end testing
    - [ ] Test complete user workflows
    - [ ] Verify Vietnamese character display in all components
    - [ ] Test error handling and user experience
    - [ ] Validate performance with realistic data volumes

- [ ] Task 25: User acceptance testing
    - [ ] Test with actual business users
    - [ ] Validate Vietnamese language support
    - [ ] Confirm import/export functionality meets requirements
    - [ ] Gather feedback and make final adjustments
