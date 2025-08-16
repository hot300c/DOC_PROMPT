# TODO: ws_BIL_Invoice_Save_Vaccine - Pre-Generation Analysis

## Handler Information
- **Handler Name**: ws_BIL_Invoice_Save_Vaccine
- **Original SP**: dbo.ws_BIL_Invoice_Save_Vaccine
- **Purpose**: Inserts a new BIL_Invoice (and related Live/CurrentDay rows) when not existing

## Analysis Results

### Business Logic
- **Authentication**: Validate SessionID and get UserID
- **Special Case**: If IsTiem = 1, use CreatedByUser of latest IsTamUng=1 invoice of this patient
- **Validation**: Check if invoice already exists (SP only inserts when not exists)
- **Data Normalization**: Normalize special empty GUIDs to null
- **Invoice Number Generation**: Build InvoiceNo using MaQuay + yymmdd + sequence
- **Description Building**: Build Description from Note (converted to non-unicode)
- **Receipt Number**: Build ReceiptNumber from ReceiptDaily
- **LanThu Calculation**: Calculate LanThu only when IsTamUng = 1
- **Total Contract**: Calculate TotalContract (approximation of SP logic)
- **Data Insertion**: Insert into BIL_Invoice, BIL_Invoice_Live, BIL_Invoice_CurrentDay

### Required Functions (Function Separation - BẮT BUỘC)

#### Authentication & Validation
- [ ] `AuthenticateUser(sessionId)` - ✅ Đã có
- [ ] `ValidateInput(parameters)` - ❌ Thiếu
- [ ] `ValidateBusinessRules(data, parameters)` - ❌ Thiếu
- [ ] `ValidateInvoiceExists(invoiceId)` - ❌ Thiếu

#### Data Retrieval
- [ ] `GetLastTamUngUserId(patientId)` - ❌ Thiếu
- [ ] `GetCounterOrderIndex(counterId, facId)` - ❌ Thiếu
- [ ] `GetLatestInvoiceNoToday(facId, counterId)` - ❌ Thiếu
- [ ] `GetReceiptDailyData(facId, counterId, isVat)` - ❌ Thiếu
- [ ] `GetMaxLanThu(patientId, hopDongId)` - ❌ Thiếu
- [ ] `GetVaccineHopDongDetails(hopDongId)` - ❌ Thiếu

#### Business Logic
- [ ] `ApplySpecialCaseLogic(parameters, userId)` - ❌ Thiếu
- [ ] `NormalizeParameters(parameters)` - ❌ Thiếu
- [ ] `BuildInvoiceNo(parameters)` - ✅ Đã có
- [ ] `BuildDescription(note)` - ✅ Đã có
- [ ] `BuildReceiptNumber(facId, counterId, isVat)` - ✅ Đã có
- [ ] `CalculateLanThu(isTamUng, patientId, hopDongId)` - ✅ Đã có
- [ ] `CalculateTotalContractApprox(hopDongId)` - ✅ Đã có

#### Data Updates
- [ ] `InsertBilInvoice(parameters, userId, invoiceNo, description, receiptNumber, lanThu, totalContract)` - ❌ Thiếu
- [ ] `InsertBilInvoiceLive(parameters, userId, invoiceNo, description, receiptNumber, lanThu, totalContract, checksumFacId)` - ❌ Thiếu
- [ ] `InsertBilInvoiceCurrentDay(parameters, invoiceNo)` - ❌ Thiếu

#### Result Creation
- [ ] `CreateSuccessResponse(invoiceId, invoiceNo)` - ❌ Thiếu
- [ ] `CreateErrorResponse(errorCode, errorMsg)` - ❌ Thiếu

### Required Entities
- **BilInvoice**: Main invoice data
- **BilInvoiceLive**: Live invoice data with checksum
- **BilInvoiceCurrentDay**: Current day invoice tracking
- **Sessions**: User authentication
- **LCounters**: Counter information for invoice numbering
- **ReceiptDailies**: Receipt number generation
- **VaccineHopDongDetails**: Contract details for total calculation

### Test Scenarios
- [ ] Happy path - successful invoice creation
- [ ] Authentication failure - invalid session ID
- [ ] Validation error - invoice already exists
- [ ] Business logic error - invalid parameters
- [ ] Special case - IsTiem = 1 with previous tam ung
- [ ] No data found - counter not found
- [ ] System error - database connection issues

## Refactoring Plan

### Phase 1: Function Separation
1. Extract validation logic into separate functions
2. Extract data retrieval logic into separate functions
3. Extract business logic into separate functions
4. Extract data insertion logic into separate functions
5. Extract response creation logic into separate functions

### Phase 2: Main Handler Restructure
1. Restructure Handle() method to follow 5-step template
2. Implement proper error handling with errorCode/errorMsg
3. Ensure all functions have try-catch and logging

### Phase 3: Testing
1. Create comprehensive test cases
2. Verify all business logic is preserved
3. Ensure performance with NoLock hints maintained

## Notes
- Current code has good helper functions but main Handle() method is too long
- Need to maintain all existing business logic while improving structure
- Must preserve NoLock hints and performance optimizations
- Error handling should use errorCode/errorMsg pattern consistently
