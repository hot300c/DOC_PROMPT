# Kết Quả Merge Procedures và FE_API

## Tổng quan
Đã thành công merge 2 file CSV:
- `Procedure.csv` (4,409 procedures)
- `FE_API.csv` (137 API calls)

## Thống kê
- **Tổng số procedures**: 4,407
- **Procedures được tìm thấy (DA_CO)**: 93 (2.11%)
- **Procedures không tìm thấy (CHUA_CO)**: 4,314 (97.89%)

## Files được tạo

### 1. `merged_procedures_fe_api.csv`
File chính chứa tất cả procedures với thông tin merge:
- **Cột từ Procedure**: ProcedureSchema, ProcedureName, object_id, CallsView, TablesCalled, ViewsCalled
- **Cột Status**: DA_CO (tìm thấy) hoặc CHUA_CO (không tìm thấy)
- **Cột từ FE_API**: FE_API_Category, FE_API_Service/Usage, FE_API_Command, FE_API_Type, FE_API_Files, FE_API_Found

### 2. `merge_summary_report.txt`
Báo cáo tóm tắt với thống kê chi tiết

## Cấu trúc file output
```
ProcedureSchema,ProcedureName,object_id,CallsView,TablesCalled,ViewsCalled,Status,FE_API_Category,FE_API_Service/Usage,FE_API_Command,FE_API_Type,FE_API_Files,FE_API_Found
```

## Ví dụ về procedures được tìm thấy (DA_CO)
- `ws_MDM_Ethnicity_List` → SettingService.fetchEthnicity
- `ws_MDM_Province_Get` → SettingService.fetchProvince
- `ws_L_Country_ListV2` → SettingService.fetchCountry
- `ws_CN_FacAdmissions_GetExistTodayV2` → Get admission exist today
- `ws_Vaccine_PhacDoBenhNhan_Save` → Save patient regimen

## Scripts được tạo
1. `merge_csv_script.py` - Script Python (cần pandas)
2. `merge_csv_script.ps1` - Script PowerShell (đã chạy thành công)

## Phân tích
- Tỷ lệ tìm thấy thấp (2.11%) cho thấy phần lớn stored procedures chưa được sử dụng trong frontend
- Các procedures được sử dụng chủ yếu thuộc nhóm:
  - Patient Management
  - Vaccine Management  
  - Contract Management
  - Setting Services
  - Room Management

## Cách sử dụng
1. Mở file `merged_procedures_fe_api.csv` trong Excel hoặc tool phân tích dữ liệu
2. Lọc theo cột `Status` để xem:
   - `DA_CO`: Procedures đã được sử dụng trong frontend
   - `CHUA_CO`: Procedures chưa được sử dụng
3. Sử dụng thông tin từ các cột FE_API để hiểu cách procedures được gọi
