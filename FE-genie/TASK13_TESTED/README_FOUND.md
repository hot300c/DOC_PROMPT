## Kết quả tìm kiếm API Usage - Genie Frontend

### Thông tin tìm kiếm
- **API Name**: `ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc`
- **Ngày tìm kiếm**: `2025-08-18`
- **Người thực hiện**: `assistant`
- **Project**: `Genie Frontend (React/Next.js)`

### Tổng quan kết quả
- **Tổng số file tìm thấy**: 2 files
- **Tổng số nơi sử dụng**: 2 nơi (1 service wrapper, 1 component gọi qua SWR)
- **Loại usage**: Service Definition, Direct Usage (qua service layer)
- **Trạng thái**: ✅ Đã tìm thấy và phân tích xong

### Phân tích sử dụng

#### Mục đích chính
1. ✅ Liệt kê chi tiết các mũi tiêm theo Hợp đồng đã đặt trước cho phác đồ được chọn
2. ✅ Hiển thị bảng chi tiết mũi (mũi, ngày dùng, giá, giảm, thành tiền, trạng thái...) để tư vấn/đối soát

#### Pattern sử dụng
- **Service Layer Pattern**: API được wrap dưới dạng hàm `fetch_LayDanhSachMuiTiemTheoHopDongDaDatTruoc` trong service hợp đồng
- **SWR Pattern**: Component dùng SWR với key `{ url, payload }`, trigger khi `isDatTruoc` và tham số đủ
- **Branching Pattern**: Toggle “đặt trước” quyết định gọi API này hay API thường (`fetch_Vaccine_Phacdo_Detail_ListWithPrice`)

### Thông tin API (FE wrapper)

1) **Service Definition**
- **File**: `genie/app/(main)/tiep-nhan/tiep-nhan-moi/contract-history/_utils/services/contract-history-api.ts`
- **Line**: ~118–133
- **Function**: `fetch_LayDanhSachMuiTiemTheoHopDongDaDatTruoc(req)`
- **Endpoint**: POST `/DataAccess`
- **Payload**:
```typescript
[
  {
    category: "QAHosGenericDB",
    command: "ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc",
    parameters: {
      FacID: req.facId,
      HopDongID: req.hopDongId,
      IDPhacDo: req.phacDoId,
    },
  },
]
```
- **Request type**: `RegimenDetailRequest`
```ts
{
  facId?: string;
  maChung?: string;            // không dùng cho API này
  servicePackageId: string;    // không dùng cho API này
  hopDongId: string;           // map → HopDongID
  phacDoId?: string;           // map → IDPhacDo
  patientId: string;           // không dùng cho API này
}
```
- **Response mapping**: `response.data.table as RegimenDetail[]`

2) **Direct Usage in Component (qua service)**
- **File**: `genie/app/(main)/tiep-nhan/tiep-nhan-moi/contract-history/_components/regimen-detail-container.tsx`
- **Line**: ~146–162
- **Context**: Khi `isDatTruoc === true` và `searchParams` đủ điều kiện, SWR gọi service để lấy danh sách mũi theo hợp đồng đã đặt trước
- **Code (rút gọn)**:
```tsx
const { data: regimenDetails } = useSWR(
  searchParams.phacDoId && searchParams.hopDongId && searchParams.patientId && searchParams.maChung
    ? { url: isDatTruoc ? "fetch_LayDanhSachMuiTiemTheoHopDongDaDatTruoc" : "fetch_Vaccine_Phacdo_Detail_ListWithPrice", payload: searchParams }
    : null,
  ({ payload }) => isDatTruoc ? fetch_LayDanhSachMuiTiemTheoHopDongDaDatTruoc(payload) : fetch_Vaccine_Phacdo_Detail_ListWithPrice(payload),
);
```

### User Journey & Testing Scenarios

#### Flow Xem chi tiết mũi theo “Hợp đồng đã đặt trước” (CLICK TRÊN VACCIN)
- **Đường dẫn màn hình**: Menu → Ngoại trú → Tiếp nhận → Tiếp nhận mới → Lịch sử hợp đồng/Phác đồ → Chi tiết mũi
- **Tiền điều kiện**: Có `hopDongId` của hợp đồng đặt trước; đã chọn phác đồ (`phacDoId`) thuộc hợp đồng; user có `facId`
- **Bước thao tác**:
  1) Mở màn hình Tiếp nhận mới và truy cập phần lịch sử hợp đồng/chi tiết phác đồ
  2) Bật chế độ “Đặt trước” (isDatTruoc = true)
  3) Chọn phác đồ thuộc hợp đồng → bảng chi tiết mũi hiển thị
- **Trigger API**: `ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc` (qua `fetch_LayDanhSachMuiTiemTheoHopDongDaDatTruoc`)
- **Kỳ vọng UI**: Bảng cột “Mũi, Ngày dùng, Đơn giá, Tiền giảm, Giảm (%), Thành tiền, T.Ngoài, T.Toán …”; tổng tiền hiển thị dưới footer
- **Nhánh quyết định**: Tắt “Đặt trước” → chuyển API sang `fetch_Vaccine_Phacdo_Detail_ListWithPrice`
- **Kết quả dữ liệu**: `RegimenDetail[]` từ `response.data.table`
- **Dữ liệu mẫu**: `facId: "8.1"`, `hopDongId: "11111111-1111-1111-1111-111111111111"`, `phacDoId: "1"`
- **Mapping UI → Code**: `regimen-detail-container.tsx` → SWR; `contract-history-api.ts` → `fetch_LayDanhSachMuiTiemTheoHopDongDaDatTruoc`


