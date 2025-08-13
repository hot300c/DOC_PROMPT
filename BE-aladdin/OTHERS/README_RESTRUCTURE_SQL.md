# RESTRUCTURE SQL - MIGRATION FROM STORED PROCEDURES TO CODE

## Tổng quan
Theo đầu bài yêu cầu là restructure cấu trúc Store Procedure sang code.
Và xử lý các giá trị là trong SQL của Store procedure là dấu = nhưng code lại là StarWith.
Sau khi sửa xong, đưa branch mới với fix và admend nó chứ ko dùng comit nhiều lần.
Có thể testing thử từ các testcase để kiểm tra lại toàn bộ code chạy phải đúng.
Kiểm tra code là khi gọi vào, nó check xem là có "handle" có file đó chưa, nếu chưa thì gọi lại vào store procedure.

## YÊU CẦU 1: FIX FILE ws_MDM_Patient_CheckExists

### 📁 Thông tin file cần sửa:
- **File**: `ws_MDM_Patient_CheckExists.cs`
> **Đường dẫn file code:** [`aladdin/WebService.Handlers/QAHosGenericDB/ws_MDM_Patient_CheckExists.cs`](../WebService.Handlers/QAHosGenericDB/ws_MDM_Patient_CheckExists.cs)

- **Đường dẫn**: `C:\PROJECTS\aladdin\WebService.Handlers\QAHosGenericDB\ws_MDM_Patient_CheckExists.cs`
#### 🔗 **Testcase path:** [`aladdin/WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_MDM_Patient_CheckExists/`](../WebService.Handlers.Tests/TestCases/QAHosGenericDB/ws_MDM_Patient_CheckExists/)
- **Testcase**: `C:\PROJECTS\aladdin\WebService.Handlers.Tests\TestCases\QAHosGenericDB\ws_MDM_Patient_CheckExists`

### 🔧 Yêu cầu kỹ thuật:
1. **Restructure**: Chuyển đổi từ Stored Procedure sang code
2. **Fix logic**: Sửa lỗi SQL dấu `=` thành `StartsWith` trong code
3. **Error handling**: Thêm try-catch và logging cẩn thận
4. **Testing**: Chạy testcase để đảm bảo code hoạt động đúng
5. **Handle check**: Kiểm tra xem có "handle" file chưa, nếu chưa thì gọi lại vào store procedure

### 📋 Checklist trước khi bắt đầu:
- [ ] Review toàn bộ source code hiện tại
- [ ] Phân tích logic của Stored Procedure gốc
- [ ] Xác định các điểm cần sửa (dấu = → StartsWith)
- [ ] Chuẩn bị testcase để verify
- [ ] Tạo branch mới cho fix

### 🚀 Quy trình thực hiện:
1. **Tạo branch mới**: `git checkout -b fix/ws_MDM_Patient_CheckExists`
2. **Review code**: Phân tích file hiện tại
3. **Implement fix**: Sửa logic và thêm error handling
4. **Testing**: Chạy testcase để verify
5. **Commit**: Sử dụng `git commit --amend` thay vì nhiều commit
6. **Push**: Đẩy lên GitLab

### ⚠️ Lưu ý quan trọng:
- Sử dụng `git commit --amend` thay vì tạo nhiều commit
- Thêm try-catch và logging cẩn thận
- Review lại toàn bộ source code trước khi commit
- Đảm bảo testcase pass trước khi push

---

## RULE CHUNG:
- Yêu cầu thêm bổ sung try catch log cẩn thận.
- Review lại toàn bộ source code.


Cau SQL:
ws_MDM_Patient_CheckExists

/*
Version: 1.0.0.0 Van 20180222 Tạo mới cho phép kiểm tra bn đã có trong MDM_Patient hay chưa
Version: 1.0.0.1 Van 20180327 Thay đổi chức năng, tạo riêng biến kiểu bit
Version: 1.0.0.2 Van 20180328 Thêm tên cho cột khi select
Version: 1.0.0.3 Van 20181120 kiểm tra theo mã patienthospitalid
Version: 1.0.0.4 Van 20181219 get PatientID and PatientHospitalID
Version: 1.0.1.0 Van 20181219 get PatientID and PatientHospitalID
Version: 1.0.1.1 Van 20181225 fix
Version: 1.0.2.0 M.Hieu 20190426 10:50 Tối ưu
Version: 1.0.3.0 Văn 20190624 16:30 lấy thêm các cột DobAccuracyCode,DoB_DD,DoB_MM,DoB_YYYY
Version: 1.0.4.0 Văn 20200831 10:50 thêm biến @IsGETPatientInfor để xác định việc có lấy thêm thông tin bn hay không
Version: 1.0.5.0 Văn 20210730 16:45 fix lỗi
*/
CREATE PROCEDURE [dbo].[ws_MDM_Patient_CheckExists]
    (
    @SessionID VARCHAR(MAX), @PatientID UNIQUEIDENTIFIER = NULL, @PatientHospitalID NVARCHAR(50) = NULL, @FacID VARCHAR(10), @IsGETPatientInfor BIT = 1, @IscheckFacID BIT = 1)
