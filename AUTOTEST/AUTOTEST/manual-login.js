// Manual Login Script for Genie
// Run this in Playwright browser console or use as a test script

const loginCredentials = {
  username: 'phucnnd',
  password: 'Hehehe@12'
};

// Function to login manually
async function manualLogin() {
  console.log('Starting manual login process...');
  
  // Wait for page to load
  await page.waitForLoadState('networkidle');
  
  // Fill username
  await page.fill('input[name="username"], input[placeholder*="tên đăng nhập"], input[type="text"]', loginCredentials.username);
  console.log('✅ Username filled:', loginCredentials.username);
  
  // Fill password
  await page.fill('input[name="password"], input[placeholder*="mật khẩu"], input[type="password"]', loginCredentials.password);
  console.log('✅ Password filled');
  
  // Click login button
  await page.click('button[type="submit"], button:has-text("Đăng nhập"), button:has-text("Login")');
  console.log('✅ Login button clicked');
  
  // Wait for navigation
  await page.waitForLoadState('networkidle');
  console.log('✅ Login completed');
}

// Instructions for manual testing:
console.log(`
🎯 MANUAL TESTING INSTRUCTIONS:

1. Trình duyệt Playwright đã mở tại: http://localhost:3000/dang-nhap

2. Đăng nhập thủ công:
   - Username: ${loginCredentials.username}
   - Password: ${loginCredentials.password}

3. Sau khi đăng nhập thành công, điều hướng đến:
   - Menu: "Tiếp nhận" → "Tiếp nhận mới"
   - Hoặc truy cập trực tiếp: http://localhost:3000/tiep-nhan/tiep-nhan-moi

4. Test Scenario 1 - In mã vạch:
   - Tìm kiếm bệnh nhân: "NGUYỄN VĂN A"
   - Chọn bệnh nhân từ danh sách
   - Click nút "In mã vạch"
   - Kiểm tra API call ws_MDM_Patient_CheckExists

5. Mở Developer Tools (F12) để xem:
   - Network tab: Kiểm tra API calls
   - Console tab: Xem logs
   - Application tab: Kiểm tra localStorage/sessionStorage

6. Kiểm tra các elements:
   - Nút "In mã vạch" có tồn tại không
   - Loading indicator xuất hiện khi click
   - Toast messages hiển thị
`);

// Export for use in test files
module.exports = { loginCredentials, manualLogin };
