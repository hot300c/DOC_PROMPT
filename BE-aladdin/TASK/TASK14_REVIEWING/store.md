USE [QAHosGenericDB]
GO
/****** Object:  StoredProcedure [dbo].[ws_CN_ClinicalSessions_GetByNgayChiDinh]    Script Date: 8/14/2025 3:32:29 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*
Version: 1.0.0.0 20161209 Trung lam lay danh sach dich vu da chi dinh
Version: 1.0.1.0 20161212 Trung sua them PatientID
Version: 1.0.2.0 20161212 Trung chi lay dich vu ngoai tru
Version: 1.0.3.0 20161212 Trung group dich vu
Version: 1.0.4.0 20170407 M.Hieu Tạo bảng tạm #CN_ClinicalSessions
Version: 1.0.5.0 20180403 Van quản lý hệ thống theo chuỗi
Version: 1.0.6.0 20180419 M.Hieu Thêm trường
Version: 1.0.6.1 20200825 Van optimize
*/
ALTER PROCEDURE [dbo].[ws_CN_ClinicalSessions_GetByNgayChiDinh]
    (
    @SessionID VARCHAR(MAX), @NgayChiDinh DATETIME, @FacID VARCHAR(10), @PatientID UNIQUEIDENTIFIER)
AS
BEGIN
    SET NOCOUNT ON
    -----------------------------Debug---------------------------------
    --DECLARE @FacAdmissionID UNIQUEIDENTIFIER
    --SET @FacAdmissionID = '97403B2C-4C63-48F0-8C53-91581210E937'   
    --DECLARE @PatientID UNIQUEIDENTIFIER
    --SET @PatientID = '07B7B773-763D-42F1-B834-00005800794A'   
    --DECLARE @NgayChiDinh DATETIME
    --SET @NgayChiDinh = '2015-08-12 14:39:01.333'   
    --DECLARE @FacID VARCHAR(10)
    --SET @FacID = '1'   
    -------------------------------------------------------------------    

    DECLARE @QuanLiBenhNhanTheoChuoi VARCHAR(1)
    DECLARE @CustomerFacID VARCHAR(10)

    SELECT @QuanLiBenhNhanTheoChuoi = Value
    FROM Application..Settings WITH (NOLOCK)
    WHERE ID = 90000 AND FacID = @FacID

    IF @QuanLiBenhNhanTheoChuoi IS NULL
    BEGIN
        SELECT @QuanLiBenhNhanTheoChuoi = Value
        FROM Application..Settings WITH (NOLOCK)
        WHERE ID = 90000 AND FacID = '0'

        IF @QuanLiBenhNhanTheoChuoi IS NULL
            SET @QuanLiBenhNhanTheoChuoi = 'N'
    END

    IF @QuanLiBenhNhanTheoChuoi = 'Y'
    BEGIN
        SELECT @CustomerFacID = CustomerID
        FROM dbo.L_Customer WITH (NOLOCK)
        WHERE FacID = @FacID
    END

    CREATE TABLE #result
        (ClinincalSessionID UNIQUEIDENTIFIER,
         ServiceID INT,
         ServiceName NVARCHAR(500),
         Qty INT,
         DonGia DECIMAL(15, 2),
         ThanhTien DECIMAL(15, 2),
         FacID VARCHAR(10),
         IsDaThanhToan BIT, --1.0.6.0
         IsDaThucHien BIT   --1.0.6.0
    )

    IF @QuanLiBenhNhanTheoChuoi = 'Y'
    BEGIN
        --SELECT ClinicalSessionID, ServiceID, Qty, DonGia, CreatedOn, FacAdmissionID, IsPaid, CompletedOn
        --INTO #CN_ClinicalSessionsChuoi
        --FROM dbo.CN_ClinicalSessions WITH (NOLOCK)
        --WHERE PatientID = @PatientID

        INSERT INTO #result
        (ClinincalSessionID, ServiceID, Qty, DonGia, FacID, IsDaThanhToan, IsDaThucHien)
        SELECT ClinicalSessionID, ServiceID, Qty, DonGia, fa.FacID, CASE WHEN cs.IsPaid = 1
                                                                             THEN 1
                                                                    ELSE 0
                                                                    END, CASE WHEN cs.CompletedOn IS NOT NULL
                                                                                  THEN 1
                                                                         ELSE 0
                                                                         END
        FROM dbo.CN_ClinicalSessions cs WITH (NOLOCK)
            INNER JOIN dbo.CN_FacAdmissions fa WITH (NOLOCK) ON fa.FacAdmissionID = cs.FacAdmissionID
        WHERE cs.PatientID = @PatientID 
		AND UserCreatedDate  = CAST(@NgayChiDinh AS DATE) 
		--CAST(cs.CreatedOn AS DATE) = CAST(@NgayChiDinh AS DATE) 
		AND ServiceID != 0 AND fa.FacAdmissionType != 'IP'


        UPDATE #result
        SET ServiceName = s.Name
        FROM dbo.L_Service s WITH (NOLOCK)
        WHERE #result.ServiceID = s.ServiceID AND s.FacID = #result.FacID

        UPDATE #result
        SET ThanhTien = DonGia * Qty

        SELECT --ClinincalSessionID ,
            ServiceID, ServiceName, SUM ( Qty ) AS Qty, DonGia, SUM ( ThanhTien ) AS ThanhTien
        FROM #result
        GROUP BY --ClinincalSessionID ,
            ServiceID, ServiceName, DonGia

    --DROP TABLE #CN_ClinicalSessionsChuoi
    END
    ELSE
    BEGIN
        --SELECT ClinicalSessionID ,
        --       ServiceID ,
        --       Qty ,
        --       DonGia ,
        --       CreatedOn ,
        --       FacAdmissionID ,
        --       IsPaid ,
        --       CompletedOn
        --INTO   #Temp_CN_ClinicalSessions
        --FROM   dbo.CN_ClinicalSessions WITH ( NOLOCK )
        --WHERE  PatientID = @PatientID

        INSERT INTO #result
        (ClinincalSessionID, ServiceID, Qty, DonGia, IsDaThanhToan, IsDaThucHien)
        SELECT ClinicalSessionID, ServiceID, Qty, DonGia, CASE WHEN cs.IsPaid = 1
                                                                   THEN 1
                                                          ELSE 0
                                                          END, CASE WHEN cs.CompletedOn IS NOT NULL
                                                                        THEN 1
                                                               ELSE 0
                                                               END
        FROM dbo.CN_ClinicalSessions cs WITH (NOLOCK)
            INNER JOIN dbo.CN_FacAdmissions fa WITH (NOLOCK)
                ON fa.FacAdmissionID = cs.FacAdmissionID
        WHERE cs.PatientID = @PatientID 
		AND UserCreatedDate  = CAST(@NgayChiDinh AS DATE) --CAST(cs.CreatedOn AS DATE) = CAST(@NgayChiDinh AS DATE) 
		AND ServiceID != 0 AND fa.FacAdmissionType != 'IP'


        UPDATE #result
        SET ServiceName = s.Name
        FROM dbo.L_Service s WITH (NOLOCK)
        WHERE #result.ServiceID = s.ServiceID AND s.FacID = @FacID

        UPDATE #result
        SET ThanhTien = DonGia * Qty

        SELECT --ClinincalSessionID ,
            ServiceID, ServiceName, SUM ( Qty ) AS Qty, DonGia, SUM ( ThanhTien ) AS ThanhTien, IsDaThanhToan, IsDaThucHien
        FROM #result
        GROUP BY --ClinincalSessionID ,
            ServiceID, ServiceName, DonGia, IsDaThanhToan, IsDaThucHien

    --DROP TABLE #Temp_CN_ClinicalSessions
    END

    DROP TABLE #result
END