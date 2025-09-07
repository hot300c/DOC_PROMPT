#!/bin/bash

# Script to create professional PDF from contract
echo "=== TẠO PDF HỢP ĐỒNG CHUYÊN NGHIỆP ==="
echo ""

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "❌ Pandoc chưa được cài đặt. Đang cài đặt..."
    brew install pandoc
fi

# Check if LaTeX is installed
if ! command -v pdflatex &> /dev/null; then
    echo "❌ LaTeX chưa được cài đặt. Đang cài đặt MacTeX..."
    echo "⚠️  MacTeX rất lớn (~4GB), quá trình cài đặt có thể mất 15-30 phút"
    brew install --cask mactex
    echo "✅ MacTeX đã được cài đặt. Vui lòng chạy lại script này."
    exit 1
fi

echo "✅ Tất cả công cụ cần thiết đã sẵn sàng!"
echo ""

# Create PDF with professional formatting
echo "📄 Đang tạo PDF chuyên nghiệp..."
pandoc HOP_DONG_OUTSOURCE_RUTGON_PDF.md \
    -o HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL.pdf \
    --pdf-engine=pdflatex \
    -V geometry:margin=2.5cm \
    -V fontsize=12pt \
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
    echo "✅ PDF đã được tạo thành công: HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL.pdf"
    echo ""
    echo "📋 Các file đã tạo:"
    echo "   • HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL.pdf (PDF chuyên nghiệp)"
    echo "   • HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL.html (HTML để xem trước)"
    echo "   • contract-style.css (CSS styling)"
    echo ""
    echo "🎉 Hoàn thành! Bạn có thể mở file PDF để xem kết quả."
else
    echo "❌ Có lỗi xảy ra khi tạo PDF. Vui lòng kiểm tra lại."
fi
