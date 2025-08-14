# Task : Convert Stored Procedure 

## 📋 Thông tin chung

- **Mục tiêu**: Convert stored procedure  sang backend Aladdin
- **Tên file handler**: ws_CN_ClinicalSessions_UpdatePaid
- đường dẫn chứa file handle: C:\PROJECTS\aladdin\WebService.Handlers\QAHosGenericDB
- đường dẫn chứa file testcase:C:\PROJECTS\aladdin\WebService.Handlers.Tests\QAHosGenericDB
- đường dẫn chứa file yaml testcase: C:\PROJECTS\aladdin\WebService.Handlers.Tests\TestCases\QAHosGenericDB

## 🎯 Yêu cầu kỹ thuật

### RULE CHUNG:

- Bạn là chuyên gia lập trình.
- ✅ Thêm try-catch và logging cẩn thận
- ✅ Review toàn bộ source code
- ✅ Đặt tên file trong cấu trúc thư mục handler
- ✅ Cần có try-catch log
- ✅ Cần tạo test cases
- Kiến trúc code phải phân tách để code gọn gàng, dễ đọc, dễ bảo trì.
- Tuân thủ lập trình file handler theo tài liệu: C:\PROJECTS\aladdin\HANDLERS.md
- Có ghi chú từ code tương ứng với SQL Store procedure (nếu có) trên code bằng tiếng anh
- Sau khi tạo xong, phải biên dịch lại project để kiểm tra lại
- Code cũng phải có With(SqlServerHints.Table.NoLock)
- Chuỗi xuất ra thì nên dùng: singleQuote: true
- Code phải đảm bảo đúng logic như store procedure.
- Khi có update nào trong source code thì cũng nên đồng bộ vào file README_GEN.md.
- Sau khi hoàn tất code thì nên sinh ra file README_GEN.md giống với file mẫu này: README_GEN.md 
trong cùng thư mục.
- Tóm tắt các bước sau khi tạo file vào file README_GEN.md.
- Trong file README_GEN.md có thêm các đường dẫn testcase mà đã gen ra để tôi có thể click vào nó đến đúng file nhanh chóng
