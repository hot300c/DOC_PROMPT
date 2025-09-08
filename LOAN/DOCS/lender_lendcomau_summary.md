LenderAPI (Lend Capital) — Tóm tắt mục đích và các API chính

1) Mục đích
- Kết nối các nhà cho vay (lenders) với hệ thống Lend để nhận lead, truy xuất dữ liệu chi tiết lead, tải tệp đính kèm, và cập nhật trạng thái/đề nghị vay/funded theo thời gian gần thực.

2) Môi trường, Phiên bản, Xác thực và Header
- Environments (Base URLs):
  - Production: https://lenders-api.lend.com.au/v1/
  - Sandbox: https://sandbox-lenders-api.lend.com.au/v1/
- Versioning: hiện tại v1 (nằm trong URL).
- Authentication: dùng API Key qua header `x-api-key`.
- Headers bắt buộc: `Accept: application/json`, `Content-Type: application/json`, `x-api-key: {YOUR_API_KEY}`.

3) Monitoring
- Kiểm tra tình trạng hệ thống: GET `/` (gọi trực tiếp base URL). Trả về `success` và `message`.

4) Thu nhận Lead (Collecting Leads)
- Hai phương thức:
  - Webhook (khuyến nghị): Lend gửi POST payload nhỏ (không chứa dữ liệu nhạy cảm) tới endpoint do bạn cung cấp, gồm `lead_ref`, thời gian gửi, cờ `been_retrieved`.
  - API polling: kiểm tra định kỳ qua API Get Leads (bên dưới).

5) Tài nguyên (Resources) — Các API chính
- Leads
  - GET `/leads?since=[timestamp]`
    - Mục đích: Liệt kê toàn bộ lead đã gửi cho bạn kể từ thời điểm `since` (Unix timestamp).
    - Trả về mảng các lead: `lead_ref`, `sent_to_you`, `been_retrieved`.
  - GET `/leads/[lead_ref]`
    - Mục đích: Lấy đầy đủ dữ liệu của một lead (thông tin doanh nghiệp, chủ sở hữu, doanh thu/chi phí, ngân hàng, ghi chú, v.v.).
    - Có thể kèm đối tượng sản phẩm chuyên biệt `asset_finance_data` (nếu là hồ sơ Asset Finance).
  - GET `/leads/get-attachments/[lead_ref]?mins=[minutes]`
    - Mục đích: Cấp quyền tạm thời để tải các tệp đính kèm (nhạy cảm) của lead. Liên kết trả về sẽ hết hạn theo `mins` (mặc định 2, tối đa 5).

- Updating (bắt buộc cập nhật trạng thái theo thời gian gần thực)
  - POST `/leads/[lead_ref]` — Cập nhật trạng thái
    - Body tối thiểu: `status` (phải thuộc danh sách Statuses), `status_changed` (Unix timestamp), tùy chọn `notes` (mảng Note Objects).
  - POST `/leads/[lead_ref]` — Gửi đề nghị vay (Loan Offer)
    - Body tối thiểu: `status` (khuyến nghị "Offer Made"), `status_changed`, `offer_amount`, tùy chọn `notes`.
  - POST `/leads/[lead_ref]` — Thông báo Funded
    - Body tối thiểu: `status` (thuộc nhóm Funded), `status_changed`, `funded_details` gồm: `product`, `deal_type` (New Deal/Refinance), `funded_amount`, `funded_date`; tùy chọn `total_payback`, và bắt buộc `broker_commission`, `lend_commission`.

- Statuses
  - GET `/statuses`
    - Mục đích: Lấy danh sách trạng thái hợp lệ (nhóm Attempting, In Progress, Rejected, Settled) để dùng khi POST cập nhật.

- Picklists
  - GET `/picklists`
    - Mục đích: Lấy toàn bộ danh mục chuẩn (purpose, industry, product_type, equipment, books_package, asset_type, liability_type).
  - GET `/picklists/[picklist_type]`
    - Mục đích: Lấy riêng từng loại picklist (giá trị hợp lệ như trên).

6) Đối tượng sản phẩm chuyên biệt (Product-Specific Objects)
- `asset_finance_data`: chỉ xuất hiện khi lead thuộc loại Asset Finance; chứa thông tin chi tiết mua sắm tài sản, người tham gia, tài sản/công nợ cá nhân và doanh nghiệp, địa chỉ, việc làm, tham chiếu, chi tiết trust, địa chỉ doanh nghiệp, cờ/chi tiết báo giá, v.v.

7) Test Leads (Sandbox)
- Các `lead_ref` mẫu: `abc1234`, `def5678`, `ghi1234` (có `asset_finance_data`), `uvw5432`, `xyz9876` (mục đích kiểm thử hành vi và lỗi). Chi tiết hành vi xem mục Test Leads trong tài liệu.

8) Lỗi & Chuẩn dữ liệu phản hồi
- Tất cả phản hồi có `success` (bool). Khi lỗi, trả về `success: false` và `error`, kèm mã HTTP tương ứng (400/403/422/500...). Ví dụ lỗi hay gặp: Invalid API Key (403), invalid `since` (400), status không hợp lệ (400), thiếu trường bắt buộc (422), không còn là lender hoạt động trên lead (403).

9) Tóm tắt nhanh các endpoint
- Monitoring: GET `/`
- Leads: GET `/leads?since=...`, GET `/leads/[lead_ref]`, GET `/leads/get-attachments/[lead_ref]?mins=...`
- Updating: POST `/leads/[lead_ref]` (Status Update | Loan Offer | Funded)
- Statuses: GET `/statuses`
- Picklists: GET `/picklists`, GET `/picklists/[picklist_type]`

Ghi chú
- Tất cả yêu cầu dùng header JSON và `x-api-key`. Nên ưu tiên Webhook để nhận lead theo sự kiện; chỉ gọi Attachments API khi `number_of_file_attachments > 0` để tiết kiệm tài nguyên.

