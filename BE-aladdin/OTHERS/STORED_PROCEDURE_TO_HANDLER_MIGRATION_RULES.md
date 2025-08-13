# Stored Procedure to Handler Migration Rules

## 🎯 **Tổng quan**

Tài liệu này mô tả các quy tắc và best practices khi chuyển đổi từ Stored Procedure sang Handler trong project Aladdin.

## 📋 **Quy tắc chuyển đổi cơ bản**

### **1. Parameter Mapping**

#### **Stored Procedure Parameters → Handler Parameters**
```sql
-- SP Parameters
@SessionID VARCHAR(MAX)
@MaChung VARCHAR(100)
@FacID VARCHAR(10)
@PatientID UNIQUEIDENTIFIER
@DoiTuongID INT
```

```csharp
// Handler Parameter Extraction
string sessionId = parameters.GetStringOrDefault("SessionID", "");
string maChung = parameters.GetStringOrDefault("MaChung", "");
string facId = parameters.GetStringOrDefault("FacID", "");
Guid? patientId = parameters.GetGuidOrDefault("PatientID", null);
int? doiTuongId = parameters.GetIntOrDefault("DoiTuongID", null);
```

#### **Quy tắc:**
- **Required parameters**: Validate và throw `ArgumentException`
- **Optional parameters**: Sử dụng default values
- **Type conversion**: Sử dụng extension methods `GetStringOrDefault()`, `GetIntOrDefault()`, etc.

### **2. Authentication & Authorization**

#### **Stored Procedure Logic:**
```sql
DECLARE @UserID UNIQUEIDENTIFIER
SELECT @UserID = UserID
FROM [Security]..[Sessions] WITH (NOLOCK)
WHERE [SessionID] = @SessionID

IF @UserID IS NULL
    RETURN
```

#### **Handler Logic:**
```csharp
// UserID is auto-injected by DataRequestDispatcher
Guid? userId = parameters.GetGuidOrDefault("UserID", null);
if (userId == null || userId == Guid.Empty)
{
    Log.Warning("Handler: User authentication required");
    throw new UnauthorizedAccessException("User authentication required");
}
```

#### **Quy tắc:**
- **Auto-injection**: UserID được inject tự động bởi DataRequestDispatcher
- **Validation**: Kiểm tra UserID trước khi thực hiện business logic
- **Logging**: Log authentication failures

### **3. Database Query Conversion**

#### **T-SQL to LinqToDB Mapping:**

| T-SQL | LinqToDB |
|-------|----------|
| `WITH (NOLOCK)` | `.With(SqlServerHints.Table.NoLock)` |
| `JOIN` | `.Join()` hoặc `join` keyword |
| `LEFT JOIN` | `.LeftJoin()` |
| `WHERE` | `.Where()` |
| `SELECT` | `.Select()` |
| `GROUP BY` | `.GroupBy()` |
| `ORDER BY` | `.OrderBy()` |

#### **Ví dụ chuyển đổi:**
```sql
-- Original SP
SELECT @MaNhomBenhs += CONVERT(NVARCHAR(10), NhomBenhID) + ';'
FROM dbo.L_NhomBenhVaccineDetail NBD WITH (NOLOCK)
JOIN dbo.L_NhomBenhVaccine NB WITH (NOLOCK) ON NBD.NhomBenhID = NB.ID
WHERE NBD.MaChung = @MaChung
```

```csharp
// Handler equivalent
var nhomBenhVaccineList = (
    from nbvd in db.QAHosGenericDB.LNhomBenhVaccineDetails.With(SqlServerHints.Table.NoLock)
    join nbv in db.QAHosGenericDB.LNhomBenhVaccines.With(SqlServerHints.Table.NoLock)
        on nbvd.NhomBenhId equals nbv.Id
    where nbvd.MaChung == maChung
    select new { nbvd.NhomBenhId }
).ToList();

string maNhomBenhs = string.Join(";", nhomBenhVaccineList.Select(x => x.NhomBenhId.ToString())) + ";";
```

### **4. Error Handling & Logging**

#### **Stored Procedure Error Handling:**
```sql
-- SP typically uses RAISERROR or returns empty result
IF @UserID IS NULL
    RETURN
```

