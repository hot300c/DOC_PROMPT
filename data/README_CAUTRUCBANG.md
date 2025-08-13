# CẤU TRÚC BẢNG QAHosGenericDB

## Tổng quan hệ thống

QAHosGenericDB là cơ sở dữ liệu chính của hệ thống quản lý tiêm chủng vaccine, được thiết kế để quản lý toàn bộ quy trình từ:
đăng ký,
lập phác đồ,
lịch hẹn,
tiêm chủng đến theo dõi sau tiêm.

## Cấu trúc thư mục

```
QAHosGenericDB/
├── Tables/           # Các bảng dữ liệu chính
├── Procedures/       # Stored procedures xử lý nghiệp vụ
├── Functions/        # Các hàm tiện ích
├── UserDefinedTypes/ # Kiểu dữ liệu tùy chỉnh
├── Storage/          # Cấu hình lưu trữ
└── DatabaseTriggers/ # Triggers tự động
```

## Phân loại bảng theo chức năng

### 1. QUẢN LÝ PHÁC ĐỒ TIÊM CHỦNG

#### Vaccine_PhacDoBenhNhan

**Mục đích**: Bảng chính lưu trữ phác đồ tiêm chủng của từng bệnh nhân
**Ý nghĩa**: Quản lý thông tin phác đồ tiêm chủng được áp dụng cho bệnh nhân

**Các trường chính**:

- `IDPhacDoBenhNhan`: Khóa chính, định danh phác đồ bệnh nhân
- `IDPhacDo`: ID phác đồ tiêm chủng
- `NhomBenhID`: ID nhóm bệnh
- `PatientID`: ID bệnh nhân
- `FacAdmissionID`: ID phiếu nhập viện
- `NgayTao`: Ngày tạo phác đồ
- `NgayDong`: Ngày đóng phác đồ
- `IsLocked`: Trạng thái khóa
- `LieuDung`: Liều dùng
- `IsHenDacBiet`: Có phải hẹn đặc biệt không

#### Vaccine_PhacDoBenhNhan_Detail

**Mục đích**: Chi tiết từng mũi tiêm trong phác đồ
**Ý nghĩa**: Quản lý thông tin chi tiết của từng mũi tiêm

**Các trường chính**:

- `IDPhacDoBenhNhan_Detail`: Khóa chính
- `IDPhacDoBenhNhan`: Tham chiếu đến phác đồ bệnh nhân
- `IDPhacDo_Detail`: ID chi tiết phác đồ
- `ClinicalSessionID`: ID phiên khám
- `NgayHenTiem`: Ngày hẹn tiêm
- `IsGoi`: Đã gọi chưa
- `IsChiDinh`: Đã chỉ định chưa
- `CompleteOn`: Ngày hoàn thành
- `IsTiemNgoai`: Tiêm ngoài bệnh viện
- `STT`: Số thứ tự

### 2. QUẢN LÝ HỢP ĐỒNG

#### Vaccine_HopDong

**Mục đích**: Quản lý hợp đồng tiêm chủng
**Ý nghĩa**: Lưu trữ thông tin hợp đồng giữa khách hàng và trung tâm tiêm chủng

**Các trường chính**:

- `HopDongID`: Khóa chính
- `SoHDong`: Số hợp đồng
- `TenDangKy`: Tên người đăng ký
- `TenSuDung`: Tên người sử dụng
- `GiaTriHD`: Giá trị hợp đồng
- `PatientID`: ID bệnh nhân
- `IsPaid`: Đã thanh toán chưa
- `IsDone`: Đã hoàn thành chưa
- `NgayHopDong`: Ngày ký hợp đồng
- `ThoiHanHopDong`: Thời hạn hợp đồng

#### Vaccine_HopDong_Detail

**Mục đích**: Chi tiết các mũi tiêm trong hợp đồng
**Ý nghĩa**: Quản lý từng mũi tiêm cụ thể trong hợp đồng

**Các trường chính**:

- `HopDongDetailID`: Khóa chính
- `HopDongID`: Tham chiếu hợp đồng
- `MaChung`: Mã chủng vaccine
- `MaMuiTiem`: Số mũi tiêm
- `ServicePackageID`: ID gói dịch vụ
- `GiaMuiTiem`: Giá mũi tiêm
- `PhanTramGiam`: Phần trăm giảm giá
- `IsTiemNgoai`: Tiêm ngoài bệnh viện
- `IsHuyMui`: Hủy mũi tiêm
- `AmountPaid`: Số tiền đã thanh toán

### 3. QUẢN LÝ DANH SÁCH CHỜ KHÁM

#### Vaccine_DanhSachChoKham

**Mục đích**: Quản lý danh sách bệnh nhân chờ khám
**Ý nghĩa**: Sắp xếp thứ tự khám bệnh cho bệnh nhân

**Các trường chính**:

- `PhysicianAdmissionID`: Khóa chính
- `STT`: Số thứ tự
- `PatientID`: ID bệnh nhân
- `FacAdmissionID`: ID phiếu nhập viện
- `RoomID`: ID phòng khám
- `IsDangGoi`: Đang gọi
- `IsDangKham`: Đang khám
- `IsHoanTat`: Đã hoàn tất
- `Ngay`: Ngày khám

