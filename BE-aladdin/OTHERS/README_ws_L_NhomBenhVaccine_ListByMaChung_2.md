### ws_L_NhomBenhVaccine_ListByMaChung — Notes

This document describes the behavior, rules, and implementation details for the handler `ws_L_NhomBenhVaccine_ListByMaChung` that migrates the stored procedure `[dbo].[ws_L_NhomBenhVaccine_ListByMaChung]` to C# using LinqToDB.

### Purpose
- **Logic**: Lấy danh sách nhóm bệnh vaccine theo mã chung (`MaChung`).
- **Output**: Một `DataSet` gồm một bảng duy nhất `MaNhomBenh` với một cột `MaNhomBenh` chứa chuỗi các `NhomBenhID` được nối bằng dấu `;` và có dấu `;` ở cuối nếu có dữ liệu. Nếu không có dữ liệu, chuỗi rỗng.

### Parameters
- **MaChung (required)**: Mã chung để lọc.
- **UserID (required by flow)**: Được auto-injected bởi `DataRequestDispatcher`. Nếu thiếu hoặc rỗng, trả về `DataSet` rỗng (giống SP `RETURN` sớm).
- Các tham số khác theo chữ ký SP gốc (ví dụ `SessionID`, `FacID`, `PatientID`, `DoiTuongID`) không ảnh hưởng tới logic xử lý của handler này.

### Rules and Conventions
- **Migration rules applied**:
  - Convert T‑SQL to LinqToDB query.
  - Bảo toàn nghiệp vụ của thủ tục gốc: lọc theo `MaChung` và ghép `NhomBenhID` thành chuỗi có `;` ở cuối khi có kết quả.
  - Sử dụng `WITH (NOLOCK)` tương đương bằng `SqlServerHints.Table.NoLock` cho hiệu năng/đọc không khóa.
  - Kiểm tra xác thực: nếu không xác định được `UserID` thì trả về rỗng (không throw), khớp SP `RETURN;`.
  - Định dạng kết quả: chỉ 1 bảng `MaNhomBenh` với chuỗi đã ghép; không trả về bảng chi tiết phụ.
- **Khác biệt có chủ ý so với một số handler khác**:
  - Không lọc theo `FacID` và không kiểm tra `IsActive` trong bảng nhóm bệnh (theo đúng SP gốc).
- **Logging**:
  - Hiện tại handler không log nội bộ. Hệ thống đã cấu hình logging ở WebService (Serilog/ASP.NET) và có thể theo dõi ở tầng API/dispatcher. Có thể bổ sung `ILogger<T>` nếu cần sau.

### Data Access
- Nguồn dữ liệu: `QAHosGenericDB.LNhomBenhVaccineDetails` join `QAHosGenericDB.LNhomBenhVaccines` (đều `NoLock`).
- Điều kiện: `LNhomBenhVaccineDetail.MaChung == @MaChung`.
- Lấy ra danh sách `NhomBenhID`, sau đó ghép bằng `;` theo đúng định dạng SP gốc.

### Output Format
- `DataSet` với một bảng:
  - Bảng: `MaNhomBenh`
  - Cột: `MaNhomBenh` (string)
  - Giá trị: Chuỗi rỗng nếu không có dữ liệu; nếu có, là danh sách `NhomBenhID` nối `;` và có `;` ở cuối, ví dụ: `"1;3;5;"`.

### Stored Procedure (original reference)

```sql
CREATE PROCEDURE [dbo].[ws_L_NhomBenhVaccine_ListByMaChung]
(
    @SessionID VARCHAR(MAX),
    @MaChung VARCHAR(100),
    @FacID VARCHAR(10),
    @PatientID UNIQUEIDENTIFIER,
    @DoiTuongID INT
)
AS
SET NOCOUNT ON;

DECLARE @debug INT = 0;

IF @debug = 1
BEGIN
    CREATE TABLE #dt
    (
        step VARCHAR(MAX),
        duration INT
    );

    DECLARE @step VARCHAR(MAX) = '1';
    DECLARE @tstart DATETIME = GETDATE();
END;

DECLARE @UserID UNIQUEIDENTIFIER;

SELECT @UserID = UserID
FROM [Security]..[Sessions] WITH (NOLOCK)
WHERE [SessionID] = @SessionID;

IF @UserID IS NULL
    RETURN;

DECLARE @MaNhomBenhs VARCHAR(200) = '';

SELECT @MaNhomBenhs += CONVERT(NVARCHAR(10), NhomBenhID) + ';'
FROM dbo.L_NhomBenhVaccineDetail NBD WITH (NOLOCK)
JOIN dbo.L_NhomBenhVaccine NB WITH (NOLOCK) ON NBD.NhomBenhID = NB.ID
WHERE NBD.MaChung = @MaChung;

SELECT @MaNhomBenhs AS MaNhomBenh;

IF @debug = 1
BEGIN
    SELECT @step step, DATEDIFF(ms, @tstart, GETDATE()) duration;
END;
```

