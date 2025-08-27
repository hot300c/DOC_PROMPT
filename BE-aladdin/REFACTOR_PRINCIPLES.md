# Refactoring According to 3 Core Principles

## Overview
This document explains how the refactoring of `ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc.cs` follows the three core principles from the workshop: **Pure Function**, **Single Responsibility Principle**, and **Immutability**.

## 1. Pure Function Principle ✅

### Definition
A pure function has no side effects and always returns the same output for the same input.

### Before Refactoring ❌
```csharp
private DataTable CalculatePaymentAmount(DataTable resultData)
{
    // Side effects: Console.WriteLine() - violates pure function
    Console.WriteLine($"DEBUG: Error in CalculatePaymentAmount: {ex.Message}");
    
    // Mixed concerns: data extraction + calculation + database access
    bool isMuiNgoaiDanhMuc = Convert.ToBoolean(originalRow["IsMuiNgoaiDanhMuc"]);
    // ... complex calculation logic mixed with data access
}
```

### After Refactoring ✅
```csharp
// Pure function: no side effects, same output for same input
private static decimal CalculatePaymentAmountLogic(PaymentCalculationData data)
{
    if (data.IsMuiNgoaiDanhMuc || data.IsTiemNgoai)
        return 0;
    
    if (data.GiaChenhLechChuaGiam > 0 || (data.GiaChenhLechChuaGiam == 0 && data.GiaChenhLechTiemNgoai == 0))
        return data.GiaMuiTiem + data.GiaChenhLechChuaGiam - data.TienGiam;
    
    // ... pure calculation logic
}

// Pure function: data extraction only
private static PaymentCalculationData ExtractPaymentData(DataRow row)
{
    return new PaymentCalculationData
    {
        IsMuiNgoaiDanhMuc = Convert.ToBoolean(row["IsMuiNgoaiDanhMuc"]),
        // ... other properties
    };
}
```

### Benefits
- **Testable**: Easy to unit test with predictable inputs/outputs
- **Predictable**: Same result every time for same input
- **Composable**: Can be combined with other pure functions

## 2. Single Responsibility Principle ✅

### Definition
Each function should have one reason to change - one responsibility.

### Before Refactoring ❌
```csharp
private DataTable UpdateSequenceNumber(DataTable resultData)
{
    // Multiple responsibilities:
    // 1. Data extraction from DataRow
    // 2. Database querying
    // 3. Data transformation
    // 4. Error handling with side effects
    
    foreach (DataRow originalRow in resultData.Rows)
    {
        int idPhacDo = Convert.ToInt32(originalRow["IDPhacDo"]); // Data extraction
        int maMuiTiem = Convert.ToInt32(originalRow["ID_Detail"]); // Data extraction
        
        var sequenceNumber = db.Query() // Database operation
            .Where(v => v.IdPhacDo == idPhacDo) // Business logic
            .Select(v => v.SttMuiTiem) // Data transformation
            .FirstOrDefault();
            
        newRow["STTMuiTiem"] = sequenceNumber ?? maMuiTiem; // Data assignment
    }
}
```

### After Refactoring ✅
```csharp
// Responsibility 1: Data extraction only
private static SequenceLookupData ExtractSequenceData(DataRow row)
{
    return new SequenceLookupData
    {
        IdPhacDo = Convert.ToInt32(row["IDPhacDo"]),
        MaMuiTiem = Convert.ToInt32(row["ID_Detail"])
    };
}

// Responsibility 2: Database operation only
private static int? GetSequenceNumberFromDatabase(SequenceLookupData data, AladdinDataConnection db)
{
    return db.QAHosGenericDB.LVaccinePhacdoDetails
        .With(SqlServerHints.Table.NoLock)
        .Where(v => v.IdPhacDo == data.IdPhacDo && v.SttMuiTiem == data.MaMuiTiem)
        .Select(v => v.SttMuiTiem)
        .FirstOrDefault();
}

// Responsibility 3: Orchestration only
private DataTable UpdateSequenceNumber(DataTable resultData, AladdinDataConnection db)
{
    var newResultData = resultData.Clone();
    
    foreach (DataRow originalRow in resultData.Rows)
    {
        var newRow = CreateNewRowWithCopiedData(originalRow, newResultData);
        
        var sequenceData = ExtractSequenceData(originalRow); // Single responsibility
        var sequenceNumber = GetSequenceNumberFromDatabase(sequenceData, db); // Single responsibility
        
        newRow["STTMuiTiem"] = sequenceNumber ?? sequenceData.MaMuiTiem;
        newResultData.Rows.Add(newRow);
    }
    
    return newResultData;
}
```

