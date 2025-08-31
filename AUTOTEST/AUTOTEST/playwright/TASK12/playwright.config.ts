import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './',
  fullyParallel: false, // Tắt parallel để đảm bảo thứ tự chạy
  workers: 1, // Chỉ sử dụng 1 worker
  reporter: 'html',
  use: {
    baseURL: 'https://dev-genie.vnvc.info',
    trace: 'on-first-retry',
    storageState: 'auth.json', // Sử dụng trạng thái đăng nhập đã lưu
  },
  projects: [
    {
      name: 'login',
      testMatch: '**/task12_login.spec.ts',
    },
    {
      name: 'main-test',
      testMatch: '**/task12_test_playwright.spec.ts',
      dependencies: ['login'], // Đảm bảo test login chạy trước
    },
  ],
});
