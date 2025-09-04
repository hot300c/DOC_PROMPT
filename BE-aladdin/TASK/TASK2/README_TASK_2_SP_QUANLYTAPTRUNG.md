CREATE PROCEDURE [dbo].[ws_QuanLyTapTrung]
(
@SessionID VARCHAR(MAX) = NULL, @TuNgay DATETIME, @DenNgay DATETIME, @FacID VARCHAR(10), @\_Type INT = 0,
@debug INT = 0)
AS
BEGIN
-----------------debug---------------
--DECLARE @SessionID VARCHAR(MAX)
--DECLARE @TuNgay DATETIME = '20210923'
--DECLARE @DenNgay DATETIME = '20210923'
--DECLARE @FacID VARCHAR(10) = '8'
--DECLARE @\_Type INT = 1
--DECLARE @debug INT = 0 /\_debug luôn là 1,Param luôn là 0\_/

    --SELECT @TuNgay='2024-07-30', @DenNgay='2024-07-30', @FacID='8', @_Type=1
    -------------------------------------
    --SET STATISTICS IO ON
    --RAISERROR(N'Vui lòng xem màn hình này ở memu mới. Quản lý tập trung (New). Cảm ơn!',16,1)

    DECLARE @TuNgayAsInt BIGINT = FORMAT ( @TuNgay, 'yyyyMMdd', 'EN-US' );
    DECLARE @DenNgayAsInt BIGINT = FORMAT ( @DenNgay, 'yyyyMMdd', 'EN-US' );
    DECLARE @TuNgayAsbigInt BIGINT = FORMAT ( @TuNgay, 'yyyyMMdd000000', 'EN-US' );
    DECLARE @DenNgayAsBigInt BIGINT = FORMAT ( @DenNgay, 'yyyyMMdd235959', 'EN-US' );
    DECLARE @check_SumFacId INT = CHECKSUM ( @FacID );
    DECLARE @FacID_ VARCHAR(10) = @FacID
    DECLARE @_Type_ INT = @_Type

    SET @TuNgay = CONVERT ( DATE, @TuNgay );
    SET @DenNgay = CONVERT ( DATE, @DenNgay );


    DECLARE @TuNgay_ DATETIME = @TuNgay
    DECLARE @DenNgay_ DATETIME = @DenNgay


    DROP TABLE IF EXISTS #dt;
    DROP TABLE IF EXISTS #tempTongquan, #TempPatientError--, #temp_BIL_InvoiceDetail_KhacCongKham--, #TSoLuong;
    DROP TABLE IF EXISTS #temp_CN_ClinicalSessionsAll;
    DROP TABLE IF EXISTS #temp_CN_FacAdmissions;
    DROP TABLE IF EXISTS #Temp_CN_ClinicalSessionID_Vaccine;
    DROP TABLE IF EXISTS #Temp_CN_PhysicianAdmissions;
    DROP TABLE IF EXISTS #temp_BIL_InvoiceDetail_All;
    DROP TABLE IF EXISTS #temp_BIL_Invoice;
    DROP TABLE IF EXISTS #temp_INV_ApprovedOut;
    DROP TABLE IF EXISTS #temp_BIL_InvoiceRefund;

    IF @debug = 1
    BEGIN
        CREATE TABLE #dt (step VARCHAR(MAX), duration INT);

        DECLARE @step VARCHAR(MAX) = '1';
        DECLARE @tstart DATETIME = GETDATE ();
    END;

    SELECT a.FacAdmissionID, NguonTiepNhan, a.PatientID, a.FacID, CreatedBy, DischargedOn, AdmitDate, AdmitDateAsInt,
           a.AdmitOn, CAST(0 AS INT) TuoiAsInt,a.IsChieu
    INTO   #temp_CN_FacAdmissions
    FROM   dbo.CN_FacAdmissions a WITH (NOLOCK)
    WHERE  a.FacID = @FacID_ AND a.AdmitDateAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt;

    UPDATE #temp_CN_FacAdmissions
    SET    TuoiAsInt = DATEDIFF ( YEAR, P.DoB, AdmitOn )
    FROM   QAHosGenericDB..MDM_Patient P WITH (NOLOCK)
    WHERE  #temp_CN_FacAdmissions.PatientID = P.PatientID;

    CREATE TABLE #temp_CN_ClinicalSessionsAll
        (ClinicalSessionID UNIQUEIDENTIFIER,
         FacAdmissionID UNIQUEIDENTIFIER,
         PhysicianAdmissionID UNIQUEIDENTIFIER,
         FacAdmissionType VARCHAR(2),
         PatientID UNIQUEIDENTIFIER,
         ServiceID INT,
         ProductID INT,
         BedID INT,
         BloodID INT,
         UserCreatedOn DATETIME,
         DoiTuongTinhTienID INT,
         IsPaid BIT,
         IsDatTruoc BIT,
         HopDongID UNIQUEIDENTIFIER,
         CompletedOn DATETIME,
         CompletedOnDateAsInt INT,
         ProductTypeID INT,
         IsDuocTiem BIT,
         UserCreatedDateAsInt INT,
         RoomID INT,
         ServiceTypeID INT,
         ServiceHospitalTypeID INT,
         STTMuiTiem INT,
         Vaccine_MaChung VARCHAR(100),
         CreatedOn DATETIME,
         FacID VARCHAR(10),
         IsKhamGoi BIT);

    IF (@_Type_ = 1 OR @_Type_ = 5 OR @_Type_ = 6 OR @_Type_ = 9 OR @_Type_ = 1111 OR @_Type_ = 7)
    BEGIN

        INSERT INTO #temp_CN_ClinicalSessionsAll
        (ClinicalSessionID, FacAdmissionID, PhysicianAdmissionID, FacAdmissionType, PatientID, ServiceID, ProductID,
         BedID, BloodID, UserCreatedOn, DoiTuongTinhTienID, IsPaid, IsDatTruoc, HopDongID, CompletedOn,
         CompletedOnDateAsInt, ProductTypeID, IsDuocTiem, UserCreatedDateAsInt, RoomID, ServiceTypeID,
         ServiceHospitalTypeID, STTMuiTiem, Vaccine_MaChung, CreatedOn, FacID, IsKhamGoi)
        SELECT DISTINCT
               [a].[ClinicalSessionID], a.[FacAdmissionID], [a].[PhysicianAdmissionID], [a].[FacAdmissionType], a.[PatientID],
               [a].[ServiceID], a.[ProductID], 0, 0, a.[UserCreatedOn], a.[DoiTuongTinhTienID], a.[IsPaid], a.IsDatTruoc,
               a.HopDongID, a.CompletedOn, a.CompletedOnDateAsInt, a.ProductTypeID, a.IsDuocTiem, a.UserCreatedDateAsInt,
               a.RoomID, a.ServiceTypeID, a.ServiceHospitalTypeID, a.STTMuiTiem, a.Vaccine_MaChung, a.CreatedOn, a.FacID, 0
        FROM   dbo.CN_ClinicalSessions a WITH (NOLOCK) join #temp_CN_FacAdmissions T ON T.PatientID = a.PatientID
        WHERE  a.UserCreatedDateAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt
               --AND
    		   --EXISTS (SELECT 1 FROM #temp_CN_FacAdmissions T WHERE T.PatientID = a.PatientID);


    END;

    --Tạo bảng tạm cho thông tin tiêm vaccine theo index
    CREATE TABLE #Temp_CN_ClinicalSessionID_Vaccine
        (ClinicalSessionID UNIQUEIDENTIFIER,
         NgayTiemAsInt INT,
         PatientID UNIQUEIDENTIFIER,
         Age INT,
         CompletedOn DATETIME,
         ProductTypeID INT,
         IsDuocTiem BIT,
         PhysicianAdmissionID UNIQUEIDENTIFIER,
         RoomID_Tiem INT,
         FacID_DaTiem VARCHAR(10),
         RoomID_ChiDInh INT,
         FacID_ChiDinh VARCHAR(10),
    	 UserCreatedByChiDinh UNIQUEIDENTIFIER);

    IF (@_Type_ = 1 OR @_Type_ = 5 OR @_Type_ = 7 OR @_Type_ = 6)
    BEGIN
        INSERT INTO #Temp_CN_ClinicalSessionID_Vaccine
        (ClinicalSessionID, NgayTiemAsInt, PatientID, CompletedOn, ProductTypeID, IsDuocTiem, PhysicianAdmissionID,
         RoomID_Tiem, FacID_DaTiem, RoomID_ChiDInh, FacID_ChiDinh,UserCreatedByChiDinh)
        SELECT   CS.ClinicalSessionID, CS.NgayTiemAsInt, T.PatientID, T.CompletedOn, T.ProductTypeID, T.IsDuocTiem,
                 T.PhysicianAdmissionID, CS.RoomIDTiem, CS.FacID_DaTiem, CS.RoomIDChiDinh, CS.FacID_ChiDinh,d.UserCreatedByChiDinh
        FROM     #temp_CN_ClinicalSessionsAll T
            JOIN dbo.CN_ClinicalSessionID_Vaccine CS WITH (NOLOCK)
                ON T.ClinicalSessionID = CS.ClinicalSessionID
            JOIN QAHosGenericDB..Vaccine_PhacDoBenhNhan_Detail d WITH (NOLOCK)
            ON t.ClinicalSessionID = d.ClinicalSessionID AND t.PatientID = d.PatientID
        WHERE    (CS.FacID_ChiDinh_Checksum = @check_SumFacId OR CS.FacID_DaTiem_Checksum = @check_SumFacId)
                 AND
                 (   CS.NgayChiDinhAsInt
                 BETWEEN @TuNgayAsInt AND @DenNgayAsInt)

INSERT INTO #Temp_CN_ClinicalSessionID_Vaccine
(ClinicalSessionID, NgayTiemAsInt, PatientID, CompletedOn, ProductTypeID, IsDuocTiem, PhysicianAdmissionID,
RoomID_Tiem, FacID_DaTiem, RoomID_ChiDInh, FacID_ChiDinh)
SELECT CS.ClinicalSessionID, CS.NgayTiemAsInt, T.PatientID, T.CompletedOn, T.ProductTypeID, T.IsDuocTiem,
T.PhysicianAdmissionID, CS.RoomIDTiem, CS.FacID_DaTiem, CS.RoomIDChiDinh, CS.FacID_ChiDinh
FROM #temp_CN_ClinicalSessionsAll T
JOIN dbo.CN_ClinicalSessionID_Vaccine CS WITH (NOLOCK)
ON T.ClinicalSessionID = CS.ClinicalSessionID
WHERE (CS.FacID_ChiDinh_Checksum = @check_SumFacId OR CS.FacID_DaTiem_Checksum = @check_SumFacId)
AND
( CS.NgayTiemAsInt
BETWEEN @TuNgayAsInt AND @DenNgayAsInt)
AND NOT EXISTS (SELECT 1 FROM #temp_CN_ClinicalSessionsAll tt WHERE tt.ClinicalSessionID=cs.ClinicalSessionID)
-- OR CS.NgayTiemAsInt
--BETWEEN @TuNgayAsInt AND @DenNgayAsInt);
END;

    --Tạo bảng tạm cho thanh toán theo index
    CREATE TABLE #temp_BIL_Invoice
        (Loai NVARCHAR(50),
         InvoiceID UNIQUEIDENTIFIER,
         IsRefund BIT,
         Reason NVARCHAR(500),
         TongTienGiam MONEY,
         PatientID UNIQUEIDENTIFIER,
         FacAdmissionID UNIQUEIDENTIFIER,
         RefundType TINYINT,
         PhysicianAdmissionID UNIQUEIDENTIFIER,
         DoiTuongID INT,
         InvoiceNo NVARCHAR(20),
         RealTotal MONEY,
         HopDongID UNIQUEIDENTIFIER,
         CounterID INT,
         ReceiptNumber NVARCHAR(50),
         [Description] NVARCHAR(250),
         HinhThucThanhToan NVARCHAR(300),
         CreatedByUser UNIQUEIDENTIFIER,
         CreatedOnByUser DATETIME,
         IsVAT BIT,
         LanThu INT,
    	 [NgayHopDongAsInt] BIGINT);

    CREATE TABLE #temp_BIL_InvoiceDetail_All
        (ClinicalSessionID UNIQUEIDENTIFIER,
         PatientPay MONEY,
         SoTienGiam MONEY,
         ServiceID INT,
         NoiDung NVARCHAR(500),
         Loai NVARCHAR(100),
         PatientID UNIQUEIDENTIFIER,
         InvoiceID UNIQUEIDENTIFIER,
         FacAdmissionID UNIQUEIDENTIFIER,
         PhysicianAdmissionID UNIQUEIDENTIFIER,
         Reason NVARCHAR(500),
         RefundType TINYINT,
         IsRefund BIT,
         TongTienGiam MONEY,
         CounterID INT,
         ReceiptNumber NVARCHAR(50),
         [Description] NVARCHAR(250),
         HinhThucThanhToan NVARCHAR(300),
         CreatedByUser UNIQUEIDENTIFIER,
         CreatedOnByUser DATETIME,
         IsVAT BIT,
         DoiTuongID INT,
         InvoiceNo NVARCHAR(20),
         RealTotal MONEY,
         LanThu INT, IsReserved BIT	,
    	 [NgayHopDongAsInt] BIGINT);

    IF (@_Type_ = 1 OR @_Type_ = 8 OR @_Type_ = 4)
    BEGIN
        INSERT INTO #temp_BIL_Invoice
        (Loai, InvoiceID, IsRefund, Reason, TongTienGiam, PatientID, FacAdmissionID, RefundType, PhysicianAdmissionID,
         DoiTuongID, InvoiceNo, RealTotal, HopDongID, CounterID, ReceiptNumber, Description, HinhThucThanhToan,
         CreatedByUser, CreatedOnByUser, IsVAT, LanThu)
        SELECT CAST('' AS NVARCHAR(100)), InvoiceID, IsRefund, Reason, TongTienGiam, PatientID, FacAdmissionID,
               RefundType, PhysicianAdmissionID, DoiTuongID, InvoiceNo, RealTotal, HopDongID, CounterID, ReceiptNumber,
               Description, HinhThucThanhToan, CreatedByUser, CreatedOnByUser, IsVAT, LanThu
        FROM   dbo.BIL_Invoice WITH (NOLOCK)
        WHERE  CheckSum_FacID = @check_SumFacId
               AND CreatedDateAsInt
               BETWEEN @TuNgayAsbigInt AND @DenNgayAsBigInt;

UPDATE [tb]
SET [tb].[NgayHopDongAsInt] = FORMAT([b].[NgayHopDong], 'yyyyMMdd000000', 'EN-US')
FROM [#temp_BIL_Invoice] [tb],
[QAHosGenericDB]..[Vaccine_HopDong] [b] WITH (NOLOCK)
WHERE [tb].[HopDongID] = [b].[HopDongID];
INSERT INTO #temp_BIL_InvoiceDetail_All
SELECT b.ClinicalSessionID, b.PatientPay, b.SoTienGiam, b.ServiceID, b.NoiDung,
CASE WHEN a.HopDongID IS NOT NULL THEN N'Hợp đồng' ELSE a.Loai END Loai, a.PatientID, a.InvoiceID,
a.FacAdmissionID, a.PhysicianAdmissionID, a.Reason, a.RefundType, a.IsRefund, a.TongTienGiam,
a.CounterID, a.ReceiptNumber, a.[Description], a.HinhThucThanhToan, a.CreatedByUser, a.CreatedOnByUser,
a.IsVAT, a.DoiTuongID, a.InvoiceNo, a.RealTotal, LanThu, b.IsReserved,a.NgayHopDongAsInt
FROM #temp_BIL_Invoice a JOIN dbo.BIL_InvoiceDetail b WITH (NOLOCK) ON b.InvoiceID = a.InvoiceID;
END;

    --Tạo bảng tạm CN_PhysicianAdmissions theo index
    CREATE TABLE #Temp_CN_PhysicianAdmissions
        (PhysicianAdmissionID UNIQUEIDENTIFIER,
         DischargedOn DATETIME,
         IsKhongDuocTiem BIT,
         DischargedBy UNIQUEIDENTIFIER,
         TGBatDauKham DATETIME,
         PatientID UNIQUEIDENTIFIER,
         PrimaryDoctor UNIQUEIDENTIFIER,
         AdmitOn DATETIME,
    RoomID INT,
         FacAdmissionID UNIQUEIDENTIFIER,
         AdmitDate DATE,
         FacID VARCHAR(10),
         AdmitDateAsInt INT);

    IF (@_Type_ = 1 OR @_Type_ = 5 OR @_Type_ = 7 OR @_Type_ = 9 OR @_Type_ = 1111)
    BEGIN
        INSERT INTO #Temp_CN_PhysicianAdmissions
        SELECT PhysicianAdmissionID, DischargedOn, IsKhongDuocTiem, DischargedBy, TGBatDauKham, PatientID,
               PrimaryDoctor, AdmitOn, RoomID, FacAdmissionID, AdmitDate, FacID, AdmitDateAsInt
        FROM   dbo.CN_PhysicianAdmissions WITH (NOLOCK)
        WHERE  FacID = @FacID_
               AND AdmitDateAsInt
               BETWEEN @TuNgayAsInt AND @DenNgayAsInt
               AND RoomID <> 0;
    END;

    --Tạo bảng tạm xuất kho theo index
    CREATE TABLE #temp_INV_ApprovedOut
        (ApprovedOutNo NVARCHAR(100),
         ApprovedOutID UNIQUEIDENTIFIER,
         FacID VARCHAR(10),
         RequestStockID INT,
         CreatedOn DATETIME);

    IF (@_Type_ = 1 OR @_Type_ = 10)
    BEGIN
        INSERT INTO #temp_INV_ApprovedOut
        SELECT ApprovedOutNo, ApprovedOutID, FacID, RequestStockID, CreatedOn
        FROM   dbo.INV_ApprovedOut WITH (NOLOCK)
        WHERE  OutTypeID IN ( 104, 105, 106, 107 )
               AND FacID = @FacID_
               AND KhoXuat_NgayXuat_AsInt
               BETWEEN @TuNgayAsInt AND @DenNgayAsInt;
    END;

    --Tạo bảng tạm hoàn phí theo index
    CREATE TABLE #temp_BIL_InvoiceRefund
        (InvoiceRefundID UNIQUEIDENTIFIER,
         RefundType TINYINT,
         RefundNo NVARCHAR(20),
         Note NVARCHAR(500),
         CounterID INT,
         CreatedOn DATETIME,
         CreatedBy UNIQUEIDENTIFIER,
         PatientID UNIQUEIDENTIFIER,
         Total MONEY);

    IF (@_Type_ = 1 OR @_Type_ = 4)
    BEGIN
        INSERT INTO #temp_BIL_InvoiceRefund
        SELECT a.InvoiceRefundID, a.RefundType, a.RefundNo, a.Note, a.CounterID, a.CreatedOn, a.CreatedBy, a.PatientID,
               a.Total
        FROM   dbo.BIL_InvoiceRefund a WITH (NOLOCK)
        WHERE  a.FacID = @FacID_
               AND a.RefundOnAsInt
               BETWEEN @TuNgayAsInt AND @DenNgayAsInt;
    END;

    IF @debug = 1
    BEGIN
        INSERT #dt (step, duration)
        SELECT @step, DATEDIFF ( ms, @tstart, GETDATE ());

        SET @step = '2';
        SET @tstart = GETDATE ();
    END;

    IF @_Type_ = 1 --Tổng quan
    BEGIN
        CREATE TABLE #tempTongquan (DienGiai NVARCHAR(100), GiaTri NVARCHAR(50), OrderIndex INT);

        /*---------------------------*/
    	DECLARE @TiepNhanTong NVARCHAR(50);
        DECLARE @TiepNhanTrucTiep NVARCHAR(50);
        DECLARE @TiepNhanTongDai NVARCHAR(50);
    	DECLARE @TiepNhanNguoiThanGT NVARCHAR(50);
    	DECLARE @TiepNhanFacebook NVARCHAR(50);
    	DECLARE @TiepNhanTruyenHinh NVARCHAR(50);
    	DECLARE @TiepNhanDiNgangQuaThay NVARCHAR(50);
    	DECLARE @TiepNhanKhac NVARCHAR(50);
        DECLARE @SoKhachDatTruoc NVARCHAR(50);
        DECLARE @SoKhachDatTruocCoKham NVARCHAR(50);
        DECLARE @SoKhachHopDong NVARCHAR(50);
        DECLARE @SoKhachHopDongCoKham NVARCHAR(50);
        DECLARE @TongSoLuotTNMoi NVARCHAR(50);
        DECLARE @TongSoKhachKham NVARCHAR(50); --Là tổng số BN đi khám từ ngày đến ngày. Nếu trong khảng thời gian đó 1 BN đến khám nhiều lần thì vẫn tính là 1
        DECLARE @TongSoKhachKhamHD NVARCHAR(50);
        DECLARE @TongSoKhachDuocTiem NVARCHAR(50);
        DECLARE @TongKhachKhongDuocTiem NVARCHAR(50);
        DECLARE @TongSoKhachDaTiem NVARCHAR(50);
        DECLARE @TongSoMuiTiem NVARCHAR(50);
        DECLARE @HeSoMuiTiem DECIMAL(8, 2);
        DECLARE @ThucThu MONEY;
        DECLARE @DanhThuQAPay MONEY; --1.0.22.0
        DECLARE @DanhThuVNPay MONEY; --1.0.22.0;
        DECLARE @DoanhThuBanThe MONEY; --1.0.22.0
        DECLARE @HoanPhi MONEY;
        DECLARE @DoanhThu MONEY;
        DECLARE @DatTruoc MONEY;
        DECLARE @HopDong MONEY;
        DECLARE @HopDongCu MONEY;
        DECLARE @KhachLe MONEY;
        DECLARE @TongKhachLoi NVARCHAR(50);
        DECLARE @TongSoNguoiLon INT;
    	DECLARE @TongSoKhamNguoiThan INT;
        DECLARE @TongKhach INT;
        DECLARE @TongKhachBuoiSang INT;
        DECLARE @TongKhachNoiTinh INT = 0;
    	DECLARE @ThuGoi MONEY
    	DECLARE @TongGiaTriGoiBanTrongNgay MONEY
        ------------------------------------------------------------------------------------------------------------------
        DECLARE @NguoiDaiDien NVARCHAR(150) = N'';
        DECLARE @FacName NVARCHAR(100) = N'';
        DECLARE @TinhTP NVARCHAR(100) = N'';

        SELECT TOP (1)
               @FacName = CustomerFullName, @NguoiDaiDien = NguoiDaiDien, @TinhTP = ProvinceID
        FROM   dbo.L_Customer WITH (NOLOCK)
        WHERE  FacID = @FacID_;

        /*---------------------------*/
        --UPDATE   a
        --SET      Loai = N'Đặt trước'
        --FROM     #temp_BIL_InvoiceDetail_All a
        --    JOIN dbo.CN_ClinicalSessions b WITH (NOLOCK)
        --        ON a.ClinicalSessionID = b.ClinicalSessionID
        --WHERE    b.IsDatTruoc = 1
                 --AND a.Loai = '';

        UPDATE   a
        SET      Loai = N'Đặt trước'
        FROM     #temp_BIL_InvoiceDetail_All a
        WHERE    a.IsReserved = 1
                 AND a.Loai = '';

        IF @debug = 1
        BEGIN
            INSERT #dt (step, duration)
            SELECT @step, DATEDIFF ( ms, @tstart, GETDATE ());

            SET @step = '2.1';
            SET @tstart = GETDATE ();
        END;

        CREATE TABLE #TempPatientError (PatientID UNIQUEIDENTIFIER, FacAdmissionsID UNIQUEIDENTIFIER);

        /* Thêm các đợt khám không thêm mũi trong ngày vào #TempPatientError*/
        INSERT #TempPatientError (PatientID, FacAdmissionsID)
        SELECT        DISTINCT
                      b.PatientID, b.FacAdmissionID
        FROM          #temp_CN_FacAdmissions b
            LEFT JOIN #temp_CN_ClinicalSessionsAll a
                ON a.FacAdmissionID = b.FacAdmissionID
        WHERE         a.FacAdmissionID IS NULL
                      AND a.FacID = @FacID_;

        IF @debug = 1
        BEGIN
            INSERT #dt (step, duration)
            SELECT @step, DATEDIFF ( ms, @tstart, GETDATE ());

            SET @step = '2.2';
            SET @tstart = GETDATE ();
        END;

        /*Thêm các đợt khám không có biên lai vào bảng #TempPatientError*/
        --INSERT #TempPatientError (PatientID, FacAdmissionsID)
        --SELECT   DISTINCT
        --         T.PatientID, T.FacAdmissionID
        --FROM
        --         (   SELECT        a.PatientID, a.FacAdmissionID
        --             FROM          #temp_CN_ClinicalSessionsAll a
        --                 LEFT JOIN #temp_BIL_Invoice b
        --                     ON a.FacAdmissionID = b.FacAdmissionID
        --             WHERE         b.FacAdmissionID IS NULL
        --                           AND a.FacID = @FacID_) R
        --    JOIN #temp_CN_FacAdmissions T
        --        ON R.FacAdmissionID = T.FacAdmissionID
        --WHERE    T.DischargedOn IS NULL;

        SET @TongKhachLoi = (SELECT COUNT ( 1 ) FROM (SELECT * FROM #TempPatientError GROUP BY PatientID,
                                                                                               FacAdmissionsID) AS A );

        IF @debug = 1
        BEGIN
            INSERT #dt (step, duration)
            SELECT @step, DATEDIFF ( ms, @tstart, GETDATE ());

            SET @step = '3';
            SET @tstart = GETDATE ();
        END;

        IF @debug = 1
        BEGIN
            INSERT #dt (step, duration)
            SELECT @step, DATEDIFF ( ms, @tstart, GETDATE ());

            SET @step = '4';
            SET @tstart = GETDATE ();
        END;

    	SET @TiepNhanTong =
        (   SELECT SUM ( a )
            FROM
                   (   SELECT    COUNT ( DISTINCT PatientID ) a
                       FROM      #temp_CN_FacAdmissions
                       GROUP  BY AdmitDate) b );
        SET @TiepNhanTrucTiep =
        (   SELECT SUM ( a )
            FROM
                   (   SELECT    COUNT ( DISTINCT PatientID ) a
                       FROM      #temp_CN_FacAdmissions
                       WHERE     NguonTiepNhan = 1
                       GROUP  BY AdmitDate) b );
    	SET @TiepNhanTongDai =
        (   SELECT SUM ( a )
            FROM
                   (   SELECT    COUNT ( DISTINCT PatientID ) a
                       FROM      #temp_CN_FacAdmissions
                       WHERE     NguonTiepNhan = 2
                       GROUP  BY AdmitDate) b );
    	SET @TiepNhanNguoiThanGT =
        (   SELECT SUM ( a )
            FROM
                   (   SELECT    COUNT ( DISTINCT PatientID ) a
                       FROM      #temp_CN_FacAdmissions
                       WHERE     NguonTiepNhan = 3
                       GROUP  BY AdmitDate) b );
    	SET @TiepNhanFacebook =
    			(   SELECT SUM ( a )
    				FROM
    					   (   SELECT    COUNT ( DISTINCT PatientID ) a
    						   FROM      #temp_CN_FacAdmissions
    						   WHERE     NguonTiepNhan = 4
    						   GROUP  BY AdmitDate) b );
    	SET @TiepNhanTruyenHinh =
    			(   SELECT SUM ( a )
    				FROM
    					   (   SELECT    COUNT ( DISTINCT PatientID ) a
    						   FROM      #temp_CN_FacAdmissions
    						   WHERE     NguonTiepNhan = 5
    						   GROUP  BY AdmitDate) b );
    	SET @TiepNhanDiNgangQuaThay =
    			(   SELECT SUM ( a )
    				FROM
    					   (   SELECT    COUNT ( DISTINCT PatientID ) a
    						   FROM      #temp_CN_FacAdmissions
    						   WHERE     NguonTiepNhan = 6
    						   GROUP  BY AdmitDate) b );
    	SET @TiepNhanKhac =
    			(   SELECT SUM ( a )
    				FROM
    					   (   SELECT    COUNT ( DISTINCT PatientID ) a
    						   FROM      #temp_CN_FacAdmissions
    						   WHERE     NguonTiepNhan = 7
    						   GROUP  BY AdmitDate) b );


        SELECT   @TongKhachNoiTinh = COUNT ( 1 )
        FROM     #temp_CN_FacAdmissions ta
            JOIN QAHosGenericDB..MDM_Patient p WITH(NOLOCK)
                ON p.PatientID = ta.PatientID
                   AND p.FacID = @FacID_
        WHERE    p.Province LIKE CONCAT ( N'%', @TinhTP, N'%' )

        --SET @TiepNhanTongDai = (SELECT COUNT(1)FROM		#temp_CN_FacAdmissions WHERE NguonTiepNhan = 2);
        SET @SoKhachDatTruoc = (SELECT COUNT ( DISTINCT PatientID ) FROM #temp_BIL_InvoiceDetail_All WHERE Loai = N'Đặt trước');
        SELECT @SoKhachDatTruocCoKham = COUNT ( DISTINCT PatientID )
        FROM   #temp_CN_FacAdmissions
        WHERE  --NguonTiepNhan = 1
               --AND
    		   PatientID IN ( SELECT DISTINCT PatientID FROM #temp_BIL_InvoiceDetail_All WHERE Loai = N'Đặt trước' );
        -------------------------------------------------------------------------------------------------------
    	DECLARE @TblKhachHopDong TABLE (PatientID UNIQUEIDENTIFIER)

        INSERT INTO @TblKhachHopDong
        SELECT
               PatientID
        FROM   dbo.Vaccine_HopDong WITH (NOLOCK)
        WHERE  CAST(NgayHopDong AS DATE)
               BETWEEN @TuNgay_ AND @DenNgay_
               AND FacID = @FacID_
               AND (IsPaid = 1
        --OR IsDone = 1 --Tối ưu bỏ
        )


        ----- Khách hợp đồng

    	--DECLARE @TuNgay_ INT = FORMAT(@TuNgay, 'yyyyMMdd', 'en-US')
    	--DECLARE @DenNgay_ INT = FORMAT(@DenNgay, 'yyyyMMdd', 'en-US')
    	DECLARE @FromDate_Formated INT = FORMAT(@TuNgay, 'yyyyMMdd', 'en-US')
    	DECLARE @ThruDate_Formated INT = FORMAT(@DenNgay, 'yyyyMMdd', 'en-US')
        SELECT
               SoHDong,HopDongID,GiaTriHD,SoTienGiam,IsPaid,PatientID
    	INTO #TblKhachHopDong
        FROM   dbo.Vaccine_HopDong WITH (NOLOCK)
        WHERE  CreatedDateAsInt BETWEEN @FromDate_Formated AND @ThruDate_Formated
    	--CAST(CreatedDateAsInt AS DATE)
        --       BETWEEN @FromDate_Formated AND @ThruDate_Formated
               AND FacID = @FacID_ AND IsPaid = 1

    	SELECT	CASE WHEN ISNULL(H.GiaChenhLechChuaGiam, 0) > 0
    					OR	(	ISNULL(H.GiaChenhLechChuaGiam, 0) = 0
    							AND ISNULL(H.GiaChenhLechTiemNgoai, 0) = 0) THEN ISNULL(H.GiaMuiTiem, 0) + ISNULL(H.GiaChenhLechChuaGiam, 0)	-- - ISNULL ( H.TienGiam, 0 )
    			ELSE ISNULL(H.GiaMuiTiem + ISNULL(H.GiaChenhLechTiemNgoai, 0), 0)														--- ( ISNULL ( H.TienGiam, 0 ) - ( ISNULL ( H.TienGiam, 0 ) - H.GiaMuiTiem * ISNULL ( H.PhanTramGiam, 0 ) / 100.00 ))
    			END ThanhTien, #TblKhachHopDong.HopDongID, H.HopDongDetailID,H.IsHuyMui
    	INTO	#TempDetail
    	FROM	#TblKhachHopDong, dbo.Vaccine_HopDong_Detail H WITH (NOLOCK)
    	WHERE	H.HopDongID = #TblKhachHopDong.HopDongID
    			--AND H.IsMuiNgoaiDanhMuc !=1
    			AND H.MuiThanhToan = 1
    			--AND H.IsTiemNgoai !=1
    			--AND H.IsHuyMui !=1
    			AND H.IsMuiNgoaiDanhMuc = 0
    			AND ISNULL(H.IsHuyMui,0) = 0
    			AND ISNULL(H.IsTiemNgoai,0) = 0

    	INSERT INTO #TempDetail
    		(ThanhTien,HopDongID,HopDongDetailID,IsHuyMui)
    	SELECT	CASE WHEN ISNULL(H.GiaChenhLechChuaGiam, 0) > 0
    					OR	(	ISNULL(H.GiaChenhLechChuaGiam, 0) = 0
    							AND ISNULL(H.GiaChenhLechTiemNgoai, 0) = 0) THEN ISNULL(H.GiaMuiTiem, 0) + ISNULL(H.GiaChenhLechChuaGiam, 0)	-- - ISNULL ( H.TienGiam, 0 )
    			ELSE ISNULL(H.GiaMuiTiem + ISNULL(H.GiaChenhLechTiemNgoai, 0), 0)														--- ( ISNULL ( H.TienGiam, 0 ) - ( ISNULL ( H.TienGiam, 0 ) - H.GiaMuiTiem * ISNULL ( H.PhanTramGiam, 0 ) / 100.00 ))
    			END ThanhTien, #TblKhachHopDong.HopDongID, H.HopDongDetailID,H.IsHuyMui
    	FROM	#TblKhachHopDong, dbo.Vaccine_HopDong_Detail H WITH (NOLOCK)
    	WHERE	H.HopDongID = #TblKhachHopDong.HopDongID
    			AND H.MuiThanhToan = 1
    			AND H.IsMuiNgoaiDanhMuc = 0
    			AND H.IsHuyMui IS NULL
    			AND H.IsTiemNgoai = 0
    			AND NOT EXISTS (SELECT		1
    								FROM	dbo.#TempDetail VHDD WITH (NOLOCK)
    								WHERE	VHDD.HopDongDetailID = H.HopDongDetailID)

        INSERT INTO #TempDetail
    		(ThanhTien,HopDongID,HopDongDetailID,IsHuyMui)
    	SELECT	CASE WHEN ISNULL(H.GiaChenhLechChuaGiam, 0) > 0
    					OR	(	ISNULL(H.GiaChenhLechChuaGiam, 0) = 0
    							AND ISNULL(H.GiaChenhLechTiemNgoai, 0) = 0) THEN ISNULL(H.GiaMuiTiem, 0) + ISNULL(H.GiaChenhLechChuaGiam, 0)	-- - ISNULL ( H.TienGiam, 0 )
    			ELSE ISNULL(H.GiaMuiTiem + ISNULL(H.GiaChenhLechTiemNgoai, 0), 0)														--- ( ISNULL ( H.TienGiam, 0 ) - ( ISNULL ( H.TienGiam, 0 ) - H.GiaMuiTiem * ISNULL ( H.PhanTramGiam, 0 ) / 100.00 ))
    			END ThanhTien, #TblKhachHopDong.HopDongID, H.HopDongDetailID,H.IsHuyMui
    	FROM	#TblKhachHopDong, dbo.Vaccine_HopDong_Detail H WITH (NOLOCK)
    	WHERE	H.HopDongID = #TblKhachHopDong.HopDongID
    			AND H.IsHuyMui IS NOT NULL
    			AND NOT EXISTS (SELECT		1
    								FROM	dbo.#TempDetail VHDD WITH (NOLOCK)
    								WHERE	VHDD.HopDongDetailID = H.HopDongDetailID)

    	DECLARE @TienCL MONEY

    	SELECT  (SUM(VHDD.GiaMuiTiem) + SUM(VHDD.GiaChenhLechChuaGiam)) - SUM(VHDD.GiaTiemNgoai) TienCL,T.HopDongID INTO #tempCL
    	FROM #TempDetail T
        INNER JOIN QAHosGenericDB..Vaccine_HopDong_Detail_Root VHDD WITH (NOLOCK)
            ON T.HopDongDetailID = VHDD.HopDongDetailID
    	WHERE IsHuyMui = 1
    	GROUP BY T.HopDongID

    	UPDATE	#TblKhachHopDong
    		SET GiaTriHD  = (SELECT SUM(ISNULL(ThanhTien, 0))
    				FROM #TempDetail H
    				WHERE H.HopDongID = t.HopDongID AND H.IsHuyMui IS NULL)+ISNULL(t2.TienCL,0)

    	FROM #TblKhachHopDong t LEFT JOIN #tempCL  t2
    	ON t.HopDongID=t2.HopDongID

    	UPDATE #TblKhachHopDong
    	SET SoTienGiam = (	SELECT	SUM(ISNULL(H.TienGiam, 0))
    								FROM	dbo.Vaccine_HopDong_Detail_Root H WITH (NOLOCK)
    							WHERE	H.HopDongID = #TblKhachHopDong.HopDongID
    									AND H.IsMuiNgoaiDanhMuc = 0 --ISNULL(H.IsMuiNgoaiDanhMuc, 0) = 0
    									--AND ISNULL ( H.IsHuyMui, 0 ) = 0
    									AND H.IsTiemNgoai = 0)	--AND ISNULL(H.IsTiemNgoai, 0) = 0)
    	SELECT DISTINCT T.*
    	INTO	#TblKhachHopDong1
    	FROM	#TblKhachHopDong T
    			JOIN QAHosGenericDB.dbo.Vaccine_HopDong_Detail HD WITH (NOLOCK) ON T.HopDongID = HD.HopDongID
    			JOIN dbo.Vaccine_PhacDoBenhNhan_Detail D WITH (NOLOCK) ON T.PatientID = D.PatientID
    																	AND HD.MaMuiTiem = D.IDPhacDo_Detail
    																	AND HD.HopDongID = D.HopDongID


        ----- Khách hợp đồng


        SET @SoKhachHopDong = (SELECT COUNT ( 1 ) FROM @TblKhachHopDong);

        ----- Khách hợp đồng có khám
        SELECT @SoKhachHopDongCoKham = COUNT ( DISTINCT PatientID )
        FROM   #temp_CN_FacAdmissions
        WHERE  --NguonTiepNhan = 1
               --AND
    		   PatientID IN ( SELECT PatientID FROM @TblKhachHopDong )
        -------------------------------------------------------------------------------------------------------

        --SELECT GETDATE()/*hơn 2s*/
        --  SELECT CreatedOn,
        --         FacID
        ----  INTO #temp_MDM_Patient
        --  FROM dbo.MDM_Patient WITH (NOLOCK)
        --  WHERE FacID = @FacID
        --        AND CreatedItemAsInt
        --        BETWEEN @TuNgayAsInt AND @DenNgayAsInt;
        SET @TongSoLuotTNMoi =
        (   SELECT COUNT ( 1 )
            --  INTO #temp_MDM_Patient
            FROM   dbo.MDM_Patient WITH (NOLOCK)
            WHERE  FacID = @FacID_
                   AND CreatedItemAsInt
                   BETWEEN @TuNgayAsInt AND @DenNgayAsInt);

        UPDATE   #temp_CN_ClinicalSessionsAll
        SET      IsKhamGoi = 1
        FROM     #temp_CN_ClinicalSessionsAll a
            JOIN QAHosGenericDB..Vaccine_HopDong b WITH (NOLOCK)
                ON b.PatientID = a.PatientID /*AND ISNULL ( b.IsCancel, 0 ) = 0 */
                   AND b.IsPaid = 1
            JOIN QAHosGenericDB..Vaccine_PhacDoBenhNhan_Detail c WITH (NOLOCK)
                ON c.HopDongID = b.HopDongID
                   AND c.PatientID = a.PatientID
        WHERE    c.CompleteOn IS NULL
        --OR	(CONVERT(DATE, a.UserCreatedOn) BETWEEN CONVERT(DATE, b.NgayHopDong) AND CONVERT(DATE, CompletedOn));

       SET @TongSoKhachKham =
        --(   SELECT   COUNT ( DISTINCT b.PatientID )
        --    FROM     #temp_CN_ClinicalSessionsAll b
        --        JOIN #Temp_CN_PhysicianAdmissions c
        --            ON b.PhysicianAdmissionID = c.PhysicianAdmissionID
        --    WHERE    b.ServiceID = 1
        --             AND c.DischargedOn IS NOT NULL
        --             AND b.RoomID <> 0
        --             AND ISNULL ( b.IsKhamGoi, 0 ) = 0);
    	(   SELECT   COUNT ( DISTINCT c.PatientID )
    	 FROM #Temp_CN_ClinicalSessionID_Vaccine cv WITH (NOLOCK),
    			#temp_CN_ClinicalSessionsAll c WITH (NOLOCK)--,
          --   QAHosGenericDB..CN_ClinicalSessions_CongKhamTrongNgay CK WITH (NOLOCK)
        WHERE cv.ClinicalSessionID = c.ClinicalSessionID
              --AND cv.PhysicianAdmissionID = CK.PhysicianAdmissionID
              AND c.HopDongID IS NULL)

        SET @TongSoKhachKhamHD =
      --  (   SELECT   COUNT ( DISTINCT b.PatientID )
      --      FROM     #temp_CN_ClinicalSessionsAll b
      --          JOIN #Temp_CN_PhysicianAdmissions c
      --              ON b.PhysicianAdmissionID = c.PhysicianAdmissionID
      --      WHERE    b.ServiceID = 1
      --               AND c.DischargedOn IS NOT NULL
      --               AND b.RoomID <> 0
    				 --and b.HopDongID is not null
      --               AND ISNULL ( b.IsKhamGoi, 0 ) = 1);
    	 (   SELECT   COUNT ( DISTINCT c.PatientID )
    	 FROM #Temp_CN_ClinicalSessionID_Vaccine cv WITH (NOLOCK),
    			#temp_CN_ClinicalSessionsAll c WITH (NOLOCK)--,
          --   QAHosGenericDB..CN_ClinicalSessions_CongKhamTrongNgay CK WITH (NOLOCK)
        WHERE cv.ClinicalSessionID = c.ClinicalSessionID
              --AND cv.PhysicianAdmissionID = CK.PhysicianAdmissionID
              AND c.HopDongID IS NOT NULL)

        IF @debug = 1
        BEGIN
            INSERT #dt (step, duration)
            SELECT @step, DATEDIFF ( ms, @tstart, GETDATE ());

            SET @step = '5';
            SET @tstart = GETDATE ();
        END;

        SET @TongSoKhachDuocTiem = (SELECT COUNT ( DISTINCT PatientID ) FROM #Temp_CN_ClinicalSessionID_Vaccine);
        SET @TongKhachKhongDuocTiem =
        (   SELECT COUNT ( 1 )
            FROM   #Temp_CN_PhysicianAdmissions
            WHERE  ISNULL ( IsKhongDuocTiem, 0 ) = 1
                   AND DischargedOn IS NOT NULL);
        SET @TongSoKhachDaTiem =
        (   SELECT COUNT ( DISTINCT PatientID )
            FROM   #Temp_CN_ClinicalSessionID_Vaccine
            WHERE  ISNULL ( NgayTiemAsInt, 29990101 ) <> 29990101);


        SET @TongSoMuiTiem =
        (   SELECT COUNT ( 1 )
            FROM
                   (   SELECT   DISTINCT
                                a.ApprovedOutNo, b.ClinicalSessionID
                       FROM     #temp_INV_ApprovedOut a WITH (NOLOCK)
                           JOIN dbo.INV_ApprovedOutDetail b WITH (NOLOCK)
                               ON a.ApprovedOutID = b.ApprovedOutID
                           JOIN QAHosGenericDB.dbo.L_Product c WITH (NOLOCK)
                               ON c.ProductID = b.ProductID
                                  AND c.FacID = a.FacID
                       WHERE    c.ProductTypeID = 17) AS R );

        IF @debug = 1
        BEGIN
            INSERT #dt (step, duration)
            SELECT @step, DATEDIFF ( ms, @tstart, GETDATE ());

            SET @step = '6';
            SET @tstart = GETDATE ();
        END;

        IF @TongSoKhachDaTiem <> 0
        BEGIN
            SET @HeSoMuiTiem = CONVERT ( INT, @TongSoMuiTiem ) * 1.00 / CONVERT ( INT, @TongSoKhachDaTiem ) * 1.00;
        END;
        ELSE BEGIN

SET @HeSoMuiTiem = 0;
END;

        IF @debug = 1
        BEGIN
            INSERT #dt (step, duration)
            SELECT @step, DATEDIFF ( ms, @tstart, GETDATE ());

            SET @step = '7';
            SET @tstart = GETDATE ();
        END;

        SET @DoanhThu =
        (   SELECT TOP (1)
                   (SUM ( PatientPay ) - SUM ( TongTienGiam ))
            FROM
                   (   SELECT    ROUND ( SUM ( ISNULL ( PatientPay, 0 )), 0 ) PatientPay,
                                 CASE
                                      WHEN TongTienGiam > 0 THEN ISNULL ( TongTienGiam, 0 )
                                      ELSE ROUND ( SUM ( ISNULL ( SoTienGiam, 0 )), 0 )
                                 END TongTienGiam
                       FROM      #temp_BIL_InvoiceDetail_All
                       WHERE     IsRefund = 0
                                 AND Reason NOT LIKE N'%Lưu doanh thu vaccine%'
                       GROUP  BY PatientID, FacAdmissionID, Reason, RefundType, IsRefund, TongTienGiam) AS R );

        --SELECT   b.RefundType, CASE
        --                           WHEN BI.InvoiceID IS NULL THEN (SUM(b.PatientReceived) - ISNULL(SUM(b.SoTienGiam), 0))
        --                       ELSE (BI.RealTotal)
        --                       END PatientReceived
        --INTO     #temp_BIL_InvoiceRefundDetail
        --FROM     #temp_BIL_InvoiceRefund a JOIN
        --         dbo.BIL_InvoiceRefundDetail b WITH (NOLOCK) ON a.InvoiceRefundID = b.InvoiceRefundID LEFT JOIN
        --         dbo.BIL_Invoice BI WITH (NOLOCK) ON BI.InvoiceID = b.InvoiceID
        --GROUP BY b.RefundType, BI.InvoiceID, BI.RealTotal;
        SET @HoanPhi =
        (   SELECT SUM ( PatientReceived ) PatientReceived
            FROM --#temp_BIL_InvoiceRefundDetail
                   (   SELECT        b.RefundType,
                                     CASE
                                 WHEN BI.InvoiceID IS NULL THEN
                                     (SUM ( b.PatientReceived ) - ISNULL ( SUM ( b.SoTienGiam ), 0 ))
                                          ELSE (BI.RealTotal)
                                     END PatientReceived
                       FROM          #temp_BIL_InvoiceRefund a
                           JOIN      dbo.BIL_InvoiceRefundDetail b WITH (NOLOCK)
                               ON a.InvoiceRefundID = b.InvoiceRefundID
                           LEFT JOIN dbo.BIL_Invoice BI WITH (NOLOCK)
                               ON BI.InvoiceID = b.InvoiceID
                       GROUP  BY     b.RefundType, BI.InvoiceID, BI.RealTotal) xx
            WHERE  RefundType = 2);
        SET @ThucThu = @DoanhThu - ISNULL ( @HoanPhi, 0 );


        --1.0.22.0 begin
        SET @DanhThuQAPay =
        (   SELECT SUM ( RealTotal )
            FROM   dbo.BIL_Invoice_QAPAY biq WITH (NOLOCK)
            --JOIN QAHosGenericDB..MDM_Patient m WITH(NOLOCK) ON biq.PatientID = m.PatientID
            WHERE  biq.CheckSum_FacID = CHECKSUM ( @FacID_ )
                   AND CAST(biq.CreatedOn AS DATE)
                   BETWEEN CAST(@TuNgay_ AS DATE) AND CAST(@DenNgay_ AS DATE))

        SELECT @DanhThuVNPay = SUM ( RealTotal )
        FROM   dbo.BIL_Invoice_VNPAY AS biv WITH (NOLOCK)
        WHERE  biv.CheckSum_FacID = CHECKSUM ( @FacID_ )
               AND CAST(biv.CreatedOn AS DATE)
               BETWEEN CAST(@TuNgay_ AS DATE) AND CAST(@DenNgay_ AS DATE)

        --SELECT TOP 1 NgayDoanhThu,CAST(CreatedOn AS DATE) a,* FROM QAHosGenericDB..L_ShiftDaily WITH(NOLOCK)
        --SELECT TOP 1  * FROM dbo.BIL_Invoice_QAPAY WITH(NOLOCK)

        --DECLARE @DoanhThu_BIL_InvoiceBusiness MONEY;
        --DECLARE @SoLuongThe_BIL_InvoiceBusiness int =0;
        --	SELECT  @DoanhThu_BIL_InvoiceBusiness  =SUM(ibd.PatientPay), @SoLuongThe_BIL_InvoiceBusiness = COUNT(1)
        --	FROM QAHosGenericDB..BIL_InvoiceBusiness ib WITH(NOLOCK)
        --	JOIN QAHosGenericDB..L_ShiftDaily s WITH ( NOLOCK ) ON s.ShiftDailyID = ib.PaidShiftDailyID
        --	JOIN QAHosGenericDB..BIL_InvoiceBusinessDetail ibd WITH(NOLOCK) ON ib.InvoiceBusinessID = ibd.InvoiceBusinessID
        --	JOIN QAHosGenericDB..fn_L_Product_List(@FacID) p ON ibd.ProductID = p.ProductID
        --	WHERE ISNULL(ib.IsRefund,0) = 0
        --	AND p.ProductTypeID = 23 --23: thẻ cào
        --	AND CAST(s.NgayDoanhThu AS DATE) BETWEEN CAST(@TuNgay AS DATE) AND CAST(@DenNgay AS DATE)
        --	AND ib.FacID=@FacID
        --GROUP BY ib.InvoiceBusinessID
        DECLARE @DoanhThu_BIL_InvoiceBusiness MONEY;
        DECLARE @SoLuongThe_BIL_InvoiceBusiness INT = 0;

        SELECT   @DoanhThu_BIL_InvoiceBusiness = SUM ( ibd.PatientPay ), @SoLuongThe_BIL_InvoiceBusiness = COUNT ( 1 )
        FROM     QAHosGenericDB..BIL_InvoiceBusiness ib WITH (NOLOCK)
            JOIN QAHosGenericDB..L_ShiftDaily s WITH (NOLOCK)
                ON s.ShiftDailyID = ib.PaidShiftDailyID
            JOIN QAHosGenericDB..BIL_InvoiceBusinessDetail ibd WITH (NOLOCK)
                ON ib.InvoiceBusinessID = ibd.InvoiceBusinessID
        WHERE    ISNULL ( ib.IsRefund, 0 ) = 0
                 AND CAST(s.NgayDoanhThu AS DATE)
                 BETWEEN CAST(@TuNgay_ AS DATE) AND CAST(@DenNgay_ AS DATE)
                 AND ib.FacID = @FacID_
                 AND ibd.Serial IS NOT NULL

        DECLARE @DoanhThu_BIL_InvoiceBusiness_Refund_Track MONEY;
        DECLARE @SoLuongThe_@DoanhThu_BIL_InvoiceBusiness_Refund_Track INT = 0;
        SELECT   @DoanhThu_BIL_InvoiceBusiness_Refund_Track = SUM ( ibd.PatientPay ),
                 @SoLuongThe_@DoanhThu_BIL_InvoiceBusiness_Refund_Track = COUNT ( 1 )
        FROM     QAHosGenericDB..BIL_InvoiceBusiness_Refund_Track ibrt WITH (NOLOCK)
            JOIN QAHosGenericDB..L_ShiftDaily s WITH (NOLOCK)
                ON s.ShiftDailyID = ibrt.ShiftDailyID
     JOIN QAHosGenericDB..BIL_InvoiceBusinessDetail ibd WITH (NOLOCK)
                ON ibrt.InvoiceID = ibd.InvoiceBusinessID
            JOIN QAHosGenericDB..fn_L_Product_List ( @FacID_ ) p
                ON ibd.ProductID = p.ProductID
        WHERE    ISNULL ( ibrt.RefundType, 0 ) = 0
                 AND IsLastest = 1
                 AND p.ProductTypeID = 23 --23: thẻ cào
                 AND CAST(s.NgayDoanhThu AS DATE)
                 BETWEEN CAST(@TuNgay_ AS DATE) AND CAST(@DenNgay_ AS DATE)
                 AND ibrt.FacID = @FacID_

        DECLARE @SoLuongThe INT = 0;
        SET @SoLuongThe = @SoLuongThe_BIL_InvoiceBusiness + @SoLuongThe_@DoanhThu_BIL_InvoiceBusiness_Refund_Track;
        SET @DoanhThuBanThe
            = ISNULL ( @DoanhThu_BIL_InvoiceBusiness, CAST(0 AS MONEY))
              + ISNULL ( @DoanhThu_BIL_InvoiceBusiness_Refund_Track, CAST(0 AS MONEY))
        --1.0.22.0 end


        --DROP TABLE #temp_BIL_InvoiceRefundDetail;
        --SELECT CASE WHEN Loai <> '' THEN Loai ELSE N'Khách lẻ' END Loai, ClinicalSessionID, PatientPay, SoTienGiam,
        --       LanThu
        --INTO   #temp_BIL_InvoiceDetail_KhacCongKham
        --FROM   #temp_BIL_InvoiceDetail_All
        --WHERE  ServiceID <> 1
        --       AND IsRefund = 0
        --       AND Reason NOT LIKE N'%Lưu doanh thu vaccine%';

        SET @DatTruoc =
        (   SELECT TOP (1)
                   (SUM ( PatientPay ) - SUM ( SoTienGiam ))
            FROM   --#temp_BIL_InvoiceDetail_KhacCongKham
    		(SELECT CASE WHEN Loai <> '' THEN Loai ELSE N'Khách lẻ' END Loai, ClinicalSessionID, PatientPay, SoTienGiam,
               LanThu
    		--INTO   #temp_BIL_InvoiceDetail_KhacCongKham
    		FROM   #temp_BIL_InvoiceDetail_All
    		WHERE  ServiceID <> 1
    			   AND IsRefund = 0
    			   AND Reason NOT LIKE N'%Lưu doanh thu vaccine%') x
            WHERE  Loai = N'Đặt trước');
       SET @HopDong =
        (   SELECT TOP (1)
               (SUM([PatientPay]) - SUM([SoTienGiam]))
        FROM --#temp_BIL_InvoiceDetail_KhacCongKham
        (
            SELECT CASE
                       WHEN [Loai] <> '' THEN
                           [Loai]
                       ELSE
                           N'Khách lẻ'
                   END [Loai],
                   [ClinicalSessionID],
                   [PatientPay],
                   [SoTienGiam],
                   [NgayHopDongAsInt]
            --INTO   #temp_BIL_InvoiceDetail_KhacCongKham
            FROM [#temp_BIL_InvoiceDetail_All]
            WHERE [ServiceID] <> 1
                  AND [IsRefund] = 0
                  AND [NoiDung] LIKE N'%Thu tạm ứng%'
        ) [x]
        WHERE [Loai] = N'Hợp đồng'
              AND [x].[NgayHopDongAsInt] = @TuNgayAsbigInt);
        SET @HopDongCu =
        (   SELECT TOP (1)
                   (SUM ( PatientPay ) - SUM ( SoTienGiam ))
            FROM   --#temp_BIL_InvoiceDetail_KhacCongKham
    		(SELECT CASE
                       WHEN [Loai] <> '' THEN
                           [Loai]
                       ELSE
                           N'Khách lẻ'
                   END [Loai],
                   [ClinicalSessionID],
                   [PatientPay],
                   [SoTienGiam],
                   [NgayHopDongAsInt]
            --INTO   #temp_BIL_InvoiceDetail_KhacCongKham
            FROM [#temp_BIL_InvoiceDetail_All]
            WHERE [ServiceID] <> 1
                  AND [IsRefund] = 0
                  AND [NoiDung] LIKE N'%Thu tạm ứng%'
        ) [x]
        WHERE [Loai] = N'Hợp đồng'
              AND [NgayHopDongAsInt] <> @TuNgayAsbigInt);
        SET @KhachLe =
        (   SELECT TOP (1)
                   (SUM ( PatientPay ) - SUM ( SoTienGiam ))
            FROM   --#temp_BIL_InvoiceDetail_KhacCongKham
    		(SELECT CASE WHEN Loai <> '' THEN Loai ELSE N'Khách lẻ' END Loai, ClinicalSessionID, PatientPay, SoTienGiam,
               LanThu
    		--INTO   #temp_BIL_InvoiceDetail_KhacCongKham
    		FROM   #temp_BIL_InvoiceDetail_All
    		WHERE  ServiceID <> 1
    			   AND IsRefund = 0
    			   AND Reason NOT LIKE N'%Lưu doanh thu vaccine%') x
            WHERE  Loai = N'Khách lẻ');

        DECLARE @SoLuotBoVe INT =
                (   SELECT   COUNT ( 1 )
                    FROM     #temp_CN_FacAdmissions a
                        JOIN dbo.CN_DoctorDecision b WITH (NOLOCK)
                            ON a.FacAdmissionID = b.FacAdmissionID
                    WHERE    b.FinalDecisionID <> 1);
        DECLARE @SoKhachDouble INT =
                (   SELECT COUNT ( 1 )
                    FROM
                           (   SELECT    c.PatientID
                               FROM      #temp_CN_FacAdmissions a
                                   JOIN  #temp_CN_ClinicalSessionsAll c
                                       ON a.FacAdmissionID = c.FacAdmissionID
                               WHERE     c.ServiceID = 1
                               GROUP  BY c.PatientID, a.AdmitDateAsInt
                               HAVING    COUNT ( 1 ) > 1) AS R );

        ----Tính tổng số người lớn (Tuoi >= 18)
        SELECT @TongSoNguoiLon =
        (   SELECT COUNT ( 1 )
            FROM
                   (   SELECT DISTINCT
                              tf.PatientID, AdmitDateAsInt
                       FROM   #temp_CN_FacAdmissions tf
                       WHERE  tf.TuoiAsInt >= 18) a );

SET @TongSoKhamNguoiThan =
( SELECT COUNT ( DISTINCT b.PatientID )
FROM #temp_CN_ClinicalSessionsAll b
JOIN #Temp_CN_PhysicianAdmissions c
ON b.PhysicianAdmissionID = c.PhysicianAdmissionID
WHERE b.ServiceTypeID = 1
AND b.RoomID IN (SELECT RoomID FROM QAHosGenericDB..L_DepartmentRoom WITH(NOLOCK) WHERE RoomName LIKE N'%Người thân%' AND FacID=@FacID))

    	--DECLARE @DateAsInt INT = FORMAT(@Date, 'yyyyMMdd', 'EN-US');
    	--DECLARE @FacilityID INT = 0;
    	--DECLARE @FacCheckSum INT  = CHECKSUM(@FacID)
    	--/*1. Tiếp nhận trực tiếp*/
    	--/*Bệnh nhân 1 ngày có 2 đợt khám vẫn được tính là 1*/
    	--DECLARE @Value INT = 0;
    	--DECLARE @RoomID int;


    	--SET @TongSoKhamNguoiThan =
    	--(
    	--   SELECT  COUNT(DISTINCT PatientID)
    	--	FROM   dbo.CN_ClinicalSessions_CongKhamTrongNgay WITH (NOLOCK)
    	--	WHERE  CreatedAdInt = @DateAsInt
    	--		   AND FacID_Checksum = @FacCheckSum
    	--		   AND RoomID IN (SELECT RoomID FROM QAHosGenericDB..L_DepartmentRoom WITH(NOLOCK) WHERE RoomName LIKE N'%Người thân%' AND FacID=@FacID)

    	--);
    	DECLARE @TongKhachBSGT INT
    		SET @TongKhachBSGT =
    	(
    	SELECT COUNT( DISTINCT PatientID) FROM [QAHosGenericDB]..[MDM_Accompany_Customers] WITH (NOLOCK) WHERE CreatedDateAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt AND FacIDCheckSum=@check_SumFacId AND ReservationType='PK'
    	)
    	DECLARE @TongKhachDiCung INT
    		SET @TongKhachDiCung =
    	(
    	SELECT COUNT( DISTINCT PatientID) FROM [QAHosGenericDB]..[MDM_Accompany_Customers] WITH (NOLOCK) WHERE CreatedDateAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt AND FacIDCheckSum=@check_SumFacId
    	)
    	DECLARE @DoanhThuBSGT MONEY
    	DECLARE @DoanhThuKHDiCung MONEY
    	SET @DoanhThuBSGT =
        (   SELECT TOP (1)
                   (SUM ( PatientPay ) - SUM ( TongTienGiam ))
            FROM
                   (   SELECT    ROUND ( SUM ( ISNULL ( PatientPay, 0 )), 0 ) PatientPay,
                                 CASE
                                      WHEN TongTienGiam > 0 THEN ISNULL ( TongTienGiam, 0 )
                                      ELSE ROUND ( SUM ( ISNULL ( SoTienGiam, 0 )), 0 )
                                 END TongTienGiam
                       FROM      #temp_BIL_InvoiceDetail_All t
    							JOIN [QAHosGenericDB]..[MDM_Accompany_Customers] ac WITH (NOLOCK)
    							ON ac.PatientID = t.patientID AND ac.FacIDCheckSum=@check_SumFacId
                       WHERE     IsRefund = 0
                                 AND Reason NOT LIKE N'%Lưu doanh thu vaccine%'
    							 AND ac.CreatedDateAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt
    							 AND ac.ReservationType='PK'
                       GROUP  BY t.PatientID, t.FacAdmissionID, Reason, RefundType, IsRefund, TongTienGiam) AS R );
    	SET @DoanhThuKHDiCung =
        (   SELECT TOP (1)
                   (SUM ( PatientPay ) - SUM ( TongTienGiam ))
            FROM
                   (   SELECT    ROUND ( SUM ( ISNULL ( PatientPay, 0 )), 0 ) PatientPay,
                                 CASE
                                      WHEN TongTienGiam > 0 THEN ISNULL ( TongTienGiam, 0 )
                                      ELSE ROUND ( SUM ( ISNULL ( SoTienGiam, 0 )), 0 )
                                 END TongTienGiam
                       FROM      #temp_BIL_InvoiceDetail_All t
    							JOIN [QAHosGenericDB]..[MDM_Accompany_Customers] ac WITH (NOLOCK)
    							ON ac.PatientID = t.patientID AND ac.FacIDCheckSum=@check_SumFacId
                       WHERE     IsRefund = 0
                                 AND Reason NOT LIKE N'%Lưu doanh thu vaccine%'
    							 AND ac.CreatedDateAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt
                       GROUP  BY t.PatientID, t.FacAdmissionID, Reason, RefundType, IsRefund, TongTienGiam) AS R );
    				   --select * from #temp_BIL_InvoiceDetail_All
    	IF(@DoanhThuBSGT IS NULL)
    	BEGIN
    		SET @DoanhThuBSGT=0
    	END
    	IF(@DoanhThuKHDiCung IS NULL)
    	BEGIN
    		SET @DoanhThuKHDiCung=0
    	END
        SET @TongKhach = (SELECT COUNT ( 1 ) FROM #temp_CN_FacAdmissions)
    	--Khách hàng dv vip
    	DECLARE @KHSuDungDVVip INT
    	DECLARE @FacilityID INT

    	SET @FacilityID = REPLACE(@FacID_,'.','')

    SET @KHSuDungDVVip= (
    SELECT COUNT(DISTINCT PatientID) FROM QAHosGenericDB..CN_ClinicalSessions  WITH(NOLOCK)
    WHERE [FacID]=@FacID AND [UserCreatedDateAsInt]  BETWEEN @TuNgayAsInt AND @DenNgayAsInt
    	AND ServiceID =11024 AND IsPaid=1)


    	DECLARE @DoanhKHSuDungDVVip MONEY
    	SELECT InvoiceID INTO #TempbillVip  FROM [#temp_BIL_InvoiceDetail_All]
            WHERE ISNULL([IsRefund],0) = 0
            AND Reason LIKE N'%Viện phí%'     AND ServiceID IN (SELECT s.ServiceID FROM QAHosGenericDB..L_Service_VIPExamination s WITH(NOLOCK) WHERE s.FacilityID = @FacilityID AND s.ServiceID<>1)
    	SET @DoanhKHSuDungDVVip =
    (
        SELECT TOP (1)
               (SUM([PatientPay]) - SUM([TongTienGiam]))
        FROM
        (
            SELECT ROUND(SUM(ISNULL([PatientPay], 0)), 0) [PatientPay],
                   CASE
                       WHEN [TongTienGiam] > 0 THEN
                           ISNULL([TongTienGiam], 0)
                       ELSE
                           ROUND(SUM(ISNULL([SoTienGiam], 0)), 0)
                   END [TongTienGiam]
            FROM [#temp_BIL_InvoiceDetail_All]
            WHERE InvoiceID in (select  InvoiceID from #TempbillVip)
            GROUP BY [PatientID],
                     [FacAdmissionID],
                     [Reason],
                     [RefundType],
                     [IsRefund],
                     [TongTienGiam]
        ) AS [R]
    );
    DROP TABLE IF EXISTS #TempbillVip

        ----Tính tổng khách vào buổi sáng
        SELECT @TongKhachBuoiSang
            = (SELECT COUNT ( distinct PatientID ) FROM #temp_CN_FacAdmissions tf WHERE tf.ischieu =0);
    	----- Thu gói
    	SET @ThuGoi =ISNULL(@HopDong,0) +ISNULL(@HopDongCu,0)
    	BEGIN
    	DECLARE @DoanhThuOnline MONEY;

    	SELECT @DoanhThuOnline = SUM(t.[RealTotal])
    	FROM  #temp_BIL_Invoice t
    	JOIN [dbo].[BIL_Invoice_AnotherSource] [biq] WITH (NOLOCK)
    	on biq.InvoiceID_Group = t.InvoiceID
    	WHERE t.IsRefund = 0


    	IF (@DoanhThuOnline IS NULL)
    	BEGIN
    		SET @DoanhThuOnline = 0;
    	END;
    	--UPDATE [#temp_Result]
    	--SET [Value] = CONVERT(NVARCHAR(50), FORMAT((@DoanhThuOnline), 'C0', 'vi-VN'))
    	--WHERE [OverviewID] = 41;
    END

    	-----Tổng giá trị hợp đồng trong ngày

    	SET @TongGiaTriGoiBanTrongNgay= (SELECT SUM(GiaTriHD) - SUM(SoTienGiam) FROM #TblKhachHopDong1);

        INSERT #tempTongquan (DienGiai, GiaTri, OrderIndex)
    	(SELECT N'Tổng lượt tiếp nhận', CONVERT ( NVARCHAR(50), @TiepNhanTong ), 0)
    	UNION
        (SELECT N'Tiếp nhận trực tiếp', CONVERT ( NVARCHAR(50), @TiepNhanTrucTiep ), 1)
        UNION
        (SELECT N'Nguồn tiếp nhận tổng đài', CONVERT(NVARCHAR(50), @TiepNhanTongDai), 3)
    	UNION
        (SELECT N'Nguồn tiếp nhận người thân giới thiệu', CONVERT(NVARCHAR(50), @TiepNhanNguoiThanGT), 4)
    	UNION
        (SELECT N'Nguồn tiếp nhận facebook', CONVERT(NVARCHAR(50), @TiepNhanFacebook), 5)
    	UNION
        (SELECT N'Nguồn tiếp nhận truyền hình', CONVERT(NVARCHAR(50), @TiepNhanTruyenHinh), 6)
    	UNION
        (SELECT N'Nguồn tiếp nhận đi ngang qua thấy', CONVERT(NVARCHAR(50), @TiepNhanDiNgangQuaThay), 7)
    	UNION
        (SELECT N'Nguồn tiếp nhận khác', CONVERT(NVARCHAR(50), @TiepNhanKhac), 8)
        ---<<< hiepnh  gom 1 cau insert dc hok ?
        UNION
        (SELECT N'Tổng số khách đặt trước', CONVERT ( NVARCHAR(50), @SoKhachDatTruoc ), 9)
        UNION
        (SELECT N'Tổng số hợp đồng', CONVERT ( NVARCHAR(50), @SoKhachHopDong ), 10)
        UNION
        (SELECT N'Tổng số lượt tiếp nhận mới', CONVERT ( NVARCHAR(50), @TongSoLuotTNMoi ), 11)
        UNION
        (SELECT N'Tổng số khách khám lẻ', CONVERT ( NVARCHAR(50), @TongSoKhachKham ), 12)
        UNION
        (SELECT N'Tổng số khách khám hợp đồng', CONVERT ( NVARCHAR(50), @TongSoKhachKhamHD ), 13)
        UNION
        (SELECT N'Tổng số lượt khách được tiêm', CONVERT ( NVARCHAR(50), @TongSoKhachDuocTiem ), 14)
        UNION
        (SELECT N'Tổng số lượt khách không được tiêm', CONVERT ( NVARCHAR(50), @TongKhachKhongDuocTiem ), 15)
        UNION
        (SELECT N'Tổng số lượt khách bỏ về', CONVERT ( NVARCHAR(50), @SoLuotBoVe ), 16)
        UNION
        (SELECT N'Tổng số khách đã tiêm', CONVERT ( NVARCHAR(50), @TongSoKhachDaTiem ), 17)
        UNION
        (SELECT N'Tổng số khách người lớn', CONVERT ( NVARCHAR(50), @TongSoNguoiLon ), 18)
    	UNION
        (SELECT N'Tổng số khách hàng phòng khám người thân', CONVERT(NVARCHAR(50),@TongSoKhamNguoiThan),19)
        UNION
        (SELECT N'Tổng số mũi tiêm', CONVERT ( NVARCHAR(50), @TongSoMuiTiem ), 20)
        UNION
        (SELECT N'Hệ số mũi tiêm', CONVERT ( NVARCHAR(50), CONVERT ( DECIMAL(8, 2), @HeSoMuiTiem )), 21)
        UNION
        (SELECT N'Doanh thu', CONVERT ( NVARCHAR(50), FORMAT ( @DoanhThu, 'C0', 'vi-VN' )), 22)
        UNION
        (SELECT N'Hoàn phí', CONVERT ( NVARCHAR(50), FORMAT ( @HoanPhi, 'C0', 'vi-VN' )), 23)
        UNION
        (SELECT N'Thực thu', CONVERT ( NVARCHAR(50), FORMAT ( @ThucThu, 'C0', 'vi-VN' )), 24)
        UNION
        (SELECT N'Doanh thu QAPay', CONVERT ( NVARCHAR(50), FORMAT ( @DanhThuQAPay, 'C0', 'vi-VN' )), 25) --1.0.22.0
        --UNION
        --(SELECT N'Doanh thu VNPay', CONVERT ( NVARCHAR(50), FORMAT ( @DanhThuVNPay, 'C0', 'vi-VN' )), 17) --1.0.22.0
        UNION
        (SELECT N'Doanh thu bán thẻ', CONVERT ( NVARCHAR(50), FORMAT ( @DoanhThuBanThe, 'C0', 'vi-VN' )), 26) --1.0.22.0
        UNION
    	(SELECT N'Doanh thu thanh toán online', CONVERT ( NVARCHAR(50), FORMAT ( @DoanhThuOnline, 'C0', 'vi-VN' )), 27) --1.0.22.0
        UNION
        (SELECT N'Đặt trước', CONVERT ( NVARCHAR(50), FORMAT ( @DatTruoc, 'C0', 'vi-VN' )), 28)
        UNION
    	(SELECT N'Thu gói', CONVERT ( NVARCHAR(50), FORMAT ( @ThuGoi, 'C0', 'vi-VN' )), 29)
    	UNION
    	(SELECT N'Tổng giá trị gói bán trong ngày', CONVERT ( NVARCHAR(50), FORMAT ( @TongGiaTriGoiBanTrongNgay, 'C0', 'vi-VN' )), 30)
    	UNION
        (SELECT N'Hợp đồng hôm nay', CONVERT ( NVARCHAR(50), FORMAT ( @HopDong, 'C0', 'vi-VN' )), 31)
        UNION
        (SELECT N'Hợp đồng cũ', CONVERT ( NVARCHAR(50), FORMAT ( @HopDongCu, 'C0', 'vi-VN' )), 32)
        UNION
        (SELECT N'Khách lẻ', CONVERT ( NVARCHAR(50), FORMAT ( @KhachLe, 'C0', 'vi-VN' )), 33)
        UNION
        (SELECT N'Số khách bị sai', CONVERT ( NVARCHAR(50), @TongKhachLoi ), 34)
        UNION
        (SELECT N'Tổng số khách có 2 công khám trở lên', CONVERT ( NVARCHAR(50), @SoKhachDouble ), 35)
        UNION
        (SELECT N'Tổng số khách khám vào buổi sáng', CONVERT ( NVARCHAR(50), @TongKhachBuoiSang ), 36)
    	UNION
        (SELECT N'Số lượng KH BSGT', CONVERT ( NVARCHAR(50), @TongKhachBSGT ), 37)
    	UNION
        (SELECT N'Số lượng KH đi cùng', CONVERT ( NVARCHAR(50), @TongKhachDiCung ), 38)
    	UNION
        (SELECT N'Doanh thu KH BSGT', CONVERT ( NVARCHAR(50),FORMAT ( @DoanhThuBSGT, 'C0', 'vi-VN' )), 39)
    	UNION
        (SELECT N'Doanh thu KH đi cùng', CONVERT ( NVARCHAR(50),FORMAT ( @DoanhThuKHDiCung, 'C0', 'vi-VN' )), 40)
    	UNION
        (SELECT N'KH sử dụng DV VIP', CONVERT ( NVARCHAR(50), @KHSuDungDVVip ), 41)
    	UNION
        (SELECT N'Doanh thu KH sử dụng DV VIP', CONVERT ( NVARCHAR(50),FORMAT ( @DoanhKHSuDungDVVip, 'C0', 'vi-VN' )), 42);

        SELECT   DienGiai, CONVERT ( NVARCHAR(50), ISNULL ( GiaTri, 0 )) GiaTri
        FROM     #tempTongquan
        ORDER BY OrderIndex;
        SELECT DienGiai AS [Key], CONVERT ( DECIMAL(8, 2), GiaTri ) AS [Value]
        FROM   #tempTongquan
        WHERE  DienGiai = N'Tổng số khách đã tiêm'
               OR DienGiai = N'Tổng số mũi tiêm';

        SELECT REPLACE ( DienGiai, N'lượt ', '' ) AS [Key], CONVERT ( DECIMAL(8, 2), GiaTri ) AS [Value]
        FROM   #tempTongquan
        WHERE  DienGiai = N'Tổng số lượt khách được tiêm'
               OR DienGiai = N'Tổng số lượt khách không được tiêm';

        SELECT COUNT ( DISTINCT PatientID ) tongBN
        FROM   dbo.CN_FacAdmissions WITH (NOLOCK)
        WHERE  AdmitDateAsInt = FORMAT ( GETDATE (), 'yyyyMMdd', 'en-US' )
               AND FacID = @FacID_; /*Chỉ lấy ngày hôm nay, ko lấy theo ngày truyền vào*/


        -------------------------Vaccine-HC/KK----------------------------------------------------------------------------------------
        BEGIN
            DECLARE @VaccineHanChe NVARCHAR(MAX) = N'', @VaccineKhuyenKhich NVARCHAR(MAX) = N'';
            DECLARE @THCKK TABLE (VaccineID INT, VaccineName NVARCHAR(250), TypeCode TINYINT, ToDate DATETIME);

            --SELECT   b.ProductID, COUNT ( 1 ) AS 'SL'
            --INTO     #TSoLuong
            --FROM     #temp_INV_ApprovedOut a WITH (NOLOCK)
            --    JOIN dbo.INV_ApprovedOutDetail b WITH (NOLOCK)
            --        ON a.ApprovedOutID = b.ApprovedOutID
            --GROUP BY b.ProductID;

            IF @FacID_ IN ( '777', '9' )
            BEGIN
                INSERT INTO @THCKK
                SELECT VaccineID, VaccineName, TypeCode, ToDate
                FROM   QAHosGenericDB..Vaccine_HanCheKhuyenKhich WITH(NOLOCK)
                WHERE  FacID = @FacID_
            END
            ELSE
            BEGIN
                INSERT INTO @THCKK
                SELECT VaccineID, VaccineName, TypeCode, ToDate
                FROM   QAHosGenericDB..Vaccine_HanCheKhuyenKhich WITH(NOLOCK)
                WHERE  FacID NOT IN ( '777', '9' )

            END

            ---- hạn chế : 0


            SELECT        @VaccineHanChe
                = @VaccineHanChe
                  + CONCAT ( N'   - ', HCKK.VaccineName, N' : ', CAST(ISNULL ( SL.SL, 0 ) AS VARCHAR(10)))
                  + CHAR ( 13 ) + CHAR ( 10 )
            FROM          @THCKK AS HCKK
                LEFT JOIN (--#TSoLuong (NOLOCK) AS SL
    			SELECT   b.ProductID, COUNT ( 1 ) AS 'SL'
            --INTO     #TSoLuong
            FROM     #temp_INV_ApprovedOut a WITH (NOLOCK)
                JOIN dbo.INV_ApprovedOutDetail b WITH (NOLOCK)
                    ON a.ApprovedOutID = b.ApprovedOutID
            GROUP BY b.ProductID
    			) SL
                    ON HCKK.VaccineID = SL.ProductID
            WHERE         HCKK.TypeCode = 0
        AND FORMAT ( ToDate, 'yyyyMMdd' ) >= FORMAT ( @TuNgay, 'yyyyMMdd' )

            ---- khuyến khích : 1

            SELECT        @VaccineKhuyenKhich
                = @VaccineKhuyenKhich
                  + CONCAT ( N'   - ', HCKK.VaccineName, N' : ', CAST(ISNULL ( SL.SL, 0 ) AS VARCHAR(10)))
                  + CHAR ( 13 ) + CHAR ( 10 )
            FROM          @THCKK AS HCKK
                LEFT JOIN (--#TSoLuong (NOLOCK) AS SL
    			SELECT   b.ProductID, COUNT ( 1 ) AS 'SL'
            --INTO     #TSoLuong
            FROM     #temp_INV_ApprovedOut a WITH (NOLOCK)
                JOIN dbo.INV_ApprovedOutDetail b WITH (NOLOCK)
                    ON a.ApprovedOutID = b.ApprovedOutID
            GROUP BY b.ProductID
    			)SL
                    ON HCKK.VaccineID = SL.ProductID
            WHERE         HCKK.TypeCode = 1
                          AND FORMAT ( ToDate, 'yyyyMMdd' ) >= FORMAT ( @TuNgay, 'yyyyMMdd' )

            IF (@debug = '1')
            BEGIN

                SELECT        HCKK.VaccineID, HCKK.VaccineName, SL
                FROM          @THCKK AS HCKK
                    LEFT JOIN (--#TSoLuong (NOLOCK) AS SL
    				SELECT   b.ProductID, COUNT ( 1 ) AS 'SL'
            --INTO     #TSoLuong
            FROM     #temp_INV_ApprovedOut a WITH (NOLOCK)
                JOIN dbo.INV_ApprovedOutDetail b WITH (NOLOCK)
                    ON a.ApprovedOutID = b.ApprovedOutID
            GROUP BY b.ProductID
    				) SL
                        ON HCKK.VaccineID = SL.ProductID
                WHERE         HCKK.TypeCode = 0
                              AND FORMAT ( ToDate, 'yyyyMMdd' ) >= FORMAT ( @DenNgay_, 'yyyyMMdd' )

                SELECT        HCKK.VaccineID, HCKK.VaccineName, SL
                FROM          @THCKK AS HCKK
                    LEFT JOIN (--#TSoLuong (NOLOCK) AS SL
    				SELECT   b.ProductID, COUNT ( 1 ) AS 'SL'
            --INTO     #TSoLuong
            FROM     #temp_INV_ApprovedOut a WITH (NOLOCK)
                JOIN dbo.INV_ApprovedOutDetail b WITH (NOLOCK)
                    ON a.ApprovedOutID = b.ApprovedOutID
            GROUP BY b.ProductID
    				)SL
                        ON HCKK.VaccineID = SL.ProductID
                WHERE         HCKK.TypeCode = 1
                              AND FORMAT ( ToDate, 'yyyyMMdd' ) >= FORMAT ( @DenNgay_, 'yyyyMMdd' )

                SELECT @VaccineHanChe, @VaccineKhuyenKhich;

                -- ty lệ KH
                SELECT CONCAT ( @TiepNhanTrucTiep, ' / ', @TongSoNguoiLon ),
                       FORMAT (
                       ISNULL (
                       CAST(ISNULL ( @TongSoNguoiLon, 0 ) AS FLOAT)
                       / NULLIF(CAST(ISNULL ( @TiepNhanTrucTiep, 0 ) AS FLOAT), 0), 0 ), 'P' ) AS 'ty lệ KH'
            END

            --DROP TABLE IF EXISTS #TSoLuong;

        END


        -------tbl mess--------------------------------
        SELECT
        --CASE WHEN @TuNgayAsInt = @DenNgayAsInt
        --		THEN N'Ngày ' + CONVERT(NVARCHAR(100), FORMAT(@TuNgay, 'dd/MM/yyyy'))
        --ELSE
        --	N'Từ ngày ' + CONVERT(NVARCHAR(100), FORMAT(@TuNgay, 'dd/MM/yyyy'))
        --	+ N' đến ngày '+ CONVERT(NVARCHAR(100), FORMAT(@DenNgay, 'dd/MM/yyyy'))
        --END + N' của TT ' + @FacName + ' '  + N'
        --			Số mũi tiêm: ' + CONVERT(NVARCHAR(50), ISNULL(@TongSoMuiTiem, 0)) + ' (HS: '
        --+ CONVERT(NVARCHAR(50), CONVERT(DECIMAL(8, 2), CONVERT(NVARCHAR(50), ISNULL(@HeSoMuiTiem, 0)))) + ')'  + '
        --			Doanh thu: '  + N'
        --				Tổng doanh thu: ' + CONVERT(NVARCHAR(50), FORMAT(ISNULL(@DoanhThu, 0), 'C0', 'vi-VN')) + ' '
        --+ N'
        --					Trong đó:'  + N'
        --					- Đặt trước: ' + CONVERT(NVARCHAR(50), FORMAT(ISNULL(@DatTruoc, 0), 'C0', 'vi-VN')) + ' '
        --+ N'
        --					- Hợp đồng gói: ' + CONVERT(NVARCHAR(50), FORMAT(ISNULL(@HopDong, 0), 'C0', 'vi-VN')) + ''
        --+ N'
        --					- Khách lẻ: ' + CONVERT(NVARCHAR(50), FORMAT(ISNULL(@KhachLe, 0), 'C0', 'vi-VN')) + ''
        ----+ N'
        ----			Số KH tiếp nhận: ' + CONVERT(NVARCHAR(50), CONVERT(INT, ISNULL(@TiepNhanTrucTiep, 0)) + CONVERT(INT, ISNULL(@TiepNhanTongDai, 0)))	+ ' '
        --+ N'
        --			Trong đó:'  + N'
        --			- KH mới: ' + CONVERT(NVARCHAR(50), ISNULL(@TongSoLuotTNMoi, 0)) + ' '  + N'
        --			- KH đặt trước: ' + CONVERT(NVARCHAR(50), ISNULL(@SoKhachDatTruoc, 0)) + ' '  + N'
        --			- KH Mua HĐ gói: ' + CONVERT(NVARCHAR(50), ISNULL(@SoKhachHopDong, 0)) + N'  (trong đó trả góp: )'
        --+ N'
        --			- KH được tiêm: ' + CONVERT(NVARCHAR(50), ISNULL(@TongSoKhachDuocTiem, 0)) + ' '  + N'
        --			- KH không được tiêm: ' + CONVERT(NVARCHAR(50), ISNULL(@TongKhachKhongDuocTiem, 0)) + ' '+

        N'

Kính gửi: Tổng Giám Đốc ' + CHAR ( 13 ) + N'
' + @FacName + CHAR ( 13 ) + N'
Báo cáo ngày: ' + CASE
WHEN @TuNgayAsInt = @DenNgayAsInt THEN CONVERT ( NVARCHAR(100), FORMAT ( @TuNgay*, 'dd/MM/yyyy' ))
ELSE CONVERT ( NVARCHAR(100), FORMAT ( @TuNgay*, 'dd/MM/yyyy' )) + N' - ' + CONVERT ( NVARCHAR(100), FORMAT ( @DenNgay\_, 'dd/MM/yyyy' ))
END + CHAR ( 13 ) + N'

1. Số tiếp nhận: ' + CONVERT ( NVARCHAR(50), CONVERT ( INT, ISNULL ( @TiepNhanTong, 0 ))) + N' KH' + CHAR ( 13 ) + N'
   KH người lớn: ' + CONVERT ( NVARCHAR(50), CONVERT ( INT, ISNULL ( @TongSoNguoiLon, 0 ))) + N' KH' + CHAR ( 13 ) + N'
   % tỉ lệ KH người lớn: ' + FORMAT (
   ISNULL (
   CAST(ISNULL ( @TongSoNguoiLon, 0 ) AS FLOAT) / NULLIF(CAST(ISNULL ( @TiepNhanTrucTiep, 0 ) AS FLOAT), 0), 0 ),
   'P' ) + CHAR ( 13 ) + N'
   Số HĐ Gói: ' + CONVERT ( NVARCHAR(50), CONVERT ( INT, ISNULL ( @SoKhachHopDong, 0 ))) + CHAR ( 13 ) + N'
   % tỉ lệ gói: ' + FORMAT (
   ISNULL (
   CAST(ISNULL ( @SoKhachHopDong, 0 ) AS FLOAT) / NULLIF(CAST(ISNULL ( @TiepNhanTrucTiep, 0 ) AS FLOAT), 0), 0 ),
   'P' ) + CHAR ( 13 ) + N'
   Hệ số mũi tiêm: ' + CONVERT ( NVARCHAR(50), CONVERT ( DECIMAL(8, 2), CONVERT ( NVARCHAR(50), ISNULL ( @HeSoMuiTiem, 0 )))) + CHAR ( 13 ) + N'
   Số lượng bán thẻ: ' + CONVERT ( NVARCHAR(50), @SoLuongThe ) + CHAR ( 13 ) + N'
   Doanh Thu thẻ: ' + CONVERT ( NVARCHAR(50), FORMAT ( ISNULL ( @DoanhThuBanThe, 0 ), 'C0', 'vi-VN' )) + CHAR ( 13 )
   +N'Số KH BSGT: '+CONVERT ( NVARCHAR(50), ISNULL ( @TongKhachBSGT, 0 ))+' KH' + CHAR ( 13 )+
   +N'Số KH BSGT: '+CONVERT ( NVARCHAR(50), ISNULL ( @TongKhachDiCung, 0 ))+' KH' + CHAR ( 13 )+
   N'
2. Tổng doanh thu: ' + CONVERT ( NVARCHAR(50), FORMAT ( ISNULL ( @DoanhThu, 0 ), 'C0', 'vi-VN' )) + CHAR ( 13 )
   - N'

- Khách lẻ: ' + CONVERT ( NVARCHAR(50), FORMAT ( ISNULL ( @KhachLe, 0 ), 'C0', 'vi-VN' )) + CHAR ( 13 ) + N'
- Hợp đồng gói: ‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬ ' + CONVERT ( NVARCHAR(50), FORMAT ( ISNULL ( @HopDong, 0 ), 'C0', 'vi-VN' )) + CHAR ( 13 ) + N'
- Đặt trước: ' + CONVERT ( NVARCHAR(50), FORMAT ( ISNULL ( @DatTruoc, 0 ), 'C0', 'vi-VN' )) + CHAR ( 13 ) + N'
- Thẻ: - ' + CHAR ( 13 ) + N'
- Doanh thu thanh toán online: - ' + CONVERT ( NVARCHAR(50), FORMAT ( ISNULL ( @DoanhThuOnline, 0 ), 'C0', 'vi-VN' )) + CHAR ( 13 ) + N'
- Doanh thu KH sử dụng DV VIP: - ' + CONVERT ( NVARCHAR(50), FORMAT ( ISNULL ( @DoanhKHSuDungDVVip, 0 ), 'C0', 'vi-VN' )) + CHAR ( 13 ) + N'

3. Cụ thể:' + CHAR ( 13 ) + N'

- KH nội tỉnh: ' + CHAR ( 13 ) + N'
- Tỉ Lệ : Sáng: ' + FORMAT (
  ISNULL (
  CAST(ISNULL ( @TongKhachBuoiSang, 0 ) AS FLOAT) / NULLIF(CAST(ISNULL ( @TongKhach, 0 ) AS FLOAT), 0),
  0 ), 'P' ) + CHAR ( 13 ) + N'
- KH mới: ' + CONVERT ( NVARCHAR(50), ISNULL ( @TongSoLuotTNMoi, 0 )) + ' ' + N' KH' + CHAR ( 13 ) + N'
- KH sử dụng DV VIP: ' + CONVERT ( NVARCHAR(50), ISNULL ( @KHSuDungDVVip, 0 )) + ' ' + N' KH' + CHAR ( 13 ) + N'
- KH đặt trước: ' + CONVERT ( NVARCHAR(50), CONVERT ( INT, ISNULL ( @SoKhachDatTruoc, 0 ))) + N' KH' + CHAR ( 13 ) + N'
- KH đặt trước không khám: ' + CONVERT (
  NVARCHAR(50),
  CONVERT ( INT, ISNULL ((CAST(@SoKhachDatTruoc AS INT) - CAST(@SoKhachDatTruocCoKham AS INT)), 0 ))) + N' KH' + CHAR ( 13 ) + N'
- KH mua HĐ không khám: ' + CONVERT (
  NVARCHAR(50),
  CONVERT ( INT, ISNULL ((CAST(@SoKhachHopDong AS INT) - CAST(@SoKhachHopDongCoKham AS INT)), 0 ))) + N' KH' + CHAR ( 13 ) + N'
- KH BSGT: ' + CONVERT ( NVARCHAR(50), FORMAT ( ISNULL ( @DoanhThuBSGT, 0 ), 'C0', 'vi-VN' )) + CHAR ( 13 )

* N'

- KH Đi cùng: ' + CONVERT ( NVARCHAR(50), FORMAT ( ISNULL ( @DoanhThuKHDiCung, 0 ), 'C0', 'vi-VN' )) + CHAR ( 13 ) + N'
- KH được tiêm: ' + CONVERT ( NVARCHAR(50), ISNULL ( @TongSoKhachDuocTiem, 0 )) + N' KH' + CHAR ( 13 ) + N'
- KH không được tiêm: ' + CONVERT ( NVARCHAR(50), ISNULL ( @TongKhachKhongDuocTiem, 0 )) + ' KH' + CHAR ( 13 ) + N'
  Lý do: ' + CHAR ( 13 ) + N'
- Số mũi tiêm: ' + CONVERT ( NVARCHAR(50), CONVERT ( INT, ISNULL ( @TongSoMuiTiem, 0 ))) + CHAR ( 13 ) + N'
- Hệ số mũi tiêm: ' + CONVERT ( NVARCHAR(50), CONVERT ( DECIMAL(8, 2), CONVERT ( NVARCHAR(50), ISNULL ( @HeSoMuiTiem, 0 )))) + CHAR ( 13 ) + N'

4. Vắc xin sử dụng:' + CHAR ( 13 ) + N'
   4.1 Vắc xin báo cáo theo yêu cầu của BTT:' + CHAR ( 13 ) + N'
   Vắc xin cần tăng cường:' + CHAR ( 13 ) + N'
   ' + ISNULL ( @VaccineKhuyenKhich, '' ) + N'
   Vắc xin cần hạn chế:' + CHAR ( 13 ) + N'
   ' + ISNULL ( @VaccineHanChe, '' ) + CHAR ( 13 ) + N'
   4.2 Vắc xin tiêu thụ đột biến trong ngày: ' + CHAR ( 13 ) + N'
   4.3 Vắc xin không tiêu thụ trong ngày: ' + CHAR ( 13 ) + N'
   4.4 Các TTTC lân cận' + CHAR ( 13 ) + N'
5. Hoạt động tại TT:' + CHAR ( 13 ) + N'

- Bàn khám: 0 bàn khám/ 0 phòng khám - Chiều: 0 bàn khám/0 phòng khám' + CHAR ( 13 ) + N'
- Bàn tiêm: Sáng: 0 bàn tiêm/ 0 phòng tiêm - Chiều: 0 bàn/0 phòng' + CHAR ( 13 ) + N'
- Phục vụ KH: Tốt.' + CHAR ( 13 ) + N'

6. Các vấn đề phát sinh và hành động khắc phục: ' + CHAR ( 13 ) + N'
7. Đề xuất: không' + CHAR ( 13 ) + N'
8. Kế hoạch ngày: ' + CHAR ( 13 ) + N'

- Bàn khám: 0 bàn khám/ 0 phòng khám - Chiều: 0 bàn khám/ 0 phòng khám' + CHAR ( 13 ) + N'
- Bàn tiêm: Sáng: 0 bàn tiêm/ 0 phòng tiêm - Chiều: 0 bàn/ 0 phòng' + CHAR ( 13 ) + N'
  Trân trọng,' + CHAR ( 13 ) + N'
  ' + @NguoiDaiDien + CHAR ( 13 ) + N'
  ' AS [MessageContent];

          DROP TABLE #tempTongquan,
                     --#temp_MDM_Patient,
                     #TempPatientError--, #temp_BIL_InvoiceDetail_KhacCongKham;
      END;

      IF @_Type_ = 3 --chi tiết tiếp nhận
      BEGIN
          --SELECT REPLACE(Province, N'Thành Phố', 'Tp.') Province, REPLACE(District, N'Thành Phố', 'Tp.') District
          --INTO   #tempTinhThanh
          --FROM   #temp_CN_FacAdmissions a JOIN
          --       dbo.MDM_Patient b WITH (NOLOCK) ON a.PatientID = b.PatientID;

          --UPDATE #tempTinhThanh
          --SET    Province = REPLACE(Province, N'Thành Phố', 'Tp.'), District = REPLACE(District, N'Thành Phố', 'Tp.');
          SELECT   Province, COUNT ( 1 ) SL
          FROM --#tempTinhThanh
                   #temp_CN_FacAdmissions a
              JOIN dbo.MDM_Patient b WITH (NOLOCK)
                  ON a.PatientID = b.PatientID
          GROUP BY Province;

          SELECT   Province, District, COUNT ( 1 ) SL
          FROM --#tempTinhThanh
                   #temp_CN_FacAdmissions a
              JOIN dbo.MDM_Patient b WITH (NOLOCK)
                  ON a.PatientID = b.PatientID
          GROUP BY Province, District;

      --DROP TABLE #tempTinhThanh;
      END;

      IF @_Type_ = 2
      BEGIN
          SELECT   CAST('' AS NVARCHAR(500)) FullName, NguonTiepNhan, COUNT ( * ) AS SL, CreatedBy
          INTO    #temp3
          FROM     #temp_CN_FacAdmissions fa
          GROUP BY fa.CreatedBy, NguonTiepNhan;

          UPDATE        #temp3
          SET           FullName = e.FullName
          FROM          #temp3 fa
              LEFT JOIN Security.dbo.Users u WITH (NOLOCK)
                  ON u.ID = fa.CreatedBy
              LEFT JOIN HR.dbo.MDM_Employee e WITH (NOLOCK)
                  ON e.EmployeeID = u.EmpID;

          SELECT *
          INTO   #temp4
          FROM   #temp3
          PIVOT (SUM(SL)

  FOR NguonTiepNhan IN ([1], [2], [3])) AS a;

          UPDATE #temp4
          SET    [1] = 0
          WHERE  [1] IS NULL;

          UPDATE #temp4
          SET    [2] = 0
          WHERE  [2] IS NULL;

          UPDATE #temp4
          SET    [3] = 0
          WHERE  [3] IS NULL;

          SELECT --DISTINCT
               FullName, [1] AS TrucTiep, [2] AS TongDai, [3] AS HopDong, [1] + [2] AS Tong
          FROM #temp4;

          CREATE TABLE #DoTuoi (MaDoTuoi INT, TenHienThi NVARCHAR(50), [TMIN] INT, [TMax] INT);

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (0,              -- MaDoTuoi - int
                  N'0 - 2 tháng', -- TenHienThi - nvarchar(50)
                  0,              -- TMIN - int
                  2               -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (1,              -- MaDoTuoi - int
                  N'2 - 6 tháng', -- TenHienThi - nvarchar(50)
                  2,              -- TMIN - int
                  6               -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (2,              -- MaDoTuoi - int
                  N'6 - 9 tháng', -- TenHienThi - nvarchar(50)
                  6,              -- TMIN - int
                  9               -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (3,               -- MaDoTuoi - int
                  N'9 - 12 tháng', -- TenHienThi - nvarchar(50)
                  9,               -- TMIN - int
                  12               -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (4,                -- MaDoTuoi - int
                  N'12 - 16 tháng', -- TenHienThi - nvarchar(50)
                  12,               -- TMIN - int
                  16                -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (5,                -- MaDoTuoi - int
                  N'16 - 24 tháng', -- TenHienThi - nvarchar(50)
                  16,               -- TMIN - int
                  24                -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (6,              -- MaDoTuoi - int
                  N'24 - 4 tuổi', -- TenHienThi - nvarchar(50)
                  24,             -- TMIN - int
                  48              -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (7,             -- MaDoTuoi - int
                  N'4 - 6 tuổi', -- TenHienThi - nvarchar(50)
                  28,            -- TMIN - int
                  72             -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (8,              -- MaDoTuoi - int
                  N'6 - 15 tuổi', -- TenHienThi - nvarchar(50)
                  72,             -- TMIN - int
                  180             -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (9,               -- MaDoTuoi - int
                  N'15 - 18 tuổi', -- TenHienThi - nvarchar(50)
                  180,             -- TMIN - int
                  216              -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (10,              -- MaDoTuoi - int
                  N'18 - 35 tuổi', -- TenHienThi - nvarchar(50)
                  216,             -- TMIN - int
                  420              -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (11,              -- MaDoTuoi - int
                  N'35 - 65 tuổi', -- TenHienThi - nvarchar(50)
                  420,             -- TMIN - int
                  780              -- TMax - int
          );

          INSERT #DoTuoi (MaDoTuoi, TenHienThi, TMIN, TMax)
          VALUES (12,              -- MaDoTuoi - int
                  N'trên 65 tuổi', -- TenHienThi - nvarchar(50)
                  780,             -- TMIN - int
                  999999           -- TMax - int
          );

          SELECT FacAdmissionID, PatientID, AdmitOn AdmitDate, CAST(NULL AS DATETIME) AS DOB,
                 CAST(NULL AS NVARCHAR(50)) AS DoTuoi, CAST(NULL AS INT) AS MaDoTuoi, CAST(NULL AS INT) AS Thang
          INTO   #PhanBoTheoTuoi
          FROM   #temp_CN_FacAdmissions;

          UPDATE   #PhanBoTheoTuoi
          SET      DOB = b.DoB
          FROM     #PhanBoTheoTuoi a
              JOIN dbo.MDM_Patient b WITH (NOLOCK)
                  ON a.PatientID = b.PatientID;

          UPDATE #PhanBoTheoTuoi
          SET    Thang = DATEDIFF ( MONTH, CONVERT ( DATE, DOB ), CONVERT ( DATE, AdmitDate ))
          WHERE  DOB IS NOT NULL;

          UPDATE   a
          SET      DoTuoi = b.TenHienThi, MaDoTuoi = b.MaDoTuoi
          FROM     #PhanBoTheoTuoi a
              JOIN #DoTuoi b
                  ON Thang >= ISNULL ( b.[TMIN], 0 )
                     AND Thang < ISNULL ( b.[TMax], 999999 )
          WHERE    Thang IS NOT NULL;

          UPDATE a
          SET    DoTuoi = N'Chưa rõ', MaDoTuoi = 99
          FROM   #PhanBoTheoTuoi a
          WHERE  MaDoTuoi IS NULL;

          --SELECT   ISNULL(DoTuoi, N'Chưa rõ') [Key], COUNT(1) [Value], MaDoTuoi
          --INTO     #ReusltTuoi
          --FROM     #PhanBoTheoTuoi
          --GROUP BY DoTuoi, MaDoTuoi, FacAdmissionID
          --ORDER BY [Value] DESC;
          SELECT   [Key], SUM ( [Value] ) [Value], MaDoTuoi
          FROM --#ReusltTuoi
                   (   SELECT      ISNULL ( DoTuoi, N'Chưa rõ' ) [Key], COUNT ( 1 ) [Value], MaDoTuoi
                       FROM        #PhanBoTheoTuoi
                       GROUP    BY DoTuoi, MaDoTuoi, FacAdmissionID
          --ORDER BY [Value] DESC
          ) xxx
          GROUP BY [Key], MaDoTuoi
          ORDER BY [Value] DESC;

          DROP TABLE #temp3, #temp4, #PhanBoTheoTuoi, #DoTuoi;
      --DROP TABLE  #ReusltTuoi;
      END;

      IF @_Type_ = 4 -- chi tiết doanh thu
      BEGIN
          ------------------------------biên lai--------------------------------------------------------------
          SELECT ID.PatientPay, ID.ClinicalSessionID, ID.SoTienGiam, ID.NoiDung, CAST('' AS DATE) UserCreatedDate,
                 PatientID, InvoiceID, FacAdmissionID, PhysicianAdmissionID, Reason, RefundType, IsRefund, TongTienGiam,
                 CounterID, ReceiptNumber, [Description], HinhThucThanhToan, CreatedByUser, CreatedOnByUser, IsVAT,
                 DoiTuongID, InvoiceNo, RealTotal
          INTO   #InvoiceWithRefundType
          FROM   #temp_BIL_InvoiceDetail_All ID
          WHERE  (RefundType IN ( 1, 2, 3 ) OR RefundType IS NULL) --AND I.IsRefund <> 1
                 AND Reason NOT LIKE N'%Lưu doanh thu vaccine%';

          UPDATE   I
          SET      UserCreatedDate = CAST(C.UserCreatedOn AS DATE)
          FROM     #InvoiceWithRefundType I
              JOIN dbo.CN_ClinicalSessions C WITH (NOLOCK)
                  ON I.ClinicalSessionID = C.ClinicalSessionID;

          SELECT   R.PatientID, R.FacAdmissionID, R.DoiTuongID, R.InvoiceID, R.InvoiceNo SoPhieu,
                   REPLACE ( R.Reason, N'Viện phí nội trú,', '' ) Reason,
                   CASE
                        WHEN R.RefundType IN ( 1, 2, 3 )
                             OR (R.IsRefund = 1 AND R.RefundType IS NULL) THEN 0
                        ELSE CASE
                                  WHEN SUM ( R.PatientPay ) > 0 THEN
                                       SUM ( R.PatientPay ) - SUM ( ISNULL ( TongTienGiam, 0 ))
                                  ELSE 0
                             END
                   END Total, CASE
                                   WHEN RealTotal = 0 THEN SUM ( R.PatientPay ) - SUM ( TongTienGiam )
                                   ELSE RealTotal
                              END RealTotal, CounterID, ReceiptNumber, [Description], HinhThucThanhToan, R.CreatedByUser,
                   R.CreatedOnByUser NgayThu, CAST(N'' AS NVARCHAR(99)) CounterName, CAST(N'' AS NVARCHAR(500)) NguoiThu,
                   CAST(N'' AS NVARCHAR(99)) DoiTuong, CAST(N'' AS VARCHAR(99)) SoKyHieu,
                   CASE
                        WHEN RefundType IN ( 1, 3 )
                             OR (IsRefund = 1 AND RefundType IS NULL) THEN N'Đã Hủy'
                        ELSE ''
                   END TrangThai, IsVAT
          INTO     #Data
          FROM
                   (   SELECT      PatientID, InvoiceID, FacAdmissionID, PhysicianAdmissionID, DoiTuongID, InvoiceNo, Reason,
                                   RefundType, IsRefund, ROUND ( SUM ( PatientPay ), 0 ) PatientPay, RealTotal,
                                   CASE
                                        WHEN TongTienGiam > 0 THEN TongTienGiam
                                        ELSE ROUND ( SUM ( SoTienGiam ), 0 )
                                   END TongTienGiam, CounterID, ReceiptNumber, Description, HinhThucThanhToan, CreatedByUser,
                                   CreatedOnByUser, IsVAT
                       FROM        #InvoiceWithRefundType I
                       GROUP    BY PatientID, InvoiceID, FacAdmissionID, PhysicianAdmissionID, DoiTuongID, InvoiceNo, Reason,
                                   RefundType, IsRefund, RealTotal, TongTienGiam, CounterID, ReceiptNumber, [Description],
                                   HinhThucThanhToan, CreatedByUser, CreatedOnByUser, IsVAT, FacAdmissionID) R
          GROUP BY PatientID, FacAdmissionID, DoiTuongID, InvoiceID, InvoiceNo, RealTotal, CounterID, CreatedByUser,
                   CreatedOnByUser, ReceiptNumber, [Description], RefundType, IsRefund, HinhThucThanhToan, Reason, IsVAT;

          UPDATE        #Data
          SET           CounterName = ISNULL ( C.CounterName, N'' )
          FROM          #Data d
              LEFT JOIN dbo.L_Counter C WITH (NOLOCK)
                  ON C.CounterID = d.CounterID
                     AND C.FacID = @FacID_;

          UPDATE        #Data
          SET           DoiTuong = DTTT.DoiTuongName
          FROM          #Data d
              LEFT JOIN dbo.L_DoiTuongTinhTien DTTT WITH (NOLOCK)
                  ON DTTT.DoiTuongID = d.DoiTuongID;

          UPDATE         #Data
          SET            NguoiThu = E.FullName
          FROM           #Data D
              INNER JOIN Security.dbo.Users U WITH (NOLOCK)
                  ON D.CreatedByUser = U.ID
              LEFT JOIN  HR.dbo.MDM_Employee E WITH (NOLOCK)
                  ON E.EmployeeID = U.EmpID;

          UPDATE #Data
          SET    SoKyHieu = SUBSTRING ( ReceiptNumber, 0, CHARINDEX ( '|', ReceiptNumber ));

          UPDATE #Data
          SET    ReceiptNumber = SUBSTRING ( ReceiptNumber, CHARINDEX ( '|', ReceiptNumber ) + 1, LEN ( ReceiptNumber ));

          SELECT   CreatedByUser, CounterName, NguoiThu AS NguoiThucHien, COUNT ( * ) AS TongSoBienLai,
                   SUM ( Total ) AS TongTien, CounterID
          INTO     #BienLai1
          FROM     #Data
          GROUP BY CreatedByUser, CounterName, NguoiThu, CounterID --,RealTotal
          ORDER BY CounterName;

          ------------------------------End biên lai--------------------------------------------------------------
          --------------------------------Hoàn phí----------------------------------------------------------------
          --  SELECT DISTINCT
          --         I.InvoiceRefundID, I.RefundNo, I.Note, I.CounterID, I.CreatedOn, I.CreatedBy, I.PatientID, I.Total,
          --         IRD.InvoiceID, IRD.PatientReceived, IRD.SoTienGiam
          ----  INTO   #Refund
          --  FROM   #temp_BIL_InvoiceRefund I INNER JOIN
          --         dbo.BIL_InvoiceRefundDetail IRD WITH (NOLOCK) ON I.InvoiceRefundID = IRD.InvoiceRefundID
          --  WHERE  I.RefundType NOT IN ( 1, 3 );
          SELECT        DISTINCT
                        I.InvoiceRefundID, I.RefundNo SoPhieu, I.InvoiceID, I.Note, BI.InvoiceNo PhieuThu, I.CounterID,
                        BI.ReceiptNumber, I.CreatedOn, I.CreatedBy, CAST(N'' AS NVARCHAR(500)) CounterName,
                        CAST(N'' AS NVARCHAR(500)) NguoiHoanPhi, CAST(N'' AS NVARCHAR(500)) DoiTuong,
                        (CASE
                              WHEN BI.InvoiceID IS NULL THEN (SUM ( I.PatientReceived ) - ISNULL ( SUM ( I.SoTienGiam ), 0 ))
                              ELSE (BI.RealTotal)
                         END) Total --20180820
          INTO          #Data2
          FROM
                        (   SELECT         DISTINCT
                                           I.InvoiceRefundID, I.RefundNo, I.Note, I.CounterID, I.CreatedOn, I.CreatedBy, I.PatientID, I.Total,
                                           IRD.InvoiceID , IRD.PatientReceived, IRD.SoTienGiam
                            --  INTO   #Refund
                            FROM           #temp_BIL_InvoiceRefund I
                                INNER JOIN dbo.BIL_InvoiceRefundDetail IRD WITH (NOLOCK)
                                    ON I.InvoiceRefundID = IRD.InvoiceRefundID
                            WHERE          I.RefundType NOT IN ( 1, 3 )) I
              JOIN      dbo.MDM_Patient P WITH (NOLOCK)
                  ON P.PatientID = I.PatientID
              LEFT JOIN dbo.BIL_Invoice BI WITH (NOLOCK)
                  ON I.InvoiceID = BI.InvoiceID
          GROUP BY      I.InvoiceRefundID, I.RefundNo, I.InvoiceID, I.Note, I.Total, I.CreatedOn, I.CreatedBy, I.CounterID,
                        BI.InvoiceID, BI.RealTotal, BI.InvoiceNo, BI.ReceiptNumber;

          UPDATE        D
          SET           CounterName = ISNULL ( C.CounterName, N'' )
          FROM          #Data2 D
              LEFT JOIN dbo.L_Counter C WITH (NOLOCK)
                  ON C.CounterID = D.CounterID;

          UPDATE         D
          SET            NguoiHoanPhi = E.FullName
          FROM           #Data2 D
              INNER JOIN Security.dbo.Users U WITH (NOLOCK)
                  ON D.CreatedBy = U.ID
              LEFT JOIN  HR.dbo.MDM_Employee E WITH (NOLOCK)
                  ON E.EmployeeID = U.EmpID;

          --SELECT   CreatedBy, CounterName, NguoiHoanPhi, COUNT(*) AS SoHoanPhi, SUM(Total) TongHoanPhi, CounterID
          ----INTO     #HoanPhi
          --FROM     #Data2
          --GROUP BY CreatedBy, CounterName, NguoiHoanPhi, CounterID;
          SELECT   CASE
                        WHEN b.CounterName IS NULL
                             OR b.CounterName = '' THEN h.CounterName
                        ELSE b.CounterName
                   END AS Quay, CASE
                                     WHEN b.NguoiThucHien IS NULL
                                          OR b.NguoiThucHien = '' THEN h.NguoiHoanPhi
                                     ELSE b.NguoiThucHien
                                END AS NguoiThaoTac, ISNULL ( b.TongSoBienLai, 0 ) AS TongSoBienLai,
                   ISNULL ( TongTien, 0 ) AS TongTien, ISNULL ( SoHoanPhi, 0 ) AS SoHoanPhi,
                   ISNULL ( TongHoanPhi, 0 ) AS TongHoanPhi,
                   ISNULL ( TongTien, 0 ) - ISNULL ( TongHoanPhi, 0 ) AS ThanhTien
          FROM     #BienLai1 b
              FULL JOIN
                   (   SELECT   CreatedBy, CounterName, NguoiHoanPhi, COUNT ( * ) AS SoHoanPhi, SUM ( Total ) TongHoanPhi,
                                CounterID
                       --INTO     #HoanPhi
                       FROM     #Data2
                       GROUP BY CreatedBy, CounterName, NguoiHoanPhi, CounterID) h
                  ON b.CreatedByUser = h.CreatedBy
                     AND b.CounterID = h.CounterID
          ORDER BY b.CounterName, b.NguoiThucHien;

          -------------------------------End Hoàn phí--------------------------------------------------------------
          DROP TABLE #InvoiceWithRefundType, #Data, #Data2,
                     -- #HoanPhi,
                     #BienLai1;
      --#Refund,
      END;

      IF @_Type_ = 5 -- chi tiết khám bệnh
      BEGIN
          --SELECT IsDuocTiem,
          --       PatientID,
          --       ProductTypeID,
          --       ServiceID,
          --       ClinicalSessionID,
          --       RoomID,
          --       FacAdmissionID,
          --       ServiceTypeID,
          --       ServiceHospitalTypeID,
          --       PhysicianAdmissionID,
          --       FacID
          ----INTO #tempDemTiem
          --FROM #temp_CN_ClinicalSessionsAll
          --WHERE ServiceID = 1
          --      AND RoomID <> 0
          --      AND FacID = @FacID
          --      AND UserCreatedDateAsInt
          --      BETWEEN @TuNgayAsInt AND @DenNgayAsInt;
          SELECT        DISTINCT
                        c.RoomName, b.PrimaryDoctor, f.FullName,
                        CASE
                             WHEN ((b.IsPracticed = 0) AND (b.DischargedOn IS NULL)) THEN N'ChoKham'
                             ELSE (CASE WHEN ((b.IsPracticed = 1) AND (b.DischargedOn IS NULL)) THEN N'DangKham' ELSE N'DaKham' END)
                        END Trangthai, CASE
                                            WHEN ISNULL ( b.IsKhongDuocTiem, 0 ) = 1 THEN N'KhongTiem'
                                            ELSE CAST(N'DuocTiem' AS NVARCHAR(20))
                                       END IsTiem,
                        --a.ClinicalSessionID ,
                        a.RoomID, a.PatientID, b.DischargedOn, b.IsPracticed, a.FacID, b.FacAdmissionID
          INTO          #Phongkhamtemp1
          FROM
                        (   SELECT IsDuocTiem, PatientID, ProductTypeID, ServiceID, ClinicalSessionID, RoomID, FacAdmissionID,
                                   ServiceTypeID, ServiceHospitalTypeID, PhysicianAdmissionID, FacID
                            --INTO #tempDemTiem
                            FROM   #temp_CN_ClinicalSessionsAll
                            WHERE  ServiceID = 1
                                   AND RoomID <> 0
                                   AND FacID = @FacID_
                                   AND UserCreatedDateAsInt
                                   BETWEEN @TuNgayAsInt AND @DenNgayAsInt) a
              LEFT JOIN dbo.CN_PhysicianAdmissions b WITH (NOLOCK)
                  ON a.PhysicianAdmissionID = b.PhysicianAdmissionID
              JOIN      dbo.L_DepartmentRoom c WITH (NOLOCK)
                  ON a.RoomID = c.RoomID
                     AND a.FacID = c.FacID
              LEFT JOIN [Security].dbo.Users e WITH (NOLOCK)
                  ON b.PrimaryDoctor = e.ID
              LEFT JOIN HR.dbo.MDM_Employee f WITH (NOLOCK)
                  ON e.EmpID = f.EmployeeID;

          --SELECT *
          --INTO   #Phongkhamtemp5
          --FROM   (   SELECT RoomName, PrimaryDoctor, FullName, Trangthai, PatientID, RoomID
          --           FROM   #Phongkhamtemp1) T
          --PIVOT (   COUNT(PatientID)
          --          FOR Trangthai IN ([DaKham], [DangKham], [ChoKham])) AS a

          --SELECT *
          --INTO   #Phongkhamtemp6
          --FROM   (   SELECT RoomName, PrimaryDoctor, FullName, IsTiem, PatientID, RoomIDtổng
          --           FROM   #Phongkhamtemp1
          --           WHERE  DischargedOn IS NOT NULL) T
          --PIVOT (   COUNT(PatientID)
          --          FOR IsTiem IN ([DuocTiem], [KhongTiem])) AS a
          CREATE TABLE #PKResult
              (RoomName NVARCHAR(100),
               BacSi NVARCHAR(200),
               BacSiID UNIQUEIDENTIFIER,
               ChoKham INT,
               DangKham INT,
               DaKham INT,
               Tong INT, --Tổng số mũi được chỉ định tiêm
               DuocTiem INT,
               KhongTiem INT,
               ThoiGianCho FLOAT,
               ThoiGianDelay FLOAT,
               RoomID INT,
               HeSo DECIMAL(18, 2),
               HeSoPTLD DECIMAL(18, 2));

          INSERT #PKResult
          (   RoomName, BacSi, BacSiID, ChoKham, DangKham, DaKham,
              --Tong,
              RoomID)
          SELECT RoomName, FullName, PrimaryDoctor, ChoKham, DangKham, DaKham,
                 --(ISNULL(ChoKham, 0) + ISNULL(DangKham, 0) + ISNULL(DaKham, 0)) Tong,
                 RoomID
          FROM --#Phongkhamtemp5
                 (   SELECT *
                     FROM   (SELECT RoomName, PrimaryDoctor, FullName, Trangthai, PatientID, RoomID FROM #Phongkhamtemp1) T
                     PIVOT (COUNT(PatientID)

  FOR Trangthai IN ([DaKham], [DangKham], [ChoKham])) AS a) xx;

          UPDATE a
          SET    DuocTiem = b.DuocTiem, KhongTiem = b.KhongTiem
          FROM   #PKResult a
              JOIN
              --#Phongkhamtemp6 b
                 (   SELECT *
                     FROM
                            (   SELECT RoomName, PrimaryDoctor, FullName, IsTiem, PatientID, RoomID
                                FROM   #Phongkhamtemp1
                                WHERE  DischargedOn IS NOT NULL) T
                     PIVOT (COUNT(PatientID)

  FOR IsTiem IN ([DuocTiem], [KhongTiem])) AS a) b
  ON a.BacSiID = b.PrimaryDoctor
  AND a.RoomName = b.RoomName;

          UPDATE   a
          SET      ChoKham = b.ChoKham, DangKham = b.DangKham
          FROM     #PKResult a
              JOIN #PKResult b
                  ON a.RoomID = b.RoomID
                     AND b.BacSiID IS NULL;

          SELECT   DATEDIFF ( MINUTE, a.TGBatDauKham, a.DischargedOn ) AS TimeTN, b.Username, a.DischargedBy
          INTO     #temp1001
          FROM     #Temp_CN_PhysicianAdmissions a
              JOIN Security.dbo.Users b WITH (NOLOCK)
                  ON a.DischargedBy = b.ID
          WHERE    a.TGBatDauKham IS NOT NULL
                   AND a.DischargedOn IS NOT NULL;

          --SELECT   AVG(TimeTN) KhamTB, Username, DischargedBy
          --INTO     #temp002
          --FROM     #temp1001
          --GROUP BY Username, DischargedBy
          --HAVING   AVG(TimeTN) IS NOT NULL

          --SELECT a.PatientID, a.ClinicalSessionID, c.PrimaryDoctor
          --INTO   #tempHeSo
          --FROM   #Temp_CN_ClinicalSessionID_Vaccine a JOIN
          --       #Temp_CN_PhysicianAdmissions c ON a.PatientID = c.PatientID
          --WHERE  c.PrimaryDoctor IS NOT NULL

          --UPDATE #PKResult
          --SET    Tong = b.SoMui
          --FROM   #PKResult c
          --    JOIN
          --       (   SELECT   PrimaryDoctor, COUNT ( 1 ) SoMui
          --           FROM --#tempHeSo
          --                    (   SELECT   a.PatientID, a.ClinicalSessionID, c.PrimaryDoctor
          --                        FROM     #Temp_CN_ClinicalSessionID_Vaccine a
          --                            JOIN #Temp_CN_PhysicianAdmissions c
          --                                ON a.PatientID = c.PatientID
          --                        WHERE    c.PrimaryDoctor IS NOT NULL) xx
          --           GROUP BY PrimaryDoctor) b
          --        ON c.BacSiID = b.PrimaryDoctor;

      	UPDATE #PKResult
          SET    Tong = b.SoMui
          FROM   #PKResult c
              JOIN
                 (   SELECT   PrimaryDoctor, COUNT ( 1 ) SoMui
                     FROM
                              (   SELECT   a.PatientID, a.ClinicalSessionID, a.UserCreatedByChiDinh as PrimaryDoctor
                                  FROM     #Temp_CN_ClinicalSessionID_Vaccine a
      								join #temp_CN_ClinicalSessionsAll b on a.ClinicalSessionID = b.ClinicalSessionID
      								JOIN QAHosGenericDB..L_DepartmentRoom d WITH (NOLOCK)
                                          ON d.RoomID = a.RoomID_ChiDInh
                                             AND d.FacID = a.FacID_ChiDinh
                                  WHERE    a.UserCreatedByChiDinh IS NOT NULL  AND d.RoomName NOT LIKE N'%lưu động%') xx
                     GROUP BY PrimaryDoctor) b
                  ON c.BacSiID = PrimaryDoctor;


          UPDATE #PKResult
          SET    HeSo = CAST(c.Tong * 1.00 / a.SoBN * 1.00 AS DECIMAL(18, 2))
          FROM   #PKResult c
              JOIN
                (   SELECT   PrimaryDoctor, COUNT ( DISTINCT PatientID ) SoBN
                     FROM --#tempHeSo
                              (   SELECT   a.PatientID, a.ClinicalSessionID, a.UserCreatedByChiDinh as PrimaryDoctor
                                  FROM     #Temp_CN_ClinicalSessionID_Vaccine a
                                      JOIN QAHosGenericDB..L_DepartmentRoom d WITH (NOLOCK)
                                          ON d.RoomID = a.RoomID_ChiDInh
                                             AND d.FacID = a.FacID_ChiDinh
                                  WHERE   a.UserCreatedByChiDinh IS NOT NULL
                                           AND d.RoomName not LIKE N'%lưu động%' ) xx
      				GROUP BY PrimaryDoctor) a ON c.BacSiID = a.PrimaryDoctor
      			   where c.RoomName NOT LIKE N'%lưu động%'

          --     JOIN
          --     (
          --         SELECT PrimaryDoctor,
          --                COUNT(1) SoMui
          --         FROM --#tempHeSo
          --         (
          --             SELECT a.PatientID,
          --                    a.ClinicalSessionID,
          --                    c.PrimaryDoctor
          --             FROM #Temp_CN_ClinicalSessionID_Vaccine a
          --                 JOIN #Temp_CN_PhysicianAdmissions c
          --                     ON a.PatientID = c.PatientID
          --JOIN QAHosGenericDB..L_DepartmentRoom d WITH(NOLOCK) ON d.RoomID = a.RoomID_ChiDInh AND d.FacID = a.FacID_ChiDinh
          --             WHERE c.PrimaryDoctor IS NOT NULL AND d.RoomName NOT LIKE N'%lưu động%'
          --         ) xx
          --         GROUP BY PrimaryDoctor
          --     ) b
          --         ON c.BacSiID = b.PrimaryDoctor;


          UPDATE #PKResult
          SET    HeSoPTLD = CAST(b.SoMui * 1.00 / a.SoBN * 1.00 AS DECIMAL(18, 2))
          FROM   #PKResult c
              JOIN
                 (   SELECT   PrimaryDoctor, COUNT ( DISTINCT PatientID ) SoBN
                     FROM --#tempHeSo
                              (  SELECT   a.PatientID, a.ClinicalSessionID, a.UserCreatedByChiDinh as PrimaryDoctor
                                  FROM     #Temp_CN_ClinicalSessionID_Vaccine a
                                      JOIN QAHosGenericDB..L_DepartmentRoom d WITH (NOLOCK)
                                          ON d.RoomID = a.RoomID_ChiDInh
                                             AND d.FacID = a.FacID_ChiDinh
                                  WHERE   a.UserCreatedByChiDinh IS NOT NULL
                                           AND d.RoomName LIKE N'%lưu động%' -- Phòng có tên giống "lưu động" là phòng tiêm lưu động, khách hàng nói điều đó. Anh Văn said -- Anhnn 09092020
                     ) xx
                     GROUP BY PrimaryDoctor) a
                  ON c.BacSiID = a.PrimaryDoctor
              JOIN
                 (   SELECT   PrimaryDoctor, COUNT (1) SoMui
                     FROM --#tempHeSo
                              (  SELECT   a.PatientID, a.ClinicalSessionID, a.UserCreatedByChiDinh as PrimaryDoctor
                                  FROM     #Temp_CN_ClinicalSessionID_Vaccine a
                                      JOIN QAHosGenericDB..L_DepartmentRoom d WITH (NOLOCK)
                                          ON d.RoomID = a.RoomID_ChiDInh
                                             AND d.FacID = a.FacID_ChiDinh
                                  WHERE   a.UserCreatedByChiDinh IS NOT NULL
                                           AND d.RoomName LIKE N'%lưu động%') xx
                     GROUP BY PrimaryDoctor) b
                  ON c.BacSiID = b.PrimaryDoctor
      			   where c.RoomName LIKE N'%lưu động%';

          SELECT a.RoomName, a.BacSi, a.BacSiID, a.ChoKham, a.DangKham, a.DaKham, ISNULL ( a.HeSo, 0 ) HeSoMuiTiem,
                 ISNULL ( DuocTiem, 0 ) DuocTiem, ISNULL ( KhongTiem, 0 ) KhongTiem, ISNULL ( b.KhamTB, 0 ) ThoiGiancho,
                 ISNULL ( a.HeSoPTLD, 0 ) HeSoMuiTiemLD, ISNULL ( a.Tong, 0 ) Tong
          --INTO             #FinalResult
          FROM   #PKResult a
              LEFT JOIN
              --#temp002 b ON a.BacSiID = b.DischargedBy;
                 (   SELECT   AVG ( TimeTN ) KhamTB, Username, DischargedBy
                     FROM     #temp1001
                     GROUP BY Username, DischargedBy
                     HAVING   AVG ( TimeTN ) IS NOT NULL) b
                  ON a.BacSiID = b.DischargedBy
      	order by bacsi,roomname

          --SELECT *
          --FROM   #FinalResult;
          CREATE TABLE #sumItem (TongChoKham INT, TongDangKham INT, TongDaKham INT, TongDuocTiem INT, TongKhongDuocTiem INT);

          INSERT #sumItem (TongChoKham, TongDangKham, TongDaKham, TongDuocTiem, TongKhongDuocTiem)
          SELECT SUM ( ISNULL ( ChoKham, 0 )) ChoKham, SUM ( ISNULL ( DangKham, 0 )) DangKham,
                 SUM ( ISNULL ( DaKham, 0 )) DaKham, SUM ( ISNULL ( DuocTiem, 0 )) DuocTiem,
                 SUM ( ISNULL ( KhongTiem, 0 )) KhongTiem
          FROM
                 (   SELECT DISTINCT
                            RoomID , BacSiID, ChoKham, DangKham, DaKham, DuocTiem, KhongTiem
                     FROM   #PKResult
                     WHERE  BacSiID IS NOT NULL) a;

          UPDATE #sumItem
          SET    TongChoKham =
                 (   SELECT ISNULL ( SUM ( ChoKham ), 0 )
                     FROM --#FinalResult
                            (   SELECT a.RoomName, a.BacSi, a.BacSiID, a.ChoKham, a.DangKham, a.DaKham,
                                       ISNULL ( a.HeSo, 0 ) HeSoMuiTiem, ISNULL ( DuocTiem, 0 ) DuocTiem,
                                       ISNULL ( KhongTiem, 0 ) KhongTiem, ISNULL ( b.KhamTB, 0 ) ThoiGiancho
                                FROM   #PKResult a
                                    LEFT JOIN
                                    --#temp002 b ON a.BacSiID = b.DischargedBy;
                                       (   SELECT   AVG ( TimeTN ) KhamTB, Username, DischargedBy
                                           FROM     #temp1001
                                           GROUP BY Username, DischargedBy
                                           HAVING   AVG ( TimeTN ) IS NOT NULL) b
                                        ON a.BacSiID = b.DischargedBy) xxx
                     WHERE  BacSiID IS NULL),
                 TongDangKham =
                 (   SELECT ISNULL ( SUM ( DangKham ), 0 )
                     FROM --#FinalResult
                            (   SELECT a.RoomName, a.BacSi, a.BacSiID, a.ChoKham, a.DangKham, a.DaKham,
                                       ISNULL ( a.HeSo, 0 ) HeSoMuiTiem, ISNULL ( DuocTiem, 0 ) DuocTiem,
                                       ISNULL ( KhongTiem, 0 ) KhongTiem, ISNULL ( b.KhamTB, 0 ) ThoiGiancho
                                FROM   #PKResult a
                                    LEFT JOIN
                                    --#temp002 b ON a.BacSiID = b.DischargedBy;
                                       (   SELECT   AVG ( TimeTN ) KhamTB, Username, DischargedBy
                                           FROM     #temp1001
                                           GROUP BY Username, DischargedBy
                                           HAVING   AVG ( TimeTN ) IS NOT NULL) b
                                        ON a.BacSiID = b.DischargedBy) xxx );

          SELECT N'Tổng khách chờ khám: ' + CONVERT ( NVARCHAR(5), TongChoKham ) + N'      Tổng Khách đang khám: '
                 + CONVERT ( NVARCHAR(5), ISNULL ( TongDangKham, 0 )) + N'      Tổng khách đã khám: '
                 + CONVERT ( NVARCHAR(5), ISNULL ( TongDaKham, 0 )) + N'      Tổng khách được tiêm: '
                 + CONVERT ( NVARCHAR(5), ISNULL ( TongDuocTiem, 0 )) + N'      Tổng khách không được tiêm: '
         + CONVERT ( NVARCHAR(5), ISNULL ( TongKhongDuocTiem, 0 ))
          FROM   #sumItem;

          DROP TABLE #Phongkhamtemp1, #PKResult,
                     -- #tempDemTiem,
                     #temp1001, #sumItem;

      --DROP TABLE #temp002, #FinalResult;#tempHeSo;, #Phongkhamtemp5, #Phongkhamtemp6
      END;

      IF @_Type_ = 6 -- chi tiết phòng tiêm
      BEGIN
          SELECT   DISTINCT
                   c.PatientID, c.ClinicalSessionID, c.RoomID, CASE WHEN c.CompletedOn IS NULL THEN 0 ELSE 1 END TrangThai,
                   r.RoomName
          INTO     #PTtemp
          FROM     #temp_CN_ClinicalSessionsAll c
              JOIN dbo.L_DepartmentRoom r WITH (NOLOCK)
                  ON c.RoomID = r.RoomID
                     AND r.FacID = @FacID_
                     AND r.IsPhongTiem = 1
          WHERE    ISNULL ( c.IsDuocTiem, 0 ) = 1
                   AND c.ProductTypeID = 17
                   AND ISNULL ( c.IsPaid, 0 ) = 1
                   AND EXISTS (SELECT 1 FROM #Temp_CN_ClinicalSessionID_Vaccine t WHERE t.ClinicalSessionID = c.ClinicalSessionID)

          SELECT PivotedOrder.RoomName, PivotedOrder.[1], PivotedOrder.[0]
          INTO   #end
          FROM
                 (   SELECT    T1.RoomName, T1.TrangThai, COUNT ( T1.PatientID ) SoNguoi
                     FROM
                               (   SELECT       RoomName, TrangThai, RoomID, PatientID
                                   FROM         #PTtemp WITH (NOLOCK)
                                   GROUP     BY RoomName, TrangThai, RoomID, PatientID) AS T1
                     GROUP  BY RoomName, TrangThai, RoomID, PatientID) T
          PIVOT (SUM(SoNguoi)

  FOR TrangThai IN ([0], [1])) AS PivotedOrder;

          SELECT PivotedOrder.RoomName, PivotedOrder.[1], PivotedOrder.[0]
          INTO   #end1
          FROM
                 (   SELECT    RoomName, TrangThai, COUNT ( ClinicalSessionID ) SoMui
                     FROM      #PTtemp WITH (NOLOCK)
                     GROUP  BY RoomName, TrangThai, RoomID, ClinicalSessionID) T
          PIVOT (SUM(SoMui)

  FOR TrangThai IN ([0], [1])) AS PivotedOrder;

          SELECT   a.RoomName, ISNULL ( a.[0], 0 ) chuatiem, ISNULL ( a.[1], 0 ) datiem, ISNULL ( b.[0], 0 ) muichuatiem,
                   ISNULL ( b.[1], 0 ) muidatiem
          FROM     #end a
              JOIN #end1 b
                  ON a.RoomName = b.RoomName;

          DROP TABLE #PTtemp, #end, #end1;
      END;

      IF @_Type_ = 7 -- chi tiết thời gian
      BEGIN
          CREATE TABLE #thoigian (phanhe NVARCHAR(50), thoigianchomin FLOAT, thoigianchomax FLOAT, trungbinh FLOAT);

          DECLARE @Min INT = 0;
          DECLARE @Max INT = 0;
          DECLARE @AVG DECIMAL(18, 2) = 0;

          SELECT   DATEDIFF ( MINUTE, b.AdmitOn, b.TGBatDauKham ) ChoKham, b.DischargedOn, b.DischargedBy, b.TGBatDauKham
          INTO     #tempT
          FROM     #Temp_CN_PhysicianAdmissions b
              JOIN dbo.CN_ClinicalSessions a WITH (NOLOCK)
                  ON a.PhysicianAdmissionID = b.PhysicianAdmissionID
          WHERE    b.TGBatDauKham IS NOT NULL;

          DELETE #tempT
          WHERE  ChoKham < 5;

          DELETE #tempT
          WHERE  ChoKham >= 360;

          SET @Min = (SELECT TOP (1) ChoKham FROM #tempT ORDER BY ChoKham);
          SET @Max = (SELECT TOP (1) ChoKham FROM #tempT ORDER BY ChoKham DESC);
          SET @AVG = (SELECT TOP (1) SUM ( ChoKham ) / COUNT ( * ) ChoKham FROM #tempT);

          INSERT #thoigian (phanhe, thoigianchomin, thoigianchomax, trungbinh)
          (SELECT N'Thời gian chờ khám', -- phanhe - nvarchar(50)
                  @Min,                  -- thoigianchomin - float
                  @Max,                  -- thoigianchomax - float
                  @AVG                   -- trungbinh - float
          );

          SELECT   DATEDIFF ( MINUTE, a.TGBatDauKham, a.DischargedOn ) Kham, a.DischargedBy PrimaryDoctor, b.Username
          INTO     #temp1T
          FROM     #tempT a
              JOIN Security.dbo.Users b WITH (NOLOCK)
                  ON a.DischargedBy = b.ID
          WHERE    a.DischargedOn IS NOT NULL;

          SET @Min = (SELECT TOP (1) Kham FROM #temp1T ORDER BY Kham);
          SET @Max = (SELECT TOP (1) Kham FROM #temp1T ORDER BY Kham DESC);
          SET @AVG =
          (   SELECT TOP (1)
                     SUM ( ISNULL ( KhamTB, 0 )) / COUNT ( 1 )
              FROM
                     (   SELECT    AVG ( Kham ) KhamTB, Username, PrimaryDoctor
                         FROM      #temp1T
                         GROUP  BY Username, PrimaryDoctor
                         HAVING    AVG ( Kham ) IS NOT NULL) a );

          INSERT #thoigian (phanhe, thoigianchomin, thoigianchomax, trungbinh)
          (SELECT N'Thời gian khám', -- phanhe - nvarchar(50)
                  @Min,              -- thoigianchomin - float
                  @Max,              -- thoigianchomax - float
                  @AVG               -- trungbinh - float
          );

          SELECT   DATEDIFF ( MINUTE, c.DischargedOn, a.CompletedOn ) Tiem
          INTO     #temp2T
          FROM     #Temp_CN_ClinicalSessionID_Vaccine a
              JOIN dbo.CN_PhysicianAdmissions c WITH (NOLOCK)
                  ON c.PhysicianAdmissionID = a.PhysicianAdmissionID
          WHERE    a.CompletedOn IS NOT NULL
                   AND c.DischargedOn IS NOT NULL
                   AND a.ProductTypeID = 17
                   AND ISNULL ( a.IsDuocTiem, 0 ) = 1;

          DELETE #temp2T
          WHERE  Tiem < 0;

          DELETE #temp2T
          WHERE  Tiem >= 360;

          SET @Min = (SELECT TOP (1) * FROM #temp2T ORDER BY Tiem);
          SET @Max = (SELECT TOP (1) * FROM #temp2T ORDER BY Tiem DESC);
          SET @AVG = (SELECT TOP (1) SUM ( Tiem ) / COUNT ( * ) Tiem FROM #temp2T);

          INSERT #thoigian (phanhe, thoigianchomin, thoigianchomax, trungbinh)
          (SELECT N'Thời gian tiêm', -- phanhe - nvarchar(50)
                  @Min,              -- thoigianchomin - float
                  @Max,              -- thoigianchomax - float
                  @AVG               -- trungbinh - float
          );

          SELECT phanhe, thoigianchomin, thoigianchomax, trungbinh
          FROM   #thoigian;

          DROP TABLE #thoigian;
          DROP TABLE #tempT, #temp1T, #temp2T;
      END;

      IF @_Type_ = 8
      BEGIN
          SELECT   e.PatientHospitalID, e.FullName, a.STTMuiTiem, d.ProductName, a.Vaccine_MaChung, a.CreatedOn,
                   a.HopDongID, a.ClinicalSessionID
          --INTO   #7temp1
          FROM     #temp_BIL_InvoiceDetail_All c JOIN dbo.CN_ClinicalSessions a WITH (NOLOCK) ON c.ClinicalSessionID = a.ClinicalSessionID
              JOIN dbo.L_Product d WITH (NOLOCK) ON a.Vaccine_MaChung = d.MaChung AND a.FacID = d.FacID
              JOIN dbo.MDM_Patient e WITH (NOLOCK) ON a.PatientID = e.PatientID
          WHERE    c.IsReserved = 1 --ISNULL ( a.IsDatTruoc, 0 ) = 1;

          --SELECT * FROM #7temp1;
          SELECT   PatientHospitalID, FullName, COUNT ( * ) qty
          FROM --#7temp1
                   (   SELECT   e.PatientHospitalID, e.FullName, a.STTMuiTiem, d.ProductName, a.Vaccine_MaChung, a.CreatedOn,
                                a.HopDongID, a.ClinicalSessionID
                       FROM     #temp_BIL_InvoiceDetail_All c
                           JOIN dbo.CN_ClinicalSessions a WITH (NOLOCK) ON c.ClinicalSessionID = a.ClinicalSessionID
                           JOIN dbo.L_Product d WITH (NOLOCK) ON a.Vaccine_MaChung = d.MaChung AND a.FacID = d.FacID
                           JOIN dbo.MDM_Patient e WITH (NOLOCK) ON a.PatientID = e.PatientID
                       WHERE    c.IsReserved = 1 --ISNULL ( a.IsDatTruoc, 0 ) = 1
      				 ) xx
          GROUP BY PatientHospitalID, FullName;

      --DROP TABLE #7temp1;
      END;

      IF @_Type_ = 9
      BEGIN
          SELECT        DISTINCT
                        CONVERT ( DATE, a.AdmitDate ) NgayKham, c.PatientHospitalID MaBenhNhan, c.FullName HovaTen, d.RoomName Phong,
                        f.FullName BacSi, ISNULL ( g.GhiChu, '' ) GhiChu, a.IsKhongDuocTiem
          FROM          #Temp_CN_PhysicianAdmissions a
              JOIN      #temp_CN_ClinicalSessionsAll b WITH (NOLOCK)
                  ON a.PhysicianAdmissionID = b.PhysicianAdmissionID
              JOIN      dbo.MDM_Patient c WITH (NOLOCK)
                  ON a.PatientID = c.PatientID
              JOIN      dbo.L_DepartmentRoom d WITH (NOLOCK)
                  ON a.RoomID = d.RoomID
                     AND a.FacID = d.FacID
              JOIN      Security.dbo.Users e WITH (NOLOCK)
                  ON a.PrimaryDoctor = e.ID
              JOIN      HR.dbo.MDM_Employee f
                  ON e.EmpID = f.EmployeeID
              LEFT JOIN dbo.CN_VitalSign g
                  ON a.FacAdmissionID = g.FacAdmissionID
                     AND a.PhysicianAdmissionID = g.PhysicianAdmissionID
          WHERE         a.IsKhongDuocTiem = 1
          ORDER BY      c.PatientHospitalID;
      END;

      IF @_Type_ = 10
      BEGIN
          SELECT   DISTINCT
                   a.ApprovedOutNo, a.RequestStockID, e.ProductName, e.ProductID, CAST(a.CreatedOn AS DATE) AS [Date],
                   a.CreatedOn, b.ClinicalSessionID, b.ApprovedQty
          INTO     #temp91
          FROM     #temp_INV_ApprovedOut a
              JOIN dbo.INV_ApprovedOutDetail b WITH (NOLOCK)
                  ON a.ApprovedOutID = b.ApprovedOutID
              JOIN dbo.L_Product e WITH (NOLOCK)
                  ON b.ProductID = e.ProductID
          WHERE    e.FacID = a.FacID
                   AND e.ProductTypeID = 17
          ORDER BY e.ProductName;

          SELECT   ProductID, ProductName, ApprovedQty LoaiXuat, SUM ( ApprovedQty ) LuongXuat, COUNT ( 1 ) AS [SL] --,SUM(ApprovedQty)/COUNT(*) TrungBinh
          FROM     #temp91
          GROUP BY ProductID, ProductName, ApprovedQty
          ORDER BY ProductName, [SL] DESC;

          SELECT   ProductID, ProductName, COUNT ( 1 ) AS [SL]
          FROM     #temp91
          GROUP BY ProductID, ProductName
          ORDER BY [SL] DESC;

          DROP TABLE #temp91;
      END;

      IF @_Type_ = 1111
      BEGIN
          SELECT   b.PatientID, COUNT ( b.FacAdmissionID ) dv, CAST('' AS NVARCHAR(500)) FullName,
                   CAST('' AS NVARCHAR(20)) SDT, CAST('' AS NVARCHAR(3)) GioiTinh, CAST('' AS DATETIME) NamSinh
          INTO     #temBNDouble
          FROM     #Temp_CN_PhysicianAdmissions b
              JOIN #temp_CN_ClinicalSessionsAll c
                  ON b.PhysicianAdmissionID = c.PhysicianAdmissionID
          WHERE    c.ServiceID = 1
          GROUP BY b.PatientID, b.AdmitDateAsInt
          HAVING   COUNT ( b.FacAdmissionID ) > 1
          ORDER BY b.PatientID;

          UPDATE   #temBNDouble
          SET      FullName = b.FullName, SDT = b.HomePhone, GioiTinh = CASE WHEN b.Gender = 0 THEN N'Nữ' ELSE N'Nam' END,
                   NamSinh = b.DoB
          FROM     #temBNDouble a
              JOIN dbo.MDM_Patient b WITH (NOLOCK)
                  ON a.PatientID = b.PatientID;

          SELECT PatientID, dv, FullName, SDT, GioiTinh, FORMAT ( NamSinh, 'dd-MM-yyyy', 'en-US' ) NamSinh
          FROM   #temBNDouble;

          DROP TABLE #temBNDouble;
      END;

      IF @debug = 1
      BEGIN
          INSERT #dt (step, duration)
          SELECT @step, DATEDIFF ( ms, @tstart, GETDATE ());

          SELECT step, duration
          FROM   #dt
          UNION
          SELECT 'Sum', SUM ( duration )
          FROM   #dt;


      END;

      DROP TABLE IF EXISTS #dt;
      DROP TABLE IF EXISTS #tempTongquan, #TempPatientError--, #temp_BIL_InvoiceDetail_KhacCongKham--, #TSoLuong;
      DROP TABLE IF EXISTS #temp_CN_ClinicalSessionsAll;
      DROP TABLE IF EXISTS #temp_CN_FacAdmissions;
      DROP TABLE IF EXISTS #Temp_CN_ClinicalSessionID_Vaccine;
      DROP TABLE IF EXISTS #Temp_CN_PhysicianAdmissions;
      DROP TABLE IF EXISTS #temp_BIL_InvoiceDetail_All;
      DROP TABLE IF EXISTS #temp_BIL_Invoice;
      DROP TABLE IF EXISTS #temp_INV_ApprovedOut;
      DROP TABLE IF EXISTS #temp_BIL_InvoiceRefund;
      DROP TABLE  IF EXISTS #TblKhachHopDong,#TempDetail,#tempCL,#TblKhachHopDong1

  END;

---
