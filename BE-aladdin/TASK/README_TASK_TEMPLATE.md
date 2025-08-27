# 🚀 Task Template: Convert Stored Procedure to Handler

## 📋 Table of Contents
- [Git Workflow](#git-workflow)
- [Technical Requirements](#technical-requirements)
- [Code Architecture Rules](#code-architecture-rules)
  - [Code Optimization Rules](#code-optimization-rules-bắt-buộc)
  - [Functional Programming Principles](#functional-programming-principles)
- [Response Patterns](#response-patterns)
- [Stored Procedure Conversion Guidelines](#stored-procedure-conversion-guidelines)
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
- **Stored Procedure Conversion**: **Phải convert đúng giá trị trả ra như store procedure gốc**

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
return new DataSet(); // Return empty DataSet for business validation error

// ✅ Use: Direct return
return new DataSet(); // Return empty DataSet for business validation error
```

#### 3. Use Data Annotations Instead of Manual Validation ✅
- **Problem**: Manual validation functions that duplicate data annotation checks
- **Solution**: Use `[Required]`, `[Range]`, `[DefaultValue]` in Parameters class
- **Example**:
```csharp
// ❌ Avoid: Manual validation
private bool ValidateInput(Parameters @params)
{
    if (string.IsNullOrWhiteSpace(@params.CounterID)) return false;
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
```

### 2. Naming Conventions

#### Function Names
- ✅ **PascalCase**: `GetApplicationSettings()`, `UpdatePaymentStatus()`
- ✅ **Descriptive**: Tên function phải mô tả rõ chức năng
- ✅ **XML Documentation**: Thêm documentation cho mỗi function

#### Variable Names
- ✅ **camelCase**: `patientData`
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
- ✅ **Return Value Conversion**: Phải convert đúng giá trị trả ra như store procedure gốc

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

### 1. Business Logic Validation Errors
```csharp
// Pattern: Return empty DataSet for business validation errors
if (!isValid)
{
    return new DataSet(); // Empty DataSet for business validation error
}
```

### 2. System/Technical Errors
```csharp
// Pattern: Throw AppException for system errors
catch (Exception ex)
{
    Console.WriteLine($"DEBUG: Exception in HandlerName: {ex.Message}");
    throw new AppException(500, "Có lỗi khi thực hiện chức năng");
}
```

### 3. No Data Found
```csharp
// Pattern: Return empty DataSet when no data matches criteria
if (!data.Any())
{
    return new DataSet(); // Empty DataSet for no data found
}
```

### 4. Success Responses
```csharp
// Pattern 1: Return DataSet with actual data (Recommended)
return query.ToDataSet();

// Pattern 2: Return DataSet with Results property
return new List<object> { new { Results = "Ok" } }.ToDataSet();

// Pattern 3: Return DataSet with success result and data
return new List<object> { new { Result = 1, Data = result } }.ToDataSet();
```

### 5. Response Pattern Summary
| Scenario | Response Type | Pattern |
|----------|---------------|---------|
| Business validation errors | Empty DataSet | `return new DataSet();` |
| No data found | Empty DataSet | `return new DataSet();` |
| System/technical errors | AppException | `throw new AppException(500, "message")` |
| Success with data | DataSet with data | `return query.ToDataSet();` |

---

## 🔄 Stored Procedure Conversion Guidelines

### 1. Return Value Conversion (BẮT BUỘC)

#### Data Type Mapping
```csharp
// SQL Server to C# Data Type Mapping
// SQL Server Type -> C# Type -> Conversion Method

// String types
NVARCHAR(MAX) -> string -> Convert.ToString(row["ColumnName"])
VARCHAR(MAX) -> string -> Convert.ToString(row["ColumnName"])
CHAR(n) -> string -> Convert.ToString(row["ColumnName"])

// Numeric types
INT -> int -> Convert.ToInt32(row["ColumnName"])
BIGINT -> long -> Convert.ToInt64(row["ColumnName"])
DECIMAL(p,s) -> decimal -> Convert.ToDecimal(row["ColumnName"])
FLOAT -> double -> Convert.ToDouble(row["ColumnName"])
BIT -> bool -> Convert.ToBoolean(row["ColumnName"])

// Date/Time types
DATETIME -> DateTime -> Convert.ToDateTime(row["ColumnName"])
DATETIME2 -> DateTime -> Convert.ToDateTime(row["ColumnName"])
DATE -> DateTime -> Convert.ToDateTime(row["ColumnName"])

// Nullable types
INT -> int? -> row["ColumnName"] == DBNull.Value ? null : Convert.ToInt32(row["ColumnName"])
DECIMAL -> decimal? -> row["ColumnName"] == DBNull.Value ? null : Convert.ToDecimal(row["ColumnName"])
```

#### Safe Conversion Methods
```csharp
// Safe conversion with null handling
private static string SafeGetString(DataRow row, string columnName)
{
    return row[columnName] == DBNull.Value ? string.Empty : Convert.ToString(row[columnName]);
}

private static int? SafeGetInt32(DataRow row, string columnName)
{
    return row[columnName] == DBNull.Value ? null : Convert.ToInt32(row[columnName]);
}

private static decimal? SafeGetDecimal(DataRow row, string columnName)
{
    return row[columnName] == DBNull.Value ? null : Convert.ToDecimal(row[columnName]);
}

private static DateTime? SafeGetDateTime(DataRow row, string columnName)
{
    return row[columnName] == DBNull.Value ? null : Convert.ToDateTime(row[columnName]);
}

private static bool SafeGetBoolean(DataRow row, string columnName)
{
    return row[columnName] != DBNull.Value && Convert.ToBoolean(row[columnName]);
}
```

#### Data Extraction Function Template
```csharp
/// <summary>
/// Extracts data from DataRow with proper type conversion (Pure function)
/// </summary>
/// <param name="row">DataRow containing data</param>
/// <returns>Extracted data structure</returns>
private static DataStructure ExtractDataFromRow(DataRow row)
{
    return new DataStructure
    {
        // String fields
        Name = SafeGetString(row, "Name"),
        Description = SafeGetString(row, "Description"),
        
        // Numeric fields
        Id = SafeGetInt32(row, "Id") ?? 0,
        Amount = SafeGetDecimal(row, "Amount") ?? 0m,
        Quantity = SafeGetInt32(row, "Quantity") ?? 0,
        
        // Boolean fields
        IsActive = SafeGetBoolean(row, "IsActive"),
        
        // DateTime fields
        CreatedDate = SafeGetDateTime(row, "CreatedDate") ?? DateTime.MinValue,
        UpdatedDate = SafeGetDateTime(row, "UpdatedDate"),
        
        // Nullable fields
        OptionalId = SafeGetInt32(row, "OptionalId"),
        OptionalAmount = SafeGetDecimal(row, "OptionalAmount")
    };
}
```

### 2. Stored Procedure Output Parameter Handling

#### Output Parameter Conversion
```csharp
// For stored procedures with OUTPUT parameters
// Convert OUTPUT parameters to return values

// Example: SP with OUTPUT parameter
// CREATE PROCEDURE GetPatientInfo @PatientId INT, @PatientName NVARCHAR(100) OUTPUT
// AS
// BEGIN
//     SET @PatientName = (SELECT Name FROM Patients WHERE Id = @PatientId)
// END

// C# Handler equivalent
public override DataSet Handle(Parameters @params)
{
    try
    {
        var result = db.GetPatientInfo(@params.PatientId, out string patientName);
        
        // Convert OUTPUT parameter to DataSet
        var dataSet = new DataSet();
        var dataTable = new DataTable("Result");
        dataTable.Columns.Add("PatientName", typeof(string));
        dataTable.Rows.Add(patientName);
        dataSet.Tables.Add(dataTable);
        
        return dataSet;
    }
    catch (Exception ex)
    {
        Console.WriteLine($"DEBUG: Exception in GetPatientInfo: {ex.Message}");
        throw new AppException(500, "Có lỗi khi lấy thông tin bệnh nhân");
    }
}
```

### 3. Multiple Result Sets Handling

#### Multiple DataTable Conversion
```csharp
// For stored procedures returning multiple result sets
// Convert each result set to separate DataTable

public override DataSet Handle(Parameters @params)
{
    try
    {
        var dataSet = new DataSet();
        
        // First result set - Patient information
        var patientData = db.GetPatientData(@params.PatientId);
        dataSet.Tables.Add(patientData);
        
        // Second result set - Patient history
        var historyData = db.GetPatientHistory(@params.PatientId);
        dataSet.Tables.Add(historyData);
        
        // Third result set - Patient medications
        var medicationData = db.GetPatientMedications(@params.PatientId);
        dataSet.Tables.Add(medicationData);
        
        return dataSet;
    }
    catch (Exception ex)
    {
        Console.WriteLine($"DEBUG: Exception in GetPatientCompleteInfo: {ex.Message}");
        throw new AppException(500, "Có lỗi khi lấy thông tin đầy đủ bệnh nhân");
    }
}
```

### 4. Return Value Validation

#### Data Validation After Conversion
```csharp
/// <summary>
/// Validates converted data matches expected format
/// </summary>
/// <param name="data">Converted data</param>
/// <returns>True if valid, false otherwise</returns>
private static bool ValidateConvertedData(DataStructure data)
{
    // Validate required fields
    if (string.IsNullOrWhiteSpace(data.Name))
        return false;
    
    // Validate numeric ranges
    if (data.Amount < 0)
        return false;
    
    // Validate date ranges
    if (data.CreatedDate > DateTime.Now)
        return false;
    
    return true;
}
```

### 5. Error Handling for Conversion

#### Conversion Error Handling
```csharp
/// <summary>
/// Safe conversion with error handling
/// </summary>
/// <param name="row">DataRow containing data</param>
/// <param name="columnName">Column name to convert</param>
/// <returns>Converted value or default</returns>
private static T SafeConvert<T>(DataRow row, string columnName, T defaultValue = default(T))
{
    try
    {
        if (row[columnName] == DBNull.Value)
            return defaultValue;
        
        return (T)Convert.ChangeType(row[columnName], typeof(T));
    }
    catch (Exception ex)
    {
        Console.WriteLine($"DEBUG: Conversion error for column {columnName}: {ex.Message}");
        return defaultValue;
    }
}
```

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

#### Data Extraction Function Template with Safe Conversion
```csharp
/// <summary>
/// Extracts data from DataRow with safe conversion (Pure function)
/// </summary>
/// <param name="row">DataRow containing data</param>
/// <returns>Extracted data structure</returns>
private static DataStructure ExtractDataFromRow(DataRow row)
{
    return new DataStructure
    {
        // Use safe conversion methods
        Property1 = SafeGetString(row, "ColumnName1"),
        Property2 = SafeGetInt32(row, "ColumnName2") ?? 0,
        Property3 = SafeGetDecimal(row, "ColumnName3") ?? 0m,
        Property4 = SafeGetDateTime(row, "ColumnName4") ?? DateTime.MinValue,
        Property5 = SafeGetBoolean(row, "ColumnName5")
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
    public string Property1 { get; init; }
    public int Property2 { get; init; }
    public decimal Property3 { get; init; }
    public DateTime Property4 { get; init; }
    public bool Property5 { get; init; }
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
        // 1. Get Data
        var mainData = GetMainData(@params);
        if (mainData == null) return new DataSet();

        // 2. Apply Business Logic
        ApplyBusinessLogic(@params, mainData);

        // 3. Update Data
        UpdateMainData(@params, userID);
        UpdateRelatedData(@params);

        // 4. Return Result
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
            return new DataSet(); // Empty DataSet for no data
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
        return new DataSet(); // Empty DataSet for error
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
- ✅ **Basic Tests**: Validation, happy path
- ✅ **Business Logic Tests**: Các trường hợp đặc biệt của business rules
- ✅ **Error Tests**: Invalid input, missing data, exceptions
- ✅ **Edge Tests**: Boundary values, null values
- ✅ **Integration Tests**: Multiple tables, complex workflows
- ✅ **Data Conversion Tests**: Verify proper type conversion from stored procedure

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
5. **Verify Data Conversion**: Kiểm tra conversion đúng như stored procedure

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
- [ ] `ValidateInput()`
- [ ] `GetMainData()`
- [ ] `ApplyBusinessLogic()`
- [ ] `UpdateData()`
- [ ] `CreateResultDataSet()`

### Required Entities
- [Entity 1]: [Purpose]
- [Entity 2]: [Purpose]

### Stored Procedure Conversion
- **Return Types**: [List of return data types]
- **Output Parameters**: [List of OUTPUT parameters if any]
- **Multiple Result Sets**: [Yes/No - if yes, describe each result set]

### Test Scenarios
- [ ] Happy path
- [ ] Validation error
- [ ] Business logic error
- [ ] No data found
- [ ] System error
- [ ] Data conversion edge cases

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
  - `ValidateInput()`: Validate input parameters
  - `GetMainData()`: Lấy dữ liệu chính
  - `ApplyBusinessLogic()`: Áp dụng business logic
  - `UpdateData()`: Cập nhật dữ liệu
  - `CreateResultDataSet()`: Tạo kết quả trả về

### 2. Stored Procedure Conversion
- **Data Type Mapping**: Đã map đúng các kiểu dữ liệu từ SQL Server sang C#
- **Safe Conversion**: Sử dụng safe conversion methods để xử lý null values
- **Return Value Preservation**: Đảm bảo giá trị trả về giống hệt stored procedure gốc

### 3. Benefits of Refactoring
- **Dễ đọc:** Code được chia thành các function có tên rõ ràng
- **Dễ test:** Mỗi function có thể được test riêng biệt
- **Dễ maintain:** Logic được tách biệt, dễ sửa đổi từng phần
- **Dễ debug:** Có thể debug từng function riêng lẻ
- **Reusable:** Các function có thể được tái sử dụng
- **Type Safe:** Sử dụng safe conversion methods để tránh runtime errors

### 4. Test Cases Created
- **File**: `[TestFileName].cs`
- **YAML**: `[TestFileName].yml`
- **Scenarios**: [List of test scenarios]

### 5. Business Logic Preserved
- Tất cả business logic gốc được giữ nguyên
- Logic tương ứng với SQL Store procedure
- Return values được convert đúng như stored procedure gốc

### 6. Performance Considerations
- Vẫn sử dụng NoLock hints cho performance
- Không thay đổi logic query, chỉ tách thành function
- Safe conversion methods không ảnh hưởng performance

## File Links
- **Handler**: `[HandlerPath]`
- **Test**: `[TestPath]`
- **Test Cases**: `[TestCasesPath]`

## Conclusion
Việc refactor đã thành công với các lợi ích đạt được và đảm bảo conversion đúng như stored procedure gốc.
```

---

## ⚡ Quick Reference

### Development Checklist
- [ ] Analyze stored procedure logic and return values
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
- [ ] **Stored Procedure Conversion Review**:
  - [ ] Verify data type mapping from SQL Server to C#
  - [ ] Implement safe conversion methods for null handling
  - [ ] Test return value conversion matches stored procedure
  - [ ] Handle OUTPUT parameters if any
  - [ ] Handle multiple result sets if any
- [ ] Compile and test handler
- [ ] Create test cases
- [ ] Run all tests
- [ ] Create README_GEN.md
- [ ] Commit and push changes

### Common Patterns

#### Response Patterns (Updated)
- **Validation Error**: `if (!isValid) return new DataSet();`
- **Success**: `return query.ToDataSet();`
- **No Data**: `if (!data.Any()) return new DataSet();`
- **System Error**: `throw new AppException(500, "message");`

#### Code Optimization Patterns
- **Remove Redundant Functions**: Avoid wrapper functions that only call pure functions (e.g., `BuildDescription()` calling `BuildDescriptionPure()`)
- **Remove Redundant Variables**: Avoid unnecessary fields like `_failureMessage` when direct string literals can be used
- **Use Data Annotations**: Replace manual validation with `[Required]`, `[Range]`, `[DefaultValue]` in Parameters class
- **Eliminate Empty Functions**: Remove functions like `ValidateBusinessRules()` that only return `true` without any logic

#### Functional Programming Patterns
- **Data Extraction**: `private static DataStructure ExtractData(DataRow row) => new DataStructure { Property = SafeGetString(row, "Column") };`
- **Pure Function**: `private static decimal CalculateLogic(DataStructure data) => data.Condition ? 0 : data.Value1 + data.Value2;`
- **Immutable Struct**: `private readonly struct DataStructure { public Type Property { get; init; } }`
- **Pipeline Pattern**: `var result = data.Pipe(ExtractData).Pipe(CalculateLogic).Pipe(TransformData);`
- **Database Operation**: `private static Type? GetFromDatabase(LookupData data, AladdinDataConnection db) => db.Table.Where(...).Select(...).FirstOrDefault();`

#### Stored Procedure Conversion Patterns
- **Safe String Conversion**: `SafeGetString(row, "ColumnName")`
- **Safe Numeric Conversion**: `SafeGetInt32(row, "ColumnName") ?? 0`
- **Safe Decimal Conversion**: `SafeGetDecimal(row, "ColumnName") ?? 0m`
- **Safe DateTime Conversion**: `SafeGetDateTime(row, "ColumnName") ?? DateTime.MinValue`
- **Safe Boolean Conversion**: `SafeGetBoolean(row, "ColumnName")`
- **Null Handling**: `row["ColumnName"] == DBNull.Value ? defaultValue : Convert.ToType(row["ColumnName"])`

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
