# TASK 17 — CompanyB2B (Business Spec)

## 1) Mục tiêu
- Xây dựng nghiệp vụ quản lý CompanyB2B (tạo/cập nhật, xem danh sách, xuất dữ liệu) thống nhất giữa BE và FE.
- Chuẩn hóa luật dữ liệu: validation, null-handling, audit trail.
- Cung cấp hướng dẫn gọi API (đăng nhập lấy token, gọi List qua Swagger) để kiểm thử nhanh.

## 2) Phạm vi
- Entity: CompanyB2B.
- Các thao tác: Create/Update (Save), List, Export, Import (XLSX).
- Không thay đổi cấu trúc DB, các thay đổi là ở mức xử lý logic và chuẩn hóa format dữ liệu trả về.

## 3) Liên quan mã nguồn
- BE branch: `feat/ws_CompanyB2B` (Aladdin) — Controller: `CompanyB2BController`, handlers liên quan `ws_L_CompanyB2B_*`.
- FE branch: `feat/ws_CompanyB2B` (genie) — form nhập liệu, danh sách, chức năng export.

## 4) Quyền truy cập và xác thực
- Yêu cầu đăng nhập, mọi API phải kèm Bearer Token.
- Thông tin đăng nhập test:
  - Username: `phucnnd`
  - Password: `Phuc*1234`
  - facId: `"8.1"`

### Cách lấy token và thử API nhanh (Swagger)
1. Mở Swagger: `http://localhost:5272/swagger/index.html`.
2. Gọi endpoint đăng nhập (Login) để lấy token (Bearer).
3. Bấm Authorize trên Swagger, dán `Bearer <token>`.
4. Tìm `CompanyB2BController`, gọi `List` để kiểm tra dữ liệu.

Gợi ý gọi nhanh (cURL — thay <token> và đường dẫn thực tế nếu khác):
```bash
curl -X GET "http://localhost:5272/api/companyb2b/list" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json"
```

## 5) Quy tắc Validation (chuẩn hoá)
- Bắt buộc:
  - `CompanyCode` (string)
  - `CompanyName` (string)
  - `EffectiveFrom` (DateTime)
  - `Hopdong` (string)
  - `UserID` (Guid) — dùng cho audit
- Không bắt buộc (optional):
  - `CompanyTax` (string?)
  - `CompanyAddress` (string?)
  - `EffectiveTo` (DateTime?)
  - `IsActive` (bool, default `true`)
- Luật bổ sung:
  - CompanyCode phải unique (Create: unique toàn bảng; Update: không trùng với record khác).
  - Nếu có `EffectiveTo` thì `EffectiveFrom ≤ EffectiveTo`.

Lưu ý hiển thị thông báo lỗi (Import):
- Tất cả lỗi trong quá trình import (thiếu cột/trường bắt buộc, trùng mã, sai định dạng ngày, vượt giới hạn độ dài, vượt quá 10.000 dòng, giá trị boolean) đều trả về tiếng Việt.
- Trường `IsActive` trong thông báo lỗi hiển thị là "Trạng thái" (ví dụ: "Giá trị Trạng thái không hợp lệ (yêu cầu true/false)").

## 6) Null-handling (nhất quán)
- Ở Save (Create/Update):
  - `CompanyTax`: null → lưu ""
  - `CompanyAddress`: null → lưu ""
- Ở Export/List response: mọi giá trị có thể null sẽ được chuẩn hoá trả về dạng string rỗng "" (đối với các cột text), và định dạng ngày/boolean theo mục 8.

Lợi ích: dữ liệu nhất quán, FE không cần phân biệt null/empty khi hiển thị, export không phải xử lý null.

## 6.1) Import (XLSX) — Quy tắc
- Định dạng đầu vào: Excel `.xlsx` (ưu tiên); có hỗ trợ CSV fallback khi cần.
- Header mapping hỗ trợ tiếng Việt/Anh (CompanyCode/Mã công ty, CompanyName/Tên công ty, CompanyTax/MST, CompanyAddress/Địa chỉ, EffectiveFrom/Ngày bắt đầu, EffectiveTo/Ngày kết thúc, IsActive/Trạng thái, Hopdong/Số PO-HĐ).
- Giới hạn kích thước: tối đa 10.000 dòng dữ liệu (không tính header). Vượt giới hạn sẽ trả lỗi và dừng xử lý.
- Kiểm tra trùng mã ngay trong file: nếu phát hiện `CompanyCode` trùng lặp trong file import, dừng import và trả về lỗi theo dòng tương ứng.
- Kiểm tra hợp lệ theo cột: độ dài tối đa theo schema (Code/Tax 50, Name/Address 500, Hopdong 100), ngày hợp lệ và `EffectiveFrom ≤ EffectiveTo`.
- Giá trị boolean: `IsActive` nhận `true/false`; thông báo lỗi hiển thị nhãn "Trạng thái".
- Toàn bộ thông báo lỗi trả về bằng tiếng Việt; nếu có bất kỳ lỗi nào, không ghi DB (rollback toàn bộ). Khi không có lỗi, thao tác upsert theo `CompanyCode` trong một transaction.

## 7) Audit trail
- Create:
  - `CreatedOn` = now, `CreatedBy` = `@params.UserID`
  - `ModifiedOn` = `CreatedOn`, `ModifiedBy` = `CreatedBy`
- Update:
  - `ModifiedOn` = now, `ModifiedBy` = `@params.UserID`
- Quy tắc:
  - `CreatedOn/CreatedBy` không thay đổi sau khi tạo.
  - `ModifiedOn/ModifiedBy` luôn cập nhật lần sửa gần nhất.

