 
/*
Version: 1.0.0.0 2017-10-27 12:00 HiepNH : ....................... auto description
Version: 1.0.0.1 2018-10-02 16:00 Anhnn : thêm cột NguoiLienHe
Version; 1.0.1.0 20190607 11:30 M.Hieu Thêm cột TypeID_LoaiThu
*/
CREATE PROCEDURE [dbo].[sp_BIL_Invoice_LogUpdate]
    (
      @InvoiceID UNIQUEIDENTIFIER ,
      @FacID VARCHAR(10) ,
      @UserID UNIQUEIDENTIFIER
    )
AS 
    SET Nocount ON
  

----------------------------------------------------------------------
-- 				 Debug
----------------------------------------------------------------------

-- Declare @UserID uniqueidentifier
-- Set @UserID = ''

-- Declare @InvoiceID uniqueidentifier
-- Declare @FacID varchar(10)
-- Set @InvoiceID = ''
-- Set @FacID = ''

----------------------------------------------------------------------


----------------------------------------------------------------------
---- Logic for BIL_Invoice
----------------------------------------------------------------------


    INSERT  [History]..[BIL_Invoice]
            ( [DeleteFlag] ,
              [InvoiceID] ,
              [FacID] ,
              [PatientID] ,
              [CustomerID] ,
              [CaseID] ,
              [FacAdmissionID] ,
              [PhysicianAdmissionID] ,
              [MedicalCostRecordID] ,
              [InvoiceNo] ,
              [DoiTuongID] ,
              [Total] ,
              [RealTotal] ,
              [IsPaid] ,
              [PatientType] ,
              [Discount] ,
              [Reason] ,
              [Description] ,
              [Note] ,
              [IsRefund] ,
              [RefundType] ,
              [IsMedicarePatient] ,
              [MedicareCardNo] ,
              [EffectiveFrom] ,
              [EffectiveThru] ,
              [PercentMedicarePay] ,
              [SoThang] ,
              [CreatedOnByUser] ,
              [CreatedByUser] ,
              [ApprovedOutID] ,
              [ApprovedInID] ,
              [ShiftID] ,
              [ShiftName] ,
              [CounterID] ,
              [ReceiptNumber] ,
              [IPUser] ,
              [MacAddressUser] ,
              [SoTK] ,
              [SoTKNhan] ,
              [IDLockShift] ,
              [UserCreatedDateAsInt] ,
              [HopDongID] ,
              [HinhThucThanhToan] ,
              [CreatedBy] ,
              [CreatedOn] ,
              [ModifiedBy] ,
              [ModifiedOn],
			  NguoiLienHe,
			  TypeID_LoaiThu
            )
            SELECT  0 ,
                    [InvoiceID] ,
                    [FacID] ,
                    [PatientID] ,
                    [CustomerID] ,
                    [CaseID] ,
                    [FacAdmissionID] ,
                    [PhysicianAdmissionID] ,
                    [MedicalCostRecordID] ,
                    [InvoiceNo] ,
                    [DoiTuongID] ,
                    [Total] ,
                    [RealTotal] ,
                    [IsPaid] ,
                    [PatientType] ,
                    [Discount] ,
                    [Reason] ,
                    [Description] ,
                    [Note] ,
                    [IsRefund] ,
                    [RefundType] ,
                    [IsMedicarePatient] ,
                    [MedicareCardNo] ,
                    [EffectiveFrom] ,
                    [EffectiveThru] ,
                    [PercentMedicarePay] ,
                    [SoThang] ,
                    [CreatedOnByUser] ,
                    [CreatedByUser] ,
                    [ApprovedOutID] ,
                    [ApprovedInID] ,
                    [ShiftID] ,
                    [ShiftName] ,
                    [CounterID] ,
                    [ReceiptNumber] ,
                    [IPUser] ,
                    [MacAddressUser] ,
                    [SoTK] ,
                    [SoTKNhan] ,
                    [IDLockShift] ,
  CreatedDateAsInt ,
                    [HopDongID] ,
                    [HinhThucThanhToan] ,
                    [CreatedBy] ,
                    [CreatedOn] ,
                    [ModifiedBy] ,
                    [ModifiedOn],
					NguoiLienHe,
					TypeID_LoaiThu
            FROM    [QAHosGenericDB]..[BIL_Invoice] WITH ( NOLOCK )
            WHERE   InvoiceID = @InvoiceID

    IF 1 = 1 
        RETURN
