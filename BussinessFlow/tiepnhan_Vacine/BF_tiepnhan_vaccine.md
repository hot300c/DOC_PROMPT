# TÀI LIỆU NGHIỆP VỤ: CHỨC NĂNG TAB VACCINE TRONG TRANG TIẾP NHẬN

## 1. TỔNG QUAN CHỨC NĂNG

### 1.1 Định nghĩa
**Tab Vaccine trong trang Tiếp nhận** là một module quan trọng của hệ thống tiếp nhận bệnh nhân, cho phép nhân viên tiếp nhận quản lý việc đặt trước vaccine, tra cứu lịch sử tiêm chủng và quản lý phác đồ tiêm cho bệnh nhân.

### 1.2 Mục đích chính
- **Đặt trước vaccine**: Cho phép bệnh nhân đặt trước các mũi vaccine theo phác đồ
- **Tra cứu lịch sử tiêm**: Xem lịch sử tiêm chủng và trạng thái các mũi vaccine
- **Quản lý phác đồ tiêm**: Theo dõi và cập nhật phác đồ tiêm chủng theo độ tuổi
- **Quản lý công khám**: Tạo và quản lý công khám cho bệnh nhân tiêm vaccine

## 2. KIẾN TRÚC HỆ THỐNG

### 2.1 Cơ sở dữ liệu
Hệ thống Tab Vaccine sử dụng cơ sở dữ liệu `QAHosGenericDB` với các bảng chính:

#### Bảng Vaccine (`L_Product`)
- `ProductID`: ID duy nhất của vaccine
- `ProductName`: Tên vaccine
- `ProductCode`: Mã vaccine
- `IsActive`: Trạng thái hoạt động
- `IsVaccine`: Đánh dấu là vaccine

#### Bảng Nhóm bệnh Vaccine (`L_NhomBenhVaccine`)
- `NhomBenhID`: ID nhóm bệnh
- `NhomBenhName`: Tên nhóm bệnh
- `IsActive`: Trạng thái hoạt động

#### Bảng Phác đồ Vaccine (`L_PhacDoVaccine`)
- `PhacDoID`: ID phác đồ
- `NhomBenhID`: Liên kết với nhóm bệnh
- `ProductID`: Liên kết với vaccine
- `SoMui`: Số mũi tiêm
- `KhoangCach`: Khoảng cách giữa các mũi

#### Bảng Lịch sử tiêm (`CN_ClinicalSession`)
- `ClinicalSessionID`: ID phiên khám
- `PatientID`: ID bệnh nhân
- `ProductID`: ID vaccine
- `NgayTiem`: Ngày tiêm
- `TrangThai`: Trạng thái tiêm

### 2.2 Cấu trúc ứng dụng
Hệ thống được tích hợp vào ứng dụng **Genie** và **QA.Reception_VNVC** với các module chính:

#### Module Tiếp nhận mới
- **Tab Vaccine**: Quản lý đặt trước vaccine và lịch sử tiêm
- **Tab Hợp đồng Vaccine**: Quản lý hợp đồng tiêm chủng
- **Quản lý thông tin bệnh nhân**: Cập nhật thông tin cá nhân

#### Module Vaccine
- **Đặt trước vaccine**: Chọn vaccine và lịch tiêm
- **Quản lý phác đồ**: Theo dõi phác đồ tiêm theo độ tuổi
- **Lịch sử tiêm**: Xem và cập nhật trạng thái tiêm

#### Module Công khám
- **Tạo công khám**: Tạo phiên khám cho bệnh nhân
- **Quản lý phòng khám**: Theo dõi trạng thái phòng khám

## 3. LUỒNG NGHIỆP VỤ CHÍNH

### 3.1 Luồng khởi tạo Tab Vaccine
```
Khởi tạo tiếp nhận → Load thông tin bệnh nhân → Khởi tạo Tab Vaccine → Load danh sách vaccine → Load lịch sử tiêm
```

**Các Stored Procedure được gọi**:
- `ws_Vaccin_NhomBenhVaccine_List`: Lấy danh sách nhóm bệnh vaccine
- `ws_Vaccine_TiepNhan_TabVaccine_List`: Lấy danh sách vaccine cho tab
- `ws_CN_PhysicianAdmission_ThongKePhongKham`: Thống kê phòng khám
- `ws_Vaccine_LichSuTiemVaccine`: Lấy lịch sử tiêm vaccine
- `ws_Vaccine_LichSuTiem`: Lấy lịch sử tiêm chung

