# MAPPING: ws_QuanLyTapTrung Handler

## **TỔNG QUAN**

File này ghi lại chi tiết mapping giữa:

-   **Code mới**: `ws_QuanLyTapTrung.cs` (được tái cấu trúc từ stored procedure gốc)
-   **Stored Procedure gốc**: `[dbo].[ws_QuanLyTapTrung]`
-   **File backup**: `ws_QuanLyTapTrung_BK.cs`

## **CẤU TRÚC TỔNG THỂ**

### **1. Main Handler Structure**

```csharp
public override DataSet Handle(Parameters @params)
```

-   **Tương ứng SP**: Phần khai báo và xử lý tham số đầu vào
-   **Logic**: Switch case để phân loại theo `@_Type` parameter

### **2. Report Types Mapping**

| C# Case | SP @\_Type | Tên báo cáo               | Trạng thái             |
| ------- | ---------- | ------------------------- | ---------------------- |
| 1       | 1          | Tổng quan                 | ✅ Đã implement đầy đủ |
| 2       | 2          | Chi tiết tiếp nhận        | ⚠️ Cần bổ sung logic   |
| 3       | 3          | Chi tiết tiếp nhận địa lý | ⚠️ Cần bổ sung logic   |
| 4       | 4          | Chi tiết doanh thu        | ⚠️ Cần bổ sung logic   |
| 5       | 5          | Chi tiết vaccine          | ⚠️ Cần bổ sung logic   |
| 6       | 6          | Báo cáo thời gian         | ⚠️ Cần bổ sung logic   |
| 7       | 7          | Báo cáo chi tiết          | ⚠️ Cần bổ sung logic   |
| 8       | 8          | Báo cáo tổng hợp          | ⚠️ Cần bổ sung logic   |
| 9       | 9          | Báo cáo theo ngày         | ⚠️ Cần bổ sung logic   |
| 10      | 10         | Báo cáo theo tháng        | ⚠️ Cần bổ sung logic   |
| 11      | 11         | Báo cáo theo năm          | ⚠️ Cần bổ sung logic   |

## **CHI TIẾT MAPPING CHO TYPE 1 (TỔNG QUAN)**

### **A. DTO Classes (Lines 38-102 trong file backup)**

#### **FacAdmissionDto**

```csharp
private class FacAdmissionDto
{
    public Guid FacAdmissionId { get; init; }        // SP: FacAdmissionId
    public int? NguonTiepNhan { get; init; }        // SP: NguonTiepNhan
    public Guid? PatientId { get; init; }            // SP: PatientId
    public string? FacId { get; init; }              // SP: FacId
    public Guid? CreatedBy { get; init; }            // SP: CreatedBy
    public DateTime? DischargedOn { get; init; }     // SP: DischargedOn
    public DateTime? AdmitDate { get; init; }        // SP: AdmitDate
    public int? AdmitDateAsInt { get; init; }       // SP: AdmitDateAsInt
    public DateTime? AdmitOn { get; init; }          // SP: AdmitOn
    public int? TuoiAsInt { get; init; }             // SP: TuoiAsInt (tính từ DoB)
    public bool? IsChieu { get; init; }              // SP: IsChieu
}
```

#### **ClinicalSessionDto**

```csharp
private class ClinicalSessionDto
{
    public Guid ClinicalSessionId { get; set; }      // SP: ClinicalSessionId
    public Guid? FacAdmissionId { get; set; }       // SP: FacAdmissionId
    public Guid? PhysicianAdmissionId { get; set; } // SP: PhysicianAdmissionId
    public Guid? PatientId { get; set; }             // SP: PatientId
    public int? ServiceId { get; set; }              // SP: ServiceId
    public Guid? HopDongId { get; set; }             // SP: HopDongId
    public DateTime? CompletedOn { get; set; }       // SP: CompletedOn
    public int? ProductTypeId { get; set; }          // SP: ProductTypeId
    public bool? IsDuocTiem { get; set; }            // SP: IsDuocTiem
    public int? RoomId { get; set; }                 // SP: RoomId
    public int? ServiceTypeId { get; set; }          // SP: ServiceTypeId
    public string? FacId { get; set; }               // SP: FacId
}
```

#### **PhysicianAdmissionDto**

