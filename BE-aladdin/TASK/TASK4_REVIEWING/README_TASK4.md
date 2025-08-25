# Task 4: Convert Stored Procedure ws_Vaccine_KiemTraDongPhacDo

## 📋 Thông tin chung

- **Ticket**: https://rm.vnvc.info/issues/137323
- **Mục tiêu**: Convert stored procedure `ws_Vaccine_KiemTraDongPhacDo` sang backend Aladdin
- **Tên file handler**: `ws_Vaccine_KiemTraDongPhacDo.cs`
- đường dẫn chứa file handle: C:\PROJECTS\aladdin\WebService.Handlers\QAHosGenericDB
- đường dẫn chứa file testcase:C:\PROJECTS\aladdin\WebService.Handlers.Tests\QAHosGenericDB
- đường dẫn chứa file yaml testcase: C:\PROJECTS\aladdin\WebService.Handlers.Tests\TestCases\QAHosGenericDB

## 🎯 Yêu cầu kỹ thuật

### RULE CHUNG:

- ✅ Thêm try-catch và logging cẩn thận
- ✅ Review toàn bộ source code
- ✅ Đặt tên file trong cấu trúc thư mục handler
- ✅ Cần có try-catch log
- ✅ Cần tạo test cases

## 📊 Thông tin Stored Procedure

### Tên gốc:

```sql
CREATE PROCEDURE [dbo].[ws_Vaccine_KiemTraDongPhacDo]
```

### Parameters:

```sql
@SessionID VARCHAR(MAX)
@PatientID UNIQUEIDENTIFIER
@IPUser VARCHAR(255)
@MacAddressUser VARCHAR(255)
```

## 🔍 Logic nghiệp vụ

### 1. Authentication & Validation

```sql
-- Lấy UserID từ SessionID
SELECT @UserID = UserID
FROM [Security]..[Sessions] WITH (NOLOCK)
WHERE [SessionID] = @SessionID

-- Nếu không tìm thấy UserID thì RETURN
IF @UserID IS NULL
    RETURN
```

### 2. Xử lý Phác đồ Vaccine chính

```sql
-- Lấy danh sách phác đồ vaccine chưa đóng
SELECT IDPhacDoBenhNhan, ROW_NUMBER() OVER (ORDER BY IDPhacDoBenhNhan) STT
INTO #tempPhacDoVaccine
FROM dbo.Vaccine_PhacDoBenhNhan WITH (NOLOCK)
WHERE PatientID = @PatientID AND NgayDong IS NULL

-- Lấy danh sách phác đồ còn mũi tiêm chưa hoàn thành
SELECT b.IDPhacDoBenhNhan
INTO #tempPhacdobenhNhanConMuiTiem
FROM #tempPhacDoVaccine a WITH (NOLOCK)
INNER JOIN Vaccine_PhacDoBenhNhan_Detail b WITH (NOLOCK)
    ON a.IDPhacDoBenhNhan = b.IDPhacDoBenhNhan
WHERE b.CompleteOn IS NULL AND b.PatientID = @PatientID

-- Đóng phác đồ vaccine (chỉ những phác đồ không còn mũi tiêm chưa hoàn thành)
UPDATE dbo.Vaccine_PhacDoBenhNhan
SET NgayDong = GETDATE(),
    NguoiDong = @UserID,
    NgayDongAsInt = FORMAT(GETDATE(), 'yyyyMMdd', 'en-US'),
    ModifiedOn = GETDATE(),
    ModifiedBy = @UserID,
    IPUser = @IPUser,
    MacAddressUser = @MacAddressUser
FROM #tempPhacDoVaccine t1
INNER JOIN Vaccine_PhacDoBenhNhan b WITH (NOLOCK)
    ON b.IDPhacDoBenhNhan = t1.IDPhacDoBenhNhan
WHERE NOT EXISTS(
    SELECT * FROM #tempPhacdobenhNhanConMuiTiem t
    WHERE t.IDPhacDoBenhNhan = t1.IDPhacDoBenhNhan
)
```

### 3. Xử lý Phác đồ Nhóm bệnh

