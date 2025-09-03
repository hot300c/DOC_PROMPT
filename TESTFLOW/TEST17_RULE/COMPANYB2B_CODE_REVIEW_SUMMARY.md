# CompanyB2B Code Review Summary & Update Guide

## 🎯 Executive Summary
**Overall Risk Level**: MODERATE  
**Critical Issues**: 3  
**High Priority Issues**: 4  
**Medium Priority Issues**: 5  

**Recommendation**: Address critical security and performance issues before production deployment.

---

## 🔥 Critical Issues (Fix Immediately)

### 1. File Upload DoS Vulnerability
**Location**: `CompanyB2BImportHandler.Handle()` line 450-460  
**Risk**: Memory exhaustion attacks via large Base64 uploads  
**Impact**: Server crash, service unavailability

**Current Code**:
```csharp
byte[]? fileBytes = Convert.FromBase64String(@params.Base64Data);
```

**Required Fix**:
```csharp
// Add validation to Parameters class
[MaxLength(13981014)] // ~10MB base64 = ~10MB * 1.33
public string Base64Data { get; init; }

// Add size check in handler
if (@params.Base64Data.Length > 13981014)
    throw new ValidationException("File size exceeds 10MB limit");
```

### 2. Information Disclosure in Error Handling  
**Location**: `CompanyB2BController.Execute()` line 66-72  
**Risk**: Exposes internal system details to attackers  
**Impact**: Information leakage, attack surface expansion

**Current Code**:
```csharp
catch (Exception ex)
{
    return new ObjectResult(new { message = ex.Message, status = 500 });
}
```

**Required Fix**:
```csharp
catch (Exception ex)
{
    _logger.LogError(ex, "CompanyB2B operation failed for handler {Handler}", handler);
    return new ObjectResult(new { 
        message = "An internal error occurred. Please contact support.", 
        status = 500,
        errorId = Guid.NewGuid().ToString() // For support tracking
    });
}
```

### 3. Export Memory Exhaustion
**Location**: `CompanyB2BExportHandler.Handle()` line 935-939  
**Risk**: Loads all records into memory  
**Impact**: OutOfMemoryException with large datasets

**Current Code**:
```csharp
var rows = db.QAHosGenericDB.LCompanyB2B.ToList();
```

**Required Fix**:
```csharp
// Add pagination parameters
public record Parameters
{
    public int Page { get; init; } = 1;
    public int PageSize { get; init; } = 1000;
    // ... existing parameters
}

// Implement pagination in query
int skip = (Math.Max(1, @params.Page) - 1) * Math.Min(@params.PageSize, 1000);
var rows = db.QAHosGenericDB.LCompanyB2B
    .With(SqlServerHints.Table.NoLock)
    .OrderByDescending(x => x.ModifiedOn ?? x.CreatedOn)
    .Skip(skip)
    .Take(Math.Min(@params.PageSize, 1000))
    .ToList();
```

---

## ⚠️ High Priority Issues (Fix This Sprint)

### 4. N+1 Query Problem in Import
**Location**: `CompanyB2BImportHandler.Handle()` line 884-897  
**Risk**: Performance degradation with large imports  
**Impact**: Slow import operations, database blocking

**Current Code**:
```csharp
foreach (var u in toUpdate)
{
    db.QAHosGenericDB.LCompanyB2B.Where(x => x.CompanyB2Bid == u.Id)
        .Set(x => x.CompanyTax, u.Data.CompanyTax)
        // ... multiple Set operations
        .Update();
}
```

**Required Fix**:
```csharp
// Use BulkUpdate or batch operations
if (toUpdate.Count > 0)
{
    var updateEntities = toUpdate.Select(u => new LCompanyB2B
    {
        CompanyB2Bid = u.Id,
        CompanyTax = u.Data.CompanyTax,
        CompanyName = u.Data.CompanyName,
        CompanyAddress = u.Data.CompanyAddress,
        EffectiveFrom = u.Data.EffectiveFrom,
        EffectiveTo = u.Data.EffectiveTo,
        IsActive = u.Data.IsActive,
        ModifiedOn = now,
        ModifiedBy = @params.UserID,
        Hopdong = u.Data.Hopdong
    }).ToList();
    
    await db.BulkUpdateAsync(updateEntities);
    updated = toUpdate.Count;
}
```