#### Vaccine_DanhSachChoKham_New

**Mục đích**: Danh sách chờ khám phiên bản mới
**Ý nghĩa**: Cải tiến quy trình quản lý danh sách chờ

### 4. QUẢN LÝ DANH SÁCH CHỜ TIÊM

#### Vaccine_DanhSachChoTiem

**Mục đích**: Quản lý danh sách bệnh nhân chờ tiêm
**Ý nghĩa**: Sắp xếp thứ tự tiêm chủng

#### Vaccine_DanhSachChoTiem_DangTiem

**Mục đích**: Danh sách bệnh nhân đang tiêm
**Ý nghĩa**: Theo dõi trạng thái tiêm chủng hiện tại

#### Vaccine_DanhSachChoTiem_DaTiem

**Mục đích**: Danh sách bệnh nhân đã tiêm
**Ý nghĩa**: Lưu trữ lịch sử tiêm chủng

### 5. THEO DÕI SAU TIÊM

#### Vaccine_TheoDoiSauTiem

**Mục đích**: Theo dõi tình trạng bệnh nhân sau tiêm
**Ý nghĩa**: Đảm bảo an toàn và hiệu quả vaccine

**Các trường chính**:

- `ClinicalSessionID`: ID phiên khám
- `PatientID`: ID bệnh nhân
- `ProductID`: ID sản phẩm vaccine
- `TrangThai`: Trạng thái theo dõi
- `TinhTrang`: Tình trạng sức khỏe
- `NhietDo`: Nhiệt độ
- `ToanThan`: Triệu chứng toàn thân
- `TaiVetTiem`: Tại vết tiêm
- `CompleteOn`: Ngày hoàn thành theo dõi

#### Vaccine_TheoDoiSauTiem_Today

**Mục đích**: Theo dõi sau tiêm trong ngày
**Ý nghĩa**: Báo cáo nhanh tình trạng hiện tại

#### Vaccine_TheoDoiSauTiem_TrongNgay

**Mục đích**: Theo dõi sau tiêm trong ngày (chi tiết)
**Ý nghĩa**: Quản lý theo dõi theo ngày

### 6. QUẢN LÝ CÂU HỎI KHÁM BỆNH

#### Vaccine_CauHoiBenhNhan

**Mục đích**: Lưu trữ câu trả lời câu hỏi khám bệnh
**Ý nghĩa**: Đánh giá tình trạng sức khỏe trước tiêm

**Các trường chính**:

- `PatientID`: ID bệnh nhân
- `FacAdmissionID`: ID phiếu nhập viện
- `IDCauHoi`: ID câu hỏi
- `Value`: Giá trị trả lời (true/false)
- `Note`: Ghi chú
- `XuLyTaiTrungTam`: Xử lý tại trung tâm
- `XuLyTaiNha`: Xử lý tại nhà

#### Vaccine_CauHoiBenhNhan_SauTiem

**Mục đích**: Câu hỏi sau tiêm
**Ý nghĩa**: Đánh giá tác dụng phụ

#### Vaccine_CauHoiKhamBenh

**Mục đích**: Danh mục câu hỏi khám bệnh
**Ý nghĩa**: Quản lý bộ câu hỏi chuẩn

### 7. QUẢN LÝ LỊCH HẸN

#### Vaccine_LichHenNhacLai

**Mục đích**: Quản lý lịch hẹn nhắc lại
**Ý nghĩa**: Đảm bảo bệnh nhân tiêm đúng lịch

**Các trường chính**:

- `IDHenNhacLai`: Khóa chính
- `PatientID`: ID bệnh nhân
- `ClininicalSessionID`: ID phiên khám
- `MaChung`: Mã chủng vaccine
- `NhomBenhID`: ID nhóm bệnh
- `NgayHen`: Ngày hẹn
- `CompletedOn`: Ngày hoàn thành

### 8. QUẢN LÝ THỜI GIAN PHÒNG TIÊM

#### Vaccine_TimeRecord_PhongTiem

**Mục đích**: Ghi nhận thời gian tại phòng tiêm
**Ý nghĩa**: Theo dõi hiệu suất phòng tiêm

**Các trường chính**:

- `ClinicalSessionID`: ID phiên khám
- `RoomID`: ID phòng tiêm
- `DuocTiemLuc`: Thời điểm được tiêm
- `HoanTatTiem`: Thời điểm hoàn tất tiêm

### 9. TÍCH HỢP WEBSITE

#### Vaccine_FromWebsite_API

**Mục đích**: Dữ liệu đăng ký từ website
**Ý nghĩa**: Tích hợp đăng ký online

**Các trường chính**:

- `ID`: Khóa chính
- `FullName`: Họ tên đầy đủ
- `CustomerID`: Mã khách hàng
- `Gender`: Giới tính
- `ParentName`: Tên phụ huynh
- `Address`: Địa chỉ
- `DoB`: Ngày sinh
- `Email`: Email
- `PhoneNumber`: Số điện thoại
- `TypeVaccine`: Loại vaccine
- `NameVaccine`: Tên vaccine
- `DateToDo`: Ngày thực hiện
- `IsDuyet`: Đã duyệt chưa

#### Vaccine_FromWebsite_Appointment

**Mục đích**: Lịch hẹn từ website
**Ý nghĩa**: Quản lý đặt lịch online

#### Vaccine_FromWebsite_Complete

**Mục đích**: Hoàn thành đăng ký từ website
**Ý nghĩa**: Xác nhận hoàn tất quy trình online

### 10. QUẢN LÝ SMS

#### Vaccine_SMS_Config

**Mục đích**: Cấu hình SMS
**Ý nghĩa**: Thiết lập thông báo SMS

#### Vaccine_SMS_LogRunning

**Mục đích**: Log chạy SMS
**Ý nghĩa**: Theo dõi việc gửi SMS

### 11. QUẢN LÝ VACCINE SỬ DỤNG THỰC TẾ

#### Vaccine_VaccineSuDungThucTe

**Mục đích**: Quản lý vaccine sử dụng thực tế
**Ý nghĩa**: Theo dõi lượng vaccine đã sử dụng

### 12. CÁC BẢNG TẠM THỜI (TMP)

#### TMP\_\*

**Mục đích**: Các bảng tạm thời cho xử lý dữ liệu
**Ý nghĩa**: Hỗ trợ các thao tác tạm thời

### 13. BẢNG LOG VÀ AUDIT

#### XMLLog

**Mục đích**: Log các thao tác XML
**Ý nghĩa**: Theo dõi giao dịch dữ liệu

## Mối quan hệ giữa các bảng

### Quan hệ chính:

1. **Vaccine_PhacDoBenhNhan** ↔ **Vaccine_PhacDoBenhNhan_Detail**

   - 1:N (Một phác đồ có nhiều chi tiết mũi tiêm)

2. **Vaccine_HopDong** ↔ **Vaccine_HopDong_Detail**

   - 1:N (Một hợp đồng có nhiều chi tiết mũi tiêm)

3. **Vaccine_PhacDoBenhNhan** ↔ **Vaccine_DanhSachChoKham**

   - N:1 (Nhiều phác đồ có thể cùng một danh sách chờ)

4. **Vaccine_PhacDoBenhNhan_Detail** ↔ **Vaccine_TheoDoiSauTiem**

   - 1:1 (Mỗi mũi tiêm có một bản ghi theo dõi)

5. **Vaccine_FromWebsite_API** ↔ **Vaccine_DanhSachChoKham**
   - 1:1 (Đăng ký online tạo ra danh sách chờ)

## Các trường chung trong hệ thống

### Trường audit:

- `CreatedBy`: Người tạo
- `CreatedOn`: Ngày tạo
- `ModifiedBy`: Người sửa
- `ModifiedOn`: Ngày sửa
- `IPUser`: IP người dùng
- `MacAddressUser`: MAC address

### Trường nghiệp vụ:

- `FacID`: Mã cơ sở y tế
- `PatientID`: ID bệnh nhân
- `FacAdmissionID`: ID phiếu nhập viện
- `ClinicalSessionID`: ID phiên khám

### Trường thời gian:

- `NgayTaoAsInt`: Ngày tạo dạng số (YYYYMMDD)
- `NgayDongAsInt`: Ngày đóng dạng số
- `CreatedDateAsInt`: Ngày tạo dạng số

## Lưu ý quan trọng

1. **Bảo mật dữ liệu**: Một số trường nhạy cảm được mã hóa (CMND, CCCD, Passport)
2. **Index tối ưu**: Hệ thống có nhiều index để tối ưu hiệu suất truy vấn
3. **Audit trail**: Tất cả thao tác đều được ghi log
4. **Tính nhất quán**: Sử dụng UNIQUEIDENTIFIER cho khóa chính
5. **Mở rộng**: Thiết kế hỗ trợ nhiều cơ sở y tế (FacID)

## Hướng dẫn sử dụng

### Để thêm bệnh nhân mới:

1. Tạo record trong `Vaccine_PhacDoBenhNhan`
2. Thêm chi tiết vào `Vaccine_PhacDoBenhNhan_Detail`
3. Tạo hợp đồng trong `Vaccine_HopDong` (nếu cần)
4. Thêm vào danh sách chờ `Vaccine_DanhSachChoKham`

### Để theo dõi tiêm chủng:

1. Cập nhật trạng thái trong `Vaccine_PhacDoBenhNhan_Detail`
2. Ghi nhận thời gian trong `Vaccine_TimeRecord_PhongTiem`
3. Tạo record theo dõi trong `Vaccine_TheoDoiSauTiem`

### Để quản lý lịch hẹn:

1. Tạo lịch hẹn trong `Vaccine_LichHenNhacLai`
2. Cập nhật trạng thái trong `Vaccine_DanhSachChoKham`
3. Gửi thông báo qua SMS (nếu được cấu hình)