#### **Handler Error Handling:**
```csharp
try
{
    // Business logic
    return dataSet;
}
catch (ArgumentException ex)
{
    Log.Error(ex, "Handler: Parameter validation failed");
    throw;
}
catch (UnauthorizedAccessException ex)
{
    Log.Error(ex, "Handler: Authentication failed");
    throw;
}
catch (Exception ex)
{
    Log.Error(ex, "Handler: Unexpected error occurred");
    throw;
}
```

#### **Quy tắc:**
- **Specific exceptions**: Catch specific exception types
- **Logging levels**: Use appropriate logging levels (Warning, Error, Information)
- **Exception propagation**: Re-throw exceptions after logging
- **Context information**: Include handler name and relevant parameters in log messages

### **5. Return Data Structure**

#### **Stored Procedure Output:**
```sql
-- SP returns single column
SELECT @MaNhomBenhs AS MaNhomBenh
```

#### **Handler Output:**
```csharp
// Create DataSet with multiple tables
var dataSet = new DataSet();

// Table 1: Main result (matching SP output)
var mainResultTable = new DataTable("MaNhomBenh");
mainResultTable.Columns.Add("MaNhomBenh", typeof(string));
mainResultTable.Rows.Add(maNhomBenhs);
dataSet.Tables.Add(mainResultTable);

// Table 2: Detailed data (additional info)
var detailTable = nhomBenhVaccineList.ToDataTable();
detailTable.TableName = "NhomBenhVaccineDetails";
dataSet.Tables.Add(detailTable);
```

#### **Quy tắc:**
- **Backward compatibility**: Maintain same output structure as SP
- **Additional data**: Provide detailed data in separate tables
- **Table naming**: Use descriptive table names
- **Data types**: Match original SP data types

## 🔧 **Performance Optimization Rules**

### **1. Query Optimization**
```csharp
// ✅ Good: Use NoLock hints
var data = db.QAHosGenericDB.TableName.With(SqlServerHints.Table.NoLock)

// ✅ Good: Use proper joins
from t1 in db.QAHosGenericDB.Table1.With(SqlServerHints.Table.NoLock)
join t2 in db.QAHosGenericDB.Table2.With(SqlServerHints.Table.NoLock)
    on t1.Id equals t2.Table1Id

// ❌ Avoid: N+1 queries
foreach (var item in items)
{
    var detail = db.QAHosGenericDB.Details.Where(x => x.ItemId == item.Id).ToList();
}
```

### **2. Caching Strategy**
```csharp
// Implement IResultCacheable for frequently accessed data
public class ws_ExampleHandler : IHandler, IResultCacheable
{
    public CacheEntryInfo? GetCacheEntryInfo(Dictionary<string, object?> parameters)
    {
        string cacheKey = $"example_{parameters.GetStringOrDefault("FacID", "")}_{parameters.GetStringOrDefault("Param1", "")}";
        return new CacheEntryInfo(cacheKey, TimeSpan.FromMinutes(30));
    }
}
```

### **3. Memory Management**
```csharp
// ✅ Good: Use ToList() for small datasets
var smallList = query.ToList();

// ✅ Good: Use ToDataTable() for DataSet
var dataTable = query.ToDataTable();

// ❌ Avoid: Large datasets in memory
var largeList = query.ToList(); // For very large datasets
```

## 📝 **Documentation Standards**

### **1. Handler Documentation Template**
```csharp
/// <summary>
/// Handler: ws_HandlerName
/// 
/// Original Stored Procedure: [dbo].[ws_HandlerName]
/// Version: X.X.X.X (YYYYMMDD HH:MM Author)
/// 
/// Logic: Brief description of business logic
/// 
/// Migration Rules Applied:
/// - Convert T-SQL to LinqToDB
/// - Maintain original business logic
/// - Add proper error handling and logging
/// - Use NoLock hints for performance
/// - Support multi-tenant with FacID
/// </summary>
```

