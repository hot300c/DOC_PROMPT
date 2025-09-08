[08/09/2025 15:06:44] Vic Nguyen: hồ sơ ở đây chỉ là form thôi á anh
[08/09/2025 15:07:27] Vic Nguyen: mình sử dụng app như 1 kênh để khách submit form Q&A, không bao gồm upload file hay tài liệu hồ sơ vay
[08/09/2025 15:07:52] Vic Nguyen: bên app cũng sẽ không lưu trữ hồ sơ vay của hay hợp đồng vay của khách trên server mobile app ạ
[08/09/2025 15:08:15] Vic Nguyen: em có đính kèm form mẫu trên brief 1.0 anh xem qua thử nha ạ
[08/09/2025 15:09:07] Vic Nguyen: chỉ cần khách submit, đẩy thông tin về mail do bên em cung cấp, rồi các broker sẽ nhận và handle từ đó ạ
[08/09/2025 15:10:31] Vic Nguyen: còn nút request for statement là cho khách đang chờ trạng thái vay, mình có thể thiết lập như 1 cái noti đến team broker, họ nhận được noti sẽ cập nhật với khách qua phone/ thay đổi trạng thái trên mobile app ạ
[08/09/2025 15:12:00] Vic Nguyen: app này chỉ đóng vai trò như 1 kênh nhắc đến hạn thanh toán thui ạ, không lưu trữ, thanh toán hay cần các tác vụ cao hơn anh nè
[08/09/2025 15:14:12] Duy Phúc: Tại bước này:
chỉ cần khách submit, đẩy thông tin về mail do bên em cung cấp, rồi các broker sẽ nhận và handle từ đó ạ
-->
Thì broker nhận bằng cách nào á em. Team broker sẽ có 1 account dùng chung vào 1 màn hình admin sẽ thấy hết các submit của KH pko nhỉ
[08/09/2025 15:14:56] Duy Phúc: Broker sẽ vào admin ở hệ  thống nhà mình dựng để vào xem á ?
[08/09/2025 15:15:33] Vic Nguyen: team broker đang có tầm 20 người, em đang snghi mình có thể tạo account phân quyền cho từng người, và chỉ thấy được thông tin khách mà người đó đảm nhận
[08/09/2025 15:15:47] Vic Nguyen: admin thì thấy hết ạ
[08/09/2025 15:16:29] Vic Nguyen: hoặc còn cách nào tối ưu chi phí hơn anh suggest giúp em nha
[08/09/2025 15:17:06] Duy Phúc: ohm, em, chỗ này kiến trúc lại cho phép nhiều người (cùng team broker). Nhưng sẽ tạm thời thấy all "form" của khách.
[08/09/2025 15:18:09] Vic Nguyen: dạ đúng rồi, form thì gửi về cho all, nhưng khúc đã được assigned rồi thì hạn chế ah
[08/09/2025 15:18:32] Vic Nguyen: để cho họ không bị rối
[08/09/2025 15:20:24] Duy Phúc: anh sẽ thiết kế tách biệt là default sẽ thấy các hồ sơ chờ Duyệt. Và có 1 nút lọc (Filter) cho các hồ sơ đã duyệt (theo user đang đăng nhập đó).
[08/09/2025 15:21:04] Duy Phúc: chỗ này:
"còn nút request for statement là cho khách đang chờ trạng thái vay, mình có thể thiết lập như 1 cái noti đến team broker, họ nhận được noti sẽ cập nhật với khách qua phone/ thay đổi trạng thái trên mobile app ạ"
--> Ok em.
Note luồng: 
team Broker cập nhật xong --> hệ thống báo noti (thông báo/email/ push notification) và phone cho KH.
[08/09/2025 15:21:54] Vic Nguyen: cập nhật rồi chỉ cần noti và in app alert thôi ạ
[08/09/2025 15:22:57] Duy Phúc: Noted:
Team Broker cập nhật xong --> hệ thống báo noti (thông báo in app/ push notification) .
Sau đó, Team phone cho KH.
[08/09/2025 15:24:20] Duy Phúc: Khách hàng submit là mình ko yêu cầu KH upload bất kỳ hồ sơ (files) của khách pko em.
[08/09/2025 15:24:58] Vic Nguyen: À không anh cho em note lại: Khách chỉ nhận được email 1 lần duy nhất, là khi khoản vay đã được duyệt, bắt đầu trạng thái active
[08/09/2025 15:25:28] Vic Nguyen: Đúng rồi a
[08/09/2025 15:26:49] Duy Phúc: - **Chức năng:** Theo dõi trạng thái đơn vay
- **Mục đích:** Broker có thể theo dõi tiến trình xử lý đơn vay, và có thể cập nhật 2 trạng thái đơn. Active & Paid-off.
Vậy thì Broker chỉ có thể chuyển từ:
 Active -->  Paid-off: hệ thống báo noti (thông báo in app/ push notification).
