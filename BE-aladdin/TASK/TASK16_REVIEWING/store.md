USE [QAHosGenericDB]
GO
/****** Object:  StoredProcedure [dbo].[ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh]    Script Date: 8/15/2025 10:10:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Hieunt
-- Create date: 2018-04-26 16:14
-- Description:	kiểm tra cảnh báo tiêm vaccine trùng nhóm bệnh
-- =============================================

/*
Version: 1.0.0.0
Version: 1.0.1.0 2019-03-14 15:12 hieunt đổi câu thông báo
Version: 1.0.2.0 20240326 quanvxa 124715-( 0 - Undefined)-Ngoại Trú>Khám Bệnh :[VNVC Nhập Lịch Sử ] : Đối tượng khác nhau nhưng chỉ định vẫn hiển thị cảnh báo đồng bộ lịch hẹn
*/

ALTER PROCEDURE [dbo].[ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh]
    @SessionID VARCHAR(MAX),
    @PatientID UNIQUEIDENTIFIER,
    @MaChung VARCHAR(100),
    @NgayChiDinh DATE,
    @PhacDoDangChiDinh UNIQUEIDENTIFIER,
    @FacID VARCHAR(10)
AS
BEGIN

    --====================================Debug=======================================
    --DECLARE @PatientID UNIQUEIDENTIFIER = 'b87020e4-9fa0-4cb5-bab5-0071f56501fd';
    --DECLARE @MaChung VARCHAR(100) = 'S00000003';
    --DECLARE @NgayChiDinh DATE = '2024-03-27';
    --DECLARE @PhacDoDangChiDinh UNIQUEIDENTIFIER = 'f51e5bb8-ec02-11ee-b780-8cec4b9f2b93';
    --DECLARE @FacID VARCHAR(10) = '8.1';
    --====================================Debug=======================================

    SET NOCOUNT ON;

    DECLARE @IDPhacDo_DangChiDinh INT;
    DECLARE @DoiTuongSuDungID_DangChiDinh INT;

    SELECT @IDPhacDo_DangChiDinh = [IDPhacDo]
    FROM [QAHosGenericDB]..[Vaccine_PhacDoBenhNhan] WITH (NOLOCK)
    WHERE [IDPhacDoBenhNhan] = @PhacDoDangChiDinh;

    SELECT @DoiTuongSuDungID_DangChiDinh = [DoiTuongSuDungID]
    FROM [QAHosGenericDB]..[L_Vaccine_Phacdo] WITH (NOLOCK)
    WHERE [IDPhacDo] = @IDPhacDo_DangChiDinh;

    SELECT [NhomBenhID]
    INTO [#tempnhombenh]
    FROM [QAHosGenericDB]..[L_NhomBenhVaccineDetail] WITH (NOLOCK)
    WHERE [MaChung] = @MaChung;

    SELECT [MaChung]
    INTO [#tempMaChungTongHop]
    FROM [QAHosGenericDB]..[L_NhomBenhVaccineDetail] [NBD] WITH (NOLOCK)
    WHERE EXISTS
    (
        SELECT 1
        FROM [#tempnhombenh] [NB] WITH (NOLOCK)
        WHERE [NB].[NhomBenhID] = [NBD].[NhomBenhID]
    )
          AND [MaChung] <> @MaChung
    GROUP BY [MaChung];


    SELECT [P].[IDPhacDoBenhNhan],
           [VP].[MaChung],
           [P].[NgayDong],
           [P].[NhomBenhID],
           [VP].[DoiTuongSuDungID]
    INTO [#tempPhacDoBenhNhan1]
    FROM [QAHosGenericDB]..[Vaccine_PhacDoBenhNhan] [P] WITH (NOLOCK),
         [QAHosGenericDB]..[L_Vaccine_Phacdo] [VP] WITH (NOLOCK)
    WHERE [P].[PatientID] = @PatientID
          AND [P].[IDPhacDo] = [VP].[IDPhacDo];


    SELECT [IDPhacDoBenhNhan],
           [MaChung],
           [NgayDong],
           [NhomBenhID]
    INTO [#tempPhacDoBenhNhan]
    FROM [#tempPhacDoBenhNhan1] [PDBN1] WITH (NOLOCK)
    WHERE EXISTS
    (
        SELECT 1
        FROM [#tempMaChungTongHop] [MC] WITH (NOLOCK)
        WHERE [MC].[MaChung] = [PDBN1].[MaChung]
    )
          AND [DoiTuongSuDungID] = @DoiTuongSuDungID_DangChiDinh
          AND [NgayDong] IS NULL;

    DROP TABLE IF EXISTS [#tempMaChungTongHop],
                         [#tempPhacDoBenhNhan1];


    SELECT [PDD].[IDPhacDoBenhNhan_Detail],
           [T].[IDPhacDoBenhNhan],
           [PDD].[IDPhacDo_Detail],
           [PDD].[NgayHenTiem],
           [T].[MaChung],
           [PDD].[CompleteOn],
           [TenNhomBenh] = CAST(N'' AS NVARCHAR(1000))
    INTO [#tempphacdobenhnhandetail]
    FROM [#tempPhacDoBenhNhan] [T],
         [QAHosGenericDB]..[Vaccine_PhacDoBenhNhan_Detail] [PDD] WITH (NOLOCK)
    WHERE [PDD].[PatientID] = @PatientID
          AND [T].[IDPhacDoBenhNhan] = [PDD].[IDPhacDoBenhNhan]
          AND [PDD].[CompleteOn] IS NOT NULL
          AND CAST([PDD].[CompleteOn] AS DATE) <> @NgayChiDinh;

    DROP TABLE IF EXISTS [#tempPhacDoBenhNhan];

    IF EXISTS (SELECT 1 FROM [#tempphacdobenhnhandetail])
    BEGIN
        UPDATE [#tempphacdobenhnhandetail]
        SET [TenNhomBenh] = (STUFF(
                                      (
                                          SELECT N', ' + [lnbv].[TenNhomBenh]
                                          FROM [QAHosGenericDB]..[L_NhomBenhVaccineDetail] AS [n] WITH (NOLOCK)
                                              INNER JOIN [QAHosGenericDB]..[L_NhomBenhVaccine] AS [lnbv] WITH (NOLOCK)
                                                  ON [n].[NhomBenhID] = [lnbv].[ID]
                                          WHERE [T].[MaChung] = [n].[MaChung]
                                                AND EXISTS
                                          (
                                              SELECT 1
                                              FROM [#tempnhombenh] [nb] WITH (NOLOCK)
                                              WHERE [n].[NhomBenhID] = [nb].[NhomBenhID]
                                          )
                                          FOR XML PATH(''), TYPE
                                      ).[value]('.', 'NVARCHAR(500)'),
                                      1,
                                      2,
                                      N''
                                  )
                            )
        FROM [#tempphacdobenhnhandetail] [T]
        WHERE [T].[IDPhacDoBenhNhan] <> @PhacDoDangChiDinh;

        --DECLARE @TenNhomBenh NVARCHAR(500) = N'';
        --SELECT @TenNhomBenh += [TenNhomBenh] + N', '
        --FROM [QAHosGenericDB]..[L_NhomBenhVaccineDetail] AS [n] WITH (NOLOCK)
        --    INNER JOIN [L_NhomBenhVaccine] AS [lnbv] WITH (NOLOCK)
        --        ON [n].[NhomBenhID] = [lnbv].[ID]
        --WHERE EXISTS
        --(
        --    SELECT 1
        --    FROM [#tempphacdobenhnhandetail] [t] WITH (NOLOCK)
        --    WHERE [t].[MaChung] = [n].[MaChung]
        --          AND [IDPhacDoBenhNhan] <> @PhacDoDangChiDinh
        --)
        --      AND EXISTS
        --(
        --    SELECT 1
        --    FROM [#tempnhombenh] [nb] WITH (NOLOCK)
        --    WHERE [n].[NhomBenhID] = [nb].[NhomBenhID]
        --);

        SELECT N'Bệnh ' + [T].[TenNhomBenh] + N' đã được tiêm bởi vaccine ' + [P].[HospitalName] + N' vào ngày '
               + FORMAT([T].[CompleteOn], 'dd/MM/yyyy', 'vi-VN')
               + N'. Bạn có muốn cập nhật lại lịch tiêm cho vaccine này không ?' [ErrMsg],
               1 [Errcode]
        FROM [#tempphacdobenhnhandetail] [T],
             [QAHosGenericDB]..[L_Product] [P] WITH (NOLOCK)
        WHERE [T].[MaChung] = [P].[MaChung]
              AND [P].[FacID] = @FacID
              AND ISNULL([T].[TenNhomBenh], N'') <> N''
        ORDER BY [T].[CompleteOn] DESC;

        DROP TABLE IF EXISTS [#tempnhombenh],
                             [#tempphacdobenhnhandetail],
                             [#tempPhacDoBenhNhan1];

    END;
    ELSE
    BEGIN
        SELECT 0 [Errcode];
    END;



END;