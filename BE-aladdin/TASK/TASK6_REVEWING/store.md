USE [QAHosGenericDB]
GO
/****** Object:  StoredProcedure [dbo].[ws_CN_ClinicalSessions_UpdatePaid]    Script Date: 8/13/2025 5:06:18 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER	PROCEDURE [dbo].[ws_CN_ClinicalSessions_UpdatePaid]
(
	@SessionID VARCHAR(MAX), @FacID VARCHAR(10), @ClinicalSessionID UNIQUEIDENTIFIER, @IsChenhLech BIT = 0, @IsPaid BIT, @IsPaidChenhLech BIT = 0,
	@IsNgoaiGio BIT = 0
)
AS
SET NOCOUNT ON

DECLARE @UserID UNIQUEIDENTIFIER

SELECT @UserID = UserID FROM [Security]..[Sessions] WITH (NOLOCK) WHERE		[SessionID] = @SessionID

-- check if user authenticated
IF @UserID IS NULL RETURN

DECLARE @Original_IsPaid BIT
DECLARE @Original_IsPaidChenhLech BIT
DECLARE @Original_DoiTuongTinhTienID INT
DECLARE @TienChenhLech MONEY
DECLARE @exists INT
DECLARE @changed INT
/*
	  [Y] : Có thu ngoài giờ; [N] : Không thu ngoài giờ
	  */
DECLARE @SettingCoChenhLechNgoaiGio VARCHAR(2) = (	SELECT	Value
														FROM	Application..Settings WITH (NOLOCK)
													WHERE --Category = 'PatientInfo' AND Name = 'CoChenhLechNgoaiGio'
														ID = 15
														AND FacID = @FacID)
DECLARE @SettingGetPriceMethod VARCHAR(2) = (SELECT		Value
												FROM	Application..Settings WITH (NOLOCK)
												WHERE --Category = 'Billing' AND Name = 'GetPriceMethod'
													ID = 338
													AND FacID = @FacID)

SET @changed = 0
SET @exists = 0

SELECT	@Original_IsPaid = [IsPaid], @Original_IsPaidChenhLech = ISNULL(IsPaidChenhLech, 0), @Original_DoiTuongTinhTienID = DoiTuongTinhTienID, --1.0.2.1
		@TienChenhLech = ISNULL(TienChenhLech, 0),																								--1.0.6.1
		@exists = 1
FROM	CN_ClinicalSessions WITH (NOLOCK)
WHERE	ClinicalSessionID = @ClinicalSessionID

----1.0.4.1
--   IF @IsChenhLech = 1 
--      SET @IsPaid = @Original_IsPaid
--   ELSE 
--      SET @IsPaidChenhLech = @Original_IsPaidChenhLech

-- TH thu chệnh lệch thì gán value cho @IsPaidChenhLech = 1 --1.0.8.1
IF @IsChenhLech = 1 SET @IsPaidChenhLech = 1

