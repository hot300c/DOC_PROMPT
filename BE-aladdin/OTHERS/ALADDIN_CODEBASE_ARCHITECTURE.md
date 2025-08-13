# Aladdin Codebase Architecture Documentation

## 🏗️ **Tổng quan kiến trúc**

Aladdin là một Web API service được xây dựng trên ASP.NET Core với kiến trúc handler-based để xử lý các request database. Project sử dụng LinqToDB để tương tác với SQL Server và có hệ thống caching với FusionCache.

## 📁 **Cấu trúc thư mục chính**

```
aladdin/
├── WebService/                 # Main API project
│   ├── Controllers/           # API Controllers
│   ├── Adapters/             # Request/Response adapters
│   ├── Api/                  # REST API endpoints
│   └── Program.cs            # Application entry point
├── WebService.Handlers/       # Business logic handlers
│   ├── QAHosGenericDB/       # Database handlers
│   ├── HR/                   # HR module handlers
│   ├── Security/             # Security handlers
│   └── GenericHandler.cs     # Base handler class
├── Entities/                 # Database entities
│   ├── QAHosGenericDB/       # Database models
│   └── History/              # History database models
└── Services/                 # Business services
```

## 🔄 **Luồng xử lý request**

### 1. **Request Flow**
```
Client Request → DataAccessController → DataRequestDispatcher → Handler/StoredProcedure → Response
```

### 2. **Chi tiết từng bước:**

#### **Bước 1: DataAccessController**
- Nhận request POST với danh sách `DataRequest`
- Mỗi request chứa: `Category`, `Command`, `Parameters`
- Ví dụ: `Category="QAHosGenericDB"`, `Command="ws_L_Vaccine_List"`

#### **Bước 2: DataRequestDispatcher**
- Kiểm tra xem có handler tương ứng không
- Nếu có handler → gọi handler
- Nếu không có → gọi stored procedure
- Thêm `SessionID` và `UserID` vào parameters

#### **Bước 3: Handler Execution**
- Tạo instance của handler với dependency injection
- Gọi method `Handle(Dictionary<string, object?> parameters)`
- Trả về `DataSet`

## 🎯 **Handler Pattern**

### **Interface IHandler**
```csharp
public interface IHandler
{
    public DataSet Handle(Dictionary<string, object?> parameters);
}
```

### **GenericHandler<T> (Optional)**
```csharp
public abstract class GenericHandler<TParameters> : IHandler 
    where TParameters : new()
{
    public DataSet Handle(Dictionary<string, object?> parameters)
    {
        TParameters typedParameters = DictionaryConverter.ConvertTo<TParameters>(parameters);
        return Handle(typedParameters);
    }
    
    public abstract DataSet Handle(TParameters @params);
}
```

### **Handler Factory**
- Tự động discover tất cả handlers trong assembly
- Mapping: `{Category}..{Command}` → `HandlerType`
- Dependency injection cho handlers

## 📊 **Database Access Pattern**

### **LinqToDB Usage**
```csharp
// Query với NoLock hint
var data = db.QAHosGenericDB.TableName
    .With(SqlServerHints.Table.NoLock)
    .Where(x => x.Condition)
    .Select(x => new { x.Field1, x.Field2 })
    .ToList();

// Join pattern
var result = from t1 in db.QAHosGenericDB.Table1.With(SqlServerHints.Table.NoLock)
             from t2 in db.QAHosGenericDB.Table2.With(SqlServerHints.Table.NoLock)
                 .LeftJoin(x => t1.Id == x.Table1Id)
             select new { t1.Field1, t2.Field2 };
```

### **DataSet Return Pattern**
```csharp
public DataSet Handle(Dictionary<string, object?> parameters)
{
    // 1. Extract parameters
    string facId = parameters.GetStringOrDefault("FacID", "");
    int nhomBenhId = parameters.GetIntOrDefault("NhomBenhID", 0);
    
    // 2. Query data
    var table1 = query1.ToDataTable();
    var table2 = query2.ToDataTable();
    
    // 3. Return DataSet
    var dataSet = new DataSet();
    dataSet.Tables.Add(table1);
    dataSet.Tables.Add(table2);
    return dataSet;
}
```

## 🔧 **Dependency Injection**

### **Services Registration**
```csharp
// Program.cs
builder.Services.AddWebServiceHandlers().AddAladdinServices();

// Handler constructor injection
public class ws_L_Vaccine_List(
    AladdinDataConnection db, 
    MasterDataService masterDataService, 
    SettingsService settingsService) : IHandler
```

### **Common Dependencies**
- `AladdinDataConnection db` - Main database connection
- `HistoryCentralDataConnection historyDb` - History database (optional)
- `MasterDataService` - Master data service
- `SettingsService` - Application settings
- `DateTimeService` - Date/time utilities

## 🗄️ **Database Schema Pattern**

### **Entity Structure**
```csharp
[Table("TableName", Database = "QAHosGenericDB")]
public class EntityName
{
    [Column("ID", DataType = DataType.Int32, IsPrimaryKey = true)] 
    public int Id { get; set; }
    
    [Column("FacID", DataType = DataType.VarChar, Length = 10)] 
    public string? FacId { get; set; }
    
    [Column("CreatedBy", DataType = DataType.Guid)] 
    public Guid? CreatedBy { get; set; }
    
    [Column("CreatedOn", DataType = DataType.DateTime)] 
    public DateTime? CreatedOn { get; set; }
}
```

