# DataRequestDispatcher Logic Analysis

## 🎯 **Tổng quan**

`DataRequestDispatcher` là class trung tâm trong kiến trúc Aladdin, có nhiệm vụ **phân phối và điều phối** các request database. Nó quyết định xem request sẽ được xử lý bởi **Handler** hay **Stored Procedure**.

## 🏗️ **Cấu trúc và Dependencies**

### **Constructor Dependencies**
```csharp
public class DataRequestDispatcher(
    IHandlerFactory handlerFactory,      // Factory để tạo handlers
    IFusionCache fusionCache,           // Cache system
    RequestAdapter requestAdapter,       // Transform request parameters
    ResponseAdapter responseAdapter,     // Transform response data
    IOptions<ExternalConfigs> configs)  // Configuration settings
```

### **Input Parameters**
- `AladdinDataConnection db` - Main database connection
- `HistoryCentralDataConnection? historyDb` - History database (optional)
- `DataRequest request` - Request data chứa Category, Command, Parameters
- `string sessionId` - Session identifier
- `Guid? userId` - Current user ID

## 🔄 **Luồng xử lý chính (Method Dispatch)**

### **Bước 1: Setup Command Timeout**
```csharp
int commandTimeout = configs.Value.SpsTimeout.GetValueOrDefault(request.Command, 60);
db.CommandTimeout = commandTimeout <= 0 ? 60 : commandTimeout;
```
- Lấy timeout từ config cho command cụ thể
- Default timeout: 60 giây
- Set timeout cho database connection

### **Bước 2: Decision Logic - Handler vs Stored Procedure**

```csharp
if (!request.PreferStoredProcedure && 
    !configs.Value.SpsPreferred.Contains(request.Command) &&
    handlerFactory.GetHandler(db, historyDb, request.Category, request.Command) is { } handler)
{
    // Use Handler
}
else
{
    // Use Stored Procedure
}
```

#### **Điều kiện để sử dụng Handler:**
1. `!request.PreferStoredProcedure` - Request không yêu cầu ưu tiên SP
2. `!configs.Value.SpsPreferred.Contains(request.Command)` - Command không nằm trong danh sách ưu tiên SP
3. `handlerFactory.GetHandler(...) is { } handler` - Tìm thấy handler tương ứng

### **Bước 3: User ID Injection (Handler Path)**
```csharp
if (userId != null)
{
    if (request.Parameters.GetGuidOrDefault("UserID", Guid.Empty) == Guid.Empty)
    {
        request.Parameters["UserID"] = userId;
    }
}
```
- Tự động inject UserID nếu chưa có
- Chỉ áp dụng cho Handler path

### **Bước 4: Session ID Injection (Stored Procedure Path)**
```csharp
if (request.Command.StartsWith("ws_") && !request.ExcludeSessionId)
{
    request.Parameters["SessionID"] = sessionId;
}
```
- Chỉ áp dụng cho commands bắt đầu bằng "ws_"
- Trừ khi `ExcludeSessionId = true`

## 🎯 **Handler Execution (CallHandler)**

### **1. APM Monitoring**
```csharp
ITransaction? transaction = Agent.Tracer.CurrentTransaction;
ISpan? span = transaction?.StartSpan($"@{category}..{command}", "app", null, "exec");
```
- Tạo span cho Elastic APM monitoring
- Span name: `@{category}..{command}`

### **2. Caching Logic**
```csharp
CacheEntryInfo? cacheEntryInfo = handler is IResultCacheable cacheableHandler
    ? cacheableHandler.GetCacheEntryInfo(parameters)
    : null;

if (cacheEntryInfo != null)
{
    DataSet? cachedResult = fusionCache.GetOrDefault<DataSet?>(cacheEntryInfo.Key);
    if (cachedResult != null)
    {
        span?.SetLabel("cache", "hit");
        return cachedResult;
    }
    else
    {
        span?.SetLabel("cache", "miss");
    }
}
```

#### **Caching Flow:**
1. **Check if handler supports caching** - Implement `IResultCacheable`
2. **Get cache key and duration** - Từ `GetCacheEntryInfo()`
3. **Try get from cache** - `fusionCache.GetOrDefault()`
4. **Cache hit** - Return cached result, set label "hit"
5. **Cache miss** - Set label "miss", continue execution

### **3. Handler Execution**
```csharp
DataSet result = handler.Handle(parameters);
```

### **4. Cache Storage**
```csharp
if (cacheEntryInfo != null)
{
    fusionCache.Set(cacheEntryInfo.Key, result, cacheEntryInfo.Duration);
}
```

