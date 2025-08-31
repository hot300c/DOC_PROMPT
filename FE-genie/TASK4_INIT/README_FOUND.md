## API: ws_Vaccine_KiemTraDongPhacDo

### Frontend (Genie)

- Service wrapper
  - File: `genie/app/lib/services/vaccineService.ts`
  - Function: `checkAndCloseVaccinationProtocol(patientId: string): Promise<void>`
  - Request body:
    ```ts
    [
      {
        category: "QAHosGenericDB",
        command: "ws_Vaccine_KiemTraDongPhacDo",
        parameters: {
          PatientID: patientId,
          IPUser: utils.getLocalIPv4(),
          MacAddressUser: utils.getMacAddresses(),
          // SessionID: (được gateway/back-end tự gắn từ phiên đăng nhập)
        },
      },
    ]
    ```

- Direct usage (transaction flow)
  - File: `genie/app/(main)/ngoai-tru/kham-benh/[patientId]/DetailMedicalCheckupPage.tsx`
  - Usage: gửi trong batch request ngay trước bước kết thúc đợt điều trị
    ```ts
    {
      category: "QAHosGenericDB",
      command: "ws_Vaccine_KiemTraDongPhacDo",
      parameters: {
        PatientID: patientId,
        IPUser: utils.getLocalIPv4(),
        MacAddressUser: utils.getMacAddresses(),
      },
    }
    ```

### Backend

- Handler: `aladdin/WebService.Handlers/QAHosGenericDB/ws_Vaccine_KiemTraDongPhacDo.cs`
  - Parameters: `SessionID (required), PatientID (Guid, required), IPUser?, MacAddressUser?`
  - Output: DataSet với bảng `Result` gồm `Success: bool`, `Message: string`
  - Ghi chú: Handler tra `UserID` từ `Security..Sessions` theo `SessionID`; nếu không có user sẽ trả về rỗng (early return).

- Procedure: `qas-db/QAHosGenericDB/Procedures/ws_Vaccine_KiemTraDongPhacDo.sql`
  - Tham số: `@SessionID, @PatientID, @IPUser, @MacAddressUser`
  - Logic: Đóng các phác đồ Vaccine/Nhóm bệnh đã hoàn tất mũi (không còn mũi `CompleteOn IS NULL`).

### Request

```typescript
{
  PatientID: string;         // GUID bệnh nhân
  IPUser?: string;           // IP máy trạm
  MacAddressUser?: string;   // MAC máy trạm
  // SessionID: tự gắn ở gateway/back-end từ phiên đang đăng nhập
}
```

### Response (BE handler)

```typescript
{
  tables: {
    Result: [{ Success: boolean; Message: string }];
  }
}
```

### cURL

```bash
curl -X POST "http://localhost:3000/api/DataAccess" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "category": "QAHosGenericDB",
      "command": "ws_Vaccine_KiemTraDongPhacDo",
      "parameters": {
        "PatientID": "33333333-3333-3333-3333-333333333333",
        "IPUser": "192.168.1.10",
        "MacAddressUser": "AA:BB:CC:DD:EE:FF"
      }
    }
  ]'
```

### User flows

- Flow 1: Kết thúc khám → đóng phác đồ
  - Màn hình: Menu → Ngoại trú → Khám bệnh (trang chi tiết)
  - Bước: Sau khi lưu chỉ định, hệ thống gọi `ws_Vaccine_KiemTraDongPhacDo` để đóng các phác đồ đã hoàn tất → tiếp tục gọi `ws_CN_PhysicanAdmissions_FinishPractice`.
  - Kết quả: Các phác đồ đủ điều kiện được đóng, quy trình kết thúc khám tiếp tục.

- Flow 2: Đóng phác đồ thủ công từ service
  - Gọi `checkAndCloseVaccinationProtocol(patientId)` để fire-and-forget đóng phác đồ nếu cần.

### Negative cases

- Thiếu `SessionID` (gateway không gắn): Handler sẽ trả về rỗng (không thực hiện), cần đảm bảo phiên đăng nhập hợp lệ.
- `PatientID` không hợp lệ: Không tìm thấy phác đồ để đóng.
- Lỗi mạng/API: Dừng flow kết thúc khám, cần hiển thị thông báo lỗi phù hợp.

### Ghi chú

- FE không đọc response của API này (fire-and-forget). Nếu cần xác nhận, có thể đọc bảng `Result` từ handler.

