Giai đoạn và Trạng thái trong Quy trình Hồ sơ Vay
1. Khởi tạo (ORIGINATION)

Mô tả: Khách hàng chuẩn bị và nộp đơn vay, bao gồm KYC và xác minh ban đầu.

Trạng thái:

DRAFT / Nháp → Khách hàng bắt đầu nhập thông tin (CMND/CCCD, thu nhập, giấy tờ).

SUBMITTED / Đã nộp đơn → Đơn đã gửi lên hệ thống.

PENDING_VERIFICATION / Chờ xác minh → Xác minh KYC, OCR, kiểm tra CIC.

PRE_APPROVED / Tiền phê duyệt → Đủ điều kiện sơ bộ, đề xuất hạn mức vay.

📱 UI: Thanh tiến độ, push notification “Đơn của bạn đã được nhận”.

2. Thẩm định (UNDERWRITING)

Mô tả: Đánh giá chi tiết rủi ro, lịch sử tín dụng, thu nhập, để quyết định phê duyệt.

Trạng thái:

IN_REVIEW / Đang thẩm định → Kiểm tra hồ sơ, dữ liệu tài chính.

UNDERWRITING / Đang đánh giá rủi ro → Phân tích sâu, tính toán DTI, AI scoring.

CONDITIONALLY_APPROVED / Phê duyệt có điều kiện → Cần bổ sung thêm (tài sản đảm bảo, giấy tờ).

APPROVED / Đã phê duyệt → Đơn hợp lệ, sẵn sàng ký hợp đồng.

REJECTED / Bị từ chối → Không đạt điều kiện vay.

📱 UI: Hiển thị tiến độ (% hoàn thành), hiển thị yêu cầu bổ sung hồ sơ.

3. Quản lý Vay (SERVICING)

Mô tả: Quản lý khoản vay sau giải ngân, theo dõi trả nợ, nhắc nhở quá hạn.

Trạng thái:

DISBURSED / Đã giải ngân → Khoản vay đã được chuyển tiền (MoMo/VNPAY).

ACTIVE / Đang hoạt động → Khách hàng trả góp định kỳ.

OVERDUE / Quá hạn → Chậm thanh toán, hệ thống cảnh báo và tính phí phạt.

IN_COLLECTION / Đang thu hồi nợ → Xử lý nợ xấu, bộ phận pháp lý hoặc thu hồi.

📱 UI: Lịch trả nợ, số dư còn lại, nút “Trả trước hạn”.

4. Kết thúc (CLOSURE)

Mô tả: Đóng khoản vay, báo cáo và lưu trữ.

Trạng thái:

PAID_OFF / Đã trả hết → Thanh toán đầy đủ, khoản vay kết thúc thành công.

CLOSED / Đã đóng → Hồ sơ đã hoàn tất (trả hết hoặc bị hủy).

DEFAULTED / Nợ xấu → Không thu hồi được, báo cáo CIC.

ARCHIVED / Lưu trữ → Lưu hồ sơ trong 5 năm (theo luật Việt Nam).

📱 UI: Hiển thị xác nhận hoàn tất hoặc báo cáo nợ xấu, chỉ admin thấy trạng thái lưu trữ.