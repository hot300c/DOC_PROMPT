import pandas as pd

# Đọc file CSV gốc
df_merged = pd.read_csv(r'c:\PROJECTS\DOCS_PROMPT\data\merged_procedures_fe_api-merged.csv')

# Đọc file Excel BE_API
df_be_api = pd.read_excel(r'c:\PROJECTS\DOCS_PROMPT\data\BE_API.xlsx')

print("=== KIỂM TRA TÊN PROCEDURE VÀ FILE ===")
print(f"Số dòng trong file merged: {len(df_merged)}")
print(f"Số dòng trong file BE_API: {len(df_be_api)}")

# Hiển thị một số tên procedure từ file merged
print("\n=== 10 TÊN PROCEDURE ĐẦU TIÊN TỪ FILE MERGED ===")
for i, proc_name in enumerate(df_merged['ProcedureName'].head(10)):
    print(f"{i+1}. {proc_name}")

# Hiển thị một số tên file từ BE_API
print("\n=== 10 TÊN FILE ĐẦU TIÊN TỪ BE_API ===")
for i, file_name in enumerate(df_be_api['Tên File'].head(10)):
    print(f"{i+1}. {file_name}")

# Tìm các procedure có chứa "ws_" (web service)
print("\n=== CÁC PROCEDURE CÓ CHỨA 'ws_' ===")
ws_procedures = df_merged[df_merged['ProcedureName'].str.contains('ws_', case=False, na=False)]
print(f"Số procedure có 'ws_': {len(ws_procedures)}")
for i, proc_name in enumerate(ws_procedures['ProcedureName'].head(10)):
    print(f"{i+1}. {proc_name}")

# Tìm các file có chứa "ws_" trong BE_API
print("\n=== CÁC FILE CÓ CHỨA 'ws_' TRONG BE_API ===")
ws_files = df_be_api[df_be_api['Tên File'].str.contains('ws_', case=False, na=False)]
print(f"Số file có 'ws_': {len(ws_files)}")
for i, file_name in enumerate(ws_files['Tên File'].head(10)):
    print(f"{i+1}. {file_name}")

# Thử tìm khớp bằng cách loại bỏ phần mở rộng .cs
print("\n=== THỬ TÌM KHỚP SAU KHI LOẠI BỎ .cs ===")
be_api_names_clean = df_be_api['Tên File'].str.replace('.cs', '', case=False)
merged_names_clean = df_merged['ProcedureName']

# Tìm các khớp
matches = []
for proc_name in merged_names_clean:
    for file_name in be_api_names_clean:
        if proc_name.lower() == file_name.lower():
            matches.append((proc_name, file_name))

print(f"Số khớp tìm được: {len(matches)}")
for i, (proc, file) in enumerate(matches[:10]):
    print(f"{i+1}. Procedure: {proc} <-> File: {file}")

# Thử tìm khớp một phần
print("\n=== THỬ TÌM KHỚP MỘT PHẦN ===")
partial_matches = []
for proc_name in merged_names_clean.head(20):  # Chỉ kiểm tra 20 procedure đầu
    for file_name in be_api_names_clean:
        if proc_name.lower() in file_name.lower() or file_name.lower() in proc_name.lower():
            partial_matches.append((proc_name, file_name))

print(f"Số khớp một phần tìm được: {len(partial_matches)}")
for i, (proc, file) in enumerate(partial_matches[:10]):
    print(f"{i+1}. Procedure: {proc} <-> File: {file}")