Đúng ko em
[08/09/2025 15:28:20] Vic Nguyen: Dạ còn 1 quyền là import + export data
[08/09/2025 15:30:33] Duy Phúc: afh, anh hiểu import & export rõ ràng hơn chỗ này rồi.
 import: Đưa data mới/ cũ về dữ liệu bên mình. 
Anh thắc mắc chỗ này luôn là import gồm 2 loại là KH đã có/ và chưa có. 
Nếu chưa có --> thêm mới.
Nếu đã có --> thì update / hay sao em nhỉ ?
[08/09/2025 15:32:14] Duy Phúc: Về Export: Thì xuất ra file excel và có 3 option filter (xuất all/ Xuất chỉ loại active/ xuất chỉ loại paid-off).
--> đúng ko em.
[08/09/2025 15:35:25] Vic Nguyen: Em đang hình dung 1st step
Từng broker sẽ quản lí file data khách hàng của mình, file bao gồm các trường sẽ hiển thị trên app, họ có thể import (cập nhật) mỗi khi được yêu cầu về trạng thái (có thể là mỗi ngày)
Và admin có thể nhìn thấy được tổng của những file con đó trên 1 file lớn
[08/09/2025 15:35:53] Vic Nguyen: Nên có thể hiểu là chưa có thêm mới. Có rồi thì update đó anh
[08/09/2025 15:36:03] Vic Nguyen: Dạ đúng
[08/09/2025 15:38:41] Vic Nguyen: Admin có thể xuất data lẻ của từng broker luôn ạ
[08/09/2025 15:41:51] Duy Phúc: Do import là thường cho dùng khá nhiều khách hàng cùng 1 lúc mới dùng import. 
Vì import có 1 số rủi ro: như import vào là nó tạo KH mới hoặc update (trạng thái). 
CHo nên anh recommend broker cẩn thận làm nhiều cùng lúc, ko kiểm soát chặt chẽ thì sửa lại take time.

Mở rộng thêm:
hệ thống admin bên mình có màn hình, cho member brokers thao tác luôn trên đó như : cập nhật thông tin khách hàng, hay cập nhật trạng thái.
[08/09/2025 15:42:06] Duy Phúc: Noted, em nhé.
[08/09/2025 15:43:52] Vic Nguyen: Vậy có chức năng broker có thể chỉnh sửa đơn giản trực tiếp trên hệ thống app, trạng thái và các trường đẩy về file tổng không anh
[08/09/2025 15:46:35] Duy Phúc: Vậy có chức năng broker có thể chỉnh sửa đơn giản trực tiếp trên hệ thống app, trạng thái
--> được em nhé. broker sẽ thực hiện trên màn hình admin hệ thống á.

Các trường đẩy về file tổng không.
--> có em nhé. Khi Broker thực hiện xong thì đã lưu vào hệ thống rồi, thì nếu xuất (export file excel) cũng thấy sự cập nhật đó.
[08/09/2025 15:47:36] Vic Nguyen: Dạ vậy để đơn giản thì mình proceed như thế này nha anh
[08/09/2025 15:49:50] Duy Phúc: ohm em nhé. vậy mình ko có chức năng import và thay thế bằng màn hình: 
Xem /cập nhật thông tin KH. 
Xem/ Cập nhật trạn thái form hồ sơ vay của KH.
Và có chức năng export theo 3 loại trạng thái & theo member broker hoặc tất cả members.