### **2. Code Comments Standards**
```csharp
// 1. Extract and validate parameters (matching SP parameters)
string param1 = parameters.GetStringOrDefault("Param1", "");

// 2. Validate required parameters (matching SP validation)
if (string.IsNullOrEmpty(param1))
{
    Log.Warning("Handler: Param1 is required");
    throw new ArgumentException("Param1 is required");
}

// 3. Execute main query (matching SP logic)
// Original SP: SELECT ... FROM Table WHERE ...
var result = query.ToList();

// 4. Create result matching SP output format
// Original SP returns: SELECT @Result AS ColumnName
var dataSet = new DataSet();
```

## 🧪 **Testing Requirements**

### **1. Unit Test Structure**
```csharp
[Theory]
[MemberData(nameof(TestData), "QAHosGenericDB", "ws_HandlerName")]
public void TestMethod(string testCase, Dictionary<string, object?> parameters, DataSet expected)
{
    // Test implementation
}

[Fact]
public void Test_WithValidParameters_ShouldReturnData()
{
    // Test with valid parameters
}

[Fact]
public void Test_WithMissingRequiredParameter_ShouldThrowException()
{
    // Test parameter validation
}

[Fact]
public void Test_WithInvalidUser_ShouldThrowUnauthorizedException()
{
    // Test authentication
}
```

### **2. Test Data Requirements**
- **Valid parameters**: Test với parameters hợp lệ
- **Missing parameters**: Test với thiếu required parameters
- **Invalid parameters**: Test với parameters không hợp lệ
- **Authentication**: Test với UserID null/empty
- **Edge cases**: Test với boundary values

## 🔒 **Security Considerations**

### **1. Parameter Validation**
```csharp
// ✅ Good: Validate all required parameters
if (string.IsNullOrEmpty(facId))
{
    Log.Warning("Handler: FacID is required");
    throw new ArgumentException("FacID is required");
}

// ✅ Good: Validate parameter types
if (!int.TryParse(parameters.GetStringOrDefault("IntParam", ""), out int intValue))
{
    Log.Warning("Handler: IntParam must be a valid integer");
    throw new ArgumentException("IntParam must be a valid integer");
}
```

### **2. SQL Injection Prevention**
```csharp
// ✅ Good: Use LinqToDB (parameterized queries)
var result = db.QAHosGenericDB.TableName
    .Where(x => x.FacId == facId && x.Status == status)
    .ToList();

// ❌ Avoid: String concatenation for queries
// var sql = $"SELECT * FROM Table WHERE FacId = '{facId}'";
```

### **3. Multi-tenant Security**
```csharp
// ✅ Good: Always filter by FacID
where nbvd.FacId == facId || nbvd.FacId == null || nbvd.FacId == "0"

// ✅ Good: Validate FacID parameter
if (string.IsNullOrEmpty(facId))
{
    throw new ArgumentException("FacID is required");
}
```

## 📊 **Migration Checklist**

### **Pre-Migration:**
- [ ] Analyze original SP logic thoroughly
- [ ] Identify all parameters and their types
- [ ] Understand business logic and edge cases
- [ ] Review SP performance characteristics
- [ ] Identify authentication/authorization requirements

### **During Migration:**
- [ ] Create handler with proper naming convention
- [ ] Implement parameter extraction and validation
- [ ] Convert T-SQL queries to LinqToDB
- [ ] Add proper error handling and logging
- [ ] Maintain backward compatibility
- [ ] Add comprehensive unit tests

### **Post-Migration:**
- [ ] Test with real data
- [ ] Verify performance characteristics
- [ ] Update documentation
- [ ] Update API analysis report
- [ ] Monitor logs for errors
- [ ] Validate with stakeholders

## 🎯 **Best Practices Summary**

1. **Maintain Original Logic**: Preserve business logic from SP
2. **Add Proper Logging**: Log all important events and errors
3. **Handle Exceptions**: Use specific exception types and proper error messages
4. **Optimize Performance**: Use NoLock hints and proper query patterns
5. **Ensure Security**: Validate parameters and maintain multi-tenant support
6. **Test Thoroughly**: Create comprehensive unit tests
7. **Document Everything**: Add detailed comments and documentation
8. **Monitor Performance**: Use APM and logging to track performance

---

*Documentation created for Stored Procedure to Handler migration guidelines*