### Benefits
- **Maintainable**: Changes to one responsibility don't affect others
- **Testable**: Each function can be tested independently
- **Reusable**: Functions can be reused in different contexts

## 3. Immutability Principle ✅

### Definition
Avoid changing data directly - create new instances instead.

### Before Refactoring ❌
```csharp
private void CalculatePaymentAmount(DataTable resultData) // void - modifies input
{
    foreach (DataRow row in resultData.Rows)
    {
        row["ThanhTien"] = thanhTien; // Direct modification of input
    }
}
```

### After Refactoring ✅
```csharp
// Immutable data structure
private readonly struct PaymentCalculationData
{
    public bool IsMuiNgoaiDanhMuc { get; init; }
    public bool IsTiemNgoai { get; init; }
    public decimal GiaMuiTiem { get; init; }
    // ... other properties are immutable
}

// Returns new DataTable instead of modifying input
private DataTable CalculatePaymentAmount(DataTable resultData)
{
    var newResultData = resultData.Clone(); // Create new instance
    
    foreach (DataRow originalRow in resultData.Rows)
    {
        var newRow = CreateNewRowWithCopiedData(originalRow, newResultData); // New row
        var paymentData = ExtractPaymentData(originalRow); // Immutable data structure
        decimal thanhTien = CalculatePaymentAmountLogic(paymentData); // Pure calculation
        
        newRow["ThanhTien"] = thanhTien; // Modify new row, not original
        newResultData.Rows.Add(newRow);
    }
    
    return newResultData; // Return new instance
}
```

### Benefits
- **Predictable**: Input data never changes
- **Thread-safe**: Immutable data can be shared safely
- **Debugging**: Easier to trace data flow

## Functional Pipeline Pattern

The refactored code uses a functional pipeline pattern:

```csharp
var processedData = resultData
    .Pipe(data => CalculatePaymentAmount(data))           // Pure calculation
    .Pipe(data => UpdateSequenceNumber(data, db))         // Database + transformation
    .Pipe(data => UpdateContractNumber(data, db))         // Database + transformation
    .Pipe(data => UpdateUsageObjectID(data, db))          // Database + transformation
    .Pipe(data => UpdateThoiGianGianCach(data, db));      // Database + transformation
```

Each step:
- Takes a DataTable as input
- Returns a new DataTable as output
- Has a single responsibility
- Is composable with other functions

## Data Structures

Immutable data structures for type safety:

```csharp
private readonly struct PaymentCalculationData { /* ... */ }
private readonly struct SequenceLookupData { /* ... */ }
private readonly struct ContractLookupData { /* ... */ }
```

## Testing Strategy

With pure functions and single responsibilities, testing becomes straightforward:

```csharp
[Test]
public void CalculatePaymentAmountLogic_WhenIsMuiNgoaiDanhMuc_ReturnsZero()
{
    // Arrange
    var data = new PaymentCalculationData { IsMuiNgoaiDanhMuc = true };
    
    // Act
    var result = CalculatePaymentAmountLogic(data);
    
    // Assert
    Assert.That(result, Is.EqualTo(0));
}
```

## Conclusion

This refactoring demonstrates how applying these three principles leads to:
- **Better testability** through pure functions
- **Easier maintenance** through single responsibilities  
- **Predictable behavior** through immutability
- **Composable code** through functional patterns

The trade-off is slightly more code, but the benefits in maintainability, testability, and reliability far outweigh the cost.