AS
BEGIN
    ----------------------------------
    --DECLARE @SessionID VARCHAR(MAX)
    --DECLARE @PatientID UNIQUEIDENTIFIER = NULL
    --DECLARE @FacID VARCHAR(10) = '8.1'
    --DECLARE @PatientHospitalID NVARCHAR(50) = N'210001410', @IsGETPatientInfor BIT = 1, @IscheckFacID BIT = 1
    ----------------------------------
    --DECLARE @UserID UNIQUEIDENTIFIER;

    --SELECT @UserID = UserID
    --FROM [Security].dbo.[Sessions] WITH ( NOLOCK )
    --WHERE [SessionID] = @SessionID;

    ---- check if user authenticated
    --IF @UserID IS NULL
    --    RETURN;

    DECLARE @CustomerId VARCHAR(10) = (SELECT TOP (1) CustomerID FROM dbo.L_Customer WHERE FacID = @FacID)

    SELECT FacID
    INTO #TempFac
    FROM dbo.L_Customer
    WHERE CustomerID = @CustomerId;

    DECLARE @IsTonTai BIT = 0

    IF @PatientID IS NOT NULL
        SELECT @IsTonTai = 1, @PatientHospitalID = PatientHospitalID
        FROM QAHosGenericDB.dbo.MDM_Patient WITH (NOLOCK)
        WHERE PatientID = @PatientID; --AND FacID = @FacID

    IF @PatientHospitalID IS NOT NULL
        SELECT @IsTonTai = 1, @PatientID = PatientID
        FROM QAHosGenericDB.dbo.MDM_Patient P WITH (NOLOCK)
        WHERE PatientHospitalID = @PatientHospitalID
              AND (EXISTS (SELECT 1 FROM #TempFac T WHERE T.FacID = P.FacID) OR @IscheckFacID = 0)

    SELECT @IsTonTai
    IF @IsGETPatientInfor = 1
    BEGIN
        SELECT PatientHospitalID, PatientID, FullName, Gender, DoB, DobAccuracyCode, DoB_DD, DoB_MM, DoB_YYYY,
               NationalIDNo, CMND_Passport, Occupation, [Address], Mobile, Email, DoB_YYYY,
               CONVERT ( NVARCHAR(10), ProvinceID ) ProvinceID, CONVERT ( NVARCHAR(10), DistrictID ) DistrictID,
               CONVERT ( NVARCHAR(10), WardID ) WardID, SoNha
        FROM QAHosGenericDB.dbo.MDM_Patient WITH (NOLOCK)
        WHERE PatientID = @PatientID

        SELECT CardID, FacID, PatientID, Code MedicareCardNo, RegHospitalCode Reg_Code, EffectiveFrom AS EffectiveFrom,
               EffectiveThru AS EffectiveThru, [ADDRESS] AS HospitalName, ISNULL ( IsActive, 0 ) IsActive,
               ISNULL ( Is5Nam, 0 ) Is5Nam, ISNULL ( IsCanNgheo, 0 ) IsCanNgheo, MaCanNgheo,
               ISNULL ( IsDefault, 0 ) CheckUsedBHYT, CAST(0 AS BIT) IsNew, ThoiGianDu5Nam
        FROM dbo.CN_MedicarePatient MP WITH (NOLOCK)
        WHERE PatientID = @PatientID

        SELECT a.CardID, a.FacID, a.PatientID, a.Code AS MedicareCardNo, EffectiveFrom EffectiveFrom,
               EffectiveThru EffectiveThru, ISNULL ( a.IsDefault, 0 ) CheckUse, CAST(0 AS BIT) IsNew, a.InsuranceID,
               b.InsuranceName
        FROM dbo.CN_InsurancePatient a WITH (NOLOCK)
            JOIN dbo.L_Insurance b WITH (NOLOCK)
                ON a.InsuranceID = b.InsuranceID
        WHERE a.PatientID = @PatientID


        SELECT a.ID,
               --PatientID,
               a.IsPatientID, ISNULL ( c.MoiQuanHe, N'Khác' ) MoiLienHe, a.NguoiLienHe, a.SoDienThoai,
               --FacID,
               ISNULL ( a.IsDefault, 0 ) CheckNguoiThan, CAST(0 AS BIT) IsNew, b.PatientHospitalID AS MaBN,
               c.IDMoiQuanHe
        FROM dbo.CN_NguoiLienHe a WITH (NOLOCK)
            LEFT JOIN dbo.MDM_Patient b WITH (NOLOCK)
                ON a.IsPatientID = b.PatientID AND EXISTS (SELECT 1 FROM #TempFac T WHERE T.FacID = b.FacID)
            LEFT JOIN dbo.L_MoiQuanHe c WITH (NOLOCK)
                ON a.IDMoiQuanHe = c.IDMoiQuanHe AND
                                                 (   c.FacID = @FacID OR
                                                                      (   c.FacID = 0 AND NOT EXISTS
    (   SELECT 1
        FROM dbo.L_MoiQuanHe d WITH (NOLOCK)
        WHERE d.FacID = @FacID AND d.IDMoiQuanHe = c.IDMoiQuanHe          )))
        WHERE a.PatientID = @PatientID;


        SELECT *
        FROM QAHosGenericDB.dbo.CN_NguonKhaoSat_Patient WITH (NOLOCK)
        WHERE PatientID = @PatientID

        SELECT TOP (1)
               *
        FROM QAHosGenericDB.dbo.L_Patient_Image WITH (NOLOCK)
        WHERE PatientID = @PatientID

        SELECT @PatientHospitalID PatientHospitalID, @PatientID PatientID


    END

    DROP TABLE #TempFac
END
