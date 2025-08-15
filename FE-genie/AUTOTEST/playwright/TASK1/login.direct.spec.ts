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

test("test", async ({ page }) => {
  await page.locator("body").click();
  await page.goto("http://localhost:3000/dang-nhap");
  await page.getByRole("textbox", { name: "Tên đăng nhập" }).click();
  await page.getByRole("textbox", { name: "Tên đăng nhập" }).fill("phucnnd");
  await page.getByRole("textbox", { name: "Tên đăng nhập" }).press("Tab");
  await page.getByRole("textbox", { name: "Mật khẩu" }).fill("Hehehe@12");
  // await page.getByRole("textbox", { name: "Mật khẩu" }).press("Enter");
  await page.getByRole("button", { name: "Đăng nhập" }).click();

  await page.waitForTimeout(30000);
  // await page.getByRole("searchbox", { name: "Tìm cơ sở" }).click();
  // await page
  //   .getByRole("searchbox", { name: "Tìm cơ sở" })
  //   .fill("hoang van thu");
  // await page
  //   .getByRole("cell", { name: "VNVC Hoàng Văn Thụ - SRV TEST Date:" })
  //   .click();
  // await page.getByRole("button", { name: "Tiếp tục" }).click();
  // await page.getByRole("button", { name: "Có" }).click();
  // await page.getByRole("textbox", { name: "Email" }).fill("phucnnd@vnvc.vn");
  // await page.getByRole("button", { name: "Cập nhật" }).click();
  // await page.getByRole("button", { name: "Ok" }).click();
  // await page.getByRole("button", { name: "Đóng" }).click();
  // await page.getByRole("button", { name: "Toggle Sidebar" }).click();
  // await page.getByRole("button", { name: "Tiếp Nhận Mới" }).click();
  // await page.getByRole("button", { name: "TIẾP NHẬN" }).click();
  // await page.getByRole("button", { name: "Tiếp Nhận Mới" }).click();
});
