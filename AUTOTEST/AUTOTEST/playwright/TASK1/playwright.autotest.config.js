const { defineConfig, devices } = require('C:/PROJECTS/genie/node_modules/@playwright/test');

module.exports = defineConfig({
  testDir: __dirname,
  timeout: 2 * 60 * 1000,
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: process.env.CI ? [['dot'], ['html']] : 'html',
  webServer: {
    command: 'cmd /c "cd C:\\PROJECTS\\genie && yarn dev"',
    url: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000',
    reuseExistingServer: true,
    stdout: 'ignore',
    stderr: 'pipe',
  },
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000',
    trace: process.env.CI ? 'on-first-retry' : 'on',
    video: process.env.CI ? 'retain-on-failure' : 'on',
    actionTimeout: 0,
    navigationTimeout: 60 * 1000,
    storageState: 'C:/PROJECTS/genie/playwright/.auth/admin.json',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
