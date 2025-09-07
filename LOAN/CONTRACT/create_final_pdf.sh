#!/bin/bash

echo "🎨 TẠO PDF HỢP ĐỒNG CHUYÊN NGHIỆP"
echo "=================================="
echo ""

# Check if MacTeX is installed
if ! command -v pdflatex &> /dev/null; then
    echo "❌ LaTeX chưa được cài đặt. Đang cài đặt BasicTeX (nhẹ hơn)..."
    brew install --cask basictex
    echo "✅ BasicTeX đã được cài đặt. Vui lòng chạy lại script này."
    exit 1
fi

echo "✅ LaTeX đã sẵn sàng!"
echo ""

# Method 1: Try to create PDF from HTML using wkhtmltopdf
echo "📄 Phương pháp 1: Chuyển đổi từ HTML sang PDF..."
if command -v wkhtmltopdf &> /dev/null; then
    wkhtmltopdf --page-size A4 \
                --margin-top 20mm \
                --margin-right 15mm \
                --margin-bottom 20mm \
                --margin-left 15mm \
                --encoding UTF-8 \
                --print-media-type \
                --enable-local-file-access \
                HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL_FINAL.html \
                HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL_FINAL.pdf
    
    if [ $? -eq 0 ]; then
        echo "✅ PDF đã được tạo thành công từ HTML!"
        echo "📁 File: HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL_FINAL.pdf"
        exit 0
    fi
else
    echo "⚠️  wkhtmltopdf chưa được cài đặt. Thử phương pháp khác..."
fi

# Method 2: Create PDF from Markdown using Pandoc
echo ""
echo "📄 Phương pháp 2: Chuyển đổi từ Markdown sang PDF..."
pandoc HOP_DONG_OUTSOURCE_RUTGON_PDF.md \
    -o HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL_FINAL.pdf \
    --pdf-engine=pdflatex \
    -V geometry:margin=2.5cm \
    -V fontsize=11pt \
    -V documentclass=article \
    -V mainfont="Times New Roman" \
    -V monofont="Courier New" \
    -V colorlinks=true \
    -V linkcolor=blue \
    -V urlcolor=blue \
    -V toccolor=black \
    --toc \
    --toc-depth=3

if [ $? -eq 0 ]; then
    echo "✅ PDF đã được tạo thành công từ Markdown!"
    echo "📁 File: HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL_FINAL.pdf"
else
    echo "❌ Có lỗi xảy ra khi tạo PDF từ Markdown."
fi

echo ""
echo "🎉 HOÀN THÀNH!"
echo "=============="
echo ""
echo "📋 Các file đã tạo:"
echo "   • HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL_FINAL.html (HTML chuyên nghiệp)"
echo "   • HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL_FINAL.pdf (PDF chuyên nghiệp)"
echo "   • professional-contract.css (CSS styling)"
echo ""
echo "💡 Hướng dẫn:"
echo "   1. Mở file HTML để xem trước và kiểm tra"
echo "   2. Nếu PDF chưa đẹp, hãy mở HTML và in sang PDF (Cmd+P)"
echo "   3. Điều chỉnh settings: A4, Normal margins, Background graphics"
echo ""
echo "🚀 Chúc bạn thành công!"
