# Task : Convert Stored Procedure ws_Vaccine_KiemTraDongPhacDo

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
- Tuân thủ lập trình file handler theo tài liệu: C:\PROJECTS\aladdin\HANDLERS.md
- Có ghi chú từ code tương ứng với SQL Store procedure (nếu có) trên code bằng tiếng anh
- Sau khi tạo xong, phải biên dịch lại project để kiểm tra lại
- Code cũng phải có With(SqlServerHints.Table.NoLock)
