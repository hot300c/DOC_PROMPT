# Task : Convert Stored Procedure

## GIT FLOW
git checkout main
git pull
git checkout -b feat/Convert_ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh

git add -A
git commit
git push origin feat/Convert_ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh

Những lần sau sẽ commit:
git add -p
git commit --amend
git push origin -f

## 🎯 Yêu cầu kỹ thuật

### RULE CHUNG:

- Bạn là chuyên gia lập trình.
- ✅ Thêm try-catch và logging cẩn thận
- ✅ Review toàn bộ source code
- ✅ Đặt tên file trong cấu trúc thư mục handler
- ✅ Cần có try-catch log
- ✅ Cần tạo test cases
- **Kiến trúc code phải phân tách thành các function để code gọn gàng, dễ đọc, dễ bảo trì.**
- đường dẫn chứa file handle: C:\PROJECTS\aladdin\WebService.Handlers\QAHosGenericDB
- đường dẫn chứa file testcase:C:\PROJECTS\aladdin\WebService.Handlers.Tests\QAHosGenericDB
- đường dẫn chứa file yaml testcase: C:\PROJECTS\aladdin\WebService.Handlers.Tests\TestCases\QAHosGenericDB


### 🔧 QUY TẮC REFACTOR CODE (BẮT BUỘC):

#### 1. **Tách code thành các function riêng biệt:**
- **Authentication & Validation:** `AuthenticateUser()`, `ValidateInput()`
- **Data Retrieval:** `GetClinicalSession()`, `GetApplicationSettings()`, `GetPatientData()`
- **Business Logic:** `ApplyBusinessLogic()`, `CalculatePayment()`, `ValidateBusinessRules()`
- **Data Updates:** `UpdateMainTable()`, `UpdateRelatedTables()`, `UpdateHistory()`
- **Result Creation:** `CreateResultDataSet()`, `FormatResponse()`

#### 2. **Naming Convention cho Function:**
- Sử dụng PascalCase: `GetClinicalSession()`, `UpdatePaymentStatus()`
- Tên function phải mô tả rõ chức năng
- Thêm XML documentation cho mỗi function


### RULE KỸ THUẬT:

- Tuân thủ lập trình file handler theo tài liệu: C:\PROJECTS\aladdin\HANDLERS.md
- Có ghi chú từ code tương ứng với SQL Store procedure (nếu có) trên code bằng tiếng anh
- Sau khi tạo xong, phải biên dịch lại project để kiểm tra lại
- Code cũng phải có With(SqlServerHints.Table.NoLock)
- Chuỗi xuất ra thì nên dùng: singleQuote: true
- Khi có update nào trong source code thì cũng nên đồng bộ vào file README_GEN.md.
- Code phải đảm bảo đúng logic như store procedure.
- Sau khi hoàn tất code thì nên sinh ra file README_GEN.md giống với file mẫu này: README_GEN.md 
trong cùng thư mục.
- Tóm tắt các bước sau khi tạo file vào file README_GEN.md.
- Nên tạo lớp  Parameters cho việc làm tham số handle public override DataSet Handle(Parameters @params). Tham thảo như file : ws_MDM_Patient_CheckExists.cs
- khi tạo các test case mà có phát sinh lỗi thì check lại các fields trong các class entity trong thư mục: C:\PROJECTS\aladdin\Entities\QAHosGenericDB để cần lấy entity tương ứng.
- Xử lý ra code nhanh.
- Sau khi suy luận ra các đầy đủ thông tin, thì tạo 1 file README_TODO_BEFORE_GEN.md để tập hợp đầy đủ các thông tin mà đã suy luận, và đầy đủ thông tin để file này làm cơ sở gen ra code.
- Khi biên dịch file code handler chạy ổn thì mới tạo code cho các file test case.
- Trong file README_GEN.md có thêm các đường dẫn testcase mà đã gen ra để tôi có thể click vào nó đến đúng file nhanh chóng.
- Sau khi gen ra các file test case xong, thì chạy để testing lại các test case đó để pass được hết các file.

#### 3. **Function Structure:**
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

#### 4. **Main Handler Structure:**
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

#### 5. **Test Cases Requirements:**
- **Test cơ bản:** Authentication, validation, happy path
- **Test business logic:** Các trường hợp đặc biệt của business rules
- **Test error cases:** Invalid input, missing data, exceptions
- **Test edge cases:** Boundary values, null values
- **Test integration:** Multiple tables, complex workflows

#### 6. **Test Case Structure:**
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

### 📝 README_GEN.md TEMPLATE:

```markdown
# [Handler Name] - Refactoring Report

## Overview
Handler `[HandlerName]` đã được refactor để tách thành các function nhỏ, dễ đọc và dễ test hơn.

## Changes Made

### 1. Code Refactoring
- **Tách code thành các function riêng biệt:**
  - `Function1()`: Mô tả chức năng
  - `Function2()`: Mô tả chức năng
  - ...

### 2. Benefits of Refactoring
- **Dễ đọc:** Code được chia thành các function có tên rõ ràng
- **Dễ test:** Mỗi function có thể được test riêng biệt
- **Dễ maintain:** Logic được tách biệt, dễ sửa đổi từng phần
- **Dễ debug:** Có thể debug từng function riêng lẻ
- **Reusable:** Các function có thể được tái sử dụng

### 3. Test Cases Updated
- Mô tả các test cases đã tạo/cập nhật

### 4. Business Logic Preserved
- Tất cả business logic gốc được giữ nguyên

### 5. Performance Considerations
- Vẫn sử dụng NoLock hints cho performance
- Không thay đổi logic query, chỉ tách thành function

## Conclusion
Việc refactor đã thành công với các lợi ích đạt được.
```
