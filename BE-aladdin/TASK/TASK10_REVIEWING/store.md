USE [QAHosGenericDB]
GO
/****** Object:  StoredProcedure [dbo].[ws_BIL_Invoice_Save_Vaccine]    Script Date: 8/14/2025 3:21:27 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[ws_BIL_Invoice_Save_Vaccine]
    @SessionID VARCHAR(300) = '',
    @InvoiceID UNIQUEIDENTIFIER,
    @FacID VARCHAR(10),
    @PatientID UNIQUEIDENTIFIER = NULL,
    @CaseID UNIQUEIDENTIFIER = NULL,
    @FacAdmissionID UNIQUEIDENTIFIER = NULL,
    @PhysicianAdmissionID UNIQUEIDENTIFIER = NULL,
    @HopDongID UNIQUEIDENTIFIER = NULL,
    @CounterID INT = 0,
    @InvoiceNo VARCHAR(40) = '',
    @DoiTuongID INT = NULL,
    @Total MONEY = 0,
    @RealTotal MONEY = 0,
    @IsPaid BIT = 1,
    @IsTamUng BIT = 0,
    @PatientType TINYINT = NULL,
    @Reason NVARCHAR(1000),
    @Note NVARCHAR(MAX) = '',
    @ReceiptNumber VARCHAR(50) = '',
    @SoKyHieu VARCHAR(20) = '',
    @ShiftID INT = 0,
    @HinhThucThanhToan NVARCHAR(200) = '',
    @IsVAT BIT = 0,
    @IsNgoaiGio BIT = 0,
    @IsChenhLech BIT = 0,
    @IsThuPhi BIT = 0,
    @TongTienGiam MONEY = 0, --1.0.3.1
    @PhanTramMienGiam FLOAT = 0,
    @LiDoMienGiam NVARCHAR(500) = '',
    @SoTK VARCHAR(250) = '',
    @SoTKNhan VARCHAR(250) = '',
    @ApprovedInID UNIQUEIDENTIFIER = NULL,
    @ApprovedOutID UNIQUEIDENTIFIER = NULL,
    @IsTiem BIT = 0,         --1.1.2.1
    @IPUser VARCHAR(250) = '',
    @MacAddressUser VARCHAR(250) = '',
    @TypeID_LoaiThu INT = 0
AS
SET NOCOUNT ON;

----------------------------------------------------------------------
-- 				 Debug
----------------------------------------------------------------------

--Declare @SessionID varchar(max) = '9BE6E1AE-4676-4454-93A7-3B5EBB9D5C3F#192.168.1.123'--(SELECT TOP 1 SessionID FROM Security..Sessions ORDER BY CreatedOn DESC)

--Declare @InvoiceID uniqueidentifier = 'aa7a3069-87b5-11e7-a207-f8bc127d7223'
--Declare @FacID varchar(10) = '3002'
--Declare @PatientID UNIQUEIDENTIFIER = '871c3436-7cfe-408a-981c-d133e4d20e6d'
--Declare @CaseID uniqueidentifier = 'a828f458-8e56-466f-8ab6-0fca7ee50e18'
--Declare @FacAdmissionID UNIQUEIDENTIFIER = '93cff70d-7ea7-4d5d-9036-cdf2edf27bd2'
--Declare @PhysicianAdmissionID UNIQUEIDENTIFIER = 'f110e5e1-7f20-4b4f-9d5b-b8e809213fbd'
--Declare @HopDongID UNIQUEIDENTIFIER = '679ff75b-9c4e-11e7-ac0d-40b89a5e97c4' 
--Declare @CounterID INT = 2
--Declare @InvoiceNo nvarchar(40) = ''
--Declare @Total money = 80000
--Declare @IsPaid bit = 1
--Declare @Reason nvarchar(1000) = N'Viện phí'
--Declare @Note nvarchar(2000) = N'Tiền viện phí: Khám Bệnh(80,000)'
--Declare @ApprovedInID UNIQUEIDENTIFIER = NULL
--Declare @ApprovedOutID uniqueidentifier= NULL
--Declare @ShiftID int = 1
--Declare @ShiftName nvarchar(300)
--Declare @ReceiptNumber nvarchar(100) = ''
--DECLARE @NguoiThuID UNIQUEIDENTIFIER = NULL
--DECLARE @DoiTuongID INT = 2
--DECLARE @IsChenhLech BIT = 0
--DECLARE @IsThuPhi BIT = 1
--DECLARE @IsTamUng BIT = 1
--DECLARE @IsNgoaiGio BIT = 0
--DECLARE @TongTienGiam MONEY = 0
--DECLARE @PhanTramMienGiam DECIMAL(18, 2) = '0'
--DECLARE @RefundType TINYINT = NULL
--DECLARE @IsVAT BIT = 0
--DECLARE @IsRightRoute BIT = 0   
--DECLARE @LiDoMienGiam NVARCHAR(100) = ''
--DECLARE @HinhThucThanhToan NVARCHAR(100) = ''
--DECLARE @SoTK NVARCHAR(100) =''
--DECLARE @SoTKNhan NVARCHAR(100) =''
--DECLARE @IPUser NVARCHAR(100) = ''
--DECLARE @MacAddressUser VARCHAR(100) ='5C260A586217'
----------------------------------------------------------------------
DECLARE @UserID UNIQUEIDENTIFIER, @EmpID UNIQUEIDENTIFIER;
DECLARE @HistoryCaptureYN VARCHAR(1);

SELECT  @UserID = UserID
  FROM  [Security]..[Sessions] WITH (NOLOCK)
 WHERE  [SessionID] = @SessionID;

-- check if user authenticated
IF @UserID IS NULL
    RETURN;

-- Lấy lại UserID của người thu tạm ứng trước đó 1.1.2.1
IF @IsTiem = 1
BEGIN
    SELECT  *
      INTO  #BIL_Invoice_T
      FROM  dbo.BIL_Invoice BI WITH (NOLOCK)
     WHERE  PatientID = @PatientID;

    SET @UserID = (   SELECT    TOP 1  CreatedByUser
                        FROM    #BIL_Invoice_T
                       WHERE    IsTamUng = 1
                       ORDER BY CreatedDateAsInt DESC);

    DROP TABLE #BIL_Invoice_T;
END;

SET @EmpID = (   SELECT EmpID
                   FROM Security..Users WITH (NOLOCK)
                  WHERE ID    = @UserID
                    AND FacID = @FacID);

DECLARE @Original_FacID VARCHAR(10);
DECLARE @Original_PatientID UNIQUEIDENTIFIER;
DECLARE @Original_CaseID UNIQUEIDENTIFIER;
DECLARE @Original_FacAdmissionID UNIQUEIDENTIFIER;
DECLARE @Original_PhysicianAdmissionID UNIQUEIDENTIFIER;
DECLARE @Original_CounterID INT;
DECLARE @Original_InvoiceNo VARCHAR(40);
DECLARE @Original_DoiTuongID INT;
DECLARE @Original_Total MONEY;
DECLARE @Original_IsPaid BIT;
DECLARE @Original_PatientType TINYINT;
DECLARE @Original_Reason NVARCHAR(500);
DECLARE @Original_Note NVARCHAR(MAX);
DECLARE @Original_ReceiptNumber VARCHAR(50);
DECLARE @Original_ShiftID INT;
DECLARE @exists INT;
DECLARE @changed INT;

SET @changed = 0;
SET @exists = 0;

SELECT  @Original_FacID          = [FacID], @Original_PatientID = [PatientID], @Original_CaseID = [CaseID],
        @Original_FacAdmissionID = [FacAdmissionID], @Original_PhysicianAdmissionID = [PhysicianAdmissionID],
        @Original_CounterID      = [CounterID], @Original_InvoiceNo = [InvoiceNo], @Original_DoiTuongID = [DoiTuongID],
        @Original_Total          = [Total], @Original_IsPaid = [IsPaid], @Original_PatientType = [PatientType],
        @Original_Reason         = [Reason], @Original_Note = [Note], @Original_ReceiptNumber = [ReceiptNumber],
        @Original_ShiftID        = [ShiftID], @exists = 1
  FROM  BIL_Invoice WITH (NOLOCK)
 WHERE  InvoiceID = @InvoiceID;

IF @CaseID = '00000000-0000-0000-0000-000000000000'
    SET @CaseID = NULL;

IF @HopDongID = '00000000-0000-0000-0000-000000000000'
    SET @HopDongID = NULL;

IF @exists = 0 -- Insert New
BEGIN
    DECLARE @Code VARCHAR(50), @Year VARCHAR(2), @Month VARCHAR(2), @Day VARCHAR(2);
    DECLARE @MaQuay VARCHAR(5), @MaDT VARCHAR(5);

    SET @MaQuay = RIGHT('00' + CAST(ISNULL ((   SELECT  OrderIndex
                                                  FROM  dbo.L_Counter WITH (NOLOCK)
                                                 WHERE  CounterID = @CounterID
                                                   AND  FacID     = @FacID),
                                            '0') AS VARCHAR(3)), 3);
    SET @MaDT = 'DV';

    DECLARE @FromTodayAsInt BIGINT = FORMAT (GETDATE (), 'yyyyMMdd000000', 'en-US');
    DECLARE @ThruTodayAsInt BIGINT = FORMAT (GETDATE (), 'yyyyMMdd235959', 'en-US');
    DECLARE @CheckSumFacID INT = CHECKSUM (@FacID);

    BEGIN
        --SELECT	CAST('00000000-0000-0000-0000-000000000000' AS UNIQUEIDENTIFIER) InvoiceID, CAST('' AS VARCHAR(50)) InvoiceNo, CAST('' AS VARCHAR(10)) FacID,
        --		CAST(0 AS BIT) IsTamUng, CAST(0 AS BIGINT) CreatedDateAsInt, CAST('' AS INT) 'yyyy'
        --INTO	#BIL_Invoice_TrongGio

        --TRUNCATE TABLE #BIL_Invoice_TrongGio
        BEGIN
            --INSERT	INTO #BIL_Invoice_TrongGio (InvoiceNo, FacID, CreatedDateAsInt, yyyy)
            --SELECT	InvoiceNo, FacID, CreatedDateAsInt, LEFT(CreatedDateAsInt, 4) 'yyyy'
            --FROM	dbo.BIL_Invoice BI WITH (NOLOCK)
            --WHERE	BI.CreatedDateAsInt BETWEEN @FromTodayAsInt AND @ThruTodayAsInt AND BI.CheckSum_FacID = @CheckSumFacID

            --WHERE    LEFT(CreatedDateAsInt, 8) = FORMAT(GETDATE(), 'yyyyMMdd', 'en-US')
            --         AND CheckSum_FacID = CHECKSUM(@FacID)  
            SET @Code = (   SELECT  TOP 1   CAST((SUBSTRING (InvoiceNo, CHARINDEX ('-', InvoiceNo) + 1, 9)) AS VARCHAR(15))
                              FROM  (   SELECT  InvoiceNo, FacID, CreatedDateAsInt  --, LEFT(CreatedDateAsInt, 4) AS yyyy
                                          FROM  dbo.BIL_Invoice_CurrentDay BI WITH (NOLOCK)
                                         WHERE  BI.CreatedDateAsInt BETWEEN @FromTodayAsInt AND @ThruTodayAsInt
                                           AND  BI.CheckSum_FacID = @CheckSumFacID) XXX
                             WHERE  LEFT(InvoiceNo, 4)                                                                               <> 'HDNG'
                               --AND SUBSTRING(InvoiceNo, CHARINDEX('-', InvoiceNo) - 8, 2) = @MaQuay
                               AND  RIGHT('00' + SUBSTRING (InvoiceNo, CHARINDEX ('-', InvoiceNo) - 9, LEN (@MaQuay)), LEN (
                                                                                                                           @MaQuay)) = @MaQuay
                             --AND LEFT(InvoiceNo, LEN(@MaQuay)) = @MaQuay
                             ORDER BY InvoiceNo DESC);
        END;

        SET @Year = RIGHT('0' + CAST(YEAR (GETDATE ()) AS VARCHAR(4)), 2);
        SET @Month = RIGHT('0' + CAST(MONTH (GETDATE ()) AS VARCHAR(2)), 2);
        SET @Day = RIGHT('0' + CAST(DAY (GETDATE ()) AS VARCHAR(2)), 2);

        /* Tính lần thu thứ mấy khi thu tiền */
        DECLARE @LanThu INT;

        SELECT  PatientID, HopDongID, ISNULL (LanThu, 0) LanThu, RefundType, IsTamUng
          INTO  #BIL_Invoice_PatientID
          FROM  dbo.BIL_Invoice BI WITH (NOLOCK)
         WHERE  PatientID = @PatientID;

        IF @IsTamUng = 1
            SET @LanThu = ISNULL ((   SELECT    MAX (LanThu) + 1
                                        FROM    #BIL_Invoice_PatientID
                                       WHERE    RefundType IS NULL
                                         AND    HopDongID = @HopDongID
                                         AND    IsTamUng  = 1),
                                  1);

        DECLARE @Prefix VARCHAR(5) = 'HD';

        IF @Code IS NULL
            SET @InvoiceNo = @MaQuay + @Year + @Month + @Day + '-00001';
        ELSE
            SET @InvoiceNo
                = @MaQuay + @Year + @Month + @Day + '-'
                  + RIGHT('00000' + CAST((SUBSTRING (@Code, CHARINDEX ('-', @Code) + 1, 9) + 1) AS VARCHAR(15)), 5);

        DROP TABLE #BIL_Invoice_PatientID;
    --DROP TABLE #BIL_Invoice_TrongGio
    END;

    /* Sửa Note  trên C#, phải sửa ở đây. 
		_Note = "Tiền viền phí: "
		_Note = "Ðồng chi trả: "
		_Note = "Tạm ứng"
	*/
    DECLARE @Description NVARCHAR(150);

    SET @Description = LEFT(dbo.CovertNoUnicode (@Note), 5);
    SET @Description = CASE
                            WHEN @Description = N'tien ' THEN N'Tiền viện phí'
                            WHEN @Description = N'dong ' THEN N'Tiền chênh lệch' -- Đóng tiền chênh lệch
                            WHEN @Description = N'tam u' THEN N'Tiền tạm ứng'
                            ELSE N'Ðồng chi trả' END;

    DECLARE @_SoBienLai VARCHAR(20), @_SoKyHieu NVARCHAR(20), @_SoDau VARCHAR(20), @_SoCuoi VARCHAR(20),
            @_MayIn     NVARCHAR(400);   --1.0.0.22

    SELECT  @_SoBienLai = SoBienLai, @_SoKyHieu = SoKyHieu, @_SoDau = SoDau, @_SoCuoi = SoCuoi, @_MayIn = MayIn --1.0.0.22
      FROM  ReceiptDaily WITH (NOLOCK)
     WHERE  FacID                                                   = @FacID
       AND  CounterID                                               = @CounterID
       AND  IsVAT                                                   = @IsVAT -- Can xem xet lai , mở commnet ra sử dụng, biên lai ĐCT thì k VAT, biên lai Thu Phí thì VAT --1.0.15.1
       AND  IsActive                                                = 1
       AND  ISNULL (RIGHT('00000000' + SoBienLai, LEN (SoCuoi)), 0) <= SoCuoi;

    SET @ReceiptNumber = @_SoBienLai;

    DECLARE @Size INT = LEN (@_SoCuoi); --1.0.0.24

    SET @ReceiptNumber
        = @_SoKyHieu + '|' + REPLICATE ('0', @Size - LEN (RTRIM (CONVERT (VARCHAR(1000), @ReceiptNumber))))
          + CONVERT (VARCHAR(1000), @ReceiptNumber);

    /*1.0.7.0*/
	
        SELECT  HopDongDetailID, HopDongID, MaChung, MaMuiTiem, ServicePackageID, IDPhacDo, PhanTramGiam, GiaMuiTiem,
                CreatedBy, CreatedOn, ModifiedBy, ModifiedOn, TienGiam, ISNULL (IsTiemNgoai, 0) IsTiemNgoai, FacID,
                ISNULL (GiaChenhLechTiemNgoai, 0) GiaChenhLechTiemNgoai,
                ISNULL (IsMuiNgoaiDanhMuc, 0)     IsMuiNgoaiDanhMuc, NgayDung, ISNULL (GiaTiemNgoai, 0) GiaTiemNgoai,
                ISNULL (
                    CASE
                         WHEN ISNULL (GiaChenhLechChuaGiam, 0) <> 0 THEN ISNULL (GiaChenhLechChuaGiam, 0)
                         ELSE
                             CASE
                                  WHEN ISNULL (IsTiemNgoai, 0) = 0
                                   AND ISNULL (IsMuiNgoaiDanhMuc, 0) = 0 THEN
                    (ISNULL (TienGiam, 0) - CASE
                                                 WHEN TienGiam > 0 THEN TienGiam
                                                 ELSE GiaMuiTiem * ISNULL (PhanTramGiam, 0) / 100.00 END)
                    + GiaChenhLechTiemNgoai
                                  ELSE 0 END END,
                    0)                            GiaChenhLechTiemNgoaiChuaGiam,
                                                                        --CASE WHEN GiaChenhLechTiemNgoai <> 0
                                                                        --                 THEN PhanTramGiam * GiaChenhLechTiemNgoai / NULLIF((100 - PhanTramGiam), 0)
                                                                        --                 ELSE 0
                                                                        --            END GiaChenhLechTiemNgoaiChuaGiam, 
                ISNULL (GiaChenhLechChuaGiam, 0)  GiaChenhLechChuaGiam,  --1.1.17.0
                ISNULL (IsHuyMui, 0)              IsHuyMui,                          --,
                ISNULL (VHDD.IsDoiMui, 0)         IsDoiMui
          --ISNULL( MuiThanhToan, 0 ) MuiThanhToan
          INTO  #Vaccine_HopDong_Detail_Temp
          FROM  QAHosGenericDB.dbo.Vaccine_HopDong_Detail VHDD WITH (NOLOCK)
         WHERE  HopDongID = @HopDongID;

		   DECLARE @giatrihopding MONEY = 0;

    SELECT @giatrihopding =VHDTT.GTriHDongTruocKhiGiam 
	from (select SUM (GTriHDongSauKhiGiam)   GTriHDongSauKhiGiam,
                                SUM (GTriHDongTruocKhiGiam) GTriHDongTruocKhiGiam, HopDongID
                           FROM (   SELECT  (SUM (GiaMuiTiem) - SUM (de.TienGiam))
                                            + (SUM (GiaChenhLechTiemNgoai) + SUM (GiaChenhLechTiemNgoaiChuaGiam)) GTriHDongSauKhiGiam,
                                                                                                                                            --SUM(GiaMuiTiem) + (SUM(GiaChenhLechTiemNgoai) + SUM(GiaChenhLechTiemNgoaiChuaGiam)) GTriHDongTruocKhiGiam, --1.1.17.0
                                            CASE
                                                 WHEN   ISNULL (IsHuyMui, 0) = 1
                                                  AND   ISNULL (IsMuiNgoaiDanhMuc, 0) = 1 THEN
                                                     SUM (GiaTiemNgoai)
                                                     - SUM (GiaTiemNgoai * (CAST(PhanTramGiam AS FLOAT) / 100)) --SUM(GiaTiemNgoai) -- 1.1.22.0
                                                 ELSE
                                                     SUM (GiaMuiTiem)
                                                     + (CASE
                                                             WHEN SUM (GiaChenhLechChuaGiam) = 0 THEN
                                                                 SUM (GiaChenhLechTiemNgoaiChuaGiam) --+ ISNULL(SUM(GiaChenhLechTiemNgoai), 0)
                                                             ELSE SUM (GiaChenhLechChuaGiam) END) END             GTriHDongTruocKhiGiam,    --1.1.17.0
                                            de.HopDongID
                                      FROM  #Vaccine_HopDong_Detail_Temp de
                                     WHERE  de.HopDongID                      = @HopDongID
                                       AND  ISNULL (de.IsTiemNgoai, 0)        = 0
                                       AND  ISNULL (de.IsMuiNgoaiDanhMuc, 0)  = 0
                                        --AND MuiThanhToan = 1 --1.1.24.0
                                        OR  (   ISNULL (IsMuiNgoaiDanhMuc, 0) = 1
                                          AND   IsHuyMui                      = 1) -- 1.1.22.0
                                        OR  (   ISNULL (IsMuiNgoaiDanhMuc, 0) = 1
                                          AND   de.IsDoiMui                   = 1)  --1.1.40.5
                                     GROUP BY de.HopDongID, IsHuyMui, IsMuiNgoaiDanhMuc) tbl
                          GROUP BY HopDongID) VHDTT;

  


   

    /*1.0.7.0*/
	--===========================================INSERT NEW BIL_Invoice=======================================================--
    INSERT  [BIL_Invoice] ([InvoiceID], [FacID], [PatientID], [CaseID], [FacAdmissionID], [PhysicianAdmissionID],
                           [HopDongID], [CounterID], [InvoiceNo], [DoiTuongID], [Total], [RealTotal], [TongTienGiam],
                           [IsTamUng], [IsPaid], [PatientType], [Reason], [Description], [Note], [LanThu], [IsVAT],
                           [IsNgoaiGio], [IsChenhLech], [ShiftID], [ReceiptNumber], [CreatedDateAsInt],
                           [CreatedDateByUser], [CreatedOnByUser], [CreatedByUser], [IPUser], [MacAddressUser],
                           [HinhThucThanhToan], [SoTK], [SoTKNhan], [PhanTramMienGiam], [ApprovedInID],
                           [ApprovedOutID], [CreatedOn], [CreatedBy], [ModifiedOn], [ModifiedBy], TotalContract)
    SELECT  @InvoiceID, @FacID, @PatientID, @CaseID, @FacAdmissionID, @PhysicianAdmissionID, @HopDongID, @CounterID,
            @InvoiceNo, @DoiTuongID, @Total, @RealTotal, @TongTienGiam, @IsTamUng, @IsPaid, 0 PatientType,
            @Reason + CASE WHEN @LiDoMienGiam = '' THEN ''
                           ELSE N', Miễn giảm: ' + @LiDoMienGiam END, 
			@Description, @Note, @LanThu, @IsVAT,
            @IsNgoaiGio, @IsChenhLech, @ShiftID, @ReceiptNumber, FORMAT (GETDATE (), 'yyyyMMddHHmmss', 'en-US'),
            CAST(GETDATE () AS DATE), GETDATE (), @UserID, @IPUser, @MacAddressUser, @HinhThucThanhToan, @SoTK,
            @SoTKNhan, @PhanTramMienGiam, @ApprovedInID, @ApprovedOutID, GETDATE (), @UserID, GETDATE (), @UserID,
            @giatrihopding;  --1.0.7.0

	 INSERT  [BIL_Invoice_Live] (CheckSum_FacID,[InvoiceID], [FacID], [PatientID], [CaseID], [FacAdmissionID], [PhysicianAdmissionID],
                           [HopDongID], [CounterID], [InvoiceNo], [DoiTuongID], [Total], [RealTotal], [TongTienGiam],
                           [IsTamUng], [IsPaid], [PatientType], [Reason], [Description], [Note], [LanThu], [IsVAT],
                           [IsNgoaiGio], [IsChenhLech], [ShiftID], [ReceiptNumber], [CreatedDateAsInt],CreatedOnAsInt,
                           [CreatedDateByUser], [CreatedOnByUser], [CreatedByUser], [IPUser], [MacAddressUser],
                           [HinhThucThanhToan], [SoTK], [SoTKNhan], [PhanTramMienGiam], [ApprovedInID],
                           [ApprovedOutID], [CreatedOn], [CreatedBy], [ModifiedOn], [ModifiedBy], TotalContract)
    SELECT  @CheckSumFacID,@InvoiceID, @FacID, @PatientID, @CaseID, @FacAdmissionID, @PhysicianAdmissionID, @HopDongID, @CounterID,
            @InvoiceNo, @DoiTuongID, @Total, @RealTotal, @TongTienGiam, @IsTamUng, @IsPaid, 0 PatientType,
            @Reason + CASE WHEN @LiDoMienGiam = '' THEN ''
                           ELSE N', Miễn giảm: ' + @LiDoMienGiam END,
			@Description, @Note, @LanThu, @IsVAT,
            @IsNgoaiGio, @IsChenhLech, @ShiftID, @ReceiptNumber, FORMAT (GETDATE (), 'yyyyMMdd', 'en-US'),FORMAT (GETDATE (), 'yyyyMMddHHmmss', 'en-US'),
            CAST(GETDATE () AS DATE), GETDATE (), @UserID, @IPUser, @MacAddressUser, @HinhThucThanhToan, @SoTK,
            @SoTKNhan, @PhanTramMienGiam, @ApprovedInID, @ApprovedOutID, GETDATE (), @UserID, GETDATE (), @UserID,
            @giatrihopding;  --1.0.7.0

    INSERT INTO dbo.BIL_Invoice_CurrentDay (InvoiceID, InvoiceNo, FacID, CreatedDateAsInt, CreatedOn)
    VALUES (@InvoiceID,                                     -- InvoiceID - uniqueidentifier
            @InvoiceNo,                                     -- InvoiceNo - nvarchar(20)
            @FacID,                                         -- FacID - varchar(10)
            FORMAT (GETDATE (), 'yyyyMMddHHmmss', 'en-US'), -- CreatedDateAsInt - bigint
            GETDATE ()                                      -- CreatedOn - datetime
        );

	--===========================================INSERT NEW BIL_Invoice=======================================================--
    SET @changed = 1;
    DROP TABLE #Vaccine_HopDong_Detail_Temp;
END;

IF @changed = 1
    EXEC History..sp_BIL_Invoice_LogUpdate @InvoiceID = @InvoiceID, -- uniqueidentifier
                                           @FacID = @FacID,         -- varchar(10)
                                           @UserID = @UserID;        -- uniqueidentifier