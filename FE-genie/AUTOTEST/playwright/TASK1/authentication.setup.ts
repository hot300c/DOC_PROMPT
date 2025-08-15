import { expect, test } from "@playwright/test";
import path from "path";
import { FacilityPage } from "../../../../genie/playwright/pages/co-so/facility";
import { LoginPage } from "../../../../genie/playwright/pages/dang-nhap/login";

// This test suite tests the login and select facility flow. It will be ran once before all tests.
// Subsequent tests will use the storage state set by this test and skip login.
// This feature is implemented at /app/login.

test.beforeEach(async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await expect(loginPage.logoImage).toBeVisible();
  await expect(loginPage.usernameInput).toBeEnabled();
  await expect(loginPage.passwordInput).toBeEnabled();
});

test.describe("No cookies", () => {
  test.use({ storageState: { cookies: [], origins: [] } });
  test("Login should fail", async ({ page }) => {
    const { step } = test;
    const loginPage = new LoginPage(page);

    await step("Login should fail with empty credentials", async () => {
      await loginPage.submit();
      await expect(loginPage.usernameEmptyError).toBeVisible();
      await expect(loginPage.passwordEmptyError).toBeVisible();
    });

    await step("Login should fail with wrong credentials", async () => {
      await loginPage.login("admin", "wrongpassword");
      await expect(loginPage.loginStatus).toBeVisible();
      await expect(loginPage.loginStatus).toHaveText(
        loginPage.wrongCredentialsError,
      );
    });
  });
});

test.describe("With cookies", () => {
  // Save storage in the genie's expected path regardless of current test file location
  const adminFile = path.join(process.cwd(), "playwright/.auth/admin.json");
  // Perform setup for all tests so that subsequent tests can skip login.
  test("Login as admin", async ({ page }) => {
    const { step } = test;

    const loginPage = new LoginPage(page);
    await step("Login with correct credentials", async () => {
      if (
        !process.env.PLAYWRIGHT_TEST_USERNAME ||
        !process.env.PLAYWRIGHT_TEST_PASSWORD
      ) {
        throw new Error(
          "Must define PLAYWRIGHT_TEST_USERNAME and PLAYWRIGHT_TEST_PASSWORD in environment variables.",
        );
      }

      await loginPage.goto();
      await loginPage.login(
        process.env.PLAYWRIGHT_TEST_USERNAME,
        process.env.PLAYWRIGHT_TEST_PASSWORD,
      );
    });

    const facilityPage = new FacilityPage(page);
    await step("Select facility after login", async () => {
      if (!process.env.PLAYWRIGHT_TEST_FACILITY) {
        throw new Error(
          "Must define PLAYWRIGHT_TEST_FACILITY in environment variables.",
        );
      }

      await facilityPage.waitFor();
      // Wait until previous step navigated to the facility page.
      await expect(facilityPage.selectFacilityHeading).toBeVisible();
      await expect(facilityPage.searchFacilityInput).toBeEnabled();

      await facilityPage.selectFacility(process.env.PLAYWRIGHT_TEST_FACILITY);
    });

    // End of authentication steps, set storage state for subsequent tests.
    await page.waitForURL("./khach-hang");
    await page.context().storageState({ path: adminFile });
  });
});
