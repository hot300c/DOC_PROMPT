-- =============================================
-- Author: Hieunt
-- Create date: 2017-12-08 9:57
-- Description: Kiểm tra tất cả phác đồ của bn, cái nào đã hoàn tất mũi mà chưa đóng thì đóng lại, nhóm bệnh và vaccine
-- Version: 1.0.0.0
-- =============================================
CREATE PROCEDURE [dbo].[ws_Vaccine_KiemTraDongPhacDo]
@SessionID VARCHAR(MAX) ,
@PatientID UNIQUEIDENTIFIER ,
@IPUser VARCHAR(255) ,
@MacAddressUser VARCHAR(255)
AS
BEGIN
SET NOCOUNT ON;
DECLARE @UserID UNIQUEIDENTIFIER

        SELECT  @UserID = UserID
        FROM    [Security]..[Sessions] WITH ( NOLOCK )
        WHERE   [SessionID] = @SessionID

        IF @UserID IS NULL
            RETURN

        SELECT  IDPhacDoBenhNhan ,
                ROW_NUMBER() OVER ( ORDER BY IDPhacDoBenhNhan ) STT
        INTO    #tempPhacDoVaccine
        FROM    dbo.Vaccine_PhacDoBenhNhan WITH ( NOLOCK )
        WHERE   PatientID = @PatientID
                AND NgayDong IS NULL

    SELECT b.IDPhacDoBenhNhan INTO #tempPhacdobenhNhanConMuiTiem FROM #tempPhacDoVaccine a WITH (NOLOCK)
    INNER JOIN Vaccine_PhacDoBenhNhan_Detail b WITH (NOLOCK)
    ON a.IDPhacDoBenhNhan=b.IDPhacDoBenhNhan
    WHERE b.CompleteOn IS NULL
    AND b.PatientID=@PatientID

      UPDATE  dbo.Vaccine_PhacDoBenhNhan
                        SET     NgayDong = GETDATE() ,
                                NguoiDong = @UserID ,
                                NgayDongAsInt = FORMAT(GETDATE(), 'yyyyMMdd',
                                                       'en-US') ,
                                ModifiedOn = GETDATE() ,
                                ModifiedBy = @UserID ,
                                IPUser = @IPUser ,
                                MacAddressUser = @MacAddressUser
    							FROM #tempPhacDoVaccine t1 INNER JOIN Vaccine_PhacDoBenhNhan b WITH (NOLOCK)
    							ON b.IDPhacDoBenhNhan = t1.IDPhacDoBenhNhan
                        WHERE   NOT EXISTS(SELECT * FROM #tempPhacdobenhNhanConMuiTiem t WHERE t.IDPhacDoBenhNhan=t1.IDPhacDoBenhNhan)


        --DECLARE @i INT= 1
        --DECLARE @C INT = ( SELECT   COUNT(1)
        --                   FROM     #tempPhacDoVaccine
        --                 )
        --WHILE @i <= @C
        --    BEGIN
        --        DECLARE @IDPhacDoBenhNhan UNIQUEIDENTIFIER

        --        SELECT  @IDPhacDoBenhNhan = IDPhacDoBenhNhan
        --        FROM    #tempPhacDoVaccine
        --        WHERE   STT = @i

        --        IF NOT EXISTS ( SELECT  1
        --                        FROM    dbo.Vaccine_PhacDoBenhNhan_Detail WITH ( NOLOCK )
        --                        WHERE   IDPhacDoBenhNhan = @IDPhacDoBenhNhan
        --                                AND CompleteOn IS NULL )
        --            BEGIN
        --                UPDATE  dbo.Vaccine_PhacDoBenhNhan
        --                SET     NgayDong = GETDATE() ,
        --                        NguoiDong = @UserID ,
        --                        NgayDongAsInt = FORMAT(GETDATE(), 'yyyyMMdd',
        --                                               'en-US') ,
        --                        ModifiedOn = GETDATE() ,
        --                        ModifiedBy = @UserID ,
        --                        IPUser = @IPUser ,
        --                        MacAddressUser = @MacAddressUser
        --                WHERE   IDPhacDoBenhNhan = @IDPhacDoBenhNhan

        --                EXEC History..sp_Vaccine_PhacDoBenhNhan_LogUpdate @UserID = @UserID, -- uniqueidentifier
        --                    @IDPhacDoBenhNhan = @IDPhacDoBenhNhan -- uniqueidentifier
        --            END
        --        SET @i = @i + 1
        --    END


        SELECT  IDPhacDoBenhNhan_NhomBenh ,
                ROW_NUMBER() OVER ( ORDER BY IDPhacDoBenhNhan ) STT
        INTO    #tempPhacDoNhomBenh
        FROM    dbo.Vaccine_PhacDoBenhNhan_NhomBenh WITH ( NOLOCK )
        WHERE   PatientID = @PatientID
                AND NgayDong IS NULL

        DECLARE @j INT= 1
        DECLARE @k INT = ( SELECT   COUNT(1)
                           FROM     #tempPhacDoNhomBenh
                         )

        WHILE @j <= @k
            BEGIN
                DECLARE @IDPhacDoBenhNhan_NhomBenh UNIQUEIDENTIFIER

                SELECT  @IDPhacDoBenhNhan_NhomBenh = IDPhacDoBenhNhan_NhomBenh
                FROM    #tempPhacDoNhomBenh
                WHERE   STT = @j

                IF NOT EXISTS ( SELECT  1
                                FROM    dbo.Vaccine_PhacDoBenhNhan_NhomBenh_Detail
                                        WITH ( NOLOCK )
                                WHERE   IDPhacDoBenhNhan_NhomBenh = @IDPhacDoBenhNhan_NhomBenh
                                        AND CompleteOn IS NULL
                                        AND TiemNgoaiOn IS NULL )
                    BEGIN
                        UPDATE  dbo.Vaccine_PhacDoBenhNhan_NhomBenh
                        SET     NgayDong = GETDATE() ,
                                NguoiDong = @UserID ,
                                NgayDongAsInt = FORMAT(GETDATE(), 'yyyyMMdd',
                                                       'en-US') ,
                                ModifiedOn = GETDATE() ,
                                ModifiedBy = @UserID ,
                                IPUser = @IPUser ,
                                MacAddressUser = @MacAddressUser
                        WHERE   IDPhacDoBenhNhan_NhomBenh = @IDPhacDoBenhNhan_NhomBenh

                        EXEC History..sp_Vaccine_PhacDoBenhNhan_NhomBenh_LogUpdate @IDPhacDoBenhNhan_NhomBenh = @IDPhacDoBenhNhan_NhomBenh, -- uniqueidentifier
                            @UserID = @UserID -- uniqueidentifier

                    END
                SET @j = @j + 1
            END
        DROP TABLE #tempPhacDoVaccine,#tempPhacDoNhomBenh,#tempPhacdobenhNhanConMuiTiem
    END
