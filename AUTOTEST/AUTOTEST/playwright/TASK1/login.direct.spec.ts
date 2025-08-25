import { test, expect, type Page } from "@playwright/test";
import fs from "fs";
import path from "path";
import { LoginPage } from "../../../../../genie/playwright/pages/dang-nhap/login";

// Hardcoded credentials
const USERNAME = "phucnnd";
const PASSWORD = "Hehehe@12";

// Save storage state into genie's expected auth file
const ADMIN_STATE_PATH = path.join(
  process.cwd(),
  "playwright/.auth/admin.json"
);
test('test', async ({ page }) => {
  await page.goto('http://localhost:3000/dang-nhap');
  await page.getByRole('textbox', { name: 'Tên đăng nhập' }).click();
  await page.getByRole('textbox', { name: 'Tên đăng nhập' }).fill('phucnnd');
  await page.getByRole('textbox', { name: 'Tên đăng nhập' }).press('Tab');
  await page.getByRole('textbox', { name: 'Mật khẩu' }).fill('Phuc*1234');
  await page.getByRole('button', { name: 'Đăng nhập' }).click();
  await page.getByRole('searchbox', { name: 'Tìm cơ sở' }).click();
  await page.getByRole('searchbox', { name: 'Tìm cơ sở' }).fill('hoang van thu');
  await page.getByRole('cell', { name: 'VNVC Hoàng Văn Thụ - SRV TEST Date:' }).click();
  await page.waitForTimeout(2000);
  await page.getByRole('button', { name: 'Tiếp tục' }).click();
  // await page.waitForTimeout(12000);


  await page.waitForURL('http://localhost:3000/khach-hang', { timeout: 20000 });

  await page.getByRole('button', { name: 'Không' }).click();
  // await page.waitForTimeout(5000);

  // await page.goto('http://localhost:3000/khach-hang');
  // await page.getByText('Trung tâm: VNVC Hoàng Văn Thụ - SRV TEST Date: 2025.08.12Xin chào, phucnnd!').click();

  await page.waitForTimeout(2000);
  await page.getByRole('button', { name: 'Toggle Sidebar' }).click();
    // await page.waitForURL('http://localhost:3000/khach-hang', { timeout: 20000 });
  await page.getByRole('button', { name: 'Tiếp Nhận Mới' }).click();

  

});
