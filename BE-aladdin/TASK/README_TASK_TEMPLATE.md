# 🚀 Task Template: Convert Stored Procedure to Handler

## 📋 Table of Contents
- [Git Workflow](#git-workflow)
- [Technical Requirements](#technical-requirements)
- [Code Architecture Rules](#code-architecture-rules)
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

### 1. Function Separation (BẮT BUỘC)

#### Authentication & Validation
```csharp
AuthenticateUser(sessionId)
ValidateInput(parameters)
ValidateBusinessRules(data)
```

#### Data Retrieval
```csharp
GetClinicalSession(sessionId)
GetApplicationSettings()
GetPatientData(patientId)
GetRelatedData(parameters)
```

#### Business Logic
```csharp
ApplyBusinessLogic(data, parameters)
CalculatePayment(amount, discount)
ProcessVaccineSchedule(patientData)
ValidateVaccineCompatibility(vaccineData)
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

### 4. Development Process Rules

#### Code Standards
- ✅ **Handler Documentation**: Tuân thủ lập trình file handler theo tài liệu: `C:\PROJECTS\aladdin\HANDLERS.md`
- ✅ **SQL Comments**: Có ghi chú từ code tương ứng với SQL Store procedure (nếu có) trên code bằng tiếng Anh
- ✅ **Compilation Check**: Sau khi tạo xong, phải biên dịch lại project để kiểm tra lại
- ✅ **NoLock Hints**: Code cũng phải có `With(SqlServerHints.Table.NoLock)`
- ✅ **String Output**: Chuỗi xuất ra thì nên dùng: `singleQuote: true`
- ✅ **Logic Preservation**: Code phải đảm bảo đúng logic như store procedure

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

### 6. Authentication Handler Pattern
```csharp
// Add _failureMessage field to track authentication failures
private string? _failureMessage;

// Set failure message when authentication fails
if (userId == null)
{
    _failureMessage = $"Session ID '{sessionId}' is not valid.";
    return new DataSet();
}
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

### 2. Main Handler Structure Template
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

### 3. Parameters Class Template
```csharp
public class Parameters
{
    public string SessionID { get; set; } = string.Empty;
    public string Param1 { get; set; } = string.Empty;
    public int Param2 { get; set; }
    // Add other parameters as needed
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
- [ ] Implement handler with function separation
- [ ] Add try-catch and logging
- [ ] Compile and test handler
- [ ] Create test cases
- [ ] Run all tests
- [ ] Create README_GEN.md
- [ ] Commit and push changes

### Common Patterns
- **Auth Check (Old)**: `if (userId == null) { _failureMessage = $"Session ID '{sessionId}' is not valid."; return new DataSet(); }`
- **Auth Check (New)**: `if (userId == null) { _failureMessage = $"Session ID '{sessionId}' is not valid."; var ds = new DataSet(); ds.Tables.Add(DataUtils.CreateDataTable(new { errorCode = 1, errorMsg = "Session ID is not valid" })); return ds; }`
- **Validation (Old)**: `if (!isValid) return new List<object> { new { Results = "message" } }.ToDataSet();`
- **Validation (New)**: `if (!isValid) { var ds = new DataSet(); ds.Tables.Add(DataUtils.CreateDataTable(new { errorCode = 2, errorMsg = "message" })); return ds; }`
- **Success (Old)**: `return new List<object> { new { Results = "Ok" } }.ToDataSet();`
- **Success (New)**: `var ds = new DataSet(); ds.Tables.Add(DataUtils.CreateDataTable(new { errorCode = 0, errorMsg = "Success" })); return ds;`
- **No Data (Old)**: `if (!data.Any()) return new DataSet();`
- **No Data (New)**: `if (!data.Any()) { var ds = new DataSet(); ds.Tables.Add(DataUtils.CreateDataTable(new { errorCode = 0, errorMsg = "No data found" })); return ds; }`

### File Naming Convention
- **Handler**: `ws_[Module]_[FunctionName].cs`
- **Test**: `ws_[Module]_[FunctionName]Tests.cs`
- **YAML**: `ws_[Module]_[FunctionName].yml`