#### Flow Đổi phác đồ trong hợp đồng đặt trước → nạp lại danh sách mũi  (CLICK TRÊN PHÁC ĐỒ)
- **Đường dẫn màn hình**: Cùng màn hình trên
- **Tiền điều kiện**: Đã bật “Đặt trước”; có nhiều phác đồ khả dụng trong hợp đồng
- **Bước thao tác**:
  1) Đổi lựa chọn phác đồ (`phacDoId`)
  2) SWR key thay đổi theo `payload` → tự động gọi lại API
- **Trigger API**: `ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc`
- **Kỳ vọng UI**: Danh sách mũi cập nhật đúng theo phác đồ mới
- **Nhánh quyết định**: Không
- **Kết quả dữ liệu**: `RegimenDetail[]`
- **Dữ liệu mẫu**: Thay đổi `phacDoId` từ `1` → `2`
- **Mapping UI → Code**: `regimen-detail-container.tsx` → phụ thuộc `searchParams.phacDoId`

### Negative cases (đề xuất kiểm thử)
- **Thiếu tham số**: Bất kỳ thiếu `phacDoId` hoặc `hopDongId` hoặc điều kiện trong SWR không thỏa → SWR không gọi API (key = null) → UI bảng rỗng
- **Rỗng dữ liệu**: API trả về `[]` → UI vẫn hiển thị bảng, tổng tiền = 0
- **Lỗi mạng/500**: Hiển thị thông báo lỗi chung (tùy middleware httpService), không treo UI
- **Sai `FacID`**: Có thể trả rỗng; cần đối chiếu facId hiện tại của user

### cURL Example (tham khảo nhanh)
```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc",
      "parameters": {
        "FacID": "8.1",
        "HopDongID": "11111111-1111-1111-1111-111111111111",
        "IDPhacDo": "1"
      }
    }
  ]'
```

### Response fields chính (FE mapping → `RegimenDetail`)
```ts
type RegimenDetail = {
  iD_Detail: number;
  idPhacDo: number;
  sttMuiTiem: number;
  thoiGian_GianCach: number;
  maChung: string;
  gia: number;
  phanTramGiam: number;
  ngayDung: Date;
  hopDongID: string;
  soHopDong: string;
  hopDongDetailID: string;
  tienGiam: number;
  slMuiMacDinh: number | null;
  isTiemNgoai: boolean;
  giaTiemNgoai: number;
  isMuiNgoaiDanhMuc: boolean;
  giaChenhLechTiemNgoai: number;
  isDaTiem: boolean;
  ngayServer: string;
  doiTuongSuDungID: number;
  vaccineName: string;
  facID: string;
  coSo: string | null;
  doiTuongSuDung: string;
  giaChenhLechChuaGiam: number;
  loaiGianCach: number;
  loaiTriSo: number;
  triSoMin: number;
  triSoMax: number;
  muiThanhToan: boolean;
  isKhongDuocBoCheckThanhToan: boolean;
  isPhacDoThieuMui: boolean;
  hopDongID_Goc: string;
  isPaidHopDong_Goc: boolean | null;
  thanhTien: number;
  isChon: number;
};
```

### Chi tiết kết quả theo loại usage

1) **Service Definition**
- **File**: `genie/app/(main)/tiep-nhan/tiep-nhan-moi/contract-history/_utils/services/contract-history-api.ts`
- **Line**: ~118–133
- **Function**: `fetch_LayDanhSachMuiTiemTheoHopDongDaDatTruoc`
- **Mục đích**: Gọi handler backend để lấy danh sách mũi theo hợp đồng đặt trước

2) **Direct Usage (Component)**
- **File**: `genie/app/(main)/tiep-nhan/tiep-nhan-moi/contract-history/_components/regimen-detail-container.tsx`
- **Line**: ~152–161
- **Context**: SWR gọi service khi `isDatTruoc` và params hợp lệ; hiển thị bảng chi tiết mũi

### Backend tham chiếu (đối chiếu nhanh)
- **Handler**: `aladdin/WebService.Handlers/QAHosGenericDB/ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc.cs`
- **Tests**: `aladdin/WebService.Handlers.Tests/QAHosGenericDB/ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc_Test.cs`
- **Issue notes**: `DOCS_PROMPT/BE-aladdin/TASK/TASK13_REVIEWING/ISSUES_ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc.md`

### Checklist tối thiểu
- [x] Xác định Service wrapper trong FE
- [x] Tìm tất cả nơi gọi trực tiếp trong FE (qua SWR ở component)
- [x] Ghi rõ màn hình/flow và trigger API
- [x] Cung cấp mẫu cURL và cấu trúc dữ liệu chính

### Ghi chú
- Điều kiện SWR yêu cầu đủ: `phacDoId`, `hopDongId`, `patientId`, `maChung`. Tuy API này chỉ dùng 3 trường đầu, logic UI vẫn yêu cầu đủ để đảm bảo đúng ngữ cảnh hiển thị.


