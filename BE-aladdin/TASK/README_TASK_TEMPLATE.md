# 🚀 Task Template: Convert Stored Procedure to Handler

## 📋 Table of Contents
- [Git Workflow](#git-workflow)
- [Technical Requirements](#technical-requirements)
- [Code Architecture Rules](#code-architecture-rules)
  - [Code Optimization Rules](#code-optimization-rules-bắt-buộc)
  - [Functional Programming Principles](#functional-programming-principles)
- [Response Patterns](#response-patterns)
- [File Structure](#file-structure)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Templates](#documentation-templates)
- [Quick Reference](#quick-reference)

---

## 🔄 Git Workflow

### Initial Setup
```bash
git checkout main
git pull
git checkout -b feat/Convert_ws_[Module]_[HandlerName]
```

### First Commit
```bash
git add -A
git commit -m "feat: Add [HandlerName] handler"
git push origin feat/Convert_ws_[Module]_[HandlerName]
```

### Subsequent Commits
```bash
git add -p
git commit --amend
git push origin -f
```

---

## 🎯 Technical Requirements

### ✅ Core Rules
- **Role**: Bạn là chuyên gia lập trình C# với kinh nghiệm về Web API và database
- **Error Handling**: Thêm try-catch và logging cẩn thận cho mọi operation
- **Code Review**: Review toàn bộ source code trước khi commit
- **File Naming**: Đặt tên file theo cấu trúc thư mục handler
- **Testing**: Bắt buộc tạo test cases cho mọi function
- **Architecture**: **Kiến trúc code phải phân tách thành các function để code gọn gàng, dễ đọc, dễ bảo trì**
- **non auto commit**: - Các commit thay đổi thì tôi tự chủ động thực hiện. 

### 📁 File Paths
- **Handler Files**: `C:\PROJECTS\aladdin\WebService.Handlers\QAHosGenericDB`
- **Test Files**: `C:\PROJECTS\aladdin\WebService.Handlers.Tests\QAHosGenericDB`
- **Test Cases**: `C:\PROJECTS\aladdin\WebService.Handlers.Tests\TestCases\QAHosGenericDB`
- **Entities**: `C:\PROJECTS\aladdin\Entities\QAHosGenericDB`
- Kiểm tra ConnectionStrings có Data Source là localhost trong file C:\PROJECTS\aladdin\WebService.Handlers.Tests\appsettings.Test.json

---

## 🔧 Code Architecture Rules

### Code Optimization Rules (BẮT BUỘC)

#### 1. Remove Redundant Functions ✅
- **Problem**: Wrapper functions that only call pure functions
- **Solution**: Call pure functions directly
- **Example**:
```csharp
// ❌ Avoid: Redundant wrapper
private string BuildDescription(string note) => BuildDescriptionPure(note);

// ✅ Use: Direct call to pure function
var description = BuildDescriptionPure(@params.Note);
```

#### 2. Remove Redundant Variables ✅
- **Problem**: Unnecessary fields that only store simple values
- **Solution**: Use direct string literals or values
- **Example**:
```csharp
// ❌ Avoid: Redundant variable
private string? _failureMessage;
_failureMessage = "Business rule validation error";
return CreateErrorResponse(2, _failureMessage ?? "Business rules validation failed");

// ✅ Use: Direct string literal
return CreateErrorResponse(2, "Business rules validation failed");
```

#### 3. Use Data Annotations Instead of Manual Validation ✅
- **Problem**: Manual validation functions that duplicate data annotation checks
- **Solution**: Use `[Required]`, `[Range]`, `[DefaultValue]` in Parameters class
- **Example**:
```csharp
// ❌ Avoid: Manual validation
private bool ValidateInput(Parameters @params)
{
    if (string.IsNullOrWhiteSpace(@params.SessionID)) return false;
    if (@params.CounterID < 0) return false;
    return true;
}

// ✅ Use: Data annotations in Parameters class
public class Parameters
{   
    [Range(0, int.MaxValue, ErrorMessage = "CounterID must be non-negative")]
    public int CounterID { get; set; }
}
```

#### 4. Eliminate Empty Functions ✅
- **Problem**: Functions that only return `true` without any logic
- **Solution**: Remove them completely
- **Example**:
```csharp
// ❌ Avoid: Empty function
private bool ValidateBusinessRules(Parameters parameters)
{
    try
    {
        // No actual validation logic
        return true;
    }
    catch (Exception ex)
    {
        Console.WriteLine($"DEBUG: Error in ValidateBusinessRules: {ex.Message}");
        return false;
    }
}

// ✅ Use: Remove completely, rely on data annotations
// All basic validations are handled by data annotations in Parameters class
```

#### 5. Direct Pure Function Calls ✅
- **Problem**: Calling pure functions through unnecessary wrappers
- **Solution**: Call pure functions directly in the main handler
- **Example**:
```csharp
// ❌ Avoid: Wrapper function
private string BuildInvoiceNo(Parameters @params) => BuildInvoiceNoPure(@params, db, dateTimeService);

// ✅ Use: Direct call in Handle method
var invoiceNo = BuildInvoiceNoPure(ExtractInvoiceCalculationData(@params), db, dateTimeService);
```

### Functional Programming Principles

#### 1. Pure Function Principle ✅
- **Definition**: Hàm không có side effects và luôn trả về cùng output cho cùng input
- **Implementation**: Tách logic tính toán thành pure functions riêng biệt
- **Benefits**: Dễ test, predictable, composable

```csharp
// Pure function example
private static decimal CalculatePaymentAmountLogic(PaymentCalculationData data)
{
    if (data.IsMuiNgoaiDanhMuc || data.IsTiemNgoai)
        return 0;
    
    return data.GiaMuiTiem + data.GiaChenhLechChuaGiam - data.TienGiam;
}
```

#### 2. Single Responsibility Principle ✅
- **Definition**: Mỗi function chỉ có một lý do để thay đổi - một trách nhiệm duy nhất
- **Implementation**: Tách riêng data extraction, business logic, database operations
- **Benefits**: Dễ maintain, test, reuse

```csharp
// Single responsibility examples
private static PaymentCalculationData ExtractPaymentData(DataRow row) { /* Data extraction only */ }
private static decimal CalculatePaymentAmountLogic(PaymentCalculationData data) { /* Calculation only */ }
private static int? GetSequenceNumberFromDatabase(SequenceLookupData data, AladdinDataConnection db) { /* DB query only */ }
```

#### 3. Immutability Principle ✅
- **Definition**: Tránh thay đổi dữ liệu trực tiếp - tạo instance mới thay thế
- **Implementation**: Sử dụng `readonly struct` với `init` properties
- **Benefits**: Predictable, thread-safe, easier debugging

```csharp
// Immutable data structure
private readonly struct PaymentCalculationData
{
    public bool IsMuiNgoaiDanhMuc { get; init; }
    public decimal GiaMuiTiem { get; init; }
    // ... other properties
}

// Returns new DataTable instead of modifying input
private DataTable CalculatePaymentAmount(DataTable resultData)
{
    var newResultData = resultData.Clone(); // Create new instance
    // ... process and return new instance
    return newResultData;
}
```

#### 4. Functional Pipeline Pattern
- **Definition**: Kết hợp các transformations qua pipeline pattern
- **Implementation**: Sử dụng extension method `Pipe<T>()`
- **Benefits**: Readable, composable, maintainable

```csharp
// Functional pipeline
var processedData = resultData
    .Pipe(data => CalculatePaymentAmount(data))           // Pure calculation
    .Pipe(data => UpdateSequenceNumber(data, db))         // Database + transformation
    .Pipe(data => UpdateContractNumber(data, db))         // Database + transformation
    .Pipe(data => UpdateUsageObjectID(data, db))          // Database + transformation
    .Pipe(data => UpdateThoiGianGianCach(data, db));      // Database + transformation
```

### 1. Function Separation (BẮT BUỘC)

#### Validation Business
```csharp
// Use Data Annotations in Parameters class for basic validation
// Only complex business logic validations should be in separate functions
// Avoid redundant ValidateInput functions that duplicate data annotation checks
```

#### Data Retrieval
```csharp
GetClinicalSession(sessionId)
GetApplicationSettings()
GetPatientData(patientId)
GetRelatedData(parameters)
```

#### Data Extraction (Pure Functions)
```csharp
ExtractPaymentData(DataRow row)           // Extract payment calculation data
ExtractSequenceData(DataRow row)          // Extract sequence lookup data
ExtractContractData(DataRow row)          // Extract contract lookup data
ExtractUsageObjectData(DataRow row)       // Extract usage object data
```

#### Business Logic (Pure Functions)
```csharp
CalculatePaymentAmountLogic(paymentData)  // Pure calculation function
ApplyBusinessLogic(data, parameters)      // Business rules application
ProcessVaccineSchedule(patientData)       // Schedule processing
ValidateVaccineCompatibility(vaccineData) // Validation logic
```

#### Database Operations
```csharp
GetSequenceNumberFromDatabase(data, db)   // Database query only
GetContractNumberFromDatabase(data, db)   // Database query only
GetUsageObjectFromDatabase(data, db)      // Database query only
```

#### Data Transformation
```csharp
CalculatePaymentAmount(dataTable)         // Transform with calculation
UpdateSequenceNumber(dataTable, db)       // Transform with DB lookup
UpdateContractNumber(dataTable, db)       // Transform with DB lookup
UpdateUsageObjectID(dataTable, db)        // Transform with DB lookup
```

#### Data Updates
```csharp
UpdateMainTable(data, userId)
UpdateRelatedTables(parameters)
UpdateHistory(action, userId)
SaveAuditLog(operation, userId)
```

#### Result Creation
```csharp
CreateResultDataSet(data)
FormatResponse(result)
BuildSuccessResponse(data)
BuildErrorResponse(message)
```

### 2. Naming Conventions

#### Function Names
- ✅ **PascalCase**: `GetClinicalSession()`, `UpdatePaymentStatus()`
- ✅ **Descriptive**: Tên function phải mô tả rõ chức năng
- ✅ **XML Documentation**: Thêm documentation cho mỗi function

#### Variable Names
- ✅ **camelCase**: `patientData`, `sessionId`
- ✅ **Meaningful**: Tên biến phải có ý nghĩa
- ✅ **Consistent**: Sử dụng nhất quán trong toàn bộ code

### 3. Code Structure Requirements

#### Database Operations
- ✅ **NoLock Hints**: `With(SqlServerHints.Table.NoLock)`
- ✅ **Single Quote**: `singleQuote: true` cho string output
- ✅ **Parameter Validation**: Validate tất cả input parameters
- ✅ **SQL Comments**: Ghi chú tương ứng với SQL Store procedure bằng tiếng Anh

#### Error Handling
- ✅ **Try-Catch**: Mọi function phải có try-catch
- ✅ **Logging**: Console.WriteLine cho debug
- ✅ **Graceful Degradation**: Xử lý lỗi một cách graceful

#### Functional Programming Requirements
- ✅ **Pure Functions**: Tách riêng logic tính toán thành pure functions (không side effects)
- ✅ **Data Extraction**: Tách riêng việc extract data từ DataRow thành functions riêng
- ✅ **Database Separation**: Tách riêng database operations thành functions riêng
- ✅ **Immutable Data**: Sử dụng `readonly struct` với `init` properties cho data structures
- ✅ **Pipeline Pattern**: Sử dụng functional pipeline để kết hợp các transformations
- ✅ **No Direct Modification**: Không thay đổi trực tiếp input data, tạo instance mới

#### Code Optimization Requirements
- ✅ **Remove Redundant Functions**: Loại bỏ wrapper functions không cần thiết (e.g., `BuildDescription()` gọi `BuildDescriptionPure()`)
- ✅ **Remove Redundant Variables**: Loại bỏ biến dư thừa (e.g., `_failureMessage` khi có thể dùng string trực tiếp)
- ✅ **Use Data Annotations**: Sử dụng `[Required]`, `[Range]`, `[DefaultValue]` thay vì validation thủ công
- ✅ **Eliminate Empty Functions**: Loại bỏ functions rỗng (e.g., `ValidateBusinessRules()` chỉ return `true`)
- ✅ **Direct Pure Function Calls**: Gọi trực tiếp pure functions thay vì qua wrapper

### 4. Development Process Rules

#### Code Standards
- ✅ **Handler Documentation**: Tuân thủ lập trình file handler theo tài liệu: `C:\PROJECTS\aladdin\HANDLERS.md`
- ✅ **SQL Comments**: Có ghi chú từ code tương ứng với SQL Store procedure (nếu có) trên code bằng tiếng Anh
- ✅ **Compilation Check**: Sau khi tạo xong, phải biên dịch lại project để kiểm tra lại
- ✅ **NoLock Hints**: Code cũng phải có `With(SqlServerHints.Table.NoLock)`
- ✅ **String Output**: Chuỗi xuất ra thì nên dùng: `singleQuote: true`
- ✅ **Logic Preservation**: Code phải đảm bảo đúng logic như store procedure

#### Functional Programming Principles (BẮT BUỘC)
- ✅ **Pure Function Principle**: Hàm không có side effects, cùng input luôn cho cùng output
- ✅ **Single Responsibility Principle**: Mỗi hàm chỉ làm một việc duy nhất
- ✅ **Immutability Principle**: Không thay đổi trực tiếp dữ liệu đầu vào, tạo instance mới

#### Code Architecture Best Practices
- ✅ **Function Separation**: Tách code thành các function nhỏ, chuyên biệt
- ✅ **Data Extraction**: Tách riêng việc extract data từ DataRow
- ✅ **Business Logic**: Tách riêng logic tính toán thành pure functions
- ✅ **Database Operations**: Tách riêng các thao tác database
- ✅ **Immutable Data Structures**: Sử dụng `readonly struct` với `init` properties
- ✅ **Functional Pipeline**: Sử dụng pipeline pattern để kết hợp các function

#### Documentation Requirements
- ✅ **README_GEN.md**: Khi có update nào trong source code thì cũng nên đồng bộ vào file `README_GEN.md`
- ✅ **Generation Report**: Sau khi hoàn tất code thì nên sinh ra file `README_GEN.md` giống với file mẫu trong cùng thư mục
- ✅ **Process Summary**: Tóm tắt các bước sau khi tạo file vào file `README_GEN.md`
- ✅ **File Links**: Trong file `README_GEN.md` có thêm các đường dẫn testcase mà đã gen ra để có thể click vào đúng file nhanh chóng

#### Development Workflow
- ✅ **Parameters Class**: Nên tạo lớp `Parameters` cho việc làm tham số handle `public override DataSet Handle(Parameters @params)`. Tham thảo như file: `ws_MDM_Patient_CheckExists.cs`
- ✅ **Entity Validation**: Khi tạo các test case mà có phát sinh lỗi thì check lại các fields trong các class entity trong thư mục: `C:\PROJECTS\aladdin\Entities\QAHosGenericDB` để cần lấy entity tương ứng
- ✅ **Quick Development**: Xử lý ra code nhanh
- ✅ **Pre-Analysis**: Sau khi suy luận ra các đầy đủ thông tin, thì tạo 1 file `README_TODO_BEFORE_GEN.md` để tập hợp đầy đủ các thông tin mà đã suy luận, và đầy đủ thông tin để file này làm cơ sở gen ra code
- ✅ **Compile First**: Khi biên dịch file code handler chạy ổn thì mới tạo code cho các file test case
- ✅ **Test Verification**: Sau khi gen ra các file test case xong, thì chạy để testing lại các test case đó để pass được hết các file

## 📋 Response Patterns

### 0. Standardized Error Response Helper (Required)
Implement a centralized error response and validation pattern in handlers:

```csharp
// 2) Input validation - Use Data Annotations instead of manual validation
// All basic validations should be handled by [Required], [Range], [DefaultValue] in Parameters class
// Only complex business logic validations should be in separate functions

// 3) Standardized error response (table with errorCode/errorMsg)
private DataSet CreateErrorResponse(int errorCode, string errorMsg)
{
    var ds = new DataSet();
    ds.Tables.Add(DataUtils.CreateDataTable(new { errorCode, errorMsg }));
    return ds;
}

// 4) Usage in Handle()
var userId = AuthenticateUser(@params.SessionID);
if (userId == null) return CreateErrorResponse(1, "Session ID is not valid");
// All basic validations are handled by data annotations in Parameters class

// For system errors, throw AppException(500, ...)
```

### 1. Authentication & Authorization Errors
```csharp
// Pattern 1: Return empty DataSet for auth failures (NO message in response)
Guid? userId = AuthenticateUser(@params.SessionID);
if (userId == null)
{
    _failureMessage = $"Session ID '{@params.SessionID}' is not valid.";
    return new DataSet(); // Empty DataSet for auth failure - client gets no data
}

// Pattern 2: Return DataSet with errorCode/errorMsg properties (Recommended) (WITH message in response)
Guid? userId = AuthenticateUser(@params.SessionID);
if (userId == null)
{
    _failureMessage = $"Session ID '{@params.SessionID}' is not valid.";
    var dataSet = new DataSet();
    dataSet.Tables.Add(DataUtils.CreateDataTable(new { errorCode = 1, errorMsg = "Session ID is not valid" }));
    return dataSet;
}
```

### 2. Business Logic Validation Errors
```csharp
// Pattern 1: Return DataSet with Results property for business validation (WITH message in response)
if (!isValid)
{
    return new List<object> { new { Results = "Error message" } }.ToDataSet();
}

// Pattern 2: Return DataSet with errorCode/errorMsg properties (Recommended) (WITH message in response)
if (!isValid)
{
    var dataSet = new DataSet();
    dataSet.Tables.Add(DataUtils.CreateDataTable(new { errorCode = 2, errorMsg = "Error message" }));
    return dataSet;
}
```

### 3. System/Technical Errors
```csharp
// Pattern: Throw AppException for system errors
catch (Exception ex)
{
    Console.WriteLine($"DEBUG: Exception in HandlerName: {ex.Message}");
    throw new AppException(500, "Có lỗi khi thực hiện chức năng");
}
```

### 4. No Data Found
```csharp
// Pattern 1: Return empty DataSet when no data matches criteria
if (!data.Any())
{
    return new DataSet(); // Empty DataSet for no data found
}

// Pattern 2: Return DataSet with errorCode/errorMsg properties (Recommended) - NOT an error, just no data
if (!data.Any())
{
    var dataSet = new DataSet();
    dataSet.Tables.Add(DataUtils.CreateDataTable(new { errorCode = 3, errorMsg = "No data found" }));
    return dataSet;
}
```

### 5. Success Responses
```csharp
// Pattern 1: Return DataSet with actual data
return query.ToDataSet();

// Pattern 2: Return DataSet with Results property
return new List<object> { new { Results = "Ok" } }.ToDataSet();

// Pattern 3: Return DataSet with errorCode/errorMsg properties (Recommended) - errorCode = 0 means success
var dataSet = new DataSet();
dataSet.Tables.Add(DataUtils.CreateDataTable(new { errorCode = 0, errorMsg = "Success" }));
return dataSet;

// Pattern 4: Return DataSet with success result and data
return new List<object> { new { Result = 1, Data = result } }.ToDataSet();
```

### 7. Error Code Convention
| Error Code | Meaning | Description |
|------------|---------|-------------|
| 0 | Success | Operation completed successfully |
| 1 | Authentication Failure | Session ID is not valid or user not authenticated |
| 2 | Business Validation Error | Business logic validation failed |
| 3 | No Data Found | No data matches criteria (NOT an error, just no data) |
| 4+ | System/Technical Error | Reserved for future system errors |

### 8. Response Pattern Summary
| Scenario | Response Type | Pattern |
|----------|---------------|---------|
| Authentication failures | ErrorCode/ErrorMsg DataSet | `{ errorCode = 1, errorMsg = "Session ID is not valid" }` |
| Business validation errors | ErrorCode/ErrorMsg DataSet | `{ errorCode = 2, errorMsg = "message" }` |
| No data found | ErrorCode/ErrorMsg DataSet | `{ errorCode = 3, errorMsg = "No data found" }` (NOT an error) |
| System/technical errors | AppException | `throw new AppException(500, "message")` |
| Success with data | ErrorCode/ErrorMsg DataSet | `{ errorCode = 0, errorMsg = "Success" }`|

---

## 🏗️ File Structure

### 1. Function Structure Template

#### Standard Function Template
```csharp
/// <summary>
/// Mô tả chức năng của function
/// </summary>
/// <param name="paramName">Mô tả parameter</param>
/// <returns>Mô tả return value</returns>
private ReturnType FunctionName(ParameterType paramName)
{
    try
    {
        // Logic implementation
        return result;
    }
    catch (Exception ex)
    {
        Console.WriteLine($"DEBUG: Error in FunctionName: {ex.Message}");
        throw;
    }
}
```

#### Pure Function Template (Recommended)
```csharp
/// <summary>
/// Pure function - no side effects, same output for same input
/// </summary>
/// <param name="data">Input data</param>
/// <returns>Calculated result</returns>
private static ReturnType PureFunctionName(InputDataType data)
{
    // Pure calculation logic - no side effects
    return calculatedResult;
}
```

#### Data Extraction Function Template
```csharp
/// <summary>
/// Extracts data from DataRow (Pure function)
/// </summary>
/// <param name="row">DataRow containing data</param>
/// <returns>Extracted data structure</returns>
private static DataStructure ExtractDataFromRow(DataRow row)
{
    return new DataStructure
    {
        Property1 = Convert.ToType(row["ColumnName1"]),
        Property2 = Convert.ToType(row["ColumnName2"]),
        // ... other properties
    };
}
```

#### Immutable Data Structure Template
```csharp
/// <summary>
/// Immutable data structure for type safety
/// </summary>
private readonly struct DataStructure
{
    public Type1 Property1 { get; init; }
    public Type2 Property2 { get; init; }
    // ... other properties
}
```

#### Functional Pipeline Template
```csharp
// Extension method for functional pipeline
public static class FunctionalExtensions
{
    public static T Pipe<T>(this T input, Func<T, T> func) => func(input);
}

// Usage in main handler
var processedData = inputData
    .Pipe(data => ExtractData(data))
    .Pipe(data => CalculateBusinessLogic(data))
    .Pipe(data => TransformData(data, db))
    .Pipe(data => CreateResult(data));
```

### 2. Main Handler Structure Template

#### Standard Handler Template
```csharp
public override DataSet Handle(Parameters @params)
{
    try
    {
        // 1. Authentication & Validation
        var userID = AuthenticateUser(@params.SessionID);
        if (userID == Guid.Empty) return new DataSet();

        // 2. Get Data
        var mainData = GetMainData(@params);
        if (mainData == null) return new DataSet();

        // 3. Apply Business Logic
        ApplyBusinessLogic(@params, mainData);

        // 4. Update Data
        UpdateMainData(@params, userID);
        UpdateRelatedData(@params);

        // 5. Return Result
        return CreateResultDataSet();
    }
    catch (Exception ex)
    {
        Console.WriteLine($"DEBUG: Exception occurred: {ex.Message}");
        return new DataSet();
    }
}
```

#### Functional Handler Template (Recommended)
```csharp
public override DataSet Handle(Parameters @params)
{
    try
    {
        // 1. Get initial data
        var resultData = GetContractDetailData(@params);
        if (resultData == null || resultData.Rows.Count == 0)
        {
            return CreateEmptyDataSet();
        }

        // 2. Process data through functional pipeline
        var processedData = resultData
            .Pipe(data => CalculatePaymentAmount(data))           // Pure calculation
            .Pipe(data => UpdateSequenceNumber(data, db))         // Database + transformation
            .Pipe(data => UpdateContractNumber(data, db))         // Database + transformation
            .Pipe(data => UpdateUsageObjectID(data, db))          // Database + transformation
            .Pipe(data => UpdateThoiGianGianCach(data, db));      // Database + transformation

        // 3. Return result
        return CreateResultDataSet(processedData);
    }
    catch (Exception ex)
    {
        Console.WriteLine($"DEBUG: Exception occurred: {ex.Message}");
        return CreateEmptyDataSet();
    }
}
```

### 3. Parameters Class Template
```csharp
public class Parameters
{
    [Required(ErrorMessage = "Param1 is required")]
    [DefaultValue("")]
    public string Param1 { get; set; } = string.Empty;
    
    [DefaultValue(0)]
    [Range(0, int.MaxValue, ErrorMessage = "Param2 must be non-negative")]
    public int Param2 { get; set; }
    
    // Add other parameters with appropriate data annotations
    // Use [Required], [Range], [DefaultValue] for validation
}
```

---

## 🧪 Testing Guidelines

### 1. Test Cases Requirements
- ✅ **Basic Tests**: Authentication, validation, happy path
- ✅ **Business Logic Tests**: Các trường hợp đặc biệt của business rules
- ✅ **Error Tests**: Invalid input, missing data, exceptions
- ✅ **Edge Tests**: Boundary values, null values
- ✅ **Integration Tests**: Multiple tables, complex workflows

### 2. Test Case Structure
```yaml
# Test case: Mô tả test case
initialData:
  - database: DatabaseName
    table: TableName
    rows:
      - Field1: "value1"
        Field2: "value2"

parameters:
  Param1: "value1"
  Param2: "value2"

expectedResult:
  Table1:
    - Result: "Expected result"

expectedData:
  - database: DatabaseName
    table: TableName
    rows:
      - Field1: "expected_value"
```

### 3. Testing Process
1. **Compile Handler**: Đảm bảo handler compile thành công
2. **Create Test Cases**: Tạo test cases cho từng scenario
3. **Run Tests**: Chạy và verify tất cả test cases pass
4. **Debug Issues**: Fix lỗi nếu có và re-run tests

---

## 📝 Documentation Templates

### 1. README_TODO_BEFORE_GEN.md Template
```markdown
# TODO: [Handler Name] - Pre-Generation Analysis

## Handler Information
- **Handler Name**: [Name]
- **Original SP**: [Stored Procedure Name]
- **Purpose**: [Brief description]

## Analysis Results
### Business Logic
- [Logic point 1]
- [Logic point 2]

### Required Functions
- [ ] `AuthenticateUser()`
- [ ] `ValidateInput()`
- [ ] `GetMainData()`
- [ ] `ApplyBusinessLogic()`
- [ ] `UpdateData()`
- [ ] `CreateResultDataSet()`

### Required Entities
- [Entity 1]: [Purpose]
- [Entity 2]: [Purpose]

### Test Scenarios
- [ ] Happy path
- [ ] Authentication failure
- [ ] Validation error
- [ ] Business logic error
- [ ] No data found
- [ ] System error

## Notes
[Additional notes and considerations]
```

### 2. README_GEN.md Template
```markdown
# [Handler Name] - Refactoring Report

## Overview
Handler `[HandlerName]` đã được refactor để tách thành các function nhỏ, dễ đọc và dễ test hơn.

## Changes Made

### 1. Code Refactoring
- **Tách code thành các function riêng biệt:**
  - `AuthenticateUser()`: Xác thực người dùng
  - `ValidateInput()`: Validate input parameters
  - `GetMainData()`: Lấy dữ liệu chính
  - `ApplyBusinessLogic()`: Áp dụng business logic
  - `UpdateData()`: Cập nhật dữ liệu
  - `CreateResultDataSet()`: Tạo kết quả trả về

### 2. Benefits of Refactoring
- **Dễ đọc:** Code được chia thành các function có tên rõ ràng
- **Dễ test:** Mỗi function có thể được test riêng biệt
- **Dễ maintain:** Logic được tách biệt, dễ sửa đổi từng phần
- **Dễ debug:** Có thể debug từng function riêng lẻ
- **Reusable:** Các function có thể được tái sử dụng

### 3. Test Cases Created
- **File**: `[TestFileName].cs`
- **YAML**: `[TestFileName].yml`
- **Scenarios**: [List of test scenarios]

### 4. Business Logic Preserved
- Tất cả business logic gốc được giữ nguyên
- Logic tương ứng với SQL Store procedure

### 5. Performance Considerations
- Vẫn sử dụng NoLock hints cho performance
- Không thay đổi logic query, chỉ tách thành function

## File Links
- **Handler**: `[HandlerPath]`
- **Test**: `[TestPath]`
- **Test Cases**: `[TestCasesPath]`

## Conclusion
Việc refactor đã thành công với các lợi ích đạt được.
```

---

## ⚡ Quick Reference

### Development Checklist
- [ ] Analyze stored procedure logic
- [ ] Create README_TODO_BEFORE_GEN.md
- [ ] Design function separation following 3 principles:
  - [ ] Pure Function: Tách logic tính toán thành pure functions
  - [ ] Single Responsibility: Mỗi function chỉ làm một việc
  - [ ] Immutability: Không thay đổi input data trực tiếp
- [ ] Implement handler with functional pipeline pattern
- [ ] Create immutable data structures (`readonly struct`)
- [ ] Add try-catch and logging
- [ ] **Code Optimization Review**:
  - [ ] Remove redundant wrapper functions (e.g., `BuildDescription()` calling `BuildDescriptionPure()`)
  - [ ] Remove redundant variables (e.g., `_failureMessage` when direct strings can be used)
  - [ ] Use Data Annotations instead of manual validation
  - [ ] Eliminate empty functions (e.g., `ValidateBusinessRules()` that only return `true`)
- [ ] Compile and test handler
- [ ] Create test cases
- [ ] Run all tests
- [ ] Create README_GEN.md
- [ ] Commit and push changes

### Common Patterns

#### Response Patterns
- **Validation (Old)**: `if (!isValid) return new List<object> { new { Results = "message" } }.ToDataSet();`
- **Validation (New)**: `if (!isValid) return CreateErrorResponse(2, "message");`
- **Success (Old)**: `return new List<object> { new { Results = "Ok" } }.ToDataSet();`
- **Success (New)**: `return CreateSuccessResponse(data);`
- **No Data (Old)**: `if (!data.Any()) return new DataSet();`
- **No Data (New)**: `if (!data.Any()) return CreateErrorResponse(3, "No data found");`

#### Code Optimization Patterns
- **Remove Redundant Functions**: Avoid wrapper functions that only call pure functions (e.g., `BuildDescription()` calling `BuildDescriptionPure()`)
- **Remove Redundant Variables**: Avoid unnecessary fields like `_failureMessage` when direct string literals can be used
- **Use Data Annotations**: Replace manual validation with `[Required]`, `[Range]`, `[DefaultValue]` in Parameters class
- **Eliminate Empty Functions**: Remove functions like `ValidateBusinessRules()` that only return `true` without any logic

#### Functional Programming Patterns
- **Data Extraction**: `private static DataStructure ExtractData(DataRow row) => new DataStructure { Property = Convert.ToType(row["Column"]) };`
- **Pure Function**: `private static decimal CalculateLogic(DataStructure data) => data.Condition ? 0 : data.Value1 + data.Value2;`
- **Immutable Struct**: `private readonly struct DataStructure { public Type Property { get; init; } }`
- **Pipeline Pattern**: `var result = data.Pipe(ExtractData).Pipe(CalculateLogic).Pipe(TransformData);`
- **Database Operation**: `private static Type? GetFromDatabase(LookupData data, AladdinDataConnection db) => db.Table.Where(...).Select(...).FirstOrDefault();`

#### Code Optimization Patterns
- **Remove Wrapper**: `// Instead of: BuildDescription() calling BuildDescriptionPure()`
- **Direct Call**: `// Use: BuildDescriptionPure() directly`
- **Remove Redundant Variable**: `// Instead of: _failureMessage = "error"; return _failureMessage;`
- **Direct String**: `// Use: return "error"; directly`
- **Data Annotations**: `[Required(ErrorMessage = "Field is required")]` instead of manual validation
- **Eliminate Empty Functions**: Remove functions that only return `true` without logic

### File Naming Convention
- **Handler**: `ws_[Module]_[FunctionName].cs`
- **Test**: `ws_[Module]_[FunctionName]Tests.cs`
- **YAML**: `ws_[Module]_[FunctionName].yml`
