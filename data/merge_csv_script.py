import pandas as pd
import csv
from typing import Dict, List, Tuple

def merge_csv_files():
    """
    Merge FE_API.csv và Procedure.csv dựa trên cột Command và ProcedureName
    Tạo file mới với các cột từ Procedure trước, sau đó từ FE_API
    Thêm cột đánh dấu DA_CO/CHUA_CO
    """
    
    # Đọc file FE_API.csv
    print("Đang đọc file FE_API.csv...")
    fe_api_df = pd.read_csv('FE_API.csv')
    print(f"Đã đọc {len(fe_api_df)} dòng từ FE_API.csv")
    
    # Đọc file Procedure.csv
    print("Đang đọc file Procedure.csv...")
    procedure_df = pd.read_csv('Procedure.csv')
    print(f"Đã đọc {len(procedure_df)} dòng từ Procedure.csv")
    
    # Tạo dictionary để map Command -> FE_API data
    fe_api_dict = {}
    for _, row in fe_api_df.iterrows():
        command = row['Command']
        if pd.notna(command) and command.strip():
            fe_api_dict[command.strip()] = row.to_dict()
    
    print(f"Đã tạo {len(fe_api_dict)} entries từ FE_API")
    
    # Tạo list để lưu kết quả merge
    merged_data = []
    
    # Xử lý từng procedure
    for _, proc_row in procedure_df.iterrows():
        proc_name = proc_row['ProcedureName']
        
        # Tìm kiếm trong FE_API
        fe_api_match = fe_api_dict.get(proc_name)
        
        # Tạo row mới với thứ tự cột: Procedure trước, FE_API sau
        new_row = {}
        
        # Thêm tất cả cột từ Procedure
        for col in procedure_df.columns:
            new_row[col] = proc_row[col]
        
        # Thêm cột đánh dấu
        if fe_api_match:
            new_row['Status'] = 'DA_CO'
            # Thêm tất cả cột từ FE_API
            for col in fe_api_df.columns:
                new_row[f'FE_API_{col}'] = fe_api_match[col]
        else:
            new_row['Status'] = 'CHUA_CO'
            # Thêm cột trống cho FE_API
            for col in fe_api_df.columns:
                new_row[f'FE_API_{col}'] = ''
        
        merged_data.append(new_row)
    
    # Tạo DataFrame từ merged data
    merged_df = pd.DataFrame(merged_data)
    
    # Lưu file kết quả
    output_filename = 'merged_procedures_fe_api.csv'
    merged_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    
    print(f"Đã tạo file {output_filename} với {len(merged_df)} dòng")
    
    # Thống kê
    da_co_count = len(merged_df[merged_df['Status'] == 'DA_CO'])
    chua_co_count = len(merged_df[merged_df['Status'] == 'CHUA_CO'])
    
    print(f"\nThống kê:")
    print(f"- Tổng số procedures: {len(merged_df)}")
    print(f"- DA_CO (tìm thấy): {da_co_count}")
    print(f"- CHUA_CO (không tìm thấy): {chua_co_count}")
    print(f"- Tỷ lệ tìm thấy: {da_co_count/len(merged_df)*100:.2f}%")
    
    return merged_df

def create_summary_report(merged_df: pd.DataFrame):
    """
    Tạo báo cáo tóm tắt về các procedures được tìm thấy và không tìm thấy
    """
    
    # Procedures được tìm thấy
    found_procedures = merged_df[merged_df['Status'] == 'DA_CO']
    not_found_procedures = merged_df[merged_df['Status'] == 'CHUA_CO']
    
    # Lưu danh sách procedures được tìm thấy
    found_filename = 'procedures_found_in_fe_api.csv'
    found_procedures.to_csv(found_filename, index=False, encoding='utf-8-sig')
    print(f"Đã lưu danh sách procedures được tìm thấy vào {found_filename}")
    
    # Lưu danh sách procedures không tìm thấy
    not_found_filename = 'procedures_not_found_in_fe_api.csv'
    not_found_procedures.to_csv(not_found_filename, index=False, encoding='utf-8-sig')
    print(f"Đã lưu danh sách procedures không tìm thấy vào {not_found_filename}")
    
    # Tạo báo cáo tóm tắt
    summary_filename = 'merge_summary_report.txt'
    with open(summary_filename, 'w', encoding='utf-8') as f:
        f.write("BÁO CÁO TÓM TẮT MERGE PROCEDURES VÀ FE_API\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Tổng số procedures: {len(merged_df)}\n")
        f.write(f"Procedures được tìm thấy (DA_CO): {len(found_procedures)}\n")
        f.write(f"Procedures không tìm thấy (CHUA_CO): {len(not_found_procedures)}\n")
        f.write(f"Tỷ lệ tìm thấy: {len(found_procedures)/len(merged_df)*100:.2f}%\n\n")
        
        f.write("TOP 10 PROCEDURES KHÔNG TÌM THẤY:\n")
        f.write("-" * 30 + "\n")
        for i, proc_name in enumerate(not_found_procedures['ProcedureName'].head(10)):
            f.write(f"{i+1}. {proc_name}\n")
        
        f.write("\nTOP 10 PROCEDURES ĐƯỢC TÌM THẤY:\n")
        f.write("-" * 30 + "\n")
        for i, proc_name in enumerate(found_procedures['ProcedureName'].head(10)):
            f.write(f"{i+1}. {proc_name}\n")
    
    print(f"Đã tạo báo cáo tóm tắt: {summary_filename}")

if __name__ == "__main__":
    print("Bắt đầu merge CSV files...")
    merged_df = merge_csv_files()
    create_summary_report(merged_df)
    print("Hoàn thành!")
