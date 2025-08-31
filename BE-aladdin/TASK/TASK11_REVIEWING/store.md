USE [QAHosGenericDB]
GO
/****** Object:  StoredProcedure [dbo].[ws_Vaccine_DanhSachChoTiem_DangTiem_Save]    Script Date: 8/14/2025 3:24:12 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*
Version 1.0.0.0: 20210609 16:38 Thonv 102961 Lưu trạng thái của bệnh nhân là đã vào phòng tiêm
Version: 1.0.1.0 2022-09-07 hieunt
*/
ALTER PROCEDURE [dbo].[ws_Vaccine_DanhSachChoTiem_DangTiem_Save]
(
	@SessionID varchar(100) = '',
	@PatientID uniqueidentifier,
	@FacID VARCHAR(10),
	@RoomID INT,
	@UserID UNIQUEIDENTIFIER = NULL
)
As
Set Nocount ON

--temp
--RETURN

DECLARE @NgayAsInt INT = FORMAT(GETDATE(), 'yyyyMMdd', 'en-US')

--IF NOT EXISTS (
--SELECT 1 FROM QAHosGenericDB..Vaccine_DanhSachChoTiem_DangTiem ds WITH (NOLOCK) 
--JOIN QAHosGenericDB..Vaccine_DanhSachChoTiem_DaTiem dg WITH (NOLOCK) ON dg.Seq = ds.Seq
--WHERE PatientID = @PatientID AND RoomID = @RoomID AND FacID = @FacID AND CreatedOnAsInt = @NgayAsInt
--)
DECLARE @ID_ChoTiem INT

SELECT @ID_ChoTiem=ID FROM dbo.Vaccine_DanhSachChoTiem WITH (NOLOCK)
WHERE PatientID=@PatientID AND RoomID=@RoomID AND FacID_CheckSum=CHECKSUM(@FacID) AND NgayAsInt=@NgayAsInt
ORDER BY ID
BEGIN
    insert [dbo].[Vaccine_DanhSachChoTiem_DangTiem]
    (
        [PatientID],
        [RoomID],
        [FacID],
        [CreatedOnAsInt],
        [CreatedOn],
        [CreatedBy],
		ID_DangTiem
    )
	select  @PatientID, @RoomID, @FacID,  FORMAT(GETDATE(), 'yyyyMMdd', 'en-US'), getdate(), @UserID,@ID_ChoTiem
END

select 'Ok' as Result