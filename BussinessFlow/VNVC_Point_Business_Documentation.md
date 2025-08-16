# TÀI LIỆU NGHIỆP VỤ: CHỨC NĂNG VNVC POINT

## 1. TỔNG QUAN CHỨC NĂNG

### 1.1 Định nghĩa
**VNVC Point** là hệ thống quản lý điểm tích lũy và thanh toán của VNVC (Vaccine National Vaccine Company), hoạt động tương tự như một hệ thống ví điện tử nội bộ. Hệ thống này cho phép khách hàng tích điểm từ các giao dịch và sử dụng điểm để thanh toán cho các dịch vụ.

### 1.2 Mục đích chính
- **Quản lý tài khoản điểm tích lũy**: Theo dõi số dư điểm của khách hàng
- **Hệ thống thanh toán**: Cho phép thanh toán bằng điểm tích lũy
- **Tích lũy điểm**: Tự động tích điểm từ các giao dịch mua hàng/dịch vụ
- **Quản lý thẻ thành viên**: Quản lý thông tin thẻ và tài khoản khách hàng

## 2. KIẾN TRÚC HỆ THỐNG

### 2.1 Cơ sở dữ liệu
Hệ thống VNVC Point sử dụng cơ sở dữ liệu `QA_Pay` với các bảng chính:

#### Bảng tài khoản (`L_Account`)
- `AccountID`: ID duy nhất của tài khoản
- `AccountIDName`: Số tài khoản
- `TypeAccount`: Loại tài khoản (0 = tài khoản khách hàng)
- `IsActive`: Trạng thái hoạt động
- `IsLock`: Trạng thái khóa

#### Bảng thẻ (`L_Card`)
- `CardID`: ID duy nhất của thẻ
- `CardIDName`: Mã thẻ
- `AccountID`: Liên kết với tài khoản

#### Bảng giao dịch thu (`CN_Receivable`)
- `TransactionID`: ID giao dịch
- `AccountID`: Tài khoản nhận
- `TotalMoney`: Số tiền nhận
- `Reason`: Lý do giao dịch
- `DateCreated`: Ngày tạo giao dịch

#### Bảng giao dịch chi (`CN_Payable`)
- `TransactionID`: ID giao dịch
- `AccountID`: Tài khoản chi
- `TotalMoney`: Số tiền chi
- `Reason`: Lý do giao dịch
- `DateCreated`: Ngày tạo giao dịch

### 2.2 Cấu trúc ứng dụng
Hệ thống được tích hợp vào ứng dụng Genie với các module chính:

#### Module Tiếp nhận
- **Kiểm tra VNVC Point**: Xem thông tin tài khoản và lịch sử giao dịch
- **Quản lý thông tin khách hàng**: Cập nhật thông tin tài khoản

#### Module Thanh toán
- **Thanh toán bằng VNVC Point**: Sử dụng điểm để thanh toán
- **Nạp tiền VNVC Point**: Nạp tiền vào tài khoản
- **Hoàn tiền VNVC Point**: Xử lý hoàn tiền

#### Module Cửa hàng
- **Thanh toán bán lẻ**: Sử dụng VNVC Point trong bán hàng
- **Quản lý giao dịch**: Theo dõi các giao dịch thanh toán

## 3. LUỒNG NGHIỆP VỤ CHÍNH

### 3.1 Luồng tích lũy điểm
```
Khách hàng mua hàng/dịch vụ → Hệ thống tính điểm → Cập nhật tài khoản VNVC Point
```

**Tỷ lệ tích lũy**: 0.05 điểm cho mỗi 100 VND chi tiêu

### 3.2 Luồng thanh toán bằng điểm
```
Nhập mã thẻ → Kiểm tra thông tin → Xác nhận thanh toán → Trừ điểm tài khoản
```

### 3.3 Luồng nạp tiền
```
Nhập mã thẻ → Kiểm tra tài khoản → Xác nhận số tiền → Cộng tiền vào tài khoản
```

### 3.4 Luồng hoàn tiền
```
Chọn giao dịch cần hoàn → Xác nhận hoàn tiền → Trừ tiền từ tài khoản VNVC Point
```

## 4. CÁC CHỨC NĂNG CHI TIẾT

### 4.1 Quản lý tài khoản
- **Xem danh sách tài khoản**: Hiển thị tất cả tài khoản VNVC Point
- **Quản lý Account**: Thêm, sửa, xóa tài khoản
- **Khóa/mở khóa tài khoản**: Quản lý trạng thái hoạt động

### 4.2 Quản lý thẻ
- **Tạo thẻ mới**: Liên kết thẻ với tài khoản
- **Quản lý thẻ**: Cập nhật thông tin thẻ
- **Khóa thẻ**: Vô hiệu hóa thẻ khi cần thiết

### 4.3 Theo dõi giao dịch
- **Lịch sử giao dịch**: Xem tất cả giao dịch của tài khoản
- **Báo cáo số dư**: Theo dõi biến động số dư theo thời gian
- **Báo cáo chi tiết**: Xem chi tiết từng giao dịch