-- Nếu là ca hành chính thì gán = 1 --1.0.5.1,1.0.11.3
--IF @IsNgoaiGio = 0
--    AND @IsChenhLech = 0
--    AND @IsPaidChenhLech = 0
--     --AND @TienChenhLech = 0 --1.0.7.1
--    OR @Original_DoiTuongTinhTienID IN (0, 31, 41, 51, 61)  --1.0.2.1
--    SET @IsPaidChenhLech = 1
IF @exists = 1
BEGIN
	--SELECT @IsPaidChenhLech
	IF @IsPaidChenhLech = 1
	BEGIN
		SET @IsPaid = CASE WHEN @Original_DoiTuongTinhTienID NOT IN (1, 2, 3, 4, 5) THEN 1
					ELSE @Original_IsPaid
					END --1.0.12.1

		UPDATE	[CN_ClinicalSessions]
			SET IsPaid = @IsPaid,	--1.0.12.1
				[IsPaidChenhLech] = @IsPaidChenhLech,
				[Note] = 'Upd IsPaid=' + CAST(ISNULL(@IsPaid, '') AS VARCHAR(10)) + ',IsPaidChenhLech=' + CAST(ISNULL(@IsPaidChenhLech, '') AS VARCHAR(10))
						+ ' by ws_CN_ClinicalSessions_UpdatePaid', [ModifiedOn] = GETDATE(), [ModifiedBy] = @UserID
		WHERE	ClinicalSessionID = @ClinicalSessionID

		UPDATE QAHosGenericDB..CN_ClinicalSessions_ChiDinh_TrongNgay
		SET IsPaid=@IsPaid
		WHERE ClinicalSessionID = @ClinicalSessionID

	END
	ELSE
	BEGIN
		IF	@Original_IsPaidChenhLech = 0
			SET @IsPaidChenhLech = CASE WHEN @TienChenhLech <> 0 THEN 0 ELSE 1 END --1.0.13.1
		ELSE SET @IsPaidChenhLech = @Original_IsPaidChenhLech

		UPDATE	[CN_ClinicalSessions]
			SET [IsPaid] = @IsPaid, [IsPaidChenhLech] = @IsPaidChenhLech,
				[Note] = 'Upd IsPaid=' + CAST(ISNULL(@IsPaid, '') AS VARCHAR(10)) + ',IsPaidChenhLech=' + CAST(ISNULL(@IsPaidChenhLech, '') AS VARCHAR(10))
						+ ' by ws_CN_ClinicalSessions_UpdatePaid', [ModifiedOn] = GETDATE(), [ModifiedBy] = @UserID
		WHERE	ClinicalSessionID = @ClinicalSessionID
		UPDATE QAHosGenericDB..CN_ClinicalSessions_ChiDinh_TrongNgay
		SET IsPaid=@IsPaid
		WHERE ClinicalSessionID = @ClinicalSessionID
	END

	EXEC	History..sp_CN_ClinicalSessions_LogUpdate @ClinicalSessionID = @ClinicalSessionID, -- uniqueidentifier
												@FacID = @FacID,							-- varchar(10)
												@UserID = @UserID							-- uniqueidentifier

	DECLARE @FacAdmissionID UNIQUEIDENTIFIER = (SELECT		FacAdmissionID
													FROM	dbo.CN_ClinicalSessions WITH (NOLOCK)
													WHERE	ClinicalSessionID = @ClinicalSessionID)

	-- Ktra có bệnh án và được điều trị trong phòng khám của Khoa nội trú --1.0.9.1
	IF EXISTS (SELECT 1 FROM dbo.CN_CaseChronicDiseaseDetail WITH (NOLOCK) WHERE FacAdmissionID = @FacAdmissionID)
	BEGIN
		SELECT	DeptID, FacID
		INTO	#Phys
		FROM	dbo.CN_PhysicianAdmissions CPA WITH (NOLOCK)
		WHERE	FacAdmissionID = @FacAdmissionID

		IF EXISTS (SELECT		1
						FROM	#Phys ph WITH (NOLOCK)
								INNER JOIN dbo.L_Department d WITH (NOLOCK) ON ph.DeptID = d.DeptID
																			AND ph.FacID = d.FacID
						WHERE	d.DeptTypeID = 3)
		BEGIN
			UPDATE	dbo.CN_RXDetail
				SET [IsPaid] = @IsPaid, [ModifiedOn] = GETDATE(), [ModifiedBy] = @UserID
			WHERE	ClinicalSessionID = @ClinicalSessionID

			EXEC History..sp_CN_RXDetail_LogUpdate @ClinicalSessionID = @ClinicalSessionID, -- uniqueidentifier
												@UserID = @UserID							-- uniqueidentifier
		END

		DROP	TABLE #Phys
	END

	EXEC	History..sp_CN_ClinicalSessions_LogUpdate @ClinicalSessionID = @ClinicalSessionID, -- uniqueidentifier
												@FacID = @FacID,							-- varchar(10)
												@UserID = @UserID							-- uniqueidentifier

	SELECT 'Updated CN_ClinicalSession' AS Result
END
ELSE
BEGIN
	--1.0.3.1       
	INSERT INTO FW..Error
		(LocalIP, [User], spName, spParameterQuery, Error, StackTrade, StackMessage, StackSource, CreatedOn, CreatedBy, ModifiedOn, ModifiedBy)
	VALUES
		('',																																			-- LocalIP - varchar(50)
		@UserID,																																		-- User - uniqueidentifier
		'ws_CN_ClinicalSessions_UpdatePaid',																											-- spName - varchar(1000)
		@ClinicalSessionID,																																-- spParameterQuery - varchar(max)
		'Khong update ClinicalSessionID, @IsPaid = ' + CAST(@IsPaid AS VARCHAR(10)) + ', @IsPaidChenhLech = ' + CAST(@IsPaidChenhLech AS VARCHAR(10)),	-- Error - varchar(max)
		'',																																				-- StackTrade - varchar(max)
		'',																																				-- StackMessage - varchar(max)
		'',																																				-- StackSource - varchar(max)
		GETDATE(),																																		-- CreatedOn - datetime
		@UserID,																																		-- CreatedBy - uniqueidentifier
		GETDATE(),																																		-- ModifiedOn - datetime
		@UserID																																			-- ModifiedBy - uniqueidentifier
		)
END

--EXEC History..sp_CN_ClinicalSessions_LogUpdate @ClinicalSessionID = @ClinicalSessionID, -- uniqueidentifier
--    @FacID = @FacID, -- varchar(10)
--    @UserID = @UserID -- uniqueidentifier