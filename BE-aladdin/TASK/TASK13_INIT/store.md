USE [QAHosGenericDB]
GO
/****** Object:  StoredProcedure [dbo].[ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc]    Script Date: 8/14/2025 3:28:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*
Version: 1.0.0.0 M.Hieu 20190730 17:30 Lấy mũi tiêm cho hợp đồng sau khi đã đặt trước
*/
ALTER PROCEDURE [dbo].[ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc]
(
    @SessionID VARCHAR(MAX),
    @FacID VARCHAR(10),
    @HopDongID UNIQUEIDENTIFIER,
    @IDPhacDo INT
)
AS
BEGIN
    SET NOCOUNT ON
    ---------------------Debug---------------------
    --DECLARE @FacID VARCHAR(10) = '8.1'
    --DECLARE @HopDongID UNIQUEIDENTIFIER = '56ee142d-b29e-11e9-8ad4-b083fe979cd3'
    --DECLARE @IDPhacDo INT = '234'
    ---------------------Debug---------------------

    --DECLARE @UserID UNIQUEIDENTIFIER
    --SELECT @UserID = UserID
    --FROM [Security].dbo.[Sessions] WITH ( NOLOCK )
    --WHERE [SessionID] = @SessionID

    ---- check if user authenticated
    --IF @UserID IS NULL
    --    RETURN

    SELECT CAST(0 AS INT) AS STTMuiTiem,
           GiaMuiTiem AS Gia,
           TienGiam,
           PhanTramGiam,
           CAST(0 AS DECIMAL(18, 2)) AS ThanhTien,
           NgayDung,
           IsTiemNgoai,
           MaMuiTiem AS ID_Detail,
           IDPhacDo,
           CAST(0 AS INT) AS ThoiGian_GianCach,
           HopDongID,
           CAST('' AS VARCHAR(100)) AS SoHopDong,
           HopDongDetailID,
           IsMuiNgoaiDanhMuc,
           GiaChenhLechTiemNgoai,
           CAST(0 AS INT) AS DoiTuongSuDungID,
           CAST(0 AS INT) AS LoaiGianCach,
           ISNULL ( MuiThanhToan, 0 ) AS MuiThanhToan,
           CAST(1 AS INT) AS IsKhongDuocBoCheckThanhToan,
           HopDongID_Goc,
           GiaChenhLechChuaGiam,
           GiaMuiTiem,
		   CAST(0 AS BIT) IsDaTiem 
    INTO #Result
    FROM dbo.Vaccine_HopDong_Detail_Root WITH ( NOLOCK )
    WHERE HopDongID = @HopDongID
          AND IDPhacDo = @IDPhacDo

    UPDATE #Result
    SET ThanhTien = CASE WHEN IsMuiNgoaiDanhMuc = 1
                              OR IsTiemNgoai = 1 THEN 0
                         ELSE
        ( CASE WHEN ( ISNULL ( GiaChenhLechChuaGiam, 0 ) > 0 )
                    OR (   ISNULL ( GiaChenhLechChuaGiam, 0 ) = 0
                           AND ISNULL ( GiaChenhLechTiemNgoai, 0 ) = 0 ) THEN ( GiaMuiTiem + ISNULL ( GiaChenhLechChuaGiam, 0 ) - ISNULL ( TienGiam, 0 ))
               ELSE ISNULL ( GiaMuiTiem - ( ISNULL ( TienGiam, 0 ) - ( ISNULL ( TienGiam, 0 ) - GiaMuiTiem * ISNULL ( PhanTramGiam, 0 ) / 100.00 )) + ISNULL ( GiaChenhLechTiemNgoai, 0 ), 0 ) END ) END

    UPDATE #Result
    SET STTMuiTiem = V.STTMuiTiem
    FROM #Result R
         JOIN dbo.L_Vaccine_Phacdo_Detail V WITH ( NOLOCK ) ON R.ID_Detail = V.ID_Detail

    UPDATE #Result
    SET SoHopDong = H.SoHDong
    FROM #Result R
         JOIN dbo.Vaccine_HopDong H WITH ( NOLOCK ) ON R.HopDongID = H.HopDongID

    UPDATE #Result
    SET DoiTuongSuDungID = V.DoiTuongSuDungID
    FROM #Result R
         JOIN dbo.L_Vaccine_Phacdo V WITH ( NOLOCK ) ON R.IDPhacDo = V.IDPhacDo

    SELECT *
    FROM #Result
    ORDER BY STTMuiTiem

    DROP TABLE #Result
END