### **Common Fields**
- `Id` - Primary key
- `FacId` - Facility ID (multi-tenant)
- `CreatedBy/CreatedOn` - Audit fields
- `ModifiedBy/ModifiedOn` - Audit fields
- `IsActive` - Soft delete flag

## 📝 **Handler Naming Convention**

### **Pattern: `ws_{Module}_{Action}_{Context}`**
- `ws_` - Web Service prefix
- `L_` - Lookup/List data
- `MDM_` - Master Data Management
- `CN_` - Clinical data
- `Vaccine_` - Vaccine module
- `BIL_` - Billing module

### **Examples:**
- `ws_L_Vaccine_List` - List vaccines
- `ws_MDM_Patient_CheckExists` - Check patient exists
- `ws_CN_FacAdmissions_ListInDay` - List admissions in day
- `ws_Vaccine_HopDong_ListByPatientID` - List contracts by patient

## 🔍 **Parameter Handling**

### **Parameter Extraction Pattern**
```csharp
// Using extension methods
string facId = parameters.GetStringOrDefault("FacID", "");
int nhomBenhId = parameters.GetIntOrDefault("NhomBenhID", 0);
DateTime? fromDate = parameters.GetDateTimeOrDefault("FromDate", null);
Guid? userId = parameters.GetGuidOrDefault("UserID", null);
```

### **Common Parameters**
- `FacID` - Facility ID (required)
- `UserID` - Current user ID (auto-injected)
- `SessionID` - Session ID (auto-injected)
- `PatientID` - Patient identifier
- `NhomBenhID` - Disease group ID

## 🚀 **Caching Strategy**

### **IResultCacheable Interface**
```csharp
public interface IResultCacheable
{
    CacheEntryInfo? GetCacheEntryInfo(Dictionary<string, object?> parameters);
}

public record CacheEntryInfo(string Key, TimeSpan Duration);
```

### **Caching Implementation**
- FusionCache for distributed caching
- Cache key based on parameters
- Configurable cache duration
- Cache hit/miss logging

## 🧪 **Testing Pattern**

### **Test Structure**
```csharp
public class ws_HandlerName_Test : BaseHandlerTest
{
    private readonly ws_HandlerName _handler;

    public ws_HandlerName_Test()
    {
        _handler = new ws_HandlerName(DbConnection, MasterDataService);
    }

    [Theory]
    [MemberData(nameof(TestData), "QAHosGenericDB", "ws_HandlerName")]
    public void TestMethod(string testCase, Dictionary<string, object?> parameters, DataSet expected)
    {
        // Test implementation
    }
}
```

## 📋 **Creating New Handler Checklist**

### **1. Handler File Structure**
```csharp
using System.Data;
using LinqToDB;
using LinqToDB.DataProvider.SqlServer;
using Aladdin.Entities;
using Aladdin.Entities.QAHosGenericDB;
using Aladdin.Services;
using Aladdin.Utilities;

namespace Aladdin.WebService.Handlers.QAHosGenericDB;

public class ws_NewHandler(AladdinDataConnection db, MasterDataService masterDataService) : IHandler
{
    public DataSet Handle(Dictionary<string, object?> parameters)
    {
        // 1. Extract parameters
        string facId = parameters.GetStringOrDefault("FacID", "");
        
        // 2. Query logic
        var result = db.QAHosGenericDB.TableName
            .With(SqlServerHints.Table.NoLock)
            .Where(x => x.FacId == facId)
            .ToDataTable();
            
        // 3. Return DataSet
        var dataSet = new DataSet();
        dataSet.Tables.Add(result);
        return dataSet;
    }
}
```

### **2. Test File Structure**
```csharp
public class ws_NewHandler_Test : BaseHandlerTest
{
    private readonly ws_NewHandler _handler;

    public ws_NewHandler_Test()
    {
        _handler = new ws_NewHandler(DbConnection, MasterDataService);
    }

    [Theory]
    [MemberData(nameof(TestData), "QAHosGenericDB", "ws_NewHandler")]
    public void TestMethod(string testCase, Dictionary<string, object?> parameters, DataSet expected)
    {
        DataSet result = _handler.Handle(parameters);
        // Assertions
    }
}
```

### **3. Registration**
- Handler tự động được discover bởi HandlerFactory
- Không cần manual registration
- Naming convention: `{Category}..{Command}`

## 🔒 **Security & Authentication**

### **Authentication Flow**
- Session-based authentication
- Cookie-based session management
- User ID injection vào parameters
- Authorization via claims

### **Data Access Security**
- Multi-tenant với FacID
- User context tracking
- Audit logging
- SQL injection prevention

## 📊 **Monitoring & Logging**

### **APM Integration**
- Elastic APM for performance monitoring
- Transaction and span tracking
- Exception capture
- Custom metrics

### **Logging Pattern**
```csharp
Log.Debug("[{@type}] {@command}{@parameters} {@duration}ms", 
    "db", request.Command, request.GetSanitizedParameters(), duration);
```

## 🎯 **Best Practices**

### **1. Performance**
- Sử dụng `With(SqlServerHints.Table.NoLock)` cho read operations
- Implement caching cho frequently accessed data
- Optimize queries với proper indexing

### **2. Error Handling**
- Use try-catch blocks
- Log exceptions với context
- Return meaningful error messages

### **3. Code Organization**
- Follow naming conventions
- Use dependency injection
- Implement proper separation of concerns
- Add comprehensive unit tests

### **4. Database**
- Use transactions for multi-table operations
- Implement proper connection management
- Follow database naming conventions
- Use appropriate data types

---

*Documentation created for Aladdin project architecture understanding*