### 4.4 Quản lý người thụ hưởng
- **Thêm người thụ hưởng**: Liên kết tài khoản với khách hàng
- **Cập nhật thông tin**: Sửa đổi thông tin người thụ hưởng
- **Xóa người thụ hưởng**: Gỡ bỏ liên kết

## 5. BÁO CÁO VÀ THỐNG KÊ

### 5.1 Báo cáo số dư tài khoản VNVC Point
**Stored Procedure**: `rep_BaoCaoSoDuTaiKhoanVNVCPoint`

**Thông tin báo cáo**:
- Số thẻ
- Số tài khoản
- Số dư đầu kỳ
- Phát sinh tăng
- Phát sinh giảm
- Số dư cuối kỳ

### 5.2 Báo cáo chi tiết tài khoản VNVC Point
**Stored Procedure**: `rep_BaoCaoChiTietTaiKhoanVNVCPoint`

**Thông tin báo cáo**:
- Số thẻ
- Số tài khoản
- Ngày giao dịch
- Mã khách hàng
- Tên khách hàng
- Số điện thoại
- Phát sinh tăng/giảm
- Nội dung giao dịch

### 5.3 Báo cáo doanh thu tích lũy
**Stored Procedure**: `JOB_PRECOOK_BaoCaoChiTietDoanhThuVNVC`

**Chức năng**: Tính toán điểm tích lũy dựa trên doanh thu

## 6. TÍCH HỢP VỚI HỆ THỐNG

### 6.1 Tích hợp với hệ thống thanh toán
- **Hình thức thanh toán**: VNVC Point được hiển thị như một phương thức thanh toán
- **Xử lý giao dịch**: Tự động cập nhật số dư khi thanh toán
- **Hoàn tiền**: Hỗ trợ hoàn tiền qua VNVC Point

### 6.2 Tích hợp với hệ thống bán hàng
- **Cửa hàng**: Sử dụng VNVC Point trong bán lẻ
- **Đặt hàng trước**: Hỗ trợ thanh toán bằng điểm
- **Hợp đồng**: Quản lý thanh toán hợp đồng

### 6.3 Tích hợp với hệ thống tiếp nhận
- **Kiểm tra tài khoản**: Xem thông tin VNVC Point của khách hàng
- **Cập nhật thông tin**: Quản lý thông tin tài khoản

## 7. BẢO MẬT VÀ PHÂN QUYỀN

### 7.1 Bảo mật giao dịch
- **Mã hóa thông tin**: Bảo vệ thông tin tài khoản
- **Xác thực giao dịch**: Kiểm tra tính hợp lệ của giao dịch
- **Lưu trữ lịch sử**: Ghi log tất cả giao dịch

### 7.2 Phân quyền người dùng
- **Quản trị viên**: Toàn quyền quản lý hệ thống
- **Nhân viên tiếp nhận**: Xem thông tin và xử lý giao dịch cơ bản
- **Nhân viên thanh toán**: Xử lý thanh toán và hoàn tiền

## 8. XỬ LÝ LỖI VÀ NGOẠI LỆ

### 8.1 Các trường hợp lỗi thường gặp
- **Số dư không đủ**: Khi thanh toán vượt quá số dư
- **Thẻ không hợp lệ**: Thẻ bị khóa hoặc không tồn tại
- **Lỗi kết nối**: Vấn đề về mạng hoặc cơ sở dữ liệu

### 8.2 Xử lý ngoại lệ
- **Rollback giao dịch**: Khôi phục trạng thái khi có lỗi
- **Ghi log lỗi**: Lưu trữ thông tin lỗi để xử lý
- **Thông báo người dùng**: Hiển thị thông báo lỗi rõ ràng

## 9. HIỆU SUẤT VÀ TỐI ƯU HÓA

### 9.1 Tối ưu hóa truy vấn
- **Index cơ sở dữ liệu**: Tối ưu hóa truy vấn báo cáo
- **Stored Procedure**: Sử dụng SP để xử lý logic phức tạp
- **Caching**: Lưu trữ tạm thời dữ liệu thường xuyên truy cập

### 9.2 Monitoring và bảo trì
- **Theo dõi hiệu suất**: Giám sát thời gian phản hồi
- **Dọn dẹp dữ liệu**: Xóa dữ liệu cũ không cần thiết
- **Backup định kỳ**: Sao lưu dữ liệu quan trọng

## 10. KẾ HOẠCH PHÁT TRIỂN

### 10.1 Tính năng dự kiến
- **Ứng dụng di động**: Truy cập VNVC Point qua mobile
- **Tích hợp ví điện tử**: Liên kết với các ví điện tử bên ngoài
- **Chương trình khuyến mãi**: Tích điểm thưởng và ưu đãi

### 10.2 Cải tiến kỹ thuật
- **Microservices**: Chuyển đổi sang kiến trúc microservices
- **API Gateway**: Tập trung hóa quản lý API
- **Real-time processing**: Xử lý giao dịch theo thời gian thực

---

**Ngày cập nhật**: [Ngày hiện tại]  
**Phiên bản**: 1.0  
**Người tạo**: AI Assistant  
**Người duyệt**: [Tên người duyệt]
