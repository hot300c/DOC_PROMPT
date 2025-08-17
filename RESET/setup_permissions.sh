#!/bin/bash

# Setup script để cấp quyền thực thi cho các script
echo "🔧 Đang cấp quyền thực thi cho các script..."

# Cấp quyền cho shell script
chmod +x run_cursor_logout.sh
echo "✅ Đã cấp quyền thực thi cho run_cursor_logout.sh"

# Cấp quyền cho setup script này
chmod +x setup_permissions.sh
echo "✅ Đã cấp quyền thực thi cho setup_permissions.sh"

echo ""
echo "🎉 Hoàn thành! Bây giờ bạn có thể chạy:"
echo "   ./run_cursor_logout.sh"
echo ""
echo "Hoặc double-click vào run_cursor_logout.bat trên Windows"
