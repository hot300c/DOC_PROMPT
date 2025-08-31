const { chromium } = require('playwright');

async function quickTest() {
  const browser = await chromium.launch({ 
    headless: false, 
    slowMo: 1000 
  });
  
  const page = await browser.newPage();
  
  try {
    console.log('🚀 Starting quick test...');
    
    // 1. Navigate to login page
    await page.goto('http://localhost:3000/dang-nhap');
    console.log('✅ Navigated to login page');
    
    // 2. Login
    await page.fill('input[name="username"], input[placeholder*="tên đăng nhập"], input[type="text"]', 'phucnnd');
    await page.fill('input[name="password"], input[placeholder*="mật khẩu"], input[type="password"]', 'Hehehe@12');
    await page.click('button[type="submit"], button:has-text("Đăng nhập"), button:has-text("Login")');
    console.log('✅ Login completed');
    
    // 3. Wait for navigation and go to Tiếp nhận mới
    await page.waitForLoadState('networkidle');
    await page.goto('http://localhost:3000/tiep-nhan/tiep-nhan-moi');
    console.log('✅ Navigated to Tiếp nhận mới page');
    
    // 4. Wait for page to load
    await page.waitForLoadState('networkidle');
    console.log('✅ Page loaded successfully');
    
    // 5. Keep browser open for manual testing
    console.log('🎯 Browser is ready for manual testing!');
    console.log('📋 Next steps:');
    console.log('   1. Tìm kiếm bệnh nhân: "NGUYỄN VĂN A"');
    console.log('   2. Chọn bệnh nhân từ danh sách');
    console.log('   3. Click nút "In mã vạch"');
    console.log('   4. Mở Developer Tools (F12) để xem API calls');
    
    // Keep browser open
    await new Promise(() => {}); // This keeps the script running
    
  } catch (error) {
    console.error('❌ Error:', error);
    await browser.close();
  }
}

// Run the test
quickTest();
