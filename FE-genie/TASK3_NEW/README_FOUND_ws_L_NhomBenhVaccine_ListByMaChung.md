# Kết quả tìm kiếm API Usage - Genie Frontend

## Thông tin tìm kiếm
- **API Name**: `ws_L_NhomBenhVaccine_ListByMaChung`
- **Ngày tìm kiếm**: `2025-09-04`
- **Người thực hiện**: `auto`
- **Project**: `Genie Frontend (React/Next.js)`

## Tổng quan kết quả
- **Tổng số file tìm thấy**: `2 files`
- **Tổng số nơi sử dụng**: `2 nơi`
- **Loại usage**: Service Definition (payload construction)
- **Trạng thái**: ✅ Đã tìm thấy và trích xuất payload

## Phân tích sử dụng

### Mục đích chính
1. ✅ Lấy danh sách nhóm bệnh vaccine theo `MaChung` để xử lý logic đặt trước/tiếp nhận

### Places

1) `app/lib/services/appLogic/reception/patientPreOrder.ts`
```ts
requestNhomBenhVaccine.push({
  category: "QAHosGenericDB",
  command: "ws_L_NhomBenhVaccine_ListByMaChung",
  parameters: {
    MaChung: item.maChung,
    FacID: facID,
    PatientID: patientStore.patientId,
    DoiTuongID: item.doiTuongSuDungId,
  },
});
```

2) `app/lib/services/preOrderService.ts`
```ts
const response = await httpService.post("/DataAccess", [
  {
    category: "QAHosGenericDB",
    command: "ws_L_NhomBenhVaccine_ListByMaChung",
    parameters: {
      FacID: facId,
      MaChung: maChung,
      PatientID: patientId,
      DoiTuongID: doiTuongSuDungId,
    },
  },
]);
```

## User Journey & Testing Scenarios (Cụ thể)

### Flow 1: Đặt trước tiêm vaccine (Pre-order)
- **Đường dẫn màn hình**: Menu → Tiếp nhận → Tiếp nhận mới (Pre-order nằm trong trang này)
- **Tiền điều kiện**: Có danh sách mục đặt trước (mỗi mục gồm `maChung`, `doiTuongSuDungId`), đã chọn cơ sở `facID`, người dùng đã đăng nhập
- **Bước thao tác**:
  1) Tại màn hình Đặt trước, chọn bệnh nhân (hoặc nhập mới) → sinh `patientId`
  2) Thêm 1 mục đặt trước tiêm có trường `maChung` và `doiTuongSuDungId`
  3) Nhấn Lưu/Hoàn tất danh sách đặt trước
- **Trigger API**: Khi gom payload các mục đặt trước, hệ thống duyệt `lstDistinctMore.forEach(...)` và push từng phần tử vào `requestNhomBenhVaccine` (file `patientPreOrder.ts`) → gọi `ws_L_NhomBenhVaccine_ListByMaChung`
- **Kỳ vọng UI**: Danh sách nhóm bệnh vaccine tương ứng được phản ánh vào form (ẩn/hiện trường liên quan, hợp lệ hóa theo nhóm bệnh)
- **Kết quả dữ liệu**: Backend trả `MaNhomBenh` (ví dụ `'1;'`) để FE tiếp tục xử lý logic nhóm bệnh theo mã chung

### Flow 2: Tiếp nhận từ phiếu đặt trước
- **Đường dẫn màn hình**: Menu → Tiếp nhận → Tiếp nhận mới
- **Tiền điều kiện**: Có phiếu đặt trước chứa `maChung`; đã chọn `facId`; `patientId` sẵn có hoặc sau khi chọn bệnh nhân
- **Bước thao tác**:
  1) Mở Tiếp nhận mới → chọn/nhập bệnh nhân
  2) Chọn phiếu đặt trước cần tiếp nhận (pre-order) → hệ thống có `maChung`, `doiTuongSuDungId`
  3) Nhấn Xác nhận/Hoàn tất tiếp nhận
- **Trigger API**: Service `preOrderService.ts` gửi POST `/DataAccess` với phần tử có `command: "ws_L_NhomBenhVaccine_ListByMaChung"` và parameters `{ FacID, MaChung, PatientID, DoiTuongID }`
- **Kỳ vọng UI**: Nhóm bệnh vaccine liên quan được áp dụng vào hồ sơ tiếp nhận (ví dụ: ràng buộc phác đồ, cảnh báo/ghi chú)
- **Kết quả dữ liệu**: FE đọc `response.data?.table[0]` và sử dụng giá trị để cập nhật trạng thái form tiếp nhận

## Thông tin API (theo usage phía FE)
- Request body phần tử:
```json
{
  "category": "QAHosGenericDB",
  "command": "ws_L_NhomBenhVaccine_ListByMaChung",
  "parameters": {
    "FacID": "<facId>",
    "MaChung": "<maChung>",
    "PatientID": "<patientId>",
    "DoiTuongID": <doiTuongSuDungId>
  }
}
```

## Ghi chú
- Hai nơi sử dụng truyền cùng các tham số: `FacID`, `MaChung`, `PatientID`, `DoiTuongID`.
- Backend handler nên chấp nhận đầy đủ các tham số này (một số có thể không dùng trực tiếp) để tương thích FE.
