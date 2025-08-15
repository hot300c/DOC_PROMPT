// @ts-nocheck
import { test, expect } from "@playwright/test";
import fs from "fs";
import path from "path";

// Hardcoded credentials
const USERNAME = "phucnnd";
const PASSWORD = "Hehehe@12";

// Save storage state into genie's expected auth file
const ADMIN_STATE_PATH = path.join(process.cwd(), "playwright/.auth/admin.json");

test("Login directly and save auth state", async ({ page, context }) => {
  // 1) Go to login page (absolute URL to bypass baseURL dependence)
  await page.goto("http://localhost:3000/dang-nhap");

  // 2) Fill username & password with resilient selectors
  const usernameInput = page.locator(
    'input[name="username"], input[autocomplete="username"], input[placeholder*="đăng nhập" i], input[type="text"]',
  ).first();
  const passwordInput = page.locator(
    'input[name="password"], input[autocomplete="current-password"], input[placeholder*="mật khẩu" i], input[type="password"]',
  ).first();

  await expect(usernameInput).toBeVisible();
  await usernameInput.fill(USERNAME);
  await expect(passwordInput).toBeVisible();
  await passwordInput.fill(PASSWORD);

  // 3) Submit login
  const loginButton = page.locator(
    'button[type="submit"], button:has-text("Đăng nhập"), button:has-text("Login")',
  ).first();
  await loginButton.click();

  // 4) Wait for navigation away from the login page
  await page.waitForLoadState("networkidle");
  await expect(page).not.toHaveURL(/\/dang-nhap$/);

  // 5) Ensure auth folder exists then save storage state
  fs.mkdirSync(path.dirname(ADMIN_STATE_PATH), { recursive: true });
  await context.storageState({ path: ADMIN_STATE_PATH });
});
