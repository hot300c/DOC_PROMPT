USE [QAHosGenericDB]
GO
/****** Object:  StoredProcedure [dbo].[ws_BIL_InvoiceDetail_Save_Vaccine]    Script Date: 8/14/2025 2:53:42 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[ws_BIL_InvoiceDetail_Save_Vaccine]
(
    @SessionID VARCHAR(MAX),
    @FacID VARCHAR(10) = '8.1', --1.1.3.1
    @InvoiceDetailID UNIQUEIDENTIFIER ,
    @InvoiceID UNIQUEIDENTIFIER,
    @PatientID UNIQUEIDENTIFIER = NULL,
    @FacAdmissionID UNIQUEIDENTIFIER = NULL,
    @PhysicianAdmissionID UNIQUEIDENTIFIER = NULL,
    @ParentClinicalSessionID UNIQUEIDENTIFIER = NULL,
    @ClinicalSessionID UNIQUEIDENTIFIER = NULL,
    @AdvancedPaymentID UNIQUEIDENTIFIER = NULL,
    @ApprovedOutID UNIQUEIDENTIFIER = NULL,
    @DoiTuongTinhTienID INT = NULL,
    @MaChung_Vaccine VARCHAR(50) = '',
    @NoiDung NVARCHAR(1000) = '',
    @ServiceID INT = 0,
    @ProductID INT = 0,
    @BedID INT = 0,
    @BloodID INT = 0,
    @UnitID INT = 0,
    @Batch NVARCHAR(50) = NULL,
    @ExpDate DATETIME = NULL,
    @Qty DECIMAL(18, 2),
    @DonGia MONEY = 0,
    @PatientPay MONEY = 0,
    @MedicarePay MONEY = 0,
    @NguonKhac MONEY = 0,
    @SoTienGiam MONEY = 0,
    @IsComplete BIT = 1,
    @IsRefund BIT = 0,
    @IsNgoaiGio BIT = 0,
    @IsGoi BIT = 0,
    @IsTiem BIT = 0             --1.1.2.1
)
AS
SET NOCOUNT ON;

----------------------------------------------------------------------
DECLARE @UserID UNIQUEIDENTIFIER;
DECLARE @HistoryCaptureYN VARCHAR(1);

SELECT  @UserID = UserID
  FROM  [Security]..[Sessions] WITH (NOLOCK)
 WHERE  [SessionID] = @SessionID;

-- check if user authenticated
IF @UserID IS NULL
    RETURN;

DECLARE @Original_InvoiceID UNIQUEIDENTIFIER;
DECLARE @Original_PatientID UNIQUEIDENTIFIER;
DECLARE @Original_FacAdmissionID UNIQUEIDENTIFIER;
DECLARE @Original_PhysicianAdmissionID UNIQUEIDENTIFIER;
DECLARE @Original_ParentClinicalSessionID UNIQUEIDENTIFIER;
DECLARE @Original_ClinicalSessionID UNIQUEIDENTIFIER;
DECLARE @Original_DoiTuongTinhTienID INT;
DECLARE @Original_NoiDung NVARCHAR(1000);
DECLARE @Original_ServiceID INT;
DECLARE @Original_ProductID INT;
DECLARE @Original_BedID INT;
DECLARE @Original_BloodID INT;
DECLARE @Original_UnitID INT;
DECLARE @Original_Qty DECIMAL(18, 2);
DECLARE @Original_DonGia MONEY;
DECLARE @Original_PatientPay MONEY;
DECLARE @Original_MedicarePay MONEY;
DECLARE @Original_IsComplete BIT;
DECLARE @Original_IsCongTruyen BIT;
DECLARE @Original_IsRefund BIT;
DECLARE @Original_RefundType TINYINT;
DECLARE @Original_DoctorBy UNIQUEIDENTIFIER;
DECLARE @exists INT;
DECLARE @changed INT;

SET @changed = 0;
SET @exists = 0;

SELECT  @Original_InvoiceID               = [InvoiceID], @Original_PatientID = [PatientID],
        @Original_FacAdmissionID          = [FacAdmissionID], @Original_PhysicianAdmissionID = [PhysicianAdmissionID],
        @Original_ParentClinicalSessionID = [ParentClinicalSessionID],
        @Original_ClinicalSessionID       = [ClinicalSessionID], @Original_DoiTuongTinhTienID = [DoiTuongTinhTienID],
        @Original_NoiDung                 = NoiDung, @Original_ServiceID = [ServiceID], @Original_ProductID = [ProductID],
        @Original_BedID                   = [BedID], @Original_BloodID = [BloodID], @Original_UnitID = [UnitID], @Original_Qty = [Qty],
        @Original_DonGia                  = [DonGia], @Original_PatientPay = [PatientPay], @Original_MedicarePay = [MedicarePay],
        @Original_IsComplete              = [IsComplete], @Original_IsRefund = [IsRefund], @Original_RefundType = [RefundType],
        @exists                           = 1
  FROM  BIL_InvoiceDetail WITH (NOLOCK)
 WHERE  InvoiceDetailID = @InvoiceDetailID;

--1.1.4.1
DECLARE @ChenhLech MONEY;

SELECT  FacID, ClinicalSessionID, ParentClinicalSessionID, Qty, IsPaid, IsPaidChenhLech, ProductID, ServiceID,
        ISNULL (IsNgoaiGio, 0) IsNgoaiGio, HopDongID, PhacDo_Detail_ID, PhacDo_ID
  INTO  #CN_ClinicalSessions
  FROM  dbo.CN_ClinicalSessions WITH (NOLOCK)
 WHERE  ClinicalSessionID = @ClinicalSessionID;

-- Lấy lại UserID của người thu tạm ứng trước đó 1.1.2.1
IF @IsTiem = 1
BEGIN

    SET @UserID = (   SELECT    TOP 1  CreatedByUser
                        FROM    dbo.BIL_Invoice BI WITH (NOLOCK)    --#BIL_Invoice_T
                       WHERE    PatientID = @PatientID
                         AND    IsTamUng     = 1
                       ORDER BY CreatedDateAsInt DESC);

    /*1.1.4.1*/
    DECLARE @HopDongID UNIQUEIDENTIFIER, @L_PhacDoDetailID INT, @L_PhacDoID INT;

    SELECT  @HopDongID = HopDongID, @L_PhacDoDetailID = PhacDo_Detail_ID, @L_PhacDoID = PhacDo_ID
      FROM  #CN_ClinicalSessions;

    --SELECT	*
    --INTO	#Vaccine_HopDong_Detail_Temp
    --FROM	dbo.Vaccine_HopDong_Detail VHDD WITH (NOLOCK)
    --WHERE	HopDongID = @HopDongID



    DECLARE @Count INT;

    SELECT  @Count = COUNT (1)
      FROM  Vaccine_HopDong_Detail WITH (NOLOCK)
     WHERE  HopDongID                     = @HopDongID
       AND  IDPhacDo                      = @L_PhacDoID
       AND  ISNULL (IsMuiNgoaiDanhMuc, 0) = 0
       AND  ISNULL (IsTiemNgoai, 0)       = 0
       AND  MaMuiTiem                     = @L_PhacDoDetailID;


    IF @Count = 1 -- trường hợp có 1 mũi trong hợp đồng, lấy trực tiếp
    BEGIN
        SELECT  TOP 1   @ChenhLech
                                    = CASE
                                           WHEN ISNULL (GiaChenhLechChuaGiam, 0) <> 0 THEN ISNULL (GiaChenhLechChuaGiam, 0)
                                           ELSE
                                               CASE
                                                    WHEN ISNULL (IsTiemNgoai, 0) = 0
                                                     AND ISNULL (IsMuiNgoaiDanhMuc, 0) = 0 THEN
            (ISNULL (TienGiam, 0) - CASE
                                         WHEN TienGiam > 0 THEN TienGiam
                                         ELSE GiaMuiTiem * ISNULL (PhanTramGiam, 0) / 100.00 END)
            + GiaChenhLechTiemNgoai
                                                    ELSE 0 END
                                      --PhanTramGiam * GiaChenhLechTiemNgoai / NULLIF((100 - PhanTramGiam), 0)
                                      END,  --GiaChenhLechTiemNgoai,
                        @SoTienGiam = TienGiam, @PatientPay = GiaMuiTiem, @DonGia = GiaMuiTiem
          FROM  dbo.Vaccine_HopDong_Detail VHDDT WITH (NOLOCK)  --#Vaccine_HopDong_Detail_Temp VHDDT
         WHERE  HopDongID                     = @HopDongID
           AND  IDPhacDo                      = @L_PhacDoID
           AND  ISNULL (IsMuiNgoaiDanhMuc, 0) = 0
           AND  ISNULL (IsTiemNgoai, 0)       = 0
           AND  VHDDT.MaMuiTiem               = @L_PhacDoDetailID
         ----AND ISNULL(TienGiam, 0) > 0
         ORDER BY MaMuiTiem;
    END;
    ELSE --trường hợp có 2 mũi trong hợp đồng trùng nhau, thì lấy trong phụ lục ra để biết mũi nào đổi
    BEGIN
        SELECT  TOP 1   @ChenhLech
                                    = CASE
                                           WHEN ISNULL (GiaChenhLechChuaGiam, 0) <> 0 THEN ISNULL (GiaChenhLechChuaGiam, 0)
                                           ELSE
                                               CASE
                                                    WHEN ISNULL (IsTiemNgoai, 0) = 0
                                                     AND ISNULL (IsMuiNgoaiDanhMuc, 0) = 0 THEN
            (ISNULL (TienGiam, 0) - CASE
                                         WHEN TienGiam > 0 THEN TienGiam
                                         ELSE GiaMuiTiem * ISNULL (PhanTramGiam, 0) / 100.00 END)
            + GiaChenhLechTiemNgoai
                                                    ELSE 0 END
                                      --PhanTramGiam * GiaChenhLechTiemNgoai / NULLIF((100 - PhanTramGiam), 0)
                                      END,  --GiaChenhLechTiemNgoai,
                        @SoTienGiam = TienGiam, @PatientPay = GiaMuiTiem, @DonGia = GiaMuiTiem
          FROM  dbo.Vaccine_HopDong_Detail                     VHDDT WITH (NOLOCK)
                INNER JOIN dbo.CN_PhuLucHopDong_Vaccine_Detail b WITH (NOLOCK) ON VHDDT.HopDongDetailID = b.HopDongDetailID
         WHERE  HopDongID                     = @HopDongID
           AND  IDPhacDo                      = @L_PhacDoID
           AND  ISNULL (IsMuiNgoaiDanhMuc, 0) = 0
           AND  ISNULL (IsTiemNgoai, 0)       = 0
           AND  VHDDT.MaMuiTiem               = @L_PhacDoDetailID
           AND  VHDDT.IsDoiMui                = 1
         ORDER BY MaMuiTiem;
    END;
    --1.1.5.1



    IF ISNULL (@PatientPay, 0) = 0
    BEGIN ---dự phòng trường hợp nếu không lấy được giá mũi tiêm từ hợp đồng do bất cứ sai sót nào của hợp đồng thì vẫn có thể lấy doanh thu
        SELECT  TOP 1   @ChenhLech
                                    = CASE
                                           WHEN ISNULL (GiaChenhLechChuaGiam, 0) <> 0 THEN ISNULL (GiaChenhLechChuaGiam, 0)
                                           ELSE
                                               CASE
                                                    WHEN ISNULL (IsTiemNgoai, 0) = 0
                                                     AND ISNULL (IsMuiNgoaiDanhMuc, 0) = 0 THEN
            (ISNULL (TienGiam, 0) - CASE
                                         WHEN TienGiam > 0 THEN TienGiam
                                         ELSE GiaMuiTiem * ISNULL (PhanTramGiam, 0) / 100.00 END)
            + GiaChenhLechTiemNgoai
                                                    ELSE 0 END
                                      --PhanTramGiam * GiaChenhLechTiemNgoai / NULLIF((100 - PhanTramGiam), 0)
                                      END,  --GiaChenhLechTiemNgoai,
                        @SoTienGiam = TienGiam, @PatientPay = GiaMuiTiem, @DonGia = GiaMuiTiem
          FROM  dbo.Vaccine_HopDong_Detail VHDDT WITH (NOLOCK)  --#Vaccine_HopDong_Detail_Temp VHDDT
         WHERE  HopDongID                     = @HopDongID
           AND  IDPhacDo                      = @L_PhacDoID
           AND  ISNULL (IsMuiNgoaiDanhMuc, 0) = 0
           AND  ISNULL (IsTiemNgoai, 0)       = 0
         --   AND VHDDT.MaMuiTiem=@L_PhacDoDetailID
         ----AND ISNULL(TienGiam, 0) > 0
         ORDER BY MaMuiTiem;
    END;