### 3.2 Luồng đặt trước vaccine
```
Chọn nhóm bệnh → Chọn vaccine → Chọn phác đồ → Chọn ngày tiêm → Xác nhận đặt trước → Lưu thông tin
```

### 3.3 Luồng tạo công khám
```
Chọn vaccine → Kiểm tra phòng khám → Tạo công khám → Cập nhật trạng thái → Lưu thông tin
```

### 3.4 Luồng lưu thông tin bệnh nhân
```
Click Lưu → Kiểm tra tab active → Lưu thông tin bệnh nhân → Lưu tab Vaccine → Hoàn tất
```

## 4. CÁC CHỨC NĂNG CHI TIẾT

### 4.1 Quản lý nhóm bệnh vaccine
- **Hiển thị danh sách nhóm bệnh**: Dropdown chọn nhóm bệnh vaccine
- **Lọc vaccine theo nhóm bệnh**: Hiển thị vaccine phù hợp với nhóm bệnh đã chọn
- **Cập nhật danh sách vaccine**: Tự động cập nhật khi thay đổi nhóm bệnh

### 4.2 Quản lý danh sách vaccine
- **Hiển thị danh sách vaccine**: Bảng hiển thị các vaccine có thể đặt trước
- **Lọc theo trạng thái**: Hiển thị vaccine theo trạng thái (có thể đặt, đã đặt, đã tiêm)
- **Thông tin vaccine**: Hiển thị tên, mã, giá, trạng thái thanh toán

### 4.3 Quản lý phác đồ tiêm
- **Lấy phác đồ theo độ tuổi**: Tự động lấy phác đồ phù hợp với độ tuổi bệnh nhân
- **Hiển thị mũi tiêm**: Hiển thị các mũi tiêm theo phác đồ
- **Cập nhật trạng thái**: Theo dõi trạng thái từng mũi tiêm

### 4.4 Quản lý lịch sử tiêm
- **Lịch sử tiêm vaccine**: Hiển thị các mũi vaccine đã tiêm
- **Lịch sử tiêm chung**: Hiển thị lịch sử tiêm các loại vaccine khác
- **Thống kê phòng khám**: Hiển thị thông tin phòng khám và bác sĩ

### 4.5 Quản lý công nợ
- **Hiển thị công nợ**: Theo dõi số tiền còn nợ của bệnh nhân
- **Cập nhật trạng thái thanh toán**: Theo dõi trạng thái thanh toán vaccine

## 5. BÁO CÁO VÀ THỐNG KÊ

### 5.1 Báo cáo danh sách vaccine tiếp nhận
**Stored Procedure**: `ws_Vaccine_TiepNhan_TabVaccine_List`

**Thông tin báo cáo**:
- Danh sách vaccine có thể đặt trước
- Trạng thái vaccine (có thể đặt, đã đặt, đã tiêm)
- Thông tin giá và thanh toán
- Lịch tiêm dự kiến

### 5.2 Báo cáo lịch sử tiêm vaccine
**Stored Procedure**: `ws_Vaccine_LichSuTiemVaccine`

**Thông tin báo cáo**:
- Các mũi vaccine đã tiêm
- Ngày tiêm và trạng thái
- Thông tin bác sĩ và phòng khám

### 5.3 Báo cáo thống kê phòng khám
**Stored Procedure**: `ws_CN_PhysicianAdmission_ThongKePhongKham`

**Chức năng**: Thống kê thông tin phòng khám và bác sĩ

## 6. TÍCH HỢP VỚI HỆ THỐNG

### 6.1 Tích hợp với hệ thống tiếp nhận
- **Quản lý thông tin bệnh nhân**: Liên kết với thông tin cá nhân bệnh nhân
- **Quản lý tiếp nhận**: Tích hợp với quy trình tiếp nhận chung
- **Lưu thông tin**: Đồng bộ với việc lưu thông tin bệnh nhân

### 6.2 Tích hợp với hệ thống vaccine
- **Quản lý danh mục vaccine**: Liên kết với danh mục vaccine hệ thống
- **Quản lý phác đồ**: Tích hợp với phác đồ tiêm chủng
- **Lịch sử tiêm**: Đồng bộ với hệ thống lịch sử tiêm