### Testing Notes
- Handler được tạo thông qua `IHandlerFactory` và được gọi bởi `DataRequestDispatcher` khi `PreferStoredProcedure=false` cho command tương ứng.
- Yêu cầu cung cấp `UserID` trong `parameters` (dispatcher sẽ inject nếu có `userId` từ context). Nếu không có `UserID`, kết quả là `DataSet` rỗng.

### Unit Tests

- Vị trí test: `WebService.Handlers.Tests/QAHosGenericDB/ws_L_NhomBenhVaccine_ListByMaChung_Test.cs`
- Base class: `WebService.Handlers.Tests.Base.BaseHandlerTest`
- Khởi tạo handler trong test:

  ```csharp
  private readonly ws_L_NhomBenhVaccine_ListByMaChung _handler;

  public ws_L_NhomBenhVaccine_ListByMaChung_Test()
  {
      _handler = new ws_L_NhomBenhVaccine_ListByMaChung(DbConnection, MasterDataService);
  }
  ```

- Các kịch bản cần cover (khớp logic đã migrate):
  - MaChung hợp lệ + có UserID: trả về `DataSet` có tối thiểu 1 bảng và có bảng `MaNhomBenh`; chuỗi kết quả có dạng `"<id1>;<id2>;...;"` hoặc rỗng nếu không có dữ liệu.
  - Thiếu `UserID` hoặc `UserID == Guid.Empty`: trả về `DataSet` rỗng (không ném exception).
  - Thiếu hoặc rỗng `MaChung`: ném `ArgumentException` với thông điệp "MaChung parameter is required".
  - Không yêu cầu `FacID`; không có bảng chi tiết thứ hai (khác với version cũ).

- Ví dụ test cơ bản:

  ```csharp
  [Fact]
  public void WithValidParameters_Returns_MaNhomBenh_Table()
  {
      var parameters = new Dictionary<string, object?>
      {
          ["MaChung"] = "1000001",
          ["UserID"] = Guid.NewGuid()
      };

      DataSet result = _handler.Handle(parameters);

      Assert.NotNull(result);
      Assert.True(result.Tables.Count >= 1);
      Assert.True(result.Tables.Contains("MaNhomBenh"));
  }

  [Fact]
  public void MissingUserId_Returns_Empty_DataSet()
  {
      var parameters = new Dictionary<string, object?>
      {
          ["MaChung"] = "1000001"
      };

      DataSet result = _handler.Handle(parameters);
      Assert.NotNull(result);
      Assert.Equal(0, result.Tables.Count);
  }

  [Fact]
  public void MissingMaChung_Throws_ArgumentException()
  {
      var parameters = new Dictionary<string, object?>
      {
          ["UserID"] = Guid.NewGuid()
      };

      var ex = Assert.Throws<ArgumentException>(() => _handler.Handle(parameters));
      Assert.Contains("MaChung parameter is required", ex.Message);
  }
  ```

- Ví dụ test dùng YAML (theo `BaseHandlerTest`):

  ```csharp
  [Theory]
  [MemberData(nameof(TestData), "QAHosGenericDB", "ws_L_NhomBenhVaccine_ListByMaChung")]
  public void Should_Match_Expected_From_Yaml(string testCase, Dictionary<string, object?> parameters, DataSet expected)
  {
      DataSet result = _handler.Handle(parameters);
      // So sánh số bảng và số cột/hàng theo expected
      Assert.Equal(expected.Tables.Count, result.Tables.Count);
      for (int i = 0; i < expected.Tables.Count; i++)
      {
          Assert.Equal(expected.Tables[i].Columns.Count, result.Tables[i].Columns.Count);
          Assert.Equal(expected.Tables[i].Rows.Count, result.Tables[i].Rows.Count);
      }
  }
  ```

- Mẫu test case YAML tối thiểu cho kết quả có dữ liệu:

  ```yaml
  # Test case 1: Return MaNhomBenh with ids
  initialData:
    - database: QAHosGenericDB
      table: L_NhomBenhVaccine
      rows:
        - ID: 1
          TenNhomBenh: N1
        - ID: 2
          TenNhomBenh: N2
    - database: QAHosGenericDB
      table: L_NhomBenhVaccineDetail
      rows:
        - ID: 11
          NhomBenhID: 1
          MaChung: 1000001
        - ID: 12
          NhomBenhID: 2
          MaChung: 1000001

  parameters:
    MaChung: 1000001
    UserID: 11111111-1111-1111-1111-111111111111

  expectedResult:
    MaNhomBenh:
      - MaNhomBenh: "1;2;"
  ```

- Chạy test:
  - `dotnet test WebService.Handlers.Tests/WebService.Handlers.Tests.csproj`
  - Có thể filter theo tên: `--filter FullyQualifiedName~ws_L_NhomBenhVaccine_ListByMaChung_Test`

### Change Log
- 2025-08: Đồng bộ logic với SP gốc: bỏ lọc `FacID`/`IsActive`, trả về một bảng `MaNhomBenh`, `RETURN` sớm khi thiếu `UserID` và giữ định dạng chuỗi kết quả như SP.