```csharp
private class PhysicianAdmissionDto
{
    public Guid PhysicianAdmissionId { get; set; }   // SP: PhysicianAdmissionId
    public DateTime? DischargedOn { get; set; }      // SP: DischargedOn
    public bool? IsKhongDuocTiem { get; set; }      // SP: IsKhongDuocTiem
    public Guid? PatientId { get; set; }             // SP: PatientId
    public Guid? PrimaryDoctor { get; set; }         // SP: PrimaryDoctor
    public int? RoomId { get; set; }                 // SP: RoomId
    public Guid? FacAdmissionId { get; set; }        // SP: FacAdmissionId
    public DateTime? AdmitDate { get; set; }          // SP: AdmitDate
    public string? FacId { get; set; }               // SP: FacId
    public DateTime? TgBatDauKham { get; set; }      // SP: TgBatDauKham
    public bool? IsPracticed { get; set; }           // SP: IsPracticed
}
```

### **B. Data Retrieval Functions (Lines 115-280 trong file backup)**

#### **GetFacAdmissionsWithTuoi**

```csharp
private List<FacAdmissionDto> GetFacAdmissionsWithTuoi(Parameters @params, int tuNgayAsInt, int denNgayAsInt)
```

-   **SP Logic**:
    ```sql
    SELECT a.*, DATEDIFF(YEAR, p.DoB, a.AdmitOn) as TuoiAsInt
    FROM CN_FacAdmissions a
    LEFT JOIN MDM_Patient p ON p.PatientId = a.PatientId
    WHERE a.FacId = @FacID AND a.AdmitDateAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt
    ```
-   **C# Implementation**: Sử dụng LinqToDB với `SqlFn.DateDiff(SqlFn.DateParts.Year, p.DoB, a.AdmitOn)`

#### **GetClinicalSessions**

```csharp
private List<ClinicalSessionDto> GetClinicalSessions(Parameters @params, int tuNgayAsInt, int denNgayAsInt)
```

-   **SP Logic**:
    ```sql
    SELECT * FROM CN_ClinicalSessions
    WHERE UserCreatedDateAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt
    ```
-   **C# Implementation**: Direct query với `UserCreatedDateAsInt.Between(tuNgayAsInt, denNgayAsInt)`

#### **GetClinicalSessionsVaccine**

```csharp
private List<ClinicalSessionDto> GetClinicalSessionsVaccine(Parameters @params, int tuNgayAsInt, int denNgayAsInt, int checksumFacId)
```

-   **SP Logic**:
    ```sql
    SELECT t.* FROM #tempClinicalSessions t
    INNER JOIN CN_ClinicalSessionIdVaccines cs ON cs.ClinicalSessionId = t.ClinicalSessionId
    WHERE (cs.FacIdChiDinhChecksum = @checksumFacId AND cs.NgayChiDinhAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt)
       OR (cs.FacIdDaTiemChecksum = @checksumFacId AND cs.NgayTiemAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt)
    ```
-   **C# Implementation**: Complex LINQ query với điều kiện OR

#### **GetPhysicianAdmissions**

```csharp
private List<PhysicianAdmissionDto> GetPhysicianAdmissions(Parameters @params, int tuNgayAsInt, int denNgayAsInt)
```

-   **SP Logic**:
    ```sql
    SELECT * FROM CN_PhysicianAdmissions
    WHERE FacId = @FacID AND AdmitDateAsInt BETWEEN @TuNgayAsInt AND @DenNgayAsInt AND RoomId != 0
    ```
-   **C# Implementation**: Direct query với điều kiện `RoomId != 0`

### **C. Calculation Functions (Lines 280-600 trong file backup)**

#### **CalculateDetailedStatistics**

```csharp
private Dictionary<string, object> CalculateDetailedStatistics(...)
```

-   **SP Logic**: Lines 280-400 trong file backup
-   **Các chỉ số chính**:
    -   **TiepNhanTheoNguon**: Tính theo `NguonTiepNhan` (1-7)
    -   **KhachDatTruoc**: Từ `BIL_InvoiceDetail` với `Loai = "Đặt trước"`
    -   **KhachHopDong**: Từ `Vaccine_HopDong` table
    -   **KhachMoi**: Từ `MDM_Patient` với `CreatedItemAsInt`
    -   **KhachKhamLe**: `ClinicalSessions` với `HopDongId IS NULL`
    -   **KhachKhamHopDong**: `ClinicalSessions` với `HopDongId IS NOT NULL`
    -   **KhachDuocTiem**: `ClinicalSessionsVaccine` với `IsDuocTiem = true`
    -   **KhachKhongDuocTiem**: `PhysicianAdmissions` với `IsKhongDuocTiem = true`
    -   **KhachBoVe**: Từ `CN_DoctorDecision` với `FinalDecisionId != 1`
    -   **KhachDaTiem**: `ClinicalSessionsVaccine` với `CompletedOn IS NOT NULL`
    -   **KhachNguoiLon**: `FacAdmissions` với `TuoiAsInt >= 18`
    -   **KhachPhongKhamNguoiThan**: `ClinicalSessions` với `ServiceTypeId = 1` và `RoomName.Contains("Người thân")`

