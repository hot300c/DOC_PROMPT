## 🏥 **TIẾP NHẬN** - Quản lý tiếp nhận bệnh nhân

### 📝 Tiếp Nhận Mới
- **Chức năng**: Tiếp nhận bệnh nhân mới vào hệ thống
- **Ý nghĩa**: Tạo hồ sơ bệnh nhân, đăng ký thông tin cá nhân, lịch sử bệnh án
- **Đối tượng sử dụng**: Nhân viên tiếp nhận, nhân viên y tế

#### 🔍 **Các Tabs trong Trang Tiếp Nhận Mới**

##### 1. **Tab Vaccine** (Tab đầu tiên)
- **Chức năng**: Quản lý đặt trước vaccine và lịch sử tiêm chủng
- **Nội dung chính**:
  - Đặt trước vaccine theo phác đồ
  - Tra cứu lịch sử tiêm chủng
  - Quản lý phác đồ tiêm theo độ tuổi
  - Tạo công khám cho bệnh nhân tiêm vaccine
- **Logic nghiệp vụ**:
  - Không cần hợp đồng, có thể đặt trước vaccine độc lập
  - Tự động tính toán phác đồ dựa trên ngày sinh
  - Kiểm tra lịch sử tiêm để tránh trùng lặp
- **Ràng buộc**:
  - Phải có thông tin bệnh nhân trước khi đặt vaccine
  - Kiểm tra độ tuổi phù hợp với loại vaccine
  - Xác nhận sức khỏe trước tiêm

##### 2. **Tab Hợp Đồng** (Tab thứ hai)
- **Chức năng**: Quản lý hợp đồng tiêm chủng cơ bản
- **Nội dung chính**:
  - Xem lịch sử hợp đồng của bệnh nhân
  - Quản lý các gói dịch vụ đã mua
  - Theo dõi trạng thái thanh toán
- **Logic nghiệp vụ**:
  - Hiển thị tất cả hợp đồng đã ký kết
  - Cho phép xem chi tiết và in hợp đồng
  - Kiểm tra quyền in hợp đồng (phải đặt trước)
- **Ràng buộc**:
  - Chỉ hiển thị hợp đồng của bệnh nhân hiện tại
  - Cần quyền để in hợp đồng

##### 3. **Tab Hợp Đồng Vaccine** (Tab thứ ba)
- **Chức năng**: Quản lý hợp đồng vaccine chi tiết
- **Nội dung chính**:
  - Danh sách hợp đồng vaccine
  - Đăng ký hợp đồng mới
  - Chi tiết phác đồ vaccine trong hợp đồng
- **Logic nghiệp vụ**:
  - Tích hợp giữa hợp đồng và vaccine
  - Cho phép tạo hợp đồng với phác đồ vaccine cụ thể
  - Quản lý lịch trình tiêm theo hợp đồng
- **Ràng buộc**:
  - Phải chọn hợp đồng trước khi xem chi tiết
  - Cần quyền để tạo/sửa hợp đồng

### 📋 Quản lý hợp đồng
- **Chức năng**: Quản lý các hợp đồng tiêm chủng, dịch vụ y tế
- **Ý nghĩa**: Theo dõi cam kết dịch vụ, lịch trình tiêm chủng, thanh toán
- **Đối tượng sử dụng**: Nhân viên tiếp nhận, quản lý

---

## 🤔 **TRẢ LỜI CÂU HỎI**

### **Hỏi 1: Logic các tabs và thứ tự?**

#### **Thứ tự xuất hiện:**
1. **Tab Vaccine** → 2. **Tab Hợp Đồng** → 3. **Tab Hợp Đồng Vaccine**

#### **Logic nghiệp vụ:**

**🔹 Tab Vaccine có trước vì:**
- Đây là chức năng cơ bản nhất, không phụ thuộc vào hợp đồng
- Bệnh nhân có thể tiêm vaccine đơn lẻ mà không cần mua gói
- Phục vụ cho tiêm chủng mở rộng và tiêm dịch vụ cơ bản
- Tự động tính toán phác đồ dựa trên độ tuổi

**🔹 Tab Hợp Đồng xuất hiện sau vì:**
- Hiển thị lịch sử các gói dịch vụ đã mua
- Cần có dữ liệu bệnh nhân trước
- Phục vụ cho việc tra cứu và quản lý

**🔹 Tab Hợp Đồng Vaccine cuối cùng vì:**
- Tích hợp cả hợp đồng và vaccine
- Cần hiểu rõ cả hai khái niệm trước
- Phức tạp nhất về logic nghiệp vụ

#### **Có thể chỉ dùng Tab Vaccine không?**

**✅ CÓ THỂ** - Tab Vaccine hoạt động độc lập:

**🔸 Trường hợp sử dụng:**
- Tiêm vaccine đơn lẻ (không mua gói)
- Tiêm chủng mở rộng
- Tiêm dịch vụ cơ bản
- Khám sức khỏe trước tiêm

**🔸 Logic hoạt động:**
- Không cần hợp đồng
- Tự động tính phác đồ theo độ tuổi
- Lưu lịch sử tiêm chủng
- Tạo công khám riêng

**🔸 Ràng buộc:**
- Vẫn cần thông tin bệnh nhân đầy đủ
- Kiểm tra sức khỏe trước tiêm
- Tuân thủ lịch tiêm chủng

---

## 📋 **TÓM TẮT LOGIC NGHIỆP VỤ**

### **Luồng xử lý chính:**
1. **Tiếp nhận bệnh nhân** → Nhập thông tin cơ bản
2. **Chọn tab phù hợp** → Dựa trên nhu cầu
3. **Xử lý nghiệp vụ** → Theo logic từng tab
4. **Lưu thông tin** → Cập nhật hệ thống

### **Quyền truy cập:**
- **RECEPTION_SHOW_VACCINE_TAB**: Quyền xem tab Vaccine
- **RECEPTION_SHOW_VACCINE_CONTRACT_TAB**: Quyền xem tab Hợp đồng
- **RECEPTION_CHANGE_APPOINTMENT_ORDER**: Quyền chỉnh sửa thứ tự

### **Tích hợp hệ thống:**
- Kết nối với module VNVC Point
- Tích hợp với hệ thống thanh toán
- Liên kết với kho vaccine
- Đồng bộ với lịch sử bệnh án