### 6.3 Tích hợp với hệ thống thanh toán
- **Quản lý công nợ**: Liên kết với hệ thống thanh toán
- **Trạng thái thanh toán**: Theo dõi trạng thái thanh toán vaccine
- **Cập nhật thanh toán**: Đồng bộ khi có thay đổi thanh toán

### 6.4 Tích hợp với hệ thống khám bệnh
- **Tạo công khám**: Tích hợp với hệ thống tạo phiên khám
- **Quản lý phòng khám**: Liên kết với hệ thống quản lý phòng khám
- **Cập nhật trạng thái**: Đồng bộ trạng thái khám bệnh

## 7. BẢO MẬT VÀ PHÂN QUYỀN

### 7.1 Bảo mật dữ liệu
- **Mã hóa thông tin bệnh nhân**: Bảo vệ thông tin cá nhân bệnh nhân
- **Kiểm tra quyền truy cập**: Xác thực người dùng trước khi truy cập
- **Lưu trữ lịch sử**: Ghi log tất cả thao tác thay đổi

### 7.2 Phân quyền người dùng
- **Nhân viên tiếp nhận**: Xem và cập nhật thông tin vaccine
- **Nhân viên y tế**: Quản lý phác đồ và lịch sử tiêm
- **Quản trị viên**: Toàn quyền quản lý hệ thống vaccine

## 8. XỬ LÝ LỖI VÀ NGOẠI LỆ

### 8.1 Các trường hợp lỗi thường gặp
- **Vaccine không tồn tại**: Khi vaccine đã chọn không còn trong hệ thống
- **Phác đồ không phù hợp**: Khi độ tuổi bệnh nhân không phù hợp với phác đồ
- **Lỗi kết nối cơ sở dữ liệu**: Vấn đề về mạng hoặc cơ sở dữ liệu
- **Trùng lịch tiêm**: Khi có lịch tiêm trùng với thời gian đã chọn

### 8.2 Xử lý ngoại lệ
- **Rollback giao dịch**: Khôi phục trạng thái khi có lỗi
- **Ghi log lỗi**: Lưu trữ thông tin lỗi để xử lý
- **Thông báo người dùng**: Hiển thị thông báo lỗi rõ ràng
- **Kiểm tra tính hợp lệ**: Validate dữ liệu trước khi xử lý

## 9. HIỆU SUẤT VÀ TỐI ƯU HÓA

### 9.1 Tối ưu hóa truy vấn
- **Index cơ sở dữ liệu**: Tối ưu hóa truy vấn vaccine và lịch sử
- **Stored Procedure**: Sử dụng SP để xử lý logic phức tạp
- **Caching**: Lưu trữ tạm thời dữ liệu thường xuyên truy cập

### 9.2 Monitoring và bảo trì
- **Theo dõi hiệu suất**: Giám sát thời gian phản hồi của các SP
- **Dọn dẹp dữ liệu**: Xóa dữ liệu cũ không cần thiết
- **Backup định kỳ**: Sao lưu dữ liệu vaccine quan trọng

## 10. KẾ HOẠCH PHÁT TRIỂN

### 10.1 Tính năng dự kiến
- **Tích hợp lịch tiêm**: Liên kết với lịch tiêm tự động
- **Thông báo nhắc nhở**: Gửi thông báo nhắc nhở tiêm vaccine
- **Báo cáo tiêm chủng**: Báo cáo chi tiết về tiêm chủng theo thời gian
- **Quản lý vaccine theo nhóm**: Quản lý vaccine theo nhóm bệnh nhân

### 10.2 Cải tiến kỹ thuật
- **API RESTful**: Chuyển đổi sang kiến trúc API hiện đại
- **Real-time updates**: Cập nhật thông tin theo thời gian thực
- **Mobile app**: Phát triển ứng dụng di động cho bệnh nhân
- **AI hỗ trợ**: Sử dụng AI để gợi ý phác đồ tiêm tối ưu

---

**Ngày cập nhật**: 08/01/2025  
**Phiên bản**: 1.0  
**Người tạo**: AI Assistant  
**Người duyệt**: [Tên người duyệt]