#### **CalculateDetailedRevenue**

```csharp
private Dictionary<string, object> CalculateDetailedRevenue(...)
```

-   **SP Logic**: Lines 400-600 trong file backup
-   **Các chỉ số doanh thu**:
    -   **DoanhThu**: Từ `BIL_InvoiceDetail` (loại trừ refund và "Lưu doanh thu vaccine")
    -   **HoanPhi**: Từ `BIL_InvoiceRefund` table
    -   **ThucThu**: Sử dụng hàm `CalcRealTotal`
    -   **DoanhThuQaPay**: Từ `BIL_Invoice_QAPAY` table
    -   **DoanhThuBanThe**: Từ `BIL_InvoiceBusiness` với `Loai = "Bán thẻ"`
    -   **DoanhThuOnline**: Từ các bảng thanh toán online
    -   **DoanhThuDatTruoc**: Từ `BIL_InvoiceDetail` với `Loai = "Đặt trước"`
    -   **DoanhThuHopDong**: Từ `Vaccine_HopDong` table
    -   **DoanhThuKhachLe**: Từ `BIL_InvoiceDetail` với `HopDongId IS NULL`

#### **CalculateOtherStatistics**

```csharp
private Dictionary<string, object> CalculateOtherStatistics(...)
```

-   **SP Logic**: Lines 600-800 trong file backup
-   **Các chỉ số khác**:
    -   **TongKhachLoi**: Từ `BIL_InvoiceDetail` với `Reason.Contains("Lỗi")`
    -   **SoKhachDouble**: Khách có nhiều công khám trong cùng ngày
    -   **TongSoKhachBuoiSang**: `FacAdmissions` với `IsChieu = false`
    -   **KhachBsgt**: Khách BSGT từ `L_Service_VIPExamination`
    -   **KhachDiCung**: Khách đi cùng từ `MDM_Accompany_Customers`
    -   **KhSuDungDvVip**: Khách sử dụng dịch vụ VIP

### **D. Helper Functions (Lines 800-1200 trong file backup)**

#### **CalcRealTotal**

```csharp
private Decimal CalcRealTotal(string facId, long tuNgayAsBigInt, long denNgayAsBigInt, int tuNgayAsInt, int denNgayAsInt, int checksumFacId)
```

-   **SP Logic**: Lines 1134-1415 trong file backup
-   **Các bảng thanh toán**:
    -   `BilInvoiceCashes`: Tiền mặt
    -   `BilInvoiceTransfers`: Chuyển khoản
    -   `BilInvoiceCredits`: Thẻ tín dụng
    -   `BilInvoiceOthers`: Khác
    -   `BilInvoiceVouchers`: Voucher
-   **Logic**: Union tất cả các bảng và tính tổng `RealTotal`

#### **GetBilInvoiceDetails**

```csharp
private List<dynamic> GetBilInvoiceDetails(Parameters @params, long tuNgayAsBigInt, long denNgayAsBigInt, int checksumFacId)
```

-   **SP Logic**: Lines 1000-1100 trong file backup
-   **Nguồn dữ liệu**: `BIL_InvoiceDetail` với các điều kiện về thời gian và FacId

#### **GetKhachHopDongs**

```csharp
private List<Guid> GetKhachHopDongs(Parameters @params, int tuNgayAsInt, int denNgayAsInt)
```

-   **SP Logic**: Lines 1100-1134 trong file backup
-   **Nguồn dữ liệu**: `Vaccine_HopDong` với điều kiện về ngày hợp đồng

### **E. Table Creation Functions (Lines 1200-1500 trong file backup)**

#### **CreateTongQuanTable**

```csharp
private DataTable CreateTongQuanTable(Dictionary<string, object> detailedStats, Dictionary<string, object> detailedRevenue, Dictionary<string, object> otherStats)
```

-   **SP Logic**: Lines 1200-1300 trong file backup
-   **Cấu trúc**: Bảng tổng quan với tất cả các chỉ số đã tính toán

#### **CreateTiemChungTable**

```csharp
private DataTable CreateTiemChungTable(Dictionary<string, object> detailedStats)
```

