Task 2: Làm 1 handler để chuyển sang store procedure.

Làm 1 page handler thay thế store procedure phần tiep-nhan
Tạo testcase đủ để testing các trường hợp.
Tạo k8s để testing API.



Rule:
Code nên cẩn thận, kỹ và có log, code đầy đủ, và convert phải chuyển đúng, chính xác.
Tạo test case cũng phải nhiều và đủ trường hợp.

TODO:
1. Quét toàn bộ danh sách store procedure thành bảng để đánh dấu cái nào đã chuyển rồi, cái nào chưa chuyển.
https://vacxinvietnam-my.sharepoint.com/:x:/g/personal/phucnnd_vnvc_vn/EZRJHalQD2ZFkC2kGQPOEaMBivz4dHWH2XRsc11Tj0IYow?e=Zk3684

2. Quét toàn bộ danh sách các API trên genie để xác định cái nào chưa có/ cái nào đã có so với code aladin.
Prompt:
trong web genie này, tôi cần quét toàn bộ api của trang mà có link dạng này link @https://dev-genie.vnvc.info/tiep-nhan/tiep-nhan-moi
và toàn bộ các nút trong đó, và sâu tất cả trang con nếu có thể để lọc ra toàn bộ các API mà nó gọi đến nhé.


3. Đánh dấu và đề xuất viết.
3.1 Kiểm tra lại theo danh sách các API tiep-nhan
prompt:
từ toàn bộ service trong danh sách @README_TIEP_NHAN_MOI_APIS.csv thì hãy kiểm tra lại trong project aladdin xem và liệt kê cho tôi dạng bảng chứa 2 cột là cái API nào gọi store procedure hay handler, hãy đánh dấu nó để tôi nhận biết cái nào chưa chuyển sang code để tôi tiếp tục convert nhé.
Và nhớ là xuất ra csv nhé



###
TODO số 1 prompt AI:
tôi cần lấy tất cả store procedure để xuất thành danh sách trong mssql. Và cũng nên có cột đánh dấu được là nó có gọi view không. 
không đúng, nó chỉ xuất ra 1 trong khi tôi có rất nhiều store procedure, ngoài ra, thêm cột thể hiện các tables nào mà store procedure có gọi đến nó.
USE QAHosGenericDB;

SELECT
    SCHEMA_NAME(p.schema_id) AS ProcedureSchema,
    p.name AS ProcedureName,
    p.object_id,
    CASE 
      WHEN EXISTS (
        SELECT 1
        FROM sys.sql_expression_dependencies d
        JOIN sys.objects o ON d.referenced_id = o.object_id
        WHERE d.referencing_id = p.object_id AND o.type = 'V'
      ) THEN 1 ELSE 0 END AS CallsView,
    -- Danh sách bảng (U)
    ISNULL(
      STUFF((
        SELECT DISTINCT ', ' + QUOTENAME(SCHEMA_NAME(o.schema_id)) + '.' + QUOTENAME(o.name)
        FROM sys.sql_expression_dependencies d2
        JOIN sys.objects o ON d2.referenced_id = o.object_id
        WHERE d2.referencing_id = p.object_id AND o.type = 'U'
        FOR XML PATH(''), TYPE
      ).value('.', 'NVARCHAR(MAX)'), 1, 2, '')
    , '') AS TablesCalled,
    -- Danh sách view (V) — tiện kiểm tra chi tiết
    ISNULL(
      STUFF((
        SELECT DISTINCT ', ' + QUOTENAME(SCHEMA_NAME(o2.schema_id)) + '.' + QUOTENAME(o2.name)
        FROM sys.sql_expression_dependencies d3
        JOIN sys.objects o2 ON d3.referenced_id = o2.object_id
        WHERE d3.referencing_id = p.object_id AND o2.type = 'V'
        FOR XML PATH(''), TYPE
      ).value('.', 'NVARCHAR(MAX)'), 1, 2, '')
    , '') AS ViewsCalled
FROM sys.procedures p
ORDER BY ProcedureSchema, ProcedureName;



TODO số 2 prompt AI:
