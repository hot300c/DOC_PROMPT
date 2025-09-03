# CompanyB2B Management System - Functional Specification

## 1. System Overview

### 1.1 Purpose
The CompanyB2B Management System is a comprehensive business partner management solution that enables organizations to efficiently manage their B2B (Business-to-Business) partner information. The system provides a centralized platform for creating, updating, viewing, and managing company partner records with robust import/export capabilities.

### 1.2 Target Users
- **Business Administrators**: Manage company partner relationships
- **Data Entry Personnel**: Input and maintain partner information
- **Business Analysts**: Export data for reporting and analysis
- **System Administrators**: Manage system configuration and user access

### 1.3 Business Value
- Centralized management of B2B partner information
- Improved data accuracy through validation and standardization
- Efficient bulk data operations through import/export
- Comprehensive audit trail for compliance and tracking
- Vietnamese language support for local business operations

---

## 2. Core Features

### 2.1 Company Partner Management

#### 2.1.1 Create New Company Partner
**Description**: Users can create new B2B company partner records with comprehensive information.

**Required Fields**:
- Company Code (unique identifier, max 50 characters)
- Company Name (max 500 characters)
- Effective From Date (start date of partnership)
- Contract/PO Number (max 100 characters)

**Optional Fields**:
- Company Tax Number (max 50 characters)
- Company Address (max 500 characters)
- Effective To Date (end date of partnership)
- Active Status (default: Active)

**Business Rules**:
- Company Code must be unique across all records
- Effective From Date is required and must be a valid date
- If Effective To Date is provided, it must be greater than or equal to Effective From Date
- All text fields automatically convert null values to empty strings for consistency

#### 2.1.2 Update Existing Company Partner
**Description**: Users can modify existing company partner information while maintaining data integrity.

**Business Rules**:
- Company Code cannot be changed once created (maintains referential integrity)
- All other fields can be updated
- Audit trail automatically tracks who made changes and when
- Validation rules apply to all updated fields

#### 2.1.3 View Company Partner List
**Description**: Users can browse and search through all company partner records.

**Display Features**:
- Sortable columns (default: Modified Date DESC, Created Date DESC)
- Search functionality across multiple fields
- Pagination support (10, 20, 50, 100 records per page)
- Total record count display

**Data Normalization**:
- Dates displayed in consistent format (yyyy-MM-dd for effective dates, yyyy-MM-dd HH:mm:ss for audit dates)
- Boolean values displayed in Vietnamese ("Kích hoạt" for Active, "Không kích hoạt" for Inactive)
- Null values displayed as empty strings for consistent user experience

#### 2.1.4 Toggle Company Status
**Description**: Users can quickly activate or deactivate company partnerships through a simple checkbox interface.

**Business Rules**:
- Status changes are immediately reflected in the system
- Audit trail tracks all status changes
- Inactive companies remain in the system but are clearly marked

### 2.2 Data Import Functionality

#### 2.2.1 Excel File Import
**Description**: Users can bulk import company partner data from Excel files.

**Supported Formats**:
- Primary: Microsoft Excel (.xlsx)
- Fallback: CSV format for compatibility

**File Requirements**:
- Maximum file size: 10MB
- Maximum records: 10,000 rows (excluding header)
- Header row must be present

**Header Mapping Support**:
- **Vietnamese Headers**: Mã công ty, Tên công ty, MST, Địa chỉ, Ngày bắt đầu, Ngày kết thúc, Trạng thái, Số PO-HĐ
- **English Headers**: CompanyCode, CompanyName, CompanyTax, CompanyAddress, EffectiveFrom, EffectiveTo, IsActive, Hopdong
- **Mixed Language Support**: System automatically detects and maps headers

**Validation During Import**:
- Required field validation (Company Code, Company Name, Effective From Date, Contract Number)
- Data type validation (dates, boolean values)
- Business rule validation (date ranges, field lengths)
- Duplicate Company Code detection within the import file
- Field length validation (Company Code: 50 chars, Company Name: 500 chars, etc.)

**Import Process**:
1. File upload and format validation
2. Header detection and mapping
3. Row-by-row data validation
4. Transaction-based import (all-or-nothing)
5. Detailed error reporting in Vietnamese
6. Success summary with import statistics

**Error Handling**:
- All validation errors displayed in Vietnamese
- Row-specific error reporting with field names
- Import stops if any validation errors occur
- No partial imports - complete rollback on errors

### 2.3 Data Export Functionality

#### 2.3.1 Export to Excel
**Description**: Users can export all company partner data to Excel format for external use.

**Export Format**:
- JSON data encoded in Base64
- UTF-8 encoding for Vietnamese character support
- Automatic file naming with timestamp (CompanyB2B_yyyyMMddHHmmss.json)

**Export Content**:
- All company partner records
- Normalized data (no null values, consistent formatting)
- Vietnamese labels for boolean fields
- Formatted dates and timestamps

**File Information**:
- File size in bytes, KB, and MB
- Total record count
- Export timestamp
- Content type and format details

**Client Processing**:
- Frontend decodes Base64 data
- Converts JSON to Excel format
- Downloads file to user's device
- Maintains Vietnamese character integrity

---

## 3. User Interface Specifications

### 3.1 Main Dashboard Layout

#### 3.1.1 Header Section
- Facility information display at the top
- User authentication status
- Navigation menu

#### 3.1.2 Search Section
- **Background**: Subtle, semi-transparent design
- **Search Field**: "Từ khóa" (Keywords) input box
- **Search Button**: "Tìm kiếm" (Search) button
- **Search Scope**: Company Code, Company Name, Tax Number, Address, Contract Number
- **Validation**: Search only executes when keywords are entered

#### 3.1.3 Data Table Section
- **Sorting**: Click column headers to sort (Modified Date DESC by default)
- **Row Highlighting**: Hover effects for better user experience
- **Click Actions**: Click any row to open edit popup
- **Status Toggle**: Checkbox for quick Active/Inactive status change

#### 3.1.4 Footer Section
- **Background**: Subtle, semi-transparent design
- **Pagination**: Page navigation with record count display
- **Records Per Page**: Dropdown (10, 20, 50, 100)
- **Action Buttons**: Right-aligned group (Add New, Import Excel, Export Excel)

### 3.2 Add/Edit Popup

#### 3.2.1 Form Layout
**Field Order** (top to bottom):
1. Company Code (read-only for edit mode)
2. Company Name
3. Company Tax Number
4. Company Address
5. Effective From Date
6. Effective To Date
7. Contract/PO Number
8. Active Status

#### 3.2.2 Validation Display
- **Required Field Indicators**: Visual markers for mandatory fields
- **Error Messages**: Vietnamese language error text below fields
- **Real-time Validation**: Immediate feedback on field changes
- **Business Rule Validation**: Date range and uniqueness validation

#### 3.2.3 Action Buttons
- **Save**: Processes form data and closes popup
- **Cancel**: Closes popup without saving
- **Success Message**: Displays confirmation after successful save

### 3.3 Import Interface

#### 3.3.1 File Upload
- **Drag & Drop**: Support for modern browsers
- **File Browser**: Traditional file selection
- **File Type Validation**: Only .xlsx and .csv files accepted
- **Size Validation**: Maximum 10MB file size

#### 3.3.2 Import Progress
- **Progress Bar**: Visual indication of import status
- **Status Messages**: Real-time updates in Vietnamese
- **Error Summary**: Count of validation errors
- **Success Summary**: Count of successfully imported records

#### 3.3.3 Error Display
- **Error List**: Detailed breakdown by row number
- **Field-specific Errors**: Clear indication of which fields failed validation
- **Vietnamese Messages**: All error text in Vietnamese language
- **Export Errors**: Option to download error report

### 3.4 Export Interface

#### 3.4.1 Export Button
- **Single Click**: Initiates export process
- **Progress Indicator**: Shows export status
- **Completion Message**: Confirms successful export
- **File Download**: Automatic download initiation

---

## 4. Business Rules and Constraints

### 4.1 Data Validation Rules

#### 4.1.1 Company Code
- **Required**: Yes
- **Uniqueness**: Must be unique across all records
- **Length**: Maximum 50 characters
- **Format**: Alphanumeric characters allowed
- **Business Rule**: Cannot be changed after creation

#### 4.1.2 Company Name
- **Required**: Yes
- **Length**: Maximum 500 characters
- **Format**: Text with Vietnamese character support
- **Business Rule**: Must be descriptive and meaningful

#### 4.1.3 Company Tax Number
- **Required**: No
- **Length**: Maximum 50 characters
- **Format**: Tax identification number format
- **Business Rule**: Optional but recommended for compliance

#### 4.1.4 Company Address
- **Required**: No
- **Length**: Maximum 500 characters
- **Format**: Full address with Vietnamese character support
- **Business Rule**: Optional but useful for business operations

#### 4.1.5 Effective Dates
- **Effective From**: Required, must be valid date
- **Effective To**: Optional, must be ≥ Effective From if provided
- **Format**: yyyy-MM-dd
- **Business Rule**: Defines partnership validity period

#### 4.1.6 Contract/PO Number
- **Required**: Yes
- **Length**: Maximum 100 characters
- **Format**: Contract or purchase order reference
- **Business Rule**: Essential for business relationship tracking

#### 4.1.7 Active Status
- **Required**: No (defaults to true)
- **Values**: true/false
- **Display**: "Kích hoạt" / "Không kích hoạt"
- **Business Rule**: Controls whether partnership is currently active

### 4.2 Data Processing Rules

#### 4.2.1 Null Value Handling
- **Text Fields**: Null values automatically converted to empty strings ("")
- **Date Fields**: Null dates remain null (no conversion)
- **Boolean Fields**: Null values default to true (Active)
- **Business Rule**: Ensures consistent data display and export

#### 4.2.2 Date Formatting
- **Effective Dates**: yyyy-MM-dd format
- **Audit Dates**: yyyy-MM-dd HH:mm:ss format
- **Display**: Consistent formatting across all interfaces
- **Export**: Maintains format for external systems

#### 4.2.3 Boolean Value Display
- **Active (true)**: Displays as "Kích hoạt"
- **Inactive (false)**: Displays as "Không kích hoạt"
- **Import**: Accepts true/false values
- **Export**: Returns Vietnamese labels

### 4.3 Audit Trail Rules

#### 4.3.1 Creation Tracking
- **Created On**: Automatically set to current timestamp
- **Created By**: Automatically set to current user ID
- **Business Rule**: Immutable after creation

#### 4.3.2 Modification Tracking
- **Modified On**: Automatically updated on each change
- **Modified By**: Automatically updated to current user ID
- **Business Rule**: Tracks all data changes for compliance

#### 4.3.3 User ID Resolution
- **Priority Order**: 
  1. NameIdentifier claim from JWT token
  2. Session cookie 's' value
  3. UserService.GetUserIdFromSessionId method
- **Business Rule**: Ensures accurate audit trail even without explicit UserID

---

## 5. System Integration

### 5.1 Authentication and Authorization

#### 5.1.1 JWT Authentication
- **Required**: All API endpoints require valid JWT token
- **Token Format**: Bearer token in Authorization header
- **Session Management**: Automatic UserID extraction from session
- **Security**: Token-based access control

#### 5.1.2 User Access Control
- **Login Required**: Users must authenticate before access
- **Facility Selection**: Users must select valid facility
- **Permission Check**: Role-based access control
- **Access Denial**: Clear message for unauthorized access

### 5.2 API Integration

#### 5.2.1 RESTful Endpoints
- **Base URL**: /api/company-b2b
- **HTTP Methods**: GET, POST
- **Response Format**: JSON with UTF-8 encoding
- **Error Handling**: Consistent error response structure

#### 5.2.2 Data Exchange
- **Request Format**: JSON payloads
- **Response Format**: Standardized JSON responses
- **File Upload**: Multipart form data for imports
- **File Download**: Base64 encoded data for exports

### 5.3 Database Integration

#### 5.3.1 Stored Procedures
- **Save Operation**: ws_L_CompanyB2B_Save
- **List Operation**: ws_L_CompanyB2B_Get
- **Import Operation**: ws_L_CompanyB2B_Import
- **Export Operation**: ws_L_CompanyB2B_Export

#### 5.3.2 Data Consistency
- **Transaction Management**: All operations within transactions
- **Rollback Support**: Automatic rollback on validation errors
- **Constraint Enforcement**: Database-level validation
- **Index Optimization**: Performance optimization for sorting

---

## 6. Performance and Scalability

### 6.1 Import Performance

#### 6.1.1 File Size Limits
- **Maximum Records**: 10,000 rows per import
- **Maximum File Size**: 10MB
- **Processing Time**: Optimized for large datasets
- **Memory Usage**: Efficient memory management

#### 6.1.2 Validation Performance
- **Row-by-Row Processing**: Sequential validation for accuracy
- **Early Termination**: Stops on first validation error
- **Error Collection**: Comprehensive error reporting
- **Transaction Efficiency**: Single transaction per import

### 6.2 Export Performance

