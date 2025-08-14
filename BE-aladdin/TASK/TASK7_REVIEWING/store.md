USE [QAHosGenericDB]
GO
/****** Object:  StoredProcedure [dbo].[ws_INV_ProductTemp_Proccessing_Vaccine_V2]    Script Date: 8/14/2025 11:24:32 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[ws_INV_ProductTemp_Proccessing_Vaccine_V2]
(
 @SessionID VARCHAR(MAX),
 @FacID VARCHAR(10),
 @RoomID INT = 0,
 @MaChung VARCHAR(50) = '',
 @Qty DECIMAL(18, 5),
 @IsHuyHoan BIT = 0,
 @PatientID UNIQUEIDENTIFIER = NULL,
 @ClinicalSessionID UNIQUEIDENTIFIER = NULL,
 @IsDebug BIT = 0
    
)
AS 
SET NOCOUNT ON
----------------------------------------------------------------------
-- 				 Debug
----------------------------------------------------------------------

--DECLARE @SessionID VARCHAR(MAX) = (SELECT TOP 1
--                                          SessionID
--                                   FROM   Security..Sessions WITH (NOLOCK)
--                                   ORDER BY CreatedOn DESC)
--DECLARE @FacID VARCHAR(10) = '8.4'
--DECLARE @RoomID INT = 20
--DECLARE @Qty DECIMAL(18, 2) = '1'
--DECLARE @MaChung VARCHAR(50)= '13'
--DECLARE @IsHuyHoan BIT = 0
--DECLARE @PatientID UNIQUEIDENTIFIER = 'a4c23420-7e9a-4c92-895a-a2f596dd26d8'
--DECLARE @ClinicalSessionID UNIQUEIDENTIFIER = 'a7c52826-1a63-e911-93f4-ac1f6b686413'
--DECLARE @IsDebug BIT = 1
----------------------------------------------------------------------

DECLARE @UserID UNIQUEIDENTIFIER
DECLARE @IsDisableOldQdenga10 VARCHAR(10) = [dbo].[fn_SettingValue_GetByName](@FacID, 'Vaccine', 'IsDisableOldQdenga10');

SELECT   @UserID = UserID
FROM     [Security]..[Sessions] WITH (NOLOCK)
WHERE    [SessionID] = @SessionID

-- check if user authenticated
IF @UserID IS NULL 
   RETURN

DECLARE @exists INT = 0
DECLARE @changed INT = 0
DECLARE @TongKhoTam DECIMAL(18, 5)
DECLARE @StockID INT

IF @IsDisableOldQdenga10 = 'Y' AND @MaChung = '1000047'
BEGIN
   SET @MaChung = '1000043'
END

DECLARE @Vaccine_MaChung_CheckSum INT = CHECKSUM(@MaChung)
    
IF ISNULL(@MaChung, '') <> '' 
BEGIN
	-- 1.0.5.1
   DECLARE @Setting_SoNgayGiuBookVaccine INT = dbo.fn_SettingValue_GetByName(@FacID, 'Duoc', 'SoNgayGiuBookVaccine')

   DECLARE @Setting_HasValidateQuantityStock VARCHAR(1) = dbo.fn_SettingValue_GetByName(@FacID, 'System',
                                                                                        'HasValidateQuantityStock') --1.0.7.3

   
   --1.0.5.1
   DECLARE @PhacDoID INT,
      @PhacDoDetailID INT,
      @NgayHenTiem DATE,
      @IsDatTruoc BIT

   SELECT   @PhacDoID = PhacDo_ID, @PhacDoDetailID = PhacDo_Detail_ID, @RoomID = RoomID,
            @IsDatTruoc = ISNULL(IsDatTruoc, 0)
   FROM     dbo.CN_ClinicalSessions CCS WITH (NOLOCK)
   WHERE    ClinicalSessionID = @ClinicalSessionID
			
   SELECT   @NgayHenTiem = CAST(NgayHenTiem AS DATE)
   FROM     dbo.Vaccine_PhacDoBenhNhan_Detail VPDBND WITH (NOLOCK)
   WHERE    PatientID = @PatientID
            AND IDPhacDo = @PhacDoID
            AND IDPhacDo_Detail = @PhacDoDetailID

   SELECT   *
   INTO     #L_InventoryStock_Table
   FROM     dbo.L_InventoryStock LIS WITH (NOLOCK)
   WHERE    FacID = @FacID
            AND StockType = 2 --1: Kho tổng, 2: Kho trung tâm, 3: Kho phòng tiêm, 4 Kho tủ trực, 5 Kho biệt trữ
            AND ISNULL(IsVatTu, 0) = 0
            AND IsActive = 1

   SELECT   @StockID = StockID
   FROM     #L_InventoryStock_Table LIST	
-----------------------Nhân comment--------------- --1.0.6.1
  --SELECT @StockID
   SELECT   ISNULL(TempQty, 0) TempQty, ISNULL(Vaccine_MaChung, '') Vaccine_MaChung, StockID
   INTO     #INV_ProductTemp_Table
   FROM     dbo.INV_ProductTemp IPT WITH (NOLOCK)
   WHERE    --Vaccine_MaChung = @MaChung --1.0.4.1
            Vaccine_MaChung_CheckSum = @Vaccine_MaChung_CheckSum --1.0.4.1
            AND FacID = @FacID
            AND StockID = @StockID


	------- tính booking bằng bảng quy đổi---------------------------------
	DECLARE @LieuDung NVARCHAR(100)

	SELECT	@LieuDung = LieuDung
	FROM	L_Vaccine_Phacdo AS lvp WITH (NOLOCK)
	WHERE	IDPhacDo = @PhacDoID

	IF EXISTS (SELECT		1
					FROM	L_Vaccine_LieuDung_Used AS lvldu WITH (NOLOCK)
					WHERE	MaChung = @MaChung AND	UnitConverted > 0 AND	Name = @LieuDung AND ISNULL(lvldu.isUsed, 0) = 1)
	BEGIN
		SELECT	@Qty = UnitConverted
		FROM	L_Vaccine_LieuDung_Used WITH (NOLOCK)
		WHERE	MaChung = @MaChung AND	UnitConverted > 0 AND	Name = @LieuDung AND ISNULL(isUsed, 0) = 1
	END


	-----------------------------------------------------------------------------




   SET @TongKhoTam = ISNULL((SELECT SUM (TempQty) FROM #INV_ProductTemp_Table WHERE StockID = @StockID --1.0.3.1
                             ), 0)
--SELECT @TongKhoTam
   IF @Setting_HasValidateQuantityStock = 'N' --1.0.7.3      
      
   BEGIN
      PRINT 'Not validate qty of stock'
   END		
   ELSE 
   BEGIN
      IF @TongKhoTam <= 0
         AND @IsHuyHoan = 0
         AND @IsDatTruoc = 0 
      BEGIN
         RAISERROR(N'Tồn kho booking không đủ, không thể đặt Vaccine cho khách !!',16,1)
         RETURN
      END
   
      IF @TongKhoTam <= 0
         AND DATEDIFF(dd, GETDATE(), @NgayHenTiem) < @Setting_SoNgayGiuBookVaccine --1.0.5.1      
         AND @IsHuyHoan = 0 
      BEGIN
         DECLARE @Setting_SoNgayGiuBookVaccine_Text VARCHAR(9) = CAST(@Setting_SoNgayGiuBookVaccine AS VARCHAR(9))
         DECLARE @Error NVARCHAR(200) = N'Không cho phép đặt vaccine quá thời gian quy định.Thời gian cho phép đặt là dưới '
            + @Setting_SoNgayGiuBookVaccine_Text + ' ngày'
         RAISERROR(@Error,16,1)
         RETURN
      END
   END			 
     
   

   IF @TongKhoTam > 0
      AND DATEDIFF(dd, GETDATE(), @NgayHenTiem) <= @Setting_SoNgayGiuBookVaccine --1.0.5.1
   BEGIN
      IF @IsHuyHoan = 0 
      BEGIN 
         IF @IsDebug = 0 
         BEGIN
            UPDATE   p
            SET      TempQty = ISNULL(@TongKhoTam,0) - @Qty, ModifiedBy = @UserID, ModifiedOn = GETDATE()
            FROM     INV_ProductTemp p
            WHERE    p.FacID = @FacID AND p.ProductID = 0 AND p.Vaccine_MaChung = @MaChung
                     AND p.Vaccine_MaChung_CheckSum = @Vaccine_MaChung_CheckSum --1.0.4.1
                     AND p.StockID = @StockID

            DECLARE @Mess NVARCHAR(500) = N'Trừ kho tạm Vaccine - ws_INV_ProductTemp_Proccessing_Vaccine @StockID='
               + CAST(@StockID AS VARCHAR(9)) + ',@TongKhoTam=' + CAST(@TongKhoTam AS VARCHAR(50)) + ',@Qty='
               + CAST(@Qty AS VARCHAR(50))

            EXEC History..sp_INV_ProductTemp_LogUpdate @StockID = @StockID, -- int
               @ProductID = 0, -- int
               @UserID = @UserID, -- uniqueidentifier
               @Notes = @Mess, -- nvarchar(200)
               @FacID = @FacID, -- varchar(10)
               @MaChung = @MaChung -- varchar(50)
         END             
      END
   END
  
   IF @IsDebug = 0
      AND @IsHuyHoan = 1 
   BEGIN       


      UPDATE   p
      SET      TempQty = @TongKhoTam + @Qty, ModifiedBy = @UserID, ModifiedOn = GETDATE()
      FROM     INV_ProductTemp p
      WHERE    p.FacID = @FacID
               AND Vaccine_MaChung_CheckSum = @Vaccine_MaChung_CheckSum --1.0.4.1
               AND p.StockID = @StockID

      DECLARE @Mess_Huy NVARCHAR(500) = N'Cộng kho tạm Vaccine - ws_INV_ProductTemp_Proccessing_Vaccine @StockID='
         + CAST(@StockID AS VARCHAR(50)) + ',@TongKhoTam=' + CAST(@TongKhoTam AS VARCHAR(50)) + ',@Qty='
         + CAST(@Qty AS VARCHAR(50))

      EXEC History..sp_INV_ProductTemp_LogUpdate @StockID = @StockID, -- int
         @ProductID = 0, -- int
         @UserID = @UserID, -- uniqueidentifier
         @Notes = @Mess_Huy, -- nvarchar(200)
         @FacID = @FacID, -- varchar(10)
         @MaChung = @MaChung -- varchar(50)
   END
 

   DROP TABLE #L_InventoryStock_Table,#INV_ProductTemp_Table

END