```sql
-- Lấy danh sách phác đồ nhóm bệnh chưa đóng
SELECT IDPhacDoBenhNhan_NhomBenh, ROW_NUMBER() OVER (ORDER BY IDPhacDoBenhNhan) STT
INTO #tempPhacDoNhomBenh
FROM dbo.Vaccine_PhacDoBenhNhan_NhomBenh WITH (NOLOCK)
WHERE PatientID = @PatientID AND NgayDong IS NULL

-- Loop qua từng phác đồ nhóm bệnh
DECLARE @j INT = 1
DECLARE @k INT = (SELECT COUNT(1) FROM #tempPhacDoNhomBenh)

WHILE @j <= @k
BEGIN
    DECLARE @IDPhacDoBenhNhan_NhomBenh UNIQUEIDENTIFIER

    SELECT @IDPhacDoBenhNhan_NhomBenh = IDPhacDoBenhNhan_NhomBenh
    FROM #tempPhacDoNhomBenh
    WHERE STT = @j

    -- Kiểm tra xem còn mũi tiêm chưa hoàn thành không
    IF NOT EXISTS (
        SELECT 1
        FROM dbo.Vaccine_PhacDoBenhNhan_NhomBenh_Detail WITH (NOLOCK)
        WHERE IDPhacDoBenhNhan_NhomBenh = @IDPhacDoBenhNhan_NhomBenh
            AND CompleteOn IS NULL
            AND TiemNgoaiOn IS NULL
    )
    BEGIN
        -- Đóng phác đồ nhóm bệnh
        UPDATE dbo.Vaccine_PhacDoBenhNhan_NhomBenh
        SET NgayDong = GETDATE(),
            NguoiDong = @UserID,
            NgayDongAsInt = FORMAT(GETDATE(), 'yyyyMMdd', 'en-US'),
            ModifiedOn = GETDATE(),
            ModifiedBy = @UserID,
            IPUser = @IPUser,
            MacAddressUser = @MacAddressUser
        WHERE IDPhacDoBenhNhan_NhomBenh = @IDPhacDoBenhNhan_NhomBenh

        -- Log lịch sử
        EXEC History..sp_Vaccine_PhacDoBenhNhan_NhomBenh_LogUpdate
            @IDPhacDoBenhNhan_NhomBenh = @IDPhacDoBenhNhan_NhomBenh,
            @UserID = @UserID
    END

    SET @j = @j + 1
END

-- Cleanup temp tables
DROP TABLE #tempPhacDoVaccine, #tempPhacDoNhomBenh, #tempPhacdobenhNhanConMuiTiem
```

## 🎯 Tóm tắt chức năng

### Mục đích:

- **Kiểm tra và đóng phác đồ vaccine** cho bệnh nhân
- Chỉ đóng những phác đồ đã hoàn thành tất cả mũi tiêm
- Ghi log lịch sử thay đổi

### Điều kiện đóng phác đồ:

1. **Phác đồ vaccine**: Không còn mũi tiêm nào có `CompleteOn IS NULL`
2. **Phác đồ nhóm bệnh**: Không còn mũi tiêm nào có `CompleteOn IS NULL` và `TiemNgoaiOn IS NULL`

### Thông tin cập nhật khi đóng:

- `NgayDong`: Thời gian đóng
- `NguoiDong`: UserID người thực hiện
- `NgayDongAsInt`: Ngày đóng dạng số (yyyyMMdd)
- `ModifiedOn`, `ModifiedBy`: Thông tin cập nhật
- `IPUser`, `MacAddressUser`: Thông tin người dùng

## 📁 Cấu trúc file handler

```
aladdin/WebService.Handlers/QAHosGenericDB/ws_Vaccine_KiemTraDongPhacDo.cs
```

## 🧪 Test Cases cần tạo

1. **Test case 1**: Đóng phác đồ vaccine thành công
2. **Test case 2**: Đóng phác đồ nhóm bệnh thành công
3. **Test case 3**: Không đóng phác đồ còn mũi tiêm chưa hoàn thành
4. **Test case 4**: Invalid SessionID
5. **Test case 5**: PatientID không tồn tại
6. **Test case 6**: UserID không có quyền

Sang Backend aldin thì theo tên:ws_Vaccine_KiemTraDongPhacDo