END;

IF @exists = 0 -- Insert New
BEGIN
    IF @DoiTuongTinhTienID NOT IN ( 88, 99 )
        SET @PatientPay = @Qty * @DonGia;

    --DECLARE @FacID VARCHAR(10)
    SELECT  @ParentClinicalSessionID = ParentClinicalSessionID  FROM  #CN_ClinicalSessions CCS;

	IF NOT EXISTS (SELECT 1 FROM #CN_ClinicalSessions WITH (NOLOCK) -- 1.0.0.9
				  )
	   AND @ProductID <> 0
	   AND @Qty <>
	   (
		   SELECT Qty FROM #CN_ClinicalSessions WITH (NOLOCK) -- 1.0.0.9
	   )
	BEGIN
		RAISERROR(N'SL thuốc đã được thay đổi. Vui lòng tải lại dữ liệu.', 16, 1);

		RETURN;
	END;

    --1.0.0.12  
	IF NOT EXISTS (SELECT 1 FROM #CN_ClinicalSessions WITH (NOLOCK))
	   AND @ServiceID <> 0
	BEGIN
		RAISERROR(N'DV KT đã được thay đổi. Vui lòng tải lại dữ liệu.', 16, 1);

		RETURN;
	END;
	--======================================================================================================================--
    BEGIN
        INSERT  [BIL_InvoiceDetail] ([InvoiceDetailID], [CheckSum_FacID], [InvoiceID], [PatientID], [FacAdmissionID],
                                     [PhysicianAdmissionID], [ParentClinicalSessionID], [ClinicalSessionID],
                                     [AdvancedPaymentID], [DoiTuongTinhTienID], [NoiDung], [MaChung_Vaccine],
                                     [ServiceID], [ProductID], [BedID], [BloodID], [UnitID], [ApprovedOutID], [Batch],
                                     [ExpDate], [Qty], [DonGia], [PatientPay], [MedicarePay], [ChenhLech],
                                     [SoTienGiam], [IsComplete], [IsGoi], [IsRefund], [CreatedDateAsInt],
                                     [CreatedDate], [CreatedOn], [CreatedBy], [ModifiedOn], [ModifiedBy])
        SELECT  @InvoiceDetailID, CHECKSUM (@FacID), @InvoiceID, @PatientID, @FacAdmissionID, @PhysicianAdmissionID,
                @ParentClinicalSessionID, @ClinicalSessionID, @AdvancedPaymentID, @DoiTuongTinhTienID, @NoiDung,
                @MaChung_Vaccine, @ServiceID, @ProductID, @BedID, @BloodID, @UnitID, @ApprovedOutID, @Batch, @ExpDate,
                @Qty, @DonGia, @PatientPay, @MedicarePay, @ChenhLech, @SoTienGiam, @IsComplete, @IsGoi, @IsRefund,
                FORMAT (GETDATE (), 'yyyyMMdd', 'en-US'), CAST(GETDATE () AS DATE), GETDATE (), @UserID, GETDATE (),
                @UserID;
		
		INSERT  [BIL_InvoiceDetail_Live] ([InvoiceDetailID], [CheckSum_FacID], [InvoiceID], [PatientID], [FacAdmissionID],
                                     [PhysicianAdmissionID], [ParentClinicalSessionID], [ClinicalSessionID],
                                     [AdvancedPaymentID], [DoiTuongTinhTienID], [NoiDung], [MaChung_Vaccine],
                                     [ServiceID], [ProductID], [BedID], [BloodID], [UnitID], [ApprovedOutID], [Batch],
                                     [ExpDate], [Qty], [DonGia], [PatientPay], [MedicarePay], [ChenhLech],
                                     [SoTienGiam], [IsComplete], [IsGoi], [IsRefund], [CreatedDateAsInt],
                                     [CreatedDate], [CreatedOn], [CreatedBy], [ModifiedOn], [ModifiedBy])
        SELECT  @InvoiceDetailID, CHECKSUM (@FacID), @InvoiceID, @PatientID, @FacAdmissionID, @PhysicianAdmissionID,
                @ParentClinicalSessionID, @ClinicalSessionID, @AdvancedPaymentID, @DoiTuongTinhTienID, @NoiDung,
                @MaChung_Vaccine, @ServiceID, @ProductID, @BedID, @BloodID, @UnitID, @ApprovedOutID, @Batch, @ExpDate,
                @Qty, @DonGia, @PatientPay, @MedicarePay, @ChenhLech, @SoTienGiam, @IsComplete, @IsGoi, @IsRefund,
                FORMAT (GETDATE (), 'yyyyMMdd', 'en-US'), CAST(GETDATE () AS DATE), GETDATE (), @UserID, GETDATE (),
                @UserID;

		EXEC [QAHosGenericDB]..[ws_BIL_InvoiceDetail_CurrentDay_ByInvoiceDetail_Save] @SessionID = @SessionID,         -- varchar(max)
	                                                                                @InvoiceDetailID = @InvoiceDetailID, -- uniqueidentifier
	                                                                                @FacID = @FacID;              -- varchar(10)
        IF @AdvancedPaymentID IS NOT NULL
        BEGIN
            INSERT INTO dbo.BIL_Invoice_AdvancedPayment (FacID_Checksum, CreatedAsInt, InvoiceID)
            VALUES (CHECKSUM (@FacID),                          -- FacID_Checksum - int
                    FORMAT (GETDATE (), 'yyyyMMdd', 'en-US'),   -- CreatedAsInt - int
                    @InvoiceID                                  -- InvoiceID - uniqueidentifier
                );
        END;
        SET @changed = 1;
		--======================================================================================================================--
    END;
END;

DROP TABLE #CN_ClinicalSessions;

IF @changed = 1
    EXEC History..sp_BIL_InvoiceDetail_LogUpdate @InvoiceDetailID, @UserID;