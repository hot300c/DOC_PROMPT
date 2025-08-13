import pandas as pd
import xlsxwriter

# Đọc file CSV gốc
print("Đang đọc file merged_procedures_fe_api-merged.csv...")
df_merged = pd.read_csv(r'c:\PROJECTS\DOCS_PROMPT\data\merged_procedures_fe_api-merged.csv')

# Đọc file Excel BE_API
print("Đang đọc file BE_API.xlsx...")
df_be_api = pd.read_excel(r'c:\PROJECTS\DOCS_PROMPT\data\BE_API.xlsx')

print(f"Số dòng trong file merged: {len(df_merged)}")
print(f"Số dòng trong file BE_API: {len(df_be_api)}")

# Hiển thị cột của file BE_API
print("\nCác cột trong file BE_API:")
print(df_be_api.columns.tolist())

# Hiển thị cột của file merged
print("\nCác cột trong file merged:")
print(df_merged.columns.tolist())

# Tìm cột ProcedureName trong file merged và cột tên file trong BE_API
print("\nTìm cột khớp để merge...")

# Kiểm tra xem có cột ProcedureName trong file merged không
if 'ProcedureName' in df_merged.columns:
    print("✓ Tìm thấy cột ProcedureName trong file merged")
else:
    print("✗ Không tìm thấy cột ProcedureName trong file merged")
    print("Các cột có sẵn:", df_merged.columns.tolist())

# Kiểm tra cột tên file trong BE_API
print(f"Các cột trong BE_API: {df_be_api.columns.tolist()}")

# Tìm cột chứa tên procedure trong BE_API (có thể là cột đầu tiên hoặc cột có tên file)
be_api_file_column = None
for col in df_be_api.columns:
    if 'file' in col.lower() or 'name' in col.lower() or 'procedure' in col.lower():
        be_api_file_column = col
        break

if be_api_file_column is None:
    # Nếu không tìm thấy, lấy cột đầu tiên
    be_api_file_column = df_be_api.columns[0]

print(f"Sử dụng cột '{be_api_file_column}' trong BE_API để merge")

# Thực hiện merge
print("\nĐang thực hiện merge...")
merged_df = df_merged.merge(
    df_be_api, 
    left_on='ProcedureName', 
    right_on=be_api_file_column, 
    how='left', 
    indicator=True
)

# Thêm cột TIMTHAY_API_BE
merged_df['TIMTHAY_API_BE'] = merged_df['_merge'].map({
    'left_only': 'CHUA_THAY',
    'both': 'DA_THAY',
    'right_only': 'CHUA_THAY'
})

# Xóa cột _merge tạm thời
merged_df = merged_df.drop('_merge', axis=1)

# Lưu file kết quả
output_file = r'c:\PROJECTS\DOCS_PROMPT\data\merged_procedures_fe_api_be_final.csv'
merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\nĐã tạo file kết quả: {output_file}")
print(f"Tổng số dòng trong file kết quả: {len(merged_df)}")

# Thống kê
da_thay_count = len(merged_df[merged_df['TIMTHAY_API_BE'] == 'DA_THAY'])
chua_thay_count = len(merged_df[merged_df['TIMTHAY_API_BE'] == 'CHUA_THAY'])

print(f"\nThống kê:")
print(f"- DA_THAY: {da_thay_count} dòng")
print(f"- CHUA_THAY: {chua_thay_count} dòng")
print(f"- Tổng: {da_thay_count + chua_thay_count} dòng")

# Hiển thị một số dòng mẫu
print(f"\nCác cột trong file kết quả:")
print(merged_df.columns.tolist())

print(f"\n5 dòng đầu tiên:")
print(merged_df.head().to_string())
