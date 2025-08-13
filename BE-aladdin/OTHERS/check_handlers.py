#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để kiểm tra danh sách stored procedures và so sánh với handlers hiện có
"""

import os
import re
from pathlib import Path

def extract_stored_procedures_from_file(file_path):
    """Đọc file README_LISTSP.md và trích xuất danh sách stored procedures"""
    stored_procedures = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Tách từng dòng và lọc các stored procedures
            lines = content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    stored_procedures.append(line)
    except Exception as e:
        print(f"Lỗi khi đọc file {file_path}: {e}")
    
    return stored_procedures

def find_handlers_in_directory(directory):
    """Tìm tất cả các file handler trong thư mục"""
    handlers = []
    
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.cs'):
                    file_path = os.path.join(root, file)
                    # Đọc nội dung file để tìm tên stored procedure
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Tìm tên stored procedure trong file
                            # Thường có dạng: "ws_ProcedureName" hoặc tương tự
                            matches = re.findall(r'ws_[A-Za-z0-9_]+', content)
                            if matches:
                                handlers.extend(matches)
                    except Exception as e:
                        print(f"Lỗi khi đọc file {file_path}: {e}")
    except Exception as e:
        print(f"Lỗi khi quét thư mục {directory}: {e}")
    
    return list(set(handlers))  # Loại bỏ trùng lặp

def compare_stored_procedures_with_handlers(stored_procedures, handlers):
    """So sánh danh sách stored procedures với handlers"""
    # Chuyển đổi thành set để dễ so sánh
    sp_set = set(stored_procedures)
    handler_set = set(handlers)
    
    # Tìm các stored procedures có handler
    have_handlers = sp_set.intersection(handler_set)
    
    # Tìm các stored procedures chưa có handler
    missing_handlers = sp_set - handler_set
    
    # Tìm các handlers không có trong danh sách stored procedures
    extra_handlers = handler_set - sp_set
    
    return {
        'have_handlers': sorted(list(have_handlers)),
        'missing_handlers': sorted(list(missing_handlers)),
        'extra_handlers': sorted(list(extra_handlers))
    }

def main():
    # Đường dẫn đến file README_LISTSP.md
    sp_file = "DOCS/README_LISTSP.md"
    
    # Đường dẫn đến thư mục handlers
    handlers_dir = "WebService.Handlers"
    
    print("=== KIỂM TRA STORED PROCEDURES VÀ HANDLERS ===\n")
    
    # Đọc danh sách stored procedures
    print("Đang đọc danh sách stored procedures...")
    stored_procedures = extract_stored_procedures_from_file(sp_file)
    print(f"Tìm thấy {len(stored_procedures)} stored procedures\n")
    
    # Tìm các handlers
    print("Đang tìm các handlers...")
    handlers = find_handlers_in_directory(handlers_dir)
    print(f"Tìm thấy {len(handlers)} handlers\n")
    
    # So sánh
    print("Đang so sánh...")
    result = compare_stored_procedures_with_handlers(stored_procedures, handlers)
    
    # In kết quả
    print("=== KẾT QUẢ ===\n")
    
    print(f"📊 TỔNG QUAN:")
    print(f"   - Tổng số stored procedures: {len(stored_procedures)}")
    print(f"   - Tổng số handlers: {len(handlers)}")
    print(f"   - Stored procedures có handler: {len(result['have_handlers'])}")
    print(f"   - Stored procedures chưa có handler: {len(result['missing_handlers'])}")
    print(f"   - Handlers không có trong danh sách SP: {len(result['extra_handlers'])}\n")
    
    print(f"✅ STORED PROCEDURES CÓ HANDLER ({len(result['have_handlers'])}):")
    for sp in result['have_handlers'][:20]:  # Chỉ hiển thị 20 đầu tiên
        print(f"   ✓ {sp}")
    if len(result['have_handlers']) > 20:
        print(f"   ... và {len(result['have_handlers']) - 20} stored procedures khác\n")
    else:
        print()
    
    print(f"❌ STORED PROCEDURES CHƯA CÓ HANDLER ({len(result['missing_handlers'])}):")
    for sp in result['missing_handlers'][:20]:  # Chỉ hiển thị 20 đầu tiên
        print(f"   ✗ {sp}")
    if len(result['missing_handlers']) > 20:
        print(f"   ... và {len(result['missing_handlers']) - 20} stored procedures khác\n")
    else:
        print()
    
    print(f"⚠️  HANDLERS KHÔNG CÓ TRONG DANH SÁCH SP ({len(result['extra_handlers'])}):")
    for handler in result['extra_handlers'][:20]:  # Chỉ hiển thị 20 đầu tiên
        print(f"   ? {handler}")
    if len(result['extra_handlers']) > 20:
        print(f"   ... và {len(result['extra_handlers']) - 20} handlers khác\n")
    else:
        print()
    
    # Lưu kết quả chi tiết vào file
    output_file = "handler_analysis_result.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== PHÂN TÍCH STORED PROCEDURES VÀ HANDLERS ===\n\n")
        f.write(f"Tổng số stored procedures: {len(stored_procedures)}\n")
        f.write(f"Tổng số handlers: {len(handlers)}\n")
        f.write(f"Stored procedures có handler: {len(result['have_handlers'])}\n")
        f.write(f"Stored procedures chưa có handler: {len(result['missing_handlers'])}\n")
        f.write(f"Handlers không có trong danh sách SP: {len(result['extra_handlers'])}\n\n")
        
        f.write("=== STORED PROCEDURES CÓ HANDLER ===\n")
        for sp in result['have_handlers']:
            f.write(f"✓ {sp}\n")
        f.write("\n")
        
        f.write("=== STORED PROCEDURES CHƯA CÓ HANDLER ===\n")
        for sp in result['missing_handlers']:
            f.write(f"✗ {sp}\n")
        f.write("\n")
        
        f.write("=== HANDLERS KHÔNG CÓ TRONG DANH SÁCH SP ===\n")
        for handler in result['extra_handlers']:
            f.write(f"? {handler}\n")
    
    print(f"📄 Kết quả chi tiết đã được lưu vào file: {output_file}")

if __name__ == "__main__":
    main()
