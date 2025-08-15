USE [QAHosGenericDB]
GO
/****** Object:  StoredProcedure [dbo].[ws_Vaccine_KiemTraTrungNhomBenhDangMo]    Script Date: 8/14/2025 3:26:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Quocpa
-- Create date: 2024-01-23
-- Description:	Kiểm tra phác đồ nhóm bệnh trùng đang mở
-- =============================================

/*
Version 1.0.0.0 20240123 quocpa 123620-( 0 - Undefined)-Ngoại Trú>Khám Bệnh :[VNVC Offline Đà Nẵng] : Nhóm bệnh mở cả 2, tiêm ngoài gỡ tiêm ngoài mất nhóm bệnh đã tiêm thực tế
*/


ALTER PROCEDURE [dbo].[ws_Vaccine_KiemTraTrungNhomBenhDangMo] 
	@SessionID VARCHAR(max),
	@MaChung VARCHAR(100),
	@PatientID UNIQUEIDENTIFIER
AS
----------------------------debug----------------------------
--DECLARE @SessionID VARCHAR(max),
--	@MaChung VARCHAR(100),
--	@PatientID UNIQUEIDENTIFIER
--SELECT @PatientID='1f74bd2f-299a-40f8-a603-00427bef0123', @MaChung='1000014'
-------------------------------------------------------------
BEGIN
	
	DECLARE @SoPhacDo INT = 0
	SELECT @SoPhacDo = MAX(SLPD) FROM (SELECT pd.NhomBenhID, Count(pd.NhomBenhID) SLPD FROM QAHosGenericDB..Vaccine_PhacDoBenhNhan_NhomBenh pd WITH(NOLOCK)
	JOIN QAHosGenericDB..L_NhomBenhVaccineDetail lb WITH(NOLOCK)
	ON lb.NhomBenhID= pd.NhomBenhID
	WHERE PatientID = @PatientID  AND lb.MaChung=@MaChung AND pd.NgayDong IS NULL
	Group By pd.NhomBenhID
	Having count(pd.NhomBenhID)>1) as p

	SELECT ISNULL(@SoPhacDo,0)

END