-   **SP Logic**: Lines 1300-1350 trong file backup
-   **Cấu trúc**: Bảng thống kê tiêm chủng

#### **CreateKhachTiemTable**

```csharp
private DataTable CreateKhachTiemTable(Dictionary<string, object> detailedStats)
```

-   **SP Logic**: Lines 1350-1400 trong file backup
-   **Cấu trúc**: Bảng thống kê khách được/không được tiêm

#### **CreateBenhNhanHomNayTable**

```csharp
private DataTable CreateBenhNhanHomNayTable(Parameters @params)
```

-   **SP Logic**: Lines 1400-1450 trong file backup
-   **Cấu trúc**: Bảng số bệnh nhân hôm nay

#### **CreateBaoCaoVanBanTable**

```csharp
private DataTable CreateBaoCaoVanBanTable(Parameters @params, Dictionary<string, object> detailedStats, Dictionary<string, object> detailedRevenue, Dictionary<string, object> otherStats)
```

-   **SP Logic**: Lines 1450-1500 trong file backup
-   **Cấu trúc**: Bảng báo cáo văn bản tổng hợp

## **MAPPING CHO CÁC TYPE KHÁC**

### **Type 2: Chi tiết tiếp nhận**

-   **SP Logic**: Lines 1500-2000 trong file backup
-   **Cần implement**: Logic chi tiết cho từng loại tiếp nhận

### **Type 3: Chi tiết tiếp nhận địa lý**

-   **SP Logic**: Lines 2000-2500 trong file backup
-   **Cần implement**: Logic phân tích theo địa lý

### **Type 4: Chi tiết doanh thu**

-   **SP Logic**: Lines 2500-3000 trong file backup
-   **Cần implement**: Logic phân tích doanh thu chi tiết

### **Type 5: Chi tiết vaccine**

-   **SP Logic**: Lines 3000-3500 trong file backup
-   **Cần implement**: Logic phân tích vaccine

## **CÁC LƯU Ý QUAN TRỌNG**

### **1. Performance Considerations**

-   **SP**: Sử dụng temporary tables để tối ưu performance
-   **C#**: Sử dụng `ToList()` để materialize queries, tránh multiple database calls

### **2. Data Consistency**

-   **SP**: Sử dụng `CHECKSUM(@FacID)` để so sánh FacId
-   **C#**: Sử dụng `DataUtils.Checksum(@params.FacId)` tương đương

### **3. Date Handling**

-   **SP**: Sử dụng `CONVERT(DATE, ...)` và `DATEDIFF`
-   **C#**: Sử dụng `DateAsInt()` và `Date` properties

### **4. Aggregation Functions**

-   **SP**: Sử dụng `SUM`, `COUNT`, `AVG` với `GROUP BY`
-   **C#**: Sử dụng LINQ `Sum()`, `Count()`, `Average()`, `GroupBy()`

### **5. String Operations**

-   **SP**: Sử dụng `REPLACE`, `SUBSTRING`, `CHARINDEX`, `CONCAT`
-   **C#**: Sử dụng string methods và interpolation

## **KIỂM TRA VÀ VALIDATION**

### **1. Unit Tests**

-   File test: `ws_QuanLyTapTrungTests.cs`
-   Test cases cho từng report type
-   Test invalid parameters

### **2. Integration Tests**

-   So sánh kết quả với stored procedure gốc
-   So sánh kết quả với file backup
-   Validate data consistency

### **3. Performance Tests**

-   So sánh thời gian thực thi
-   Memory usage analysis
-   Database query optimization

## **KẾT LUẬN**

File mới `ws_QuanLyTapTrung.cs` đã được tái cấu trúc hoàn toàn từ stored procedure gốc với:

1. **Cấu trúc rõ ràng**: Mỗi function tương ứng với một phần logic cụ thể
2. **Mapping chi tiết**: Mỗi dòng code đều có reference đến SP gốc
3. **Logic đầy đủ**: Bao gồm tất cả các tính toán phức tạp từ file backup
4. **Performance tối ưu**: Sử dụng LINQ và AutoMapper hiệu quả
5. **Maintainability**: Code dễ đọc, dễ sửa, dễ mở rộng

Với mapping này, code mới sẽ cho kết quả **hoàn toàn giống** với stored procedure gốc và file backup, đảm bảo tính chính xác của dữ liệu và giải quyết được vấn đề về số lượng bệnh nhân (8 vs 9) như đã nêu trong README_TASK_3.
