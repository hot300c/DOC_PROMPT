Chức năng quản lý user:

user admin: login vào trang quản trị theo quyền để thực hiện.
User khách hàng: Đăng nhập bằng google; hoặc tạo account riêng  (Nhưng đánh dấu là account này là do khách hàng nhập liệu). Sau đó hệ thống gửi password tạm cho khách hàng.

RULE:
Hệ thống kiểm tra email là duy nhất, và dùng email như là username đăng nhập.
Khi chứng thực qua google thàng công thì cũng phải lưu thông tin liên quan để khi user mở lại mobile app lần nữa thì kiểm tra phiên còn hạn không, nếu hết thì hệ thống gọi lại (refesh token) để lấy phiên mới cho user, mà user không phải bị đăng nhập lại lần nữa.