### 5. CSV Injection Vulnerability
**Location**: Import processing throughout `CompanyB2BImportHandler`  
**Risk**: Malicious Excel formulas in imported data  
**Impact**: Code execution when exported data is opened in Excel

**Required Fix**:
```csharp
private static string SanitizeCsvField(string field)
{
    if (string.IsNullOrEmpty(field)) return field;
    
    // Escape formula indicators
    if (field.StartsWith("=") || field.StartsWith("@") || 
        field.StartsWith("+") || field.StartsWith("-") || 
        field.StartsWith("\t") || field.StartsWith("\r"))
    {
        return "'" + field; // Prefix with single quote
    }
    
    return field;
}

// Apply to all imported fields
companyCode = SanitizeCsvField(vals.ElementAtOrDefault(iCompanyCode)?.Trim());
companyName = SanitizeCsvField(vals.ElementAtOrDefault(iCompanyName)?.Trim());
```

### 6. Mass Assignment Risk
**Location**: All controller endpoints  
**Risk**: Client manipulation of sensitive fields  
**Impact**: Unauthorized data modification

**Required Fix**:
```csharp
// Create separate DTOs for API
public class CompanyB2BSaveRequest
{
    public Guid? CompanyB2BID { get; init; }
    public string? CompanyTax { get; init; }
    [Required] public string CompanyCode { get; init; }
    [Required] public string CompanyName { get; init; }
    public string? CompanyAddress { get; init; }
    [Required] public DateTime EffectiveFrom { get; init; }
    public DateTime? EffectiveTo { get; init; }
    public bool IsActive { get; init; } = true;
    [Required] public string? Hopdong { get; init; }
    // NOTE: UserID intentionally excluded - set from auth context
}

// Map in controller
public IActionResult Save([FromBody] CompanyB2BSaveRequest request)
{
    var userId = GetCurrentUserId();
    var parameters = new CompanyB2BSaveHandler.Parameters
    {
        CompanyB2BID = request.CompanyB2BID,
        CompanyTax = request.CompanyTax,
        CompanyCode = request.CompanyCode,
        CompanyName = request.CompanyName,
        CompanyAddress = request.CompanyAddress,
        EffectiveFrom = request.EffectiveFrom,
        EffectiveTo = request.EffectiveTo,
        IsActive = request.IsActive,
        Hopdong = request.Hopdong,
        UserID = userId // Always from auth context
    };
    return Execute("CompanyB2BSaveHandler", parameters, db, dispatcher);
}
```

---

## 📋 Medium Priority Issues (Next Sprint)

### 7. Add Rate Limiting
**Location**: All controller endpoints  
**Required**: Implement rate limiting for expensive operations

```csharp
// In Program.cs or Startup.cs
services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("ImportPolicy", opt =>
    {
        opt.Window = TimeSpan.FromMinutes(1);
        opt.PermitLimit = 5; // 5 imports per minute
    });
});

// On controller endpoints
[EnableRateLimiting("ImportPolicy")]
public IActionResult Import([FromBody] CompanyB2BImportHandler.Parameters dto)
```

### 8. Enhanced Input Validation
**Location**: Handler parameter classes  
**Required**: Add business logic validation

```csharp
public record Parameters
{
    [RegularExpression(@"^\d{10}$", ErrorMessage = "Tax ID must be 10 digits")]
    public string? CompanyTax { get; init; }
    
    [Required]
    [StringLength(50, MinimumLength = 2)]
    public string CompanyCode { get; init; }
    
    [Required] 
    [StringLength(500, MinimumLength = 3)]
    public string CompanyName { get; init; }
    
    [DateRange(MinYear = 2000, MaxYear = 2050)]
    public DateTime EffectiveFrom { get; init; }
    
    [ContractNumberValidation]
    public string? Hopdong { get; init; }
}
```

### 9. Add Response Caching
**Location**: Controller GET endpoints  
**Required**: Implement caching for read operations

