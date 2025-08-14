USE [QAHosGenericDB]
GO
/****** Object:  StoredProcedure [dbo].[ws_Vaccine_ThongBaoKhongchan]    Script Date: 8/14/2025 3:30:48 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Hieunt
-- Create date: 2019-08-15 13:43
-- Description:	thông báo không chặn
-- Version: 1.0.0.0
-- =============================================


/*
Version 1.0.1.0 20241014 quocpa  131048-( 0 - Undefined)-Báo cáo>Xem báo cáo : Đối với trường hợp đặt trước thanh toán 1 phần đa phương thức nếu chưa thanh toán đủ thì lấy lên bill con ở báo cáo thu ngân không chi tiết (tách từ ticket 131025 )
Version 1.0.2.0 20241125 quocpa  132000-( 4 - Hot fix)-Thanh Toán>Thanh Toán Vaccine : Xử lý dữ liệu cũ đối với trường hợp KH thanh toán tam ứng đủ để click tiêm
*/


ALTER   PROCEDURE [dbo].[ws_Vaccine_ThongBaoKhongchan] 
	@SessionID VARCHAR(MAX)  , 
	@ClinicalSessionID UNIQUEIDENTIFIER
AS
-------------------Debug-----------------------------------
--DECLARE 	@SessionID VARCHAR(MAX)  , 
--	@ClinicalSessionID UNIQUEIDENTIFIER
--	SELECT TOP 1 @SessionID = SessionID FROM Security..Sessions  WITH(NOLOCK) ORDER BY CreatedOn DESC
--	SELECT @ClinicalSessionID ='18FE059E-AB01-11EF-A87F-40490F86DD6C'
-----------------------------------------------------------
BEGIN
	SET NOCOUNT ON;

	---1 cảnh báo thanh toán với mũi tiêm đã thanh toán 1 nữa
	IF EXISTS (SELECT 1 FROM CN_ClinicalSessions AS ccs WITH (NOLOCK)
	WHERE ClinicalSessionID=@ClinicalSessionID AND IsDatTruoc =1)
	BEGIN
	   IF  EXISTS
            (
                SELECT 1
                FROM QAHosGenericDB..BIL_InvoiceDetail_TempForHinhThucThanhToan AS bidtfhttt WITH (NOLOCK)
					JOIN QAHosGenericDB..BIL_Invoice_TempForHinhThucThanhToan bifhttt WITH(NOLOCK)
					ON bifhttt.InvoiceID = bidtfhttt.InvoiceID
                    LEFT JOIN BIL_InvoiceDetail AS bid WITH (NOLOCK)
                        ON bid.InvoiceDetailID = bidtfhttt.InvoiceDetailID
                WHERE bidtfhttt.ClinicalSessionID = @ClinicalSessionID
                      AND bid.ClinicalSessionID IS NULL
					  AND bifhttt.IsRefund = 0
					  AND EXISTS (SELECT 1 FROM QAHosGenericDB..BIL_Invoice_PTTT_Link l WITH(NOLOCK) WHERE l.InvoiceID = bidtfhttt.InvoiceID)
            )
			BEGIN
				
				DECLARE @InvoiceID_Group UNIQUEIDENTIFIER
				DECLARE @PatientID UNIQUEIDENTIFIER
				DECLARE @DonGia MONEY 
				DECLARE @FacID VARCHAR(10)
				SELECT @DonGia = (DonGia - SoTienGiam) FROM QAHosGenericDB..BIL_InvoiceDetail_TempForHinhThucThanhToan WITH(NOLOCK) WHERE ClinicalSessionID = @ClinicalSessionID
				SELECT @InvoiceID_Group = InvoiceID_Group   FROM QAHosGenericDB..CN_Data_Log_Vaccine_Payment WITH (NOLOCK) WHERE ClinicalSessionID=@ClinicalSessionID


				IF(@InvoiceID_Group IS NULL)
				BEGIN
				     SELECT @InvoiceID_Group = bifhttt.InvoiceID, @PatientID=bifhttt.PatientID
                FROM QAHosGenericDB..BIL_InvoiceDetail_TempForHinhThucThanhToan AS bidtfhttt WITH (NOLOCK)
					JOIN QAHosGenericDB..BIL_Invoice_TempForHinhThucThanhToan bifhttt WITH(NOLOCK)
					ON bifhttt.InvoiceID = bidtfhttt.InvoiceID
                    LEFT JOIN BIL_InvoiceDetail AS bid WITH (NOLOCK)
                        ON bid.InvoiceDetailID = bidtfhttt.InvoiceDetailID
                WHERE bidtfhttt.ClinicalSessionID = @ClinicalSessionID
                      AND bid.ClinicalSessionID IS NULL
					  AND bifhttt.IsRefund = 0
					  AND EXISTS (SELECT 1 FROM QAHosGenericDB..BIL_Invoice_PTTT_Link l WITH(NOLOCK) WHERE l.InvoiceID = bidtfhttt.InvoiceID)
					EXEC QAHosGenericDB..ws_CN_Data_Log_Vaccine_Payment_Save @SessionID = @SessionID,         -- varchar(max)
					                                                         @FacID = @FacID,             -- varchar(10)
					                                                         @InvoiceID_Group = @InvoiceID_Group, -- uniqueidentifier
					                                                         @PatientID = @PatientID,       -- uniqueidentifier
					                                                         @Payment = 0,         -- money
					                                                         @Total = 0,           -- money
					                                                         @IsCompleted = 0,     -- bit
					                                                         @LoaiHinhSP = 1          -- int
	
					DROP TABLE IF EXISTS #tempPayment
				END

				DECLARE @ConLai MONEY
				SELECT  @ConLai = MIN(ConLai) FROM QAHosGenericDB..CN_Data_Log_Vaccine_Perform WITH(NOLOCK)  WHERE InvoiceID_Group= @InvoiceID_Group
				
				



				IF(@ConLai IS NULL)
				SELECT @ConLai = AdvanceAmount FROM QAHosGenericDB..CN_Data_Log_Vaccine_Payment WITH(NOLOCK) WHERE ClinicalSessionID=@ClinicalSessionID
					IF(@DonGia > @ConLai)
				BEGIN
					SELECT N'Vui lòng đi thanh toán đủ tiền mũi tiêm' Mess
				END			    
			END
 
	END
	   

END