## 8) Quy tắc dữ liệu trả về (List/Export)
- Sắp xếp mặc định: `ModifiedOn` (DESC, nếu null dùng `CreatedOn`) rồi `CreatedOn` (DESC).
- Chuẩn hoá hiển thị:
  - Ngày hiệu lực: `EffectiveFrom/EffectiveTo` dùng format `yyyy-MM-dd`.
  - Audit: `CreatedOn/ModifiedOn` dùng `yyyy-MM-dd HH:mm:ss`.
  - Boolean: `IsActive` hiển thị: `"Kích hoạt"` hoặc `"Không kích hoạt"`.
  - Text null → `""`.

## 9) Export (định dạng và ràng buộc)
- Xuất toàn bộ dữ liệu CompanyB2B, không áp dụng filter (giai đoạn này).
- Dữ liệu được chuyển thành JSON, encode UTF-8, sau đó Base64.
- Response chuẩn (rút gọn):
```json
{
  "Table1": [{
    "FileName": "CompanyB2B_yyyyMMddHHmmss.json",
    "FileExtension": ".json",
    "FileData": "<base64>",
    "TotalCount": <int>,
    "FileSizeBytes": <int>,
    "FileSizeKB": <number>,
    "FileSizeMB": <number>,
    "ExportDate": "yyyy-MM-dd HH:mm:ss",
    "DataFormat": "json",
    "ContentType": "application/json"
  }]
}
```
- Client decode (JS):
```javascript
const jsonString = atob(response.Table1[0].FileData);
const exportData = JSON.parse(jsonString);
```
- Ghi chú hiệu năng:
  - Base64 tăng kích thước ~33% so với JSON gốc.
  - Đọc toàn bộ vào bộ nhớ; với dữ liệu rất lớn có thể cần streaming/pagination trong tương lai.

## 10) Hướng dẫn kiểm thử nhanh
- BE chạy tại `http://localhost:5272`.
- Vào Swagger, login lấy token, Authorize, rồi gọi `CompanyB2BController → List`.
- Lưu ý token phải có facId hợp lệ (ví dụ "8.1").

## 11) Rủi ro & Lưu ý
- Export khối lượng lớn có thể chậm, tốn bộ nhớ.
- Base64 không phải mã hoá bảo mật; cần kiểm soát quyền truy cập.
- Bắt buộc giữ nguyên thiết lập JSON serialization để đảm bảo tiếng Việt hiển thị đúng khi decode.

## 12) Tiêu chí hoàn thành
- List hiển thị đúng thứ tự, định dạng dữ liệu theo quy tắc trên.
- Create/Update lưu audit trail đúng; null-handling áp dụng nhất quán.
- Export trả về đúng format, FE decode và tạo file Excel hiển thị tiếng Việt chính xác.

---

## Phụ lục — Ghi chú triển khai
- JSON settings (BE) cần đảm bảo tương thích tiếng Việt; phía client decode bằng UTF-8 để hiển thị chuẩn.
- Chỉ số hoá `ModifiedOn`, `CreatedOn` được khuyến nghị để tối ưu sắp xếp.

---

## TODO (sau khi hoàn tất Import)
- Lấy `UserID` từ session cookie (user đã đăng nhập) trong `CompanyB2BController` thay vì nhận trực tiếp từ request. Dùng scheme xác thực theo session để map `UserID` và áp dụng cho audit (`CreatedBy`/`ModifiedBy`).

---

## Ghi chú Test17 (đã triển khai)
- Controller `CompanyB2BController` tự động lấy `UserID` theo thứ tự: claim `NameIdentifier` → cookie `s` qua `UserService.GetUserIdFromSessionId`. Nếu tìm thấy sẽ override `UserID` trong body.
- Chuẩn hoá thông báo tiếng Việt trong toàn bộ handler `ws_L_CompanyB2B` (Save/Get/Delete/List/Import/Export). Các message lỗi và trạng thái như: "Không tìm thấy công ty", "Ngày hiệu lực từ phải nhỏ hơn hoặc bằng ngày hiệu lực đến", "Thành công"…
- Chuẩn hoá kiểu tham số khi gọi Stored Procedure/Handler trong `DataRequestDispatcher` để tránh lỗi convert Guid → String (map đúng `Guid` → `UniqueIdentifier`, `bool` → `Bit`, `DateTime` → `DateTime2`, v.v.).
- API Save đang dùng handler: `ws_L_CompanyB2B_Save` với DTO `ws_L_CompanyB2B_Save.Parameters`. Get/List/Import/Export giữ nguyên.
- Import: kiểm tra đầy đủ ràng buộc, trả về lỗi tiếng Việt theo dòng, rollback nếu có lỗi.

### Hướng dẫn kiểm thử nhanh (Test17)
1. Đăng nhập để có cookie `s` (hoặc đảm bảo claim `NameIdentifier` tồn tại). Gọi `POST /api/company-b2b/save` mà không gửi `UserID` → BE sẽ tự set `CreatedBy/ModifiedBy` theo user.
2. Lỗi ràng buộc (thiếu `CompanyCode`, `CompanyName`, `EffectiveFrom`, `Hopdong` hoặc sai thứ tự ngày) trả về HTTP 400 với thông điệp tiếng Việt.
3. Gọi `GET /api/company-b2b/list` → dữ liệu được chuẩn hoá theo mục 8 (format ngày/boolean, text null → "").
4. Gọi `POST /api/company-b2b/import` với file hợp lệ/không hợp lệ để xác nhận quy tắc lỗi tiếng Việt và giao dịch rollback khi có lỗi.
5. Gọi `GET /api/company-b2b/export` → nhận `FileData` (base64 JSON, UTF-8), decode kiểm tra tiếng Việt hiển thị đúng.