### **5. Error Handling & Cleanup**
```csharp
catch (Exception e)
{
    span?.CaptureException(e);
    throw;
}
finally
{
    span?.End();
}
```

## 🗄️ **Stored Procedure Execution (CallStoredProcedure)**

### **1. Parameter Transformation**
```csharp
parameters = requestAdapter.Transform(category, command, parameters);
```
- Transform parameters theo rules của RequestAdapter

### **2. SQL Command Setup**
```csharp
using SqlCommand sqlCommand = new(
    category + ".." + command,  // SP name: "Category..Command"
    (SqlConnection)db.Connection);
sqlCommand.Transaction = (SqlTransaction?)db.Transaction;
sqlCommand.CommandType = CommandType.StoredProcedure;
sqlCommand.CommandTimeout = db.CommandTimeout;
```

### **3. Parameter Binding**
```csharp
foreach (KeyValuePair<string, object?> keyValuePair in parameters)
{
    string name = keyValuePair.Key.SafeSqlName();
    if (keyValuePair.Value is JArray jArray)
    {
        // Handle JSON Array as Table-Valued Parameter
        DataTable dataSave = DataUtils.ConvertJArrayToDataTable(jArray);
        sqlCommand.Parameters.Add("@" + name, SqlDbType.Structured).Value = dataSave;
    }
    else
    {
        // Handle regular parameters
        sqlCommand.Parameters.Add("@" + name, SqlDbType.NVarChar).Value = keyValuePair.Value;
    }
}
```

#### **Parameter Types:**
- **JArray** → Table-Valued Parameter (SqlDbType.Structured)
- **Others** → Regular parameter (SqlDbType.NVarChar)

### **4. Execute and Transform**
```csharp
using SqlDataAdapter sqlDataAdapter = new(sqlCommand);
DataSet dataSet = new();
sqlDataAdapter.Fill(dataSet);
return responseAdapter.Transform(category, command, dataSet);
```

## 📊 **Decision Matrix**

| Condition | Handler | Stored Procedure |
|-----------|---------|------------------|
| `PreferStoredProcedure = true` | ❌ | ✅ |
| `Command in SpsPreferred` | ❌ | ✅ |
| `Handler exists` | ✅ | ❌ |
| `Default fallback` | ❌ | ✅ |

## 🔧 **Configuration Options**

### **ExternalConfigs Settings**
```json
{
  "SpsTimeout": {
    "ws_L_Vaccine_List": 30,
    "ws_MDM_Patient_CheckExists": 15
  },
  "SpsPreferred": [
    "ws_Legacy_Command",
    "ws_Complex_StoredProcedure"
  ]
}
```

### **DataRequest Options**
```csharp
public class DataRequest
{
    public bool PreferStoredProcedure { get; set; } = false;
    public bool ExcludeSessionId { get; set; } = false;
    public string Category { get; set; } = "";
    public string Command { get; set; } = "";
    public Dictionary<string, object?> Parameters { get; set; } = new();
}
```

## 🚀 **Performance Optimizations**

### **1. Caching Strategy**
- **FusionCache** cho distributed caching
- **Cache key** dựa trên parameters
- **Configurable duration** cho từng handler
- **Cache hit/miss** logging

### **2. Database Optimization**
- **Command timeout** configurable per command
- **Connection reuse** với transaction support
- **NoLock hints** trong handlers
- **Parameter binding** optimization

### **3. Monitoring**
- **Elastic APM** integration
- **Transaction tracking**
- **Span creation** cho performance analysis
- **Exception capture**

## 🔒 **Security Features**

### **1. Parameter Sanitization**
```csharp
string name = keyValuePair.Key.SafeSqlName();
```
- Sanitize parameter names để tránh SQL injection

### **2. User Context**
- **UserID injection** cho handlers
- **SessionID injection** cho stored procedures
- **Multi-tenant support** với FacID

### **3. Transaction Management**
- **Automatic transaction** support
- **Rollback** on exception
- **Connection state** preservation

## 🎯 **Best Practices**

### **1. Handler vs Stored Procedure**
- **Use Handlers** cho business logic phức tạp
- **Use Stored Procedures** cho legacy code hoặc performance-critical operations
- **Configurable preference** via settings

### **2. Caching Strategy**
- **Implement IResultCacheable** cho frequently accessed data
- **Set appropriate cache duration** based on data volatility
- **Monitor cache hit rates** via APM

### **3. Error Handling**
- **Proper exception propagation**
- **APM exception capture**
- **Transaction rollback** on error

### **4. Performance Monitoring**
- **Use APM spans** cho detailed tracking
- **Monitor command timeouts**
- **Track cache performance**

---

*Documentation created for DataRequestDispatcher logic understanding*