```csharp
[HttpGet]
[Route("/api/company-b2b/get")]
[ResponseCache(Duration = 300)] // 5 minutes
public IActionResult Get([FromQuery] CompanyB2BGetHandler.Parameters dto)

[HttpGet]  
[Route("/api/company-b2b/list")]
[ResponseCache(Duration = 60)] // 1 minute
public IActionResult List([FromQuery] CompanyB2BListHandler.Parameters dto)
```

### 10. Transaction Scope Optimization
**Location**: Import handler transaction  
**Required**: Minimize transaction scope

```csharp
// Split into separate transactions
// 1. Insert new records
if (toInsert.Count > 0)
{
    using var insertTran = db.BeginTransaction();
    try
    {
        db.BulkCopy(toInsert);
        insertTran.Commit();
        created = toInsert.Count;
    }
    catch
    {
        insertTran.Rollback();
        throw;
    }
}

// 2. Update existing records
if (toUpdate.Count > 0)
{
    using var updateTran = db.BeginTransaction();
    try
    {
        await db.BulkUpdateAsync(updateEntities);
        updateTran.Commit();
        updated = toUpdate.Count;
    }
    catch
    {
        updateTran.Rollback();
        throw;
    }
}
```

---

## 🧪 Testing Requirements

### Security Tests to Add
```csharp
[Theory]
[InlineData("=")] // Formula injection
[InlineData("@")]
[InlineData("+")]
[InlineData("-")]
public void Import_Should_SanitizeFormulaFields(string formulaPrefix)
{
    var csvData = $"CompanyCode,CompanyName\nTEST001,{formulaPrefix}SUM(1,1)";
    // Test that formula is escaped
}

[Fact]
public void Import_Should_RejectLargeFiles()
{
    var largeBase64 = new string('A', 20000000); // >10MB
    // Test that ValidationException is thrown
}
```

### Performance Tests to Add
```csharp
[Fact]
public void Export_Should_UsePagination()
{
    // Create 2000 test records
    // Verify that export doesn't load all into memory
}

[Fact]
public void Import_Should_UseBatchOperations()
{
    // Import 1000 records
    // Verify query count is minimal (not N+1)
}
```

---

## 📊 Database Indexes to Add

```sql
-- For CompanyB2B operations
CREATE NONCLUSTERED INDEX [IX_L_CompanyB2B_CompanyCode] 
ON [QAHosGenericDB].[dbo].[L_CompanyB2B] ([CompanyCode])

CREATE NONCLUSTERED INDEX [IX_L_CompanyB2B_Active_Effective] 
ON [QAHosGenericDB].[dbo].[L_CompanyB2B] ([IsActive], [EffectiveFrom])
INCLUDE ([CompanyName], [CompanyCode], [Hopdong])

CREATE NONCLUSTERED INDEX [IX_L_CompanyB2B_ModifiedOn] 
ON [QAHosGenericDB].[dbo].[L_CompanyB2B] ([ModifiedOn] DESC, [CreatedOn] DESC)
```

---

## 🔄 Implementation Priority

### Week 1 (Critical)
1. ✅ Fix file upload DoS vulnerability
2. ✅ Secure error handling  
3. ✅ Add export pagination

### Week 2 (High)
4. ✅ Fix N+1 queries in import
5. ✅ Add CSV injection protection
6. ✅ Implement separate API DTOs

### Week 3 (Medium)
7. ✅ Add rate limiting
8. ✅ Enhanced validation
9. ✅ Response caching
10. ✅ Optimize transactions

### Week 4 (Testing & Polish)
11. ✅ Security tests
12. ✅ Performance tests
13. ✅ Database indexes
14. ✅ Documentation update

---

## 📝 Code Review Checklist

Before merging any CompanyB2B changes:

**Security**
- [ ] File size limits enforced
- [ ] Error messages don't expose internals
- [ ] CSV injection protection implemented
- [ ] Rate limiting configured
- [ ] Mass assignment prevented

**Performance**
- [ ] No N+1 queries
- [ ] Pagination implemented
- [ ] Bulk operations used
- [ ] Memory usage optimized
- [ ] Database indexes in place

**Quality**
- [ ] Unit tests passing
- [ ] Integration tests added
- [ ] Error handling tested
- [ ] Documentation updated
- [ ] Code review approved

This guide provides everything needed to systematically address the identified issues and improve the CompanyB2B module's security, performance, and reliability.
