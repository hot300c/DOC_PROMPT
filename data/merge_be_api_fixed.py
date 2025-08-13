import pandas as pd

# Đọc file CSV gốc
print("Đang đọc file merged_procedures_fe_api-merged.csv...")
df_merged = pd.read_csv(r'c:\PROJECTS\DOCS_PROMPT\data\merged_procedures_fe_api-merged.csv')

# Đọc file Excel BE_API
print("Đang đọc file BE_API.xlsx...")
df_be_api = pd.read_excel(r'c:\PROJECTS\DOCS_PROMPT\data\BE_API.xlsx')

print(f"Số dòng trong file merged: {len(df_merged)}")
print(f"Số dòng trong file BE_API: {len(df_be_api)}")

# Chuẩn bị tên file từ BE_API (loại bỏ .cs)
df_be_api['File_Name_Clean'] = df_be_api['Tên File'].str.replace('.cs', '', case=False)

# Chuẩn bị tên procedure từ merged (loại bỏ dấu gạch dưới đầu nếu có)
df_merged['ProcedureName_Clean'] = df_merged['ProcedureName'].str.replace('^_', '', regex=True)

# Thực hiện merge với tên đã được chuẩn hóa
print("\nĐang thực hiện merge với tên đã được chuẩn hóa...")
merged_df = df_merged.merge(
    df_be_api, 
    left_on='ProcedureName_Clean', 
    right_on='File_Name_Clean', 
    how='left', 
    indicator=True
)

# Thêm cột TIMTHAY_API_BE
merged_df['TIMTHAY_API_BE'] = merged_df['_merge'].map({
    'left_only': 'CHUA_THAY',
    'both': 'DA_THAY',
    'right_only': 'CHUA_THAY'
})

# Xóa các cột tạm thời
merged_df = merged_df.drop(['_merge', 'ProcedureName_Clean', 'File_Name_Clean'], axis=1)

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

# Hiển thị các cột trong file kết quả
print(f"\nCác cột trong file kết quả:")
print(merged_df.columns.tolist())

# Hiển thị một số dòng khớp
print(f"\n5 dòng DA_THAY đầu tiên:")
da_thay_rows = merged_df[merged_df['TIMTHAY_API_BE'] == 'DA_THAY']
if len(da_thay_rows) > 0:
    for i, row in da_thay_rows.head().iterrows():
        print(f"Procedure: {row['ProcedureName']} <-> File: {row['Tên File']}")
else:
    print("Không có dòng nào khớp")

# Hiển thị tổng quan về các cột BE_API được thêm vào
print(f"\nCác cột BE_API được thêm vào:")
be_api_columns = ['STT', 'Tên File', 'Kích thước', 'Số dòng']
for col in be_api_columns:
    if col in merged_df.columns:
        print(f"- {col}")

print(f"\nHoàn thành!")
