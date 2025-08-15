# TASK 11: Convert Stored Procedure to C# Handler

## Task Summary
Convert SQL stored procedure `ws_Vaccine_DanhSachChoTiem_DangTiem_Save` to C# handler following established patterns and rules.

## Stored Procedure Analysis
**File**: `store.md`
**Procedure**: `ws_Vaccine_DanhSachChoTiem_DangTiem_Save`

### Logic Flow
1. **Input Parameters**: `@PatientID`, `@FacID`, `@RoomID`, `@UserID`
2. **Data Retrieval**: 
   - Select `ID` from `dbo.Vaccine_DanhSachChoTiem`
   - Filter by: `PatientID`, `RoomID`, `FacID_CheckSum` (CHECKSUM(@FacID)), `NgayAsInt` (FORMAT(GETDATE(), 'yyyyMMdd'))
   - Order by `ID`
3. **Data Insert**: Insert into `[dbo].[Vaccine_DanhSachChoTiem_DangTiem]`
   - Fields: `PatientID`, `RoomID`, `FacID`, `CreatedOnAsInt`, `CreatedOn`, `CreatedBy`, `ID_DangTiem`

### Key Dependencies
- `Vaccine_DanhSachChoTiem` table (source)
- `Vaccine_DanhSachChoTiem_DangTiem` table (target)
- `DateAsInt()` utility function
- `CHECKSUM()` function for FacID

## Implementation Requirements

### Handler Structure
- **Class Name**: `ws_Vaccine_DanhSachChoTiem_DangTiem_Save`
- **Base Class**: `GenericHandler<Parameters>`
- **Namespace**: `Aladdin.WebService.Handlers.QAHosGenericDB`

### Parameters Record
```csharp
public record Parameters
{
    public string? SessionID { get; set; }
    public Guid PatientID { get; set; }
    public string? FacID { get; set; }
    public int RoomID { get; set; }
    public Guid? UserID { get; set; }
}
```

### Required Methods
1. **ValidateInput**: Validate PatientID, FacID, RoomID
2. **GetIdChoTiem**: Query Vaccine_DanhSachChoTiem with NoLock hint
3. **InsertDangTiem**: Insert into Vaccine_DanhSachChoTiem_DangTiem
4. **CreateResultDataSet**: Return success result

### Technical Requirements
- Use `With(SqlServerHints.Table.NoLock)` for read queries
- Use `DateTimeService` for time operations
- Implement try-catch with proper error handling
- Use `DateAsInt()` extension method
- Use `DataUtils.Checksum()` for FacID checksum

## Test Cases Required
1. **Test-01**: Happy path - existing ChoTiem row
2. **Test-02**: No data scenario - no ChoTiem row
3. **Test-03**: Validation error - missing FacID

## Files to Create
- `aladdin/WebService.Handlers/QAHosGenericDB/ws_Vaccine_DanhSachChoTiem_DangTiem_Save.cs`
- `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_Vaccine_DanhSachChoTiem_DangTiem_Save_Test.cs`
- Test case YAML files in `TestCases/QAHosGenericDB/ws_Vaccine_DanhSachChoTiem_DangTiem_Save/`

## Dependencies to Verify
- `VaccineDanhSachChoTiem` entity exists
- `VaccineDanhSachChoTiemDangTiem` entity exists
- `DateTimeExtensions.DateAsInt()` method available
- `DataUtils.Checksum()` method available
- `DateTimeService` available for injection