#### 6.2.1 Data Retrieval
- **Efficient Queries**: Optimized database queries
- **Memory Management**: Streaming for large datasets
- **Format Conversion**: Fast JSON serialization
- **Base64 Encoding**: Efficient encoding process

#### 6.2.2 File Generation
- **Automatic Naming**: Timestamp-based file names
- **Size Calculation**: Real-time file size computation
- **Download Initiation**: Automatic file download
- **Progress Tracking**: User feedback during export

### 6.3 Search and List Performance

#### 6.3.1 Database Optimization
- **Indexed Fields**: CompanyCode, CreatedOn, ModifiedOn
- **Query Optimization**: Efficient sorting and filtering
- **Pagination Support**: Limit result sets for performance
- **Caching Strategy**: Intelligent data caching

#### 6.3.2 User Experience
- **Responsive Interface**: Fast search response times
- **Progressive Loading**: Load data as needed
- **Sorting Performance**: Efficient column sorting
- **Search Optimization**: Fast keyword search

---

## 7. Error Handling and User Experience

### 7.1 Error Message Standards

#### 7.1.1 Language Requirements
- **Primary Language**: Vietnamese for all user-facing messages
- **Error Clarity**: Clear, actionable error descriptions
- **Field Identification**: Specific field names in error messages
- **Business Context**: Error messages explain business impact

#### 7.1.2 Error Categories
- **Validation Errors**: Field-level validation failures
- **Business Rule Errors**: Rule violation messages
- **System Errors**: Technical failure messages
- **User Action Errors**: Incorrect user input messages

### 7.2 User Feedback

#### 7.2.1 Success Messages
- **Operation Confirmation**: Clear success indicators
- **Data Updates**: Automatic list refresh after operations
- **Progress Indicators**: Visual feedback during operations
- **Completion Status**: Clear indication of operation completion

#### 7.2.2 Error Recovery
- **Clear Instructions**: Step-by-step error resolution
- **Field Highlighting**: Visual indication of problematic fields
- **Help Text**: Contextual help for complex fields
- **Retry Options**: Easy retry mechanisms for failed operations

---

## 8. Compliance and Security

### 8.1 Data Security

#### 8.1.1 Access Control
- **Authentication Required**: All operations require valid login
- **Session Management**: Secure session handling
- **Permission Validation**: Role-based access control
- **Audit Logging**: Complete audit trail for all operations

#### 8.1.2 Data Protection
- **Input Validation**: Protection against injection attacks
- **File Upload Security**: Type and size validation
- **Data Encryption**: Secure data transmission
- **Access Logging**: Track all system access

### 8.2 Compliance Requirements

#### 8.2.1 Audit Trail
- **Complete Tracking**: All data changes logged
- **User Identification**: Clear identification of who made changes
- **Timestamp Recording**: Accurate timing of all operations
- **Change History**: Complete record of data modifications

#### 8.2.2 Data Integrity
- **Validation Rules**: Comprehensive data validation
- **Business Rules**: Enforced business logic
- **Constraint Enforcement**: Database-level integrity
- **Error Prevention**: Proactive error detection

---

## 9. Future Enhancements

### 9.1 Planned Features
- **Advanced Search**: Multi-criteria search with filters
- **Bulk Operations**: Multi-record selection and operations
- **Reporting**: Built-in reporting and analytics
- **Integration**: API integration with external systems

### 9.2 Scalability Improvements
- **Pagination**: Enhanced pagination for large datasets
- **Caching**: Advanced caching strategies
- **Performance**: Query optimization and indexing
- **Monitoring**: System performance monitoring

---

## 10. Success Criteria

### 10.1 Functional Requirements
- ✅ All CRUD operations work correctly
- ✅ Import/export functionality handles Vietnamese characters
- ✅ Validation rules enforce business requirements
- ✅ Audit trail captures all data changes
- ✅ User interface supports Vietnamese language

### 10.2 Performance Requirements
- ✅ Import processes 10,000 records efficiently
- ✅ Export generates files within acceptable time
- ✅ Search and list operations respond quickly
- ✅ System handles concurrent users effectively

### 10.3 User Experience Requirements
- ✅ Interface is intuitive and easy to use
- ✅ Error messages are clear and actionable
- ✅ Vietnamese language support is comprehensive
- ✅ All operations provide clear feedback

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Next Review**: [Future Date]  
**Document Owner**: Development Team  
**Stakeholders**: Business Users, Development Team, QA Team
