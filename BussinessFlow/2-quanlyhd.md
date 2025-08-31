
## 🏥 **TIẾP NHẬN** - Quản lý tiếp nhận bệnh nhân

### 📋 Quản lý hợp đồng
- **Chức năng**: Quản lý các hợp đồng tiêm chủng, dịch vụ y tế
- **Ý nghĩa**: Theo dõi cam kết dịch vụ, lịch trình tiêm chủng, thanh toán
- **Đối tượng sử dụng**: Nhân viên tiếp nhận, quản lý

### Link: 
https://dev-genie.vnvc.info/tiep-nhan/quan-ly-hop-dong

---

## 🔍 **CHI TIẾT TRANG QUẢN LÝ HỢP ĐỒNG**

### 📊 **Cấu trúc trang**
Trang Quản lý hợp đồng được chia thành 3 phần chính:
1. **Form Filter** - Bộ lọc tìm kiếm
2. **Data Table** - Bảng dữ liệu hợp đồng
3. **Footer Actions** - Các nút thao tác

---

## 🔍 **1. FORM FILTER - Bộ lọc tìm kiếm**

### 📅 **Bộ lọc theo thời gian**
- **Từ ngày**: Chọn ngày bắt đầu tìm kiếm
- **Đến ngày**: Chọn ngày kết thúc tìm kiếm
- **Mặc định**: Ngày hiện tại

### 🏥 **Bộ lọc theo cơ sở**
- **Cơ sở**: Dropdown chọn trung tâm/chi nhánh
- **Mặc định**: Cơ sở của user hiện tại
- **Quyền**: Chỉ hiển thị cơ sở được phân quyền

### 🔍 **Tìm kiếm theo tiêu chí**
- **Nhập tiêu chí tìm kiếm**: Text input
- **Placeholder**: "Nhập mã khách hàng/ mã hợp đồng"
- **Chức năng**: Tìm kiếm theo mã KH hoặc mã hợp đồng

### 🔘 **Nút thao tác**
- **Nút "Lọc"**: Áp dụng bộ lọc thời gian và cơ sở
- **Nút "Tìm kiếm"**: Thực hiện tìm kiếm theo tiêu chí

---

## 📋 **2. DATA TABLE - Bảng dữ liệu hợp đồng**

### 📊 **Các cột thông tin**

#### **Thông tin khách hàng:**
- **Mã KH**: Mã bệnh nhân trong hệ thống
- **Khách tiêm**: Tên người được tiêm vaccine
- **Người đăng ký**: Tên người đăng ký hợp đồng
- **SĐT**: Số điện thoại liên hệ

#### **Thông tin hợp đồng:**
- **Số H.Đồng**: Mã số hợp đồng
- **Ngày HĐ**: Ngày ký hợp đồng
- **Gói tiêm**: Tên gói vaccine/dịch vụ
- **Ghi chú gói**: Mô tả chi tiết gói dịch vụ

#### **Thông tin tài chính:**
- **Giá trị HĐ**: Tổng giá trị hợp đồng
- **Giá trị HĐ tính miễn giảm**: Giá trị sau tính toán miễn giảm
- **%**: Phần trăm giảm giá
- **Tiền giảm**: Số tiền được giảm
- **G.Trị HĐ sau giảm**: Giá trị cuối cùng
- **TTĐT**: Tổng tiền đã thanh toán
- **TTCT**: Tổng tiền còn thiếu

#### **Thông tin tiêm chủng:**
- **SL mũi**: Tổng số mũi tiêm trong hợp đồng
- **SLĐT**: Số lượng đã tiêm
- **SLCT**: Số lượng chưa tiêm
- **% GG Còn lại**: Phần trăm giảm giá còn lại

#### **Thông tin khác:**
- **Trung tâm đăng ký**: Cơ sở đăng ký hợp đồng
- **Người tạo H.Đồng**: Nhân viên tạo hợp đồng
- **Thu hồi giảm giá**: Số tiền giảm giá bị thu hồi
- **Hủy**: Checkbox trạng thái hủy hợp đồng

### 🔘 **Cột thao tác**
- **Nút "In"**: In hợp đồng (dấu "..." trong button)
- **Chức năng**: Mở modal in hợp đồng PDF

### 📊 **Tính năng bảng**
- **Sắp xếp**: Click header để sắp xếp
- **Lọc cột**: Bộ lọc theo từng cột
- **Tìm kiếm**: Tìm kiếm toàn bộ dữ liệu
- **Phân trang**: Hiển thị theo trang
- **Chọn dòng**: Click để chọn hợp đồng
- **Double click**: Mở chi tiết hợp đồng

---

## 🔘 **3. FOOTER ACTIONS - Các nút thao tác**

### 📊 **Nút Excel**
- **Chức năng**: Xuất dữ liệu ra file Excel
- **Nội dung**: Tất cả hợp đồng trong bảng + tổng cộng
- **Format**: File .xlsx với định dạng tiền tệ
- **Tên file**: "contracts.xlsx"

### 🔄 **Nút Đổi** (Có điều kiện)
- **Quyền**: `CONTRACT_MANAGEMENT_CHANGE_INJECTION`
- **Chức năng**: Thay đổi mũi tiêm trong hợp đồng
- **Ràng buộc**: Chỉ hiển thị khi có quyền

### ❌ **Nút Hủy** (Có điều kiện)
- **Quyền**: `CONTRACT_MANAGEMENT_CANCEL_INJECTION`
- **Chức năng**: Hủy mũi tiêm trong hợp đồng
- **Ràng buộc**: Chỉ hiển thị khi có quyền

### 💰 **Nút Điều chỉnh giá** (Có điều kiện)
- **Quyền**: `RECEPTION_ADJUST_PRICE`
- **Chức năng**: Thay đổi giá trị hợp đồng
- **Ràng buộc**: Chỉ hiển thị khi có quyền

### 📋 **Nút Tra cứu phụ lục**
- **Chức năng**: Mở modal tra cứu phụ lục hợp đồng
- **Nội dung**: Danh sách phụ lục của hợp đồng

### 👁️ **Nút Xem chi tiết**
- **Chức năng**: Mở modal xem chi tiết hợp đồng
- **Nội dung**: Thông tin đầy đủ về hợp đồng

---

## 📋 **4. MODAL CHI TIẾT HỢP ĐỒNG**

### 📊 **Header thông tin**
- **Tiêu đề**: "Thông tin hợp đồng"
- **Thông tin cơ bản**: Tên khách hàng, người thụ hưởng, số hợp đồng
- **Thông tin tài chính**: Giá trị hợp đồng, số tiền còn lại

### 📋 **Các tab thông tin**
1. **Bảng đã tiêm**: Danh sách các mũi đã tiêm
2. **Bảng chưa tiêm**: Danh sách các mũi chưa tiêm
3. **Bảng đã hủy**: Danh sách các mũi đã hủy
4. **Bảng biên lai**: Lịch sử thanh toán

---

## 🔐 **5. PHÂN QUYỀN VÀ RÀNG BUỘC**

### 👤 **Quyền truy cập**
- **CONTRACT_MANAGEMENT_CHANGE_INJECTION**: Đổi mũi tiêm
- **CONTRACT_MANAGEMENT_CANCEL_INJECTION**: Hủy mũi tiêm
- **RECEPTION_ADJUST_PRICE**: Điều chỉnh giá

### 🔒 **Ràng buộc nghiệp vụ**
- **Chỉ xem hợp đồng của cơ sở được phân quyền**
- **Không thể sửa hợp đồng đã thanh toán hoàn tất**
- **Cần quyền để thực hiện các thao tác quan trọng**
- **Hợp đồng hủy không thể chỉnh sửa**

### 🔗 **Liên kết hệ thống**
- **Kết nối với module VNVC Point**: Quản lý thanh toán
- **Tích hợp với kho vaccine**: Kiểm tra tồn kho
- **Liên kết với lịch sử tiêm**: Theo dõi tiến độ
- **Đồng bộ với báo cáo**: Xuất báo cáo tài chính

---

## 📊 **6. LOGIC NGHIỆP VỤ**

### 🔄 **Luồng xử lý chính**
1. **Tải dữ liệu**: Theo bộ lọc thời gian và cơ sở
2. **Hiển thị bảng**: Danh sách hợp đồng
3. **Chọn hợp đồng**: Click để chọn
4. **Thực hiện thao tác**: Theo quyền hạn
5. **Cập nhật dữ liệu**: Refresh bảng

### 📈 **Tính toán tự động**
- **Tổng cộng**: Tự động tính tổng các cột số
- **Phần trăm**: Tính % giảm giá còn lại
- **Số mũi**: Đếm mũi đã tiêm/chưa tiêm
- **Tiền tệ**: Format tiền tệ theo định dạng VND

### 🔍 **Tìm kiếm và lọc**
- **Tìm kiếm nhanh**: Theo mã KH hoặc mã hợp đồng
- **Lọc theo thời gian**: Khoảng thời gian cụ thể
- **Lọc theo cơ sở**: Chỉ xem hợp đồng của cơ sở
- **Sắp xếp**: Theo bất kỳ cột nào

---

## 🎯 **7. TÍNH NĂNG ĐẶC BIỆT**

### 📄 **In hợp đồng**
- **Format**: PDF
- **Nội dung**: Thông tin đầy đủ hợp đồng
- **Cấu hình**: Theo base setting "HopDongVaccine"

### 📊 **Xuất Excel**
- **Format**: .xlsx với định dạng chuyên nghiệp
- **Nội dung**: Tất cả dữ liệu + tổng cộng
- **Cấu hình cột**: Định dạng tiền tệ, căn lề

### 🔄 **Real-time cập nhật**
- **Auto refresh**: Khi có thay đổi dữ liệu
- **Loading state**: Hiển thị trạng thái tải
- **Error handling**: Xử lý lỗi gracefully

---

## 📝 **8. GHI CHÚ KỸ THUẬT**

### 🏗️ **Kiến trúc**
- **Component-based**: Chia nhỏ thành các component
- **Context Provider**: Quản lý state toàn cục
- **Custom Hooks**: Tái sử dụng logic
- **TypeScript**: Type safety

### 🔧 **Performance**
- **Virtual scrolling**: Cho bảng lớn
- **Lazy loading**: Tải dữ liệu theo nhu cầu
- **Memoization**: Tối ưu re-render
- **Debounce**: Tối ưu tìm kiếm

### 🐛 **Error Handling**
- **Loading states**: Hiển thị trạng thái tải
- **Error boundaries**: Bắt lỗi component
- **Fallback UI**: Giao diện dự phòng
- **User feedback**: Thông báo lỗi rõ ràng 
