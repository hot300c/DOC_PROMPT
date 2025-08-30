# Company B2B Management – User Requirements (Summary)

## 1) Mục tiêu
- Cung cấp màn hình quản lý Công ty B2B cho phép: xem danh sách, tìm kiếm, thêm/sửa, bật/tắt trạng thái, nhập dữ liệu từ file Excel và xuất dữ liệu ra Excel.

## 2) Phạm vi
- Chức năng: Công ty B2B (CompanyB2B).
- Chức năng bao gồm: Danh sách, Tìm kiếm, Thêm/Sửa, Bật/Tắt trạng thái, Import (Excel), Export (Excel).
- Không thay đổi cấu trúc dữ liệu hệ thống hiện có; chỉ chuẩn hóa hiển thị, quy tắc kiểm tra dữ liệu và thông báo.

## 3) Người dùng và truy cập
- Yêu cầu đăng nhập hệ thống và chọn đúng cơ sở (facility) trước khi truy cập.
- Chỉ người dùng có quyền mới xem/Thêm/Sửa/Xuất/Nhập được; nếu không có quyền, hiển thị thông báo không truy cập được trang.

## 4) Giao diện và trải nghiệm người dùng
- Bố cục chuẩn:
  - Phần thông tin cơ sở ở trên cùng.
  - Khối Tìm kiếm (nền mờ) với ô “Từ khóa” và nút “Tìm kiếm”.
  - Bảng dữ liệu ở giữa, hỗ trợ sắp xếp, di chuột nổi bật, hiển thị rõ ràng.
  - Thanh footer phía dưới (nền mờ) hiển thị tổng số dòng, các nút phân trang và chọn số dòng mỗi trang; nhóm nút hành động (Thêm mới, Nhập Excel, Xuất Excel) nằm bên phải.
- Trạng thái hiển thị trong bảng bằng ô check (đã bật/đang kích hoạt hoặc đã tắt/ngưng kích hoạt). Bấm vào ô check để bật/tắt nhanh.
- Bấm vào một dòng để mở popup Thêm/Sửa.

## 5) Trường dữ liệu chính
- Bắt buộc nhập khi Thêm/Sửa: Mã công ty, Tên công ty, Ngày hiệu lực từ, Số PO-HĐ.
- Không bắt buộc: Mã số thuế, Địa chỉ, Ngày hiệu lực đến, Trạng thái (mặc định kích hoạt).
- Quy tắc ngày: Nếu có “Ngày hiệu lực đến”, thì “Ngày hiệu lực từ” phải nhỏ hơn hoặc bằng “Ngày hiệu lực đến”.

## 6) Tìm kiếm và danh sách
- Ô “Từ khóa” cho phép tìm theo Mã/Tên/MST/Địa chỉ/Số PO-HĐ.
- Nút “Tìm kiếm” chỉ thực hiện khi có từ khóa; nếu rỗng hiển thị nhắc nhập.
- Bảng có thể sắp xếp theo cột “Hiệu lực” (ưu tiên ngày bắt đầu).
- Hiển thị tổng số dòng và hỗ trợ chọn số dòng mỗi trang (10, 20, 50, 100).

## 7) Thêm/Sửa (Popup)
- Thứ tự trường: Mã công ty → Tên công ty → Mã số thuế → Địa chỉ → Ngày hiệu lực từ → Ngày hiệu lực đến → Số PO-HĐ → Trạng thái.
- Khi sửa, “Mã công ty” không cho phép thay đổi.
- Kiểm tra trước khi lưu: các trường bắt buộc; kiểm tra quan hệ ngày hợp lệ.
- Lưu thành công: đóng popup, làm mới danh sách và hiển thị thông báo thành công.

## 8) Import (Excel)
- Chỉ chấp nhận tệp .xlsx/.xls, tối đa 5MB.
- Trước khi import, người dùng cần có dữ liệu đã tải lên màn hình (để tránh nhầm thao tác).
- Popup hướng dẫn nêu rõ cấu trúc cột và yêu cầu dữ liệu.
- Kết quả import:
  - Thành công: hiển thị số dòng thêm mới/cập nhật, làm mới danh sách.
  - Có lỗi: hiển thị thông báo lỗi tóm tắt và mở popup liệt kê chi tiết theo từng dòng lỗi (dễ kiểm tra và sửa lại tệp).

## 9) Export (Excel)
- Xuất toàn bộ dữ liệu hiện có thành tệp Excel với các cột: Mã công ty, Tên công ty, Số PO-HĐ, Ngày bắt đầu, Ngày kết thúc, Trạng thái.
- Nếu không có dữ liệu phù hợp: thông báo “Không có dữ liệu để export”.

## 10) Thông báo lỗi – nguyên tắc hiển thị
- Backend trả về thông điệp lỗi cụ thể (ví dụ: “Ngày hiệu lực từ phải nhỏ hơn hoặc bằng ngày hiệu lực đến”): hiển thị đúng nội dung này.
- Backend trả lỗi theo từng trường (nhiều lỗi): hiển thị dòng lỗi đầu tiên dễ hiểu nhất.
- Trường hợp khác: hiển thị thông báo lỗi chung theo ngữ cảnh hành động (lưu/tải/xử lý).

## 11) Quy tắc hiển thị dữ liệu
- Ngày hiệu lực trong danh sách: hiển thị “dd/MM/yyyy - dd/MM/yyyy”.
- Trạng thái: “Kích hoạt” hoặc “Ngưng kích hoạt” tương ứng tình trạng check.
- Giá trị trống có thể hiển thị rỗng, không gây nhầm lẫn cho người dùng.

## 12) Tiêu chí hoàn thành
- Người dùng có thể: tìm kiếm nhanh, xem danh sách rõ ràng, thêm/sửa thuận tiện, bật/tắt trạng thái trực tiếp, import/export dễ dùng.
- Tất cả quy tắc kiểm tra dữ liệu (đặc biệt quan hệ ngày) được áp dụng nhất quán, báo lỗi tiếng Việt tường minh.
- Thông báo tình trạng thao tác (thành công/thất bại/đang xử lý) rõ ràng và nhất quán.

## 13) Ngoài phạm vi
- Không thay đổi cấu trúc dữ liệu lõi hoặc quyền hệ thống.
- Không xử lý các yêu cầu báo cáo, phân quyền nâng cao ngoài chức năng đã mô tả.


