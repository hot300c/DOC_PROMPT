import { test, expect } from "@playwright/test";
import { NewAdmissionPage } from "../pages/khach-hang/tiep-nhan/admission";

test.describe("Tiếp nhận mới - In mã vạch", () => {
  test.beforeEach(async ({ page }) => {
    const admissionPage = new NewAdmissionPage(page);
    await admissionPage.goto();
    await expect(admissionPage.nameInput).toBeFocused();
  });

  test("Scenario 1: In mã vạch gọi ws_MDM_Patient_CheckExists và xử lý thành công", async ({ page }) => {
    const admissionPage = new NewAdmissionPage(page);

    // 1) Tìm kiếm và chọn bệnh nhân có sẵn
    const searchPatientName = "NGUYỄN VĂN A";
    const displayName = searchPatientName.toUpperCase();
    await admissionPage.searchByFieldOpenDialog(admissionPage.nameInput, displayName);
    await admissionPage.selectFirstPatient();
    await expect(admissionPage.customerCodeInput).not.toBeEmpty({ timeout: 60000 });

    // 2) Chờ request DataAccess với command ws_MDM_Patient_CheckExists khi bấm In mã vạch
    const waitForCheckExists = page.waitForRequest((req) => {
      if (!req.url().includes("/DataAccess") || req.method() !== "POST") return false;
      try {
        const body = req.postData();
        if (!body) return false;
        const payload = JSON.parse(body);
        return (
          Array.isArray(payload) &&
          payload.some((x: any) => x?.command === "ws_MDM_Patient_CheckExists")
        );
      } catch {
        return false;
      }
    });

    await page.getByRole("button", { name: "In mã vạch" }).click();

    const request = await waitForCheckExists;
    const body = JSON.parse(request.postData() || "[]");
    const call = body.find((x: any) => x?.command === "ws_MDM_Patient_CheckExists");
    expect(call).toBeTruthy();
    // Kiểm tra tham số gửi lên có PatientID và FacID (tên key có thể khác nhau theo layer)
    const params = call?.parameters ?? {};
    expect(
      params?.PatientID || params?.patientID,
      "PatientID/patientID phải có giá trị",
    ).toBeTruthy();
    expect(params?.FacID || params?.facID, "FacID/facID phải có giá trị").toBeTruthy();

    // 3) Xác nhận có hiển thị loading và ẩn đi (quy trình in mã vạch chạy)
    await expect(admissionPage.dataProcessingLoading).toBeVisible();
    await expect(admissionPage.dataProcessingLoading).toBeHidden({ timeout: 60000 });
  });
});


