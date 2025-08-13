import pandas as pd
import xlsxwriter

# Đọc file CSV kết quả
print("Đang đọc file merged_procedures_fe_api_be_final.csv...")
df_final = pd.read_csv(r'c:\PROJECTS\DOCS_PROMPT\data\merged_procedures_fe_api_be_final.csv')

print(f"Số dòng trong file kết quả: {len(df_final)}")

# Tạo file Excel
output_excel = r'c:\PROJECTS\DOCS_PROMPT\data\merged_procedures_fe_api_be_final.xlsx'

# Sử dụng xlsxwriter để tạo file Excel với định dạng
with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
    # Ghi dữ liệu vào sheet
    df_final.to_excel(writer, sheet_name='Merged_Data', index=False)
    
    # Lấy workbook và worksheet để format
    workbook = writer.book
    worksheet = writer.sheets['Merged_Data']
    
    # Tạo format cho header
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    # Tạo format cho cột TIMTHAY_API_BE
    da_thay_format = workbook.add_format({
        'fg_color': '#C6EFCE',  # Màu xanh nhạt
        'border': 1
    })
    
    chua_thay_format = workbook.add_format({
        'fg_color': '#FFC7CE',  # Màu đỏ nhạt
        'border': 1
    })
    
    # Format header
    for col_num, value in enumerate(df_final.columns.values):
        worksheet.write(0, col_num, value, header_format)
    
    # Format cột TIMTHAY_API_BE
    timthay_col = df_final.columns.get_loc('TIMTHAY_API_BE')
    for row_num in range(1, len(df_final) + 1):
        cell_value = df_final.iloc[row_num - 1]['TIMTHAY_API_BE']
        if cell_value == 'DA_THAY':
            worksheet.write(row_num, timthay_col, cell_value, da_thay_format)
        else:
            worksheet.write(row_num, timthay_col, cell_value, chua_thay_format)
    
    # Điều chỉnh độ rộng cột
    for col_num, column in enumerate(df_final.columns):
        max_length = max(
            df_final[column].astype(str).apply(len).max(),
            len(str(column))
        )
        # Giới hạn độ rộng tối đa
        column_width = min(max_length + 2, 50)
        worksheet.set_column(col_num, col_num, column_width)
    
    # Tạo sheet thống kê
    stats_df = pd.DataFrame({
        'Thống kê': ['Tổng số dòng', 'DA_THAY', 'CHUA_THAY', 'Tỷ lệ khớp (%)'],
        'Số lượng': [
            len(df_final),
            len(df_final[df_final['TIMTHAY_API_BE'] == 'DA_THAY']),
            len(df_final[df_final['TIMTHAY_API_BE'] == 'CHUA_THAY']),
            round(len(df_final[df_final['TIMTHAY_API_BE'] == 'DA_THAY']) / len(df_final) * 100, 2)
        ]
    })
    
    stats_df.to_excel(writer, sheet_name='Thống_kê', index=False)
    
    # Format sheet thống kê
    stats_worksheet = writer.sheets['Thống_kê']
    for col_num, value in enumerate(stats_df.columns.values):
        stats_worksheet.write(0, col_num, value, header_format)
    
    # Điều chỉnh độ rộng cột cho sheet thống kê
    stats_worksheet.set_column(0, 0, 20)
    stats_worksheet.set_column(1, 1, 15)

print(f"Đã tạo file Excel: {output_excel}")

# Hiển thị thống kê
da_thay_count = len(df_final[df_final['TIMTHAY_API_BE'] == 'DA_THAY'])
chua_thay_count = len(df_final[df_final['TIMTHAY_API_BE'] == 'CHUA_THAY'])
total_count = len(df_final)
match_percentage = round(da_thay_count / total_count * 100, 2)

print(f"\nThống kê:")
print(f"- Tổng số dòng: {total_count}")
print(f"- DA_THAY: {da_thay_count} dòng")
print(f"- CHUA_THAY: {chua_thay_count} dòng")
print(f"- Tỷ lệ khớp: {match_percentage}%")

print(f"\nCác cột trong file kết quả:")
for i, col in enumerate(df_final.columns, 1):
    print(f"{i}. {col}")

print(f"\nHoàn thành!")
