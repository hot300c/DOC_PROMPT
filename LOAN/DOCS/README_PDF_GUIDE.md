# 📄 HƯỚNG DẪN TẠO PDF HỢP ĐỒNG CHUYÊN NGHIỆP

## 🎯 Tổng quan

Tôi đã chuẩn bị sẵn tất cả các file cần thiết để tạo PDF hợp đồng chuyên nghiệp:

### 📁 Các file đã tạo:

1. **`HOP_DONG_OUTSOURCE_RUTGON_PDF.md`** - File Markdown với bố cục chuyên nghiệp
2. **`contract-style.css`** - CSS styling chuyên nghiệp
3. **`HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL.html`** - File HTML để xem trước
4. **`create_pdf.sh`** - Script tự động tạo PDF
5. **`README_PDF_GUIDE.md`** - Hướng dẫn này

---

## 🚀 Cách tạo PDF (3 phương pháp)

### **Phương pháp 1: Sử dụng Script tự động (Khuyến nghị)**

```bash
# Chạy script tự động
./create_pdf.sh
```

Script sẽ:
- ✅ Kiểm tra và cài đặt Pandoc (nếu cần)
- ✅ Kiểm tra và cài đặt MacTeX (nếu cần)
- ✅ Tạo PDF với formatting chuyên nghiệp
- ✅ Báo cáo kết quả

### **Phương pháp 2: Tạo PDF thủ công**

```bash
# Tạo PDF với LaTeX
pandoc HOP_DONG_OUTSOURCE_RUTGON_PDF.md \
    -o HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL.pdf \
    --pdf-engine=pdflatex \
    -V geometry:margin=2.5cm \
    -V fontsize=12pt \
    -V documentclass=article \
    -V mainfont="Times New Roman" \
    -V colorlinks=true \
    --toc \
    --toc-depth=3
```

### **Phương pháp 3: Chuyển đổi từ HTML**

1. Mở file `HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL.html` trong trình duyệt
2. Nhấn `Ctrl+P` (Windows) hoặc `Cmd+P` (Mac)
3. Chọn "Save as PDF"
4. Điều chỉnh settings:
   - **Paper size:** A4
   - **Margins:** Normal
   - **Options:** Background graphics (nếu muốn)

---

## 🎨 Tính năng chuyên nghiệp đã áp dụng

### **Bố cục:**
- ✅ Header và footer với số hợp đồng
- ✅ Table of Contents (Mục lục)
- ✅ Page breaks hợp lý
- ✅ Margins chuẩn (2.5cm)
- ✅ Font Times New Roman chuyên nghiệp

### **Styling:**
- ✅ Tables với shadow và hover effects
- ✅ Color scheme chuyên nghiệp (xanh dương)
- ✅ Typography hierarchy rõ ràng
- ✅ Responsive design
- ✅ Print-friendly layout

### **Nội dung:**
- ✅ Tất cả 14 điều khoản đầy đủ
- ✅ Bảng chi phí chi tiết
- ✅ Timeline và milestone rõ ràng
- ✅ Phụ lục đầy đủ
- ✅ Signature blocks

---

## 📋 Checklist trước khi in

- [ ] Kiểm tra thông tin công ty (Bên A)
- [ ] Điền ngày ký hợp đồng
- [ ] Điền địa điểm ký
- [ ] Kiểm tra số tiền và currency
- [ ] Review tất cả điều khoản
- [ ] Kiểm tra signature blocks

---

## 🔧 Troubleshooting

### **Lỗi: "pdflatex not found"**
```bash
# Cài đặt MacTeX
brew install --cask mactex
# Hoặc cài đặt BasicTeX (nhẹ hơn)
brew install --cask basictex
```

### **Lỗi: "pandoc not found"**
```bash
# Cài đặt Pandoc
brew install pandoc
```

### **Lỗi font không hiển thị đúng**
- Đảm bảo font Times New Roman đã được cài đặt
- Hoặc thay đổi font trong script:
```bash
-V mainfont="Arial"
```

### **File PDF quá lớn**
- Sử dụng BasicTeX thay vì MacTeX
- Hoặc tạo HTML và chuyển đổi thủ công

---

## 📞 Hỗ trợ

Nếu gặp vấn đề, bạn có thể:

1. **Chạy script tự động:** `./create_pdf.sh`
2. **Xem file HTML trước:** Mở `HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL.html`
3. **Sử dụng online converter:** Upload file .md lên [Dillinger.io](https://dillinger.io/)

---

## 🎉 Kết quả mong đợi

File PDF cuối cùng sẽ có:
- **Kích thước:** A4
- **Font:** Times New Roman 12pt
- **Margins:** 2.5cm
- **Pages:** ~15-20 trang
- **Quality:** Professional, ready for printing

**Chúc bạn thành công! 🚀**
