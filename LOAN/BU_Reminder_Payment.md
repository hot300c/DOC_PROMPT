Chức năng này kiểm tra nợ của khách hàng đang bị nợ gần đến hạn thì:
Hệ thống tự động nhắc nợ khách hàng qua các kênh thông tin như: Email; Thông báo; Push notification.

Flow:
Mỗi ngày vào lúc 17:00 PM, hệ thống kích hoạt chạy quét toàn bộ khách hàng có hồ sơ Loan đang active;
Và kiểm tra ngày thanh toán nợ trước 5 ngày và chưa thông báo lần nào cho khách hàng thì gửi thông báo.

Rule:
Cũng cho phép cấu hình thời gian hệ thống kích hoạt.
Số ngày kiểm tra vay nợ loan để nhắc nợ.
Hệ thống chạy mỗi ngày theo thời gian kích hoạt trên.
Cho phép chọn số lần nhắc. Tất nhiên là nhỏ hơn số ngày nhắc. Vì nhắc ít nhất 1 lần.
Cũng lưu log history lại về thông báo nhắc nợ đã được gửi.
Cũng cần nó lưu template theo các kênh,
Và khi bắt đầu gửi, thì nó cache lại template đó để lần sau có thể dùng nội dung đó gửi tiếp cho khách hàng tiếp theo.

https://github.com/PNTSOL/RENTCAR_GATEWAY/issues/5