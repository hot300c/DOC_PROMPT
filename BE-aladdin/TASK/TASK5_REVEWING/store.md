USE [QAHosGenericDB]
GO
/**\*\*** Object: StoredProcedure [dbo].[ws_Vaccine_KiemTraTuongTac] Script Date: 8/13/2025 10:08:09 AM **\*\***/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- =============================================
ALTER PROCEDURE [dbo].[ws_Vaccine_KiemTraTuongTac]
-- Add the parameters for the stored procedure here
@SessionID VARCHAR(MAX) ,
@MaChung VARCHAR(100) ,
@PatientID UNIQUEIDENTIFIER ,
@FacID VARCHAR(10),
@Ngay DATETIME=NULL
AS

BEGIN
SET NOCOUNT ON;

    SELECT B.MaChung,
           C.CompleteOn
    INTO #MACHUNGTONG
    FROM QAHosGenericDB..Vaccine_PhacDoBenhNhan_Detail C WITH (NOLOCK)
        JOIN QAHosGenericDB..Vaccine_PhacDoBenhNhan A WITH (NOLOCK)
            ON C.IDPhacDoBenhNhan = A.IDPhacDoBenhNhan
        JOIN QAHosGenericDB..L_Vaccine_Phacdo B WITH (NOLOCK)
            ON A.IDPhacDo = B.IDPhacDo
    WHERE A.PatientID = @PatientID
          AND C.CompleteOn IS NOT NULL;

    INSERT INTO #MACHUNGTONG
    (
        MaChung,
        CompleteOn
    )
    SELECT B.MaChung,
           C.UserCreatedOn AS CompleteOn
    FROM QAHosGenericDB..Vaccine_PhacDoBenhNhan_Detail C WITH (NOLOCK)
        JOIN QAHosGenericDB..Vaccine_PhacDoBenhNhan A WITH (NOLOCK)
            ON C.IDPhacDoBenhNhan = A.IDPhacDoBenhNhan
        JOIN QAHosGenericDB..L_Vaccine_Phacdo B WITH (NOLOCK)
            ON A.IDPhacDo = B.IDPhacDo
    WHERE A.PatientID = @PatientID
          AND C.IsChiDinh = 1;

    SELECT MAX(CompleteOn) NGAYTIEM,
           MaChung
    INTO #NGAYTIEMSAUCUNG
    FROM #MACHUNGTONG
    GROUP BY MaChung;

    SELECT a.MaChung,
           MaChungTuongTac,
           FacID,
           SoNgay,
           IsHienThiPhieuChiDinh,
           Chan,
           CanhBao,
           TuNgayThu TuNgayThu1,
           DenNgayThu DenNgayThu1,
           GETDATE() - TuNgayThu TuNgayThu,
           GETDATE() - DenNgayThu DenNgayThu,
           b.NGAYTIEM,
                                   --, CASE WHEN CAST(b.NGAYTIEM AS DATE) BETWEEN DATEADD(DAY,-DenNgayThu, GETDATE())  AND DATEADD(DAY,-TuNgayThu, GETDATE()) THEN 1 ELSE 0 END  result,
           CASE
               WHEN
               (
                   CAST(b.NGAYTIEM AS DATE) >= CAST(GETDATE() - DenNgayThu AS DATE)
                   AND CAST(b.NGAYTIEM AS DATE) <= CAST(GETDATE() - TuNgayThu AS DATE)
               ) THEN
                   1
               ELSE
                   0
           END result,
           CAST('' AS NVARCHAR(1000)) Msg,
           CAST(0 AS BIT) IsError,
           CAST('' AS NVARCHAR(1000)) HospitalNameDaChiDinh,
           CAST('' AS NVARCHAR(1000)) HospitalNameChuanBiChiDinh,
           CAST(0 AS INT) [Return] ---1.0.1.0
    INTO #RESULT
    FROM QAHosGenericDB..L_Vaccine_TuongTacVaccine a WITH (NOLOCK)
        JOIN #NGAYTIEMSAUCUNG b
            ON a.MaChungTuongTac = b.MaChung
    WHERE a.MaChung = @MaChung
          AND MaChungTuongTac IN
              (
                  SELECT MaChung FROM #MACHUNGTONG
              );

    UPDATE #RESULT
    SET HospitalNameDaChiDinh = p.HospitalName
    FROM #RESULT t
        INNER JOIN dbo.L_Product p WITH (NOLOCK)
            ON t.MaChung = p.MaChung
               AND p.FacID = @FacID;

    UPDATE #RESULT
    SET HospitalNameChuanBiChiDinh = p.HospitalName
    FROM #RESULT t
        INNER JOIN dbo.L_Product p WITH (NOLOCK)
            ON t.MaChungTuongTac = p.MaChung
               AND p.FacID = @FacID;


    IF EXISTS (SELECT 1 FROM #RESULT WHERE result = 1)
    BEGIN
        UPDATE #RESULT
        SET Msg = CHAR(10) + HospitalNameDaChiDinh + N' tương tác với ' + HospitalNameChuanBiChiDinh
                  + N' Bạn có muốn tiếp tục!',
            IsError = 1
        FROM #RESULT t
        WHERE result = 1
              AND t.CanhBao = 1;

        UPDATE #RESULT
        SET [Return] = 1,
            Msg = N'Không thể chỉ định. ' + CHAR(10) + '' + HospitalNameDaChiDinh + N' tương tác với '
                  + HospitalNameChuanBiChiDinh,
            IsError = 1
        FROM #RESULT t
        WHERE result = 1
              AND t.Chan = 1;
    END;

    -----1.0.1.0 end
    IF EXISTS (SELECT 1 FROM #RESULT WHERE IsError = 1)
    BEGIN
        IF EXISTS (SELECT 1 FROM #RESULT WHERE IsError = 1 AND [Return] = 1)
        BEGIN
            SELECT Msg,
                   IsError,
                   [Return] --, ---1.0.1.0
            FROM #RESULT
            WHERE IsError = 1 AND [Return] = 1;
        END;
    	ELSE
    	BEGIN
    	   SELECT Msg,
                   IsError,
                   [Return] --, ---1.0.1.0
            FROM #RESULT
            WHERE IsError = 1 AND [Return] = 0;
    	END
    END;
    ELSE
    BEGIN
        SELECT 0 IsError,
               0 [Return];
    END;

    DROP TABLE #RESULT;
    DROP TABLE #MACHUNGTONG;
    DROP TABLE #NGAYTIEMSAUCUNG;

END;
