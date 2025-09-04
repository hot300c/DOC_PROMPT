# TASK 3: SỬA LỖI TRANG QUẢN LÝ TẬP TRUNG

## Mô tả vấn đề

**Trang quản lý tập trung** đang hiển thị **8** khách hàng, trong khi **Trang cửa hàng** (tabs CHI TIẾT DOANH THU → biên lai chi tiết) hiển thị **9** khách hàng (môi trường production).

**Root cause:** Trang quản lý tập trung đang hiển thị thiếu 1 số khách hàng.

## Link trang quản lý tập trung

```
https://dev-genie.vnvc.info/thong-ke-nhanh/quan-ly-tap-trung/tong-quan?facId=8.1&date=2025-07-01&chartFromDate=2025-07-01&chartToDate=2025-07-01
```

## TODO

1. **Check stored procedure**
2. **Check source code** để kiểm tra lại toàn bộ phải đúng với API
   - Source code: `ws_QuanLyTapTrung`
3. **Check API**

## PROMPT

dựa trên yêu cầu từ README_TASK_3 và có store procedure tương ứng để chuyển sang code, chúng ta sẽ theo cấu trúc project để tạo file handle như cấu trúc các file nằm trong thư mục: WebService.Handlers

từ file mới tạo là @ws_QuanLyTapTrung.cs so với code @ws_QuanLyTapTrung_BK.cs thì có cùng kết quả như vậy không? Hãy review code backup để xem kết quả trả ra như thế nào. Sau đó review lại code mới vừa sinh ra để đánh giá lại. Lưu ý là chỉ show ra, mà không sửa. Cũng như phải comment/ ghi chú từng phần code là tương ứng với đoạn code nào store procedure để tôi dễ dàng kiểm tra.

## API và Stored Procedure

### API

- **Tên:** `ws_QuanLyTapTrung`

### Stored Procedure

```sql
CREATE PROCEDURE [dbo].[ws_QuanLyTapTrung]
(
    @SessionID VARCHAR(MAX) = NULL,
    @TuNgay DATETIME,
    @DenNgay DATETIME,
    @FacID VARCHAR(10),
    @_Type INT = 0,
    @debug INT = 0
)
AS
BEGIN
    -- ... existing code ...
END
```

## Phân tích chi tiết

### Các bảng tạm được tạo:

- `#temp_CN_FacAdmissions` - Thông tin tiếp nhận bệnh nhân
- `#temp_CN_ClinicalSessionsAll` - Thông tin phiên khám
- `#Temp_CN_ClinicalSessionID_Vaccine` - Thông tin tiêm vaccine
- `#temp_BIL_Invoice` - Thông tin hóa đơn
- `#temp_BIL_InvoiceDetail_All` - Chi tiết hóa đơn
- `#Temp_CN_PhysicianAdmissions` - Thông tin bác sĩ khám
- `#temp_INV_ApprovedOut` - Thông tin xuất kho
- `#temp_BIL_InvoiceRefund` - Thông tin hoàn phí

### Các loại báo cáo (@\_Type):

- **@\_Type = 1:** Tổng quan
- **@\_Type = 2:** Chi tiết tiếp nhận
- **@\_Type = 3:** Chi tiết tiếp nhận (theo địa lý)
- **@\_Type = 4:** Chi tiết doanh thu
- **@\_Type = 5:** Chi tiết khám bệnh
- **@\_Type = 6:** Chi tiết phòng tiêm
- **@\_Type = 7:** Chi tiết thời gian
- **@\_Type = 8:** Chi tiết đặt trước
- **@\_Type = 9:** Chi tiết không được tiêm
- **@\_Type = 10:** Chi tiết xuất kho vaccine
- **@\_Type = 1111:** Bệnh nhân có nhiều công khám

## Các chỉ số chính được tính toán

### Tiếp nhận:

- Tổng lượt tiếp nhận
- Tiếp nhận trực tiếp
- Nguồn tiếp nhận tổng đài
- Nguồn tiếp nhận người thân giới thiệu
- Nguồn tiếp nhận facebook
- Nguồn tiếp nhận truyền hình
- Nguồn tiếp nhận đi ngang qua thấy
- Nguồn tiếp nhận khác

### Khách hàng:

- Tổng số khách đặt trước
- Tổng số hợp đồng
- Tổng số lượt tiếp nhận mới
- Tổng số khách khám lẻ
- Tổng số khách khám hợp đồng
- Tổng số lượt khách được tiêm
- Tổng số lượt khách không được tiêm
- Tổng số lượt khách bỏ về
- Tổng số khách đã tiêm
- Tổng số khách người lớn
- Tổng số khách hàng phòng khám người thân

### Tiêm chủng:

- Tổng số mũi tiêm
- Hệ số mũi tiêm

### Doanh thu:

- Doanh thu
- Hoàn phí
- Thực thu
- Doanh thu QAPay
- Doanh thu bán thẻ
- Doanh thu thanh toán online
- Đặt trước
- Thu gói
- Tổng giá trị gói bán trong ngày
- Hợp đồng hôm nay
- Hợp đồng cũ
- Khách lẻ

### Thống kê khác:

- Số khách bị sai
- Tổng số khách có 2 công khám trở lên
- Tổng số khách khám vào buổi sáng
- Số lượng KH BSGT
- Số lượng KH đi cùng
- Doanh thu KH BSGT
- Doanh thu KH đi cùng
- KH sử dụng DV VIP
- Doanh thu KH sử dụng DV VIP

## Vấn đề cần kiểm tra

### 1. Kiểm tra Stored Procedure

- Xem xét logic tính toán trong SP
- Kiểm tra các điều kiện JOIN và WHERE
- Xác minh các bảng tạm được tạo đúng

### 2. Kiểm tra Source Code

- Review code trong `ws_QuanLyTapTrung`
- So sánh logic với SP
- Kiểm tra xử lý dữ liệu trả về

### 3. Kiểm tra API

- Xác minh tham số truyền vào
- Kiểm tra response format
- So sánh với dữ liệu thực tế

## Bước tiếp theo

1. **Phân tích SP:** Tìm hiểu tại sao SP trả về 8 thay vì 9
2. **Debug code:** Chạy với @debug = 1 để xem các bước thực thi
3. **So sánh dữ liệu:** Đối chiếu kết quả với trang cửa hàng
4. **Sửa lỗi:** Cập nhật logic tính toán nếu cần
5. **Test:** Kiểm tra kết quả sau khi sửa

## Lưu ý quan trọng

- SP này rất phức tạp với nhiều bảng tạm và logic tính toán
- Cần chú ý đến các điều kiện JOIN và WHERE
- Kiểm tra kỹ các biến @\_Type khác nhau
- Đảm bảo dữ liệu được tính toán chính xác cho từng loại báo cáo

---