----------------------------------------------------------------------
---- Logic for BIL_InvoiceLog
----------------------------------------------------------------------


    DECLARE @Original_FacID NVARCHAR(MAX)
    DECLARE @Original_PatientID NVARCHAR(MAX)
    DECLARE @Original_CustomerID NVARCHAR(MAX)
    DECLARE @Original_CaseID NVARCHAR(MAX)
    DECLARE @Original_FacAdmissionID NVARCHAR(MAX)
    DECLARE @Original_PhysicianAdmissionID NVARCHAR(MAX)
    DECLARE @Original_InvoiceNo NVARCHAR(MAX)
    DECLARE @Original_DoiTuongID NVARCHAR(MAX)
    DECLARE @Original_Total NVARCHAR(MAX)
    DECLARE @Original_RealTotal NVARCHAR(MAX)
    DECLARE @Original_IsPaid NVARCHAR(MAX)
    DECLARE @Original_PatientType NVARCHAR(MAX)
    DECLARE @Original_Discount NVARCHAR(MAX)
    DECLARE @Original_Reason NVARCHAR(MAX)
    DECLARE @Original_Description NVARCHAR(MAX)
    DECLARE @Original_Note NVARCHAR(MAX)
    DECLARE @Original_IsRefund NVARCHAR(MAX)
    DECLARE @Original_IsMedicarePatient NVARCHAR(MAX)
    DECLARE @Original_MedicareCardNo NVARCHAR(MAX)
    DECLARE @Original_EffectiveFrom NVARCHAR(MAX)
    DECLARE @Original_EffectiveThru NVARCHAR(MAX)
    DECLARE @Original_PercentMedicarePay NVARCHAR(MAX)
    DECLARE @Original_SoThang NVARCHAR(MAX)
    DECLARE @Original_ApprovedOutID NVARCHAR(MAX)
    DECLARE @Original_ApprovedInID NVARCHAR(MAX)
    DECLARE @Original_ShiftID NVARCHAR(MAX)
    DECLARE @Original_ShiftName NVARCHAR(MAX)
    DECLARE @Original_CounterID NVARCHAR(MAX)
    DECLARE @Original_ReceiptNumber NVARCHAR(MAX)
    DECLARE @exists INT


    SET @exists = 0


    SELECT  @Original_FacID = [FacID] ,
            @Original_PatientID = [PatientID] ,
            @Original_CustomerID = [CustomerID] ,
            @Original_CaseID = [CaseID] ,
            @Original_FacAdmissionID = [FacAdmissionID] ,
            @Original_PhysicianAdmissionID = [PhysicianAdmissionID] ,
            @Original_InvoiceNo = [InvoiceNo] ,
            @Original_DoiTuongID = [DoiTuongID] ,
            @Original_Total = [Total] ,
            @Original_RealTotal = [RealTotal] ,
            @Original_IsPaid = [IsPaid] ,
            @Original_PatientType = [PatientType] ,
            @Original_Discount = [Discount] ,
            @Original_Reason = [Reason] ,
            @Original_Description = [Description] ,
            @Original_Note = [Note] ,
            @Original_IsRefund = [IsRefund] ,
            @Original_IsMedicarePatient = [IsMedicarePatient] ,
            @Original_MedicareCardNo = [MedicareCardNo] ,
            @Original_EffectiveFrom = [EffectiveFrom] ,
            @Original_EffectiveThru = [EffectiveThru] ,
            @Original_PercentMedicarePay = [PercentMedicarePay] ,
            @Original_SoThang = [SoThang] ,
            @Original_ApprovedOutID = [ApprovedOutID] ,
            @Original_ApprovedInID = [ApprovedInID] ,
            @Original_ShiftID = [ShiftID] ,
            @Original_ShiftName = [ShiftName] ,
            @Original_CounterID = [CounterID] ,
            @Original_ReceiptNumber = [ReceiptNumber] ,
            @exists = 1
    FROM    [History]..[BIL_Invoice] WITH ( NOLOCK )
    WHERE   InvoiceID = @InvoiceID
            AND FacID = @FacID
            AND HistorySeq = ( SELECT   MAX(HistorySeq)
                               FROM     [History]..[BIL_Invoice] WITH ( NOLOCK )
                               WHERE    InvoiceID = @InvoiceID
                                        AND FacID = @FacID
                             )


    IF @exists = 1 
        BEGIN
            DECLARE @HistorySeq BIGINT 
            SET @HistorySeq = ( SELECT  MAX(HistorySeq)
                                FROM    [History]..[BIL_Invoice] WITH ( NOLOCK )
                                WHERE   InvoiceID = @InvoiceID
                                        AND FacID = @FacID
                              )
        END
    DECLARE @New_FacID NVARCHAR(MAX)
    DECLARE @New_PatientID NVARCHAR(MAX)
    DECLARE @New_CustomerID NVARCHAR(MAX)
    DECLARE @New_CaseID NVARCHAR(MAX)
    DECLARE @New_FacAdmissionID NVARCHAR(MAX)
    DECLARE @New_PhysicianAdmissionID NVARCHAR(MAX)
    DECLARE @New_InvoiceNo NVARCHAR(MAX)
    DECLARE @New_DoiTuongID NVARCHAR(MAX)
    DECLARE @New_Total NVARCHAR(MAX)
    DECLARE @New_RealTotal NVARCHAR(MAX)
    DECLARE @New_IsPaid NVARCHAR(MAX)
    DECLARE @New_PatientType NVARCHAR(MAX)
    DECLARE @New_Discount NVARCHAR(MAX)
    DECLARE @New_Reason NVARCHAR(MAX)
    DECLARE @New_Description NVARCHAR(MAX)
    DECLARE @New_Note NVARCHAR(MAX)
    DECLARE @New_IsRefund NVARCHAR(MAX)
    DECLARE @New_IsMedicarePatient NVARCHAR(MAX)
    DECLARE @New_MedicareCardNo NVARCHAR(MAX)
    DECLARE @New_EffectiveFrom NVARCHAR(MAX)
    DECLARE @New_EffectiveThru NVARCHAR(MAX)
    DECLARE @New_PercentMedicarePay NVARCHAR(MAX)
    DECLARE @New_SoThang NVARCHAR(MAX)
    DECLARE @New_ApprovedOutID NVARCHAR(MAX)
    DECLARE @New_ApprovedInID NVARCHAR(MAX)
    DECLARE @New_ShiftID NVARCHAR(MAX)
    DECLARE @New_ShiftName NVARCHAR(MAX)
    DECLARE @New_CounterID NVARCHAR(MAX)
    DECLARE @New_ReceiptNumber NVARCHAR(MAX)

    SELECT  @New_FacID = [FacID] ,
            @New_PatientID = [PatientID] ,
            @New_CustomerID = [CustomerID] ,
            @New_CaseID = [CaseID] ,
            @New_FacAdmissionID = [FacAdmissionID] ,
            @New_PhysicianAdmissionID = [PhysicianAdmissionID] ,
            @New_InvoiceNo = [InvoiceNo] ,
            @New_DoiTuongID = [DoiTuongID] ,
            @New_Total = [Total] ,
            @New_RealTotal = [RealTotal] ,
            @New_IsPaid = [IsPaid] ,
            @New_PatientType = [PatientType] ,
            @New_Discount = [Discount] ,
            @New_Reason = [Reason] ,
            @New_Description = [Description] ,
            @New_Note = [Note] ,
            @New_IsRefund = [IsRefund] ,
            @New_IsMedicarePatient = [IsMedicarePatient] ,
            @New_MedicareCardNo = [MedicareCardNo] ,
            @New_EffectiveFrom = [EffectiveFrom] ,
            @New_EffectiveThru = [EffectiveThru] ,
            @New_PercentMedicarePay = [PercentMedicarePay] ,
            @New_SoThang = [SoThang] ,
            @New_ApprovedOutID = [ApprovedOutID] ,
            @New_ApprovedInID = [ApprovedInID] ,
            @New_ShiftID = [ShiftID] ,
            @New_ShiftName = [ShiftName] ,
            @New_CounterID = [CounterID] ,
            @New_ReceiptNumber = [ReceiptNumber]
    FROM    [QAHosGenericDB]..[BIL_Invoice] WITH ( NOLOCK )
    WHERE   InvoiceID = @InvoiceID
            AND FacID = @FacID


    DECLARE @ModifiedOn DATETIME
    SET @ModifiedOn = GETDATE()


    IF ISNULL(@Original_FacID, '') <> ISNULL(@New_FacID, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'FacID' ,
                  @Original_FacID ,
                  @New_FacID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_PatientID, '') <> ISNULL(@New_PatientID, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'PatientID' ,
                  @Original_PatientID ,
                  @New_PatientID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_CustomerID, '') <> ISNULL(@New_CustomerID, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'CustomerID' ,
                  @Original_CustomerID ,
                  @New_CustomerID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_CaseID, '') <> ISNULL(@New_CaseID, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'CaseID' ,
                  @Original_CaseID ,
                  @New_CaseID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_FacAdmissionID, '') <> ISNULL(@New_FacAdmissionID, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'FacAdmissionID' ,
                  @Original_FacAdmissionID ,
                  @New_FacAdmissionID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_PhysicianAdmissionID, '') <> ISNULL(@New_PhysicianAdmissionID,
                                                            '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'PhysicianAdmissionID' ,
                  @Original_PhysicianAdmissionID ,
                  @New_PhysicianAdmissionID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_InvoiceNo, '') <> ISNULL(@New_InvoiceNo, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'InvoiceNo' ,
                  @Original_InvoiceNo ,
                  @New_InvoiceNo ,
                  @HistorySeq
                )

    IF ISNULL(@Original_DoiTuongID, '') <> ISNULL(@New_DoiTuongID, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'DoiTuongID' ,
                  @Original_DoiTuongID ,
                  @New_DoiTuongID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_Total, '') <> ISNULL(@New_Total, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'Total' ,
                  @Original_Total ,
                  @New_Total ,
                  @HistorySeq
                )

    IF ISNULL(@Original_RealTotal, '') <> ISNULL(@New_RealTotal, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'Total' ,
                  @Original_RealTotal ,
                  @New_RealTotal ,
                  @HistorySeq
                )


    IF ISNULL(@Original_IsPaid, '') <> ISNULL(@New_IsPaid, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'IsPaid' ,
                  @Original_IsPaid ,
                  @New_IsPaid ,
                  @HistorySeq
                )

    IF ISNULL(@Original_PatientType, '') <> ISNULL(@New_PatientType, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'PatientType' ,
                  @Original_PatientType ,
                  @New_PatientType ,
                  @HistorySeq
                )

    IF ISNULL(@Original_Discount, '') <> ISNULL(@New_Discount, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'Discount' ,
                  @Original_Discount ,
                  @New_Discount ,
                  @HistorySeq
                )

    IF ISNULL(@Original_Reason, '') <> ISNULL(@New_Reason, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'Reason' ,
                  @Original_Reason ,
                  @New_Reason ,
                  @HistorySeq
                )

    IF ISNULL(@Original_Description, '') <> ISNULL(@New_Description, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'Description' ,
                  @Original_Description ,
                  @New_Description ,
                  @HistorySeq
                )

    IF ISNULL(@Original_Note, '') <> ISNULL(@New_Note, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'Note' ,
                  @Original_Note ,
                  @New_Note ,
                  @HistorySeq
                )

    IF ISNULL(@Original_IsRefund, '') <> ISNULL(@New_IsRefund, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'IsRefund' ,
                  @Original_IsRefund ,
                  @New_IsRefund ,
                  @HistorySeq
                )

    IF ISNULL(@Original_IsMedicarePatient, '') <> ISNULL(@New_IsMedicarePatient,
                                                         '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'IsMedicarePatient' ,
                  @Original_IsMedicarePatient ,
                  @New_IsMedicarePatient ,
                  @HistorySeq
                )

    IF ISNULL(@Original_MedicareCardNo, '') <> ISNULL(@New_MedicareCardNo, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'MedicareCardNo' ,
                  @Original_MedicareCardNo ,
                  @New_MedicareCardNo ,
                  @HistorySeq
                )

    IF ISNULL(@Original_EffectiveFrom, '') <> ISNULL(@New_EffectiveFrom, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'EffectiveFrom' ,
                  @Original_EffectiveFrom ,
                  @New_EffectiveFrom ,
                  @HistorySeq
                )

    IF ISNULL(@Original_EffectiveThru, '') <> ISNULL(@New_EffectiveThru, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'EffectiveThru' ,
                  @Original_EffectiveThru ,
                  @New_EffectiveThru ,
                  @HistorySeq
                )

    IF ISNULL(@Original_PercentMedicarePay, '') <> ISNULL(@New_PercentMedicarePay,
                                                          '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'PercentMedicarePay' ,
                  @Original_PercentMedicarePay ,
                  @New_PercentMedicarePay ,
                  @HistorySeq
                )

    IF ISNULL(@Original_SoThang, '') <> ISNULL(@New_SoThang, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'SoThang' ,
                  @Original_SoThang ,
                  @New_SoThang ,
                  @HistorySeq
                )

    IF ISNULL(@Original_ApprovedOutID, '') <> ISNULL(@New_ApprovedOutID, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'ApprovedOutID' ,
                  @Original_ApprovedOutID ,
                  @New_ApprovedOutID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_ApprovedInID, '') <> ISNULL(@New_ApprovedInID, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'ApprovedInID' ,
                  @Original_ApprovedInID ,
                  @New_ApprovedInID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_ShiftID, '') <> ISNULL(@New_ShiftID, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'ShiftID' ,
                  @Original_ShiftID ,
                  @New_ShiftID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_ShiftName, '') <> ISNULL(@New_ShiftName, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'ShiftName' ,
                  @Original_ShiftName ,
                  @New_ShiftName ,
                  @HistorySeq
                )

    IF ISNULL(@Original_CounterID, '') <> ISNULL(@New_CounterID, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'CounterID' ,
                  @Original_CounterID ,
                  @New_CounterID ,
                  @HistorySeq
                )

    IF ISNULL(@Original_ReceiptNumber, '') <> ISNULL(@New_ReceiptNumber, '')
        AND @exists = 1 
        INSERT  [History]..[BIL_InvoiceLog]
                ( ModifiedOn ,
                  ModifiedBy ,
                  FieldName ,
                  ValueOriginal ,
                  ValueNew ,
                  HistorySeq
                )
        VALUES  ( @ModifiedOn ,
                  @UserID ,
                  'ReceiptNumber' ,
                  @Original_ReceiptNumber ,
                  @New_ReceiptNumber ,
                  @HistorySeq
                )