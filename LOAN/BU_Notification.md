Tài liệu nghiệp vụ người dùng - chức năng Gửi thông báo:

Chức năng:
Quản lý thông tin thông báo tin tức cho người dùng (khách hàng đã đăng ký), và khách hàng chưa đăng ký.
Người quản trị: Quản lý danh sách template các nội dung tin qua 3 kênh Gửi qua email| Push notification | Trang thông báo mobile app và khi định nghĩa các template thì phải có nêu Tên Chiến dịch đó, active hoặc không active;
Và chiến dịch đó có các cột là active theo kênh (Default là active)
Có chức năng gửi thông báo ngay theo chiến dịch cho khách hàng đã đăng ký.
Có chức năng gửi thông báo ngay theo chiến dịch cho khách hàng chưa đăng ký.

Có chức năng lưu lại lịch sử các thông báo đã gửi đến user theo kênh.

Dữ liệu gửi:
Khách hàng đã đăng ký: là lấy từ danh sách hệ thống từ loan.com.us. (Theo email nếu có). Và gửi Push notification và thông báo trên mobile app nếu khách hàng đã đăng ký.
Khách hàng chưa đăng ký: Thì chỉ có kênh mobile app và trang thông báo.

Kênh gửi:
Khách hàng đã đăng ký: Gửi qua email| Push notification | Trang thông báo mobile app
Khách hàng chưa đăng ký: Push notification | Trang thông báo mobile app

Flow:
Khi khách hàng cài đặt app là hệ thống giữ token device của khách hàng (theo yêu cầu firebase) để gửi Push notification; và có trang Thông báo để khách hàng xem được thông tin.

Admin:
Chức năng của chức năng gửi thông báo ngay theo chiến dịch cho khách hàng đã đăng ký;
User đăng nhập --> user vào màn hình--> User chọn chiến dịch (đã active) --> User có thể xem lại nội dung của chiến dịch để kiểm tra, đọc lại kỹ trước khi gửi, và màn hình cũng cho phép user mở popup để xem danh sách các user cần gửi --> User Bấm nút gửi --> Hệ thống hiển thị popup thông báo xác nhận rằng user xác nhận chắc chắn gửi --> User bấm nút đồng ý --> Hệ thống sẽ gửi danh sách user đi theo tuần tự là theo kênh Trang thông báo --> Email --> Push notification theo từng user.

Chức năng của chức năng gửi thông báo ngay theo chiến dịch cho khách hàng Chưa đăng ký;
User đăng nhập --> user vào màn hình--> User chọn chiến dịch loại Khách hàng CHƯA ĐĂNG KÝ (nhưng chiến dịch đã active) --> User có thể xem lại nội dung của chiến dịch để kiểm tra, đọc lại kỹ trước khi gửi --> User Bấm nút gửi --> Hệ thống hiển thị popup thông báo xác nhận rằng user xác nhận chắc chắn gửi --> User bấm nút đồng ý --> Hệ thống sẽ gửi danh sách user đi theo tuần tự là theo kênh Trang thông báo --> Push notification theo từng user.

Ràng buộc:
Mỗi kênh gửi có độ dài khác nhau. Và có kênh có upload được hình hoặc không.
Khách hàng đã đăng ký là khi đăng ký thành công, hệ thống sẽ cập nhật email, username, mã loan của KH đó vào thông tin Token.
Nếu thông tin Token mà không có các thông tin email, username, mã loan thì nghĩa là khách hàng chưa đăng ký.
Có chức năng gửi thông báo ngay theo chiến dịch cho khách hàng đã đăng ký: Là gửi cho tất cả khách hàng đã đăng ký.
Có chức năng gửi thông báo ngay theo chiến dịch cho khách hàng chưa đăng ký: là những khách hàng chưa có 1 trong 3 thông tin: email hoặc username hoặc mã loan;

https://github.com/PNTSOL/RENTCAR_GATEWAY/issues/4