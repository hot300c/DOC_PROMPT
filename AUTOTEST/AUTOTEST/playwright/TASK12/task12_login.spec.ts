import { test, expect } from '@playwright/test';

test('TASK12_Login', async ({ page, context }) => {
  // Đăng nhập
  await page.goto('https://dev-genie.vnvc.info/dang-nhap');
  await page.getByRole('textbox', { name: 'Tên đăng nhập' }).click();
  await page.getByRole('textbox', { name: 'Tên đăng nhập' }).fill('phucnnd');
  await page.getByRole('textbox', { name: 'Tên đăng nhập' }).press('Tab');
  await page.getByRole('textbox', { name: 'Mật khẩu' }).fill('Phuc*1234');
  await page.getByRole('button', { name: 'Đăng nhập' }).click();
  
  // Chọn cơ sở
  await page.getByRole('searchbox', { name: 'Tìm cơ sở' }).fill('hoang van thu');
  await page.getByRole('cell', { name: 'VNVC Hoàng Văn Thụ - SRV TEST Date:' }).click();
  await page.getByRole('button', { name: 'Tiếp tục' }).click();
  await page.getByRole('button', { name: 'TIẾP NHẬN' }).click();
  await page.getByRole('button', { name: 'Tiếp Nhận Mới' }).click();
  await page.getByTestId('admission-patientInfo-nameInput').click();
  const randomSuffix = Math.random().toString(36).substring(2, 8).toUpperCase();
  await page.getByTestId('admission-patientInfo-nameInput').fill(`TEST ${randomSuffix}`);
  await page.getByTestId('admission-patientInfo-dobContainer').getByRole('spinbutton', { name: 'year' }).click();
  await page.getByTestId('admission-patientInfo-dobContainer').getByRole('spinbutton', { name: 'year' }).fill('2020');
  await page.getByTestId('admission-patientInfo-dobContainer').getByRole('spinbutton', { name: 'year' }).press('Enter');

  await page.waitForTimeout(2000);

  // await page.getByTestId('admission-patientInfo-addressInput').click();
  // await page.getByTestId('admission-patientInfo-addressInput').fill('HC-M');
  // await page.getByTestId('admission-patientInfo-addressInput').press('Enter');

  await page.getByTestId('admission-patientInfo-addressInput').click();
  await page.getByTestId('admission-patientInfo-addressInput').fill('Thành Phố Hồ Chí Minh');
  await page.getByTestId('admission-patientInfo-addressInput').press('Enter');
  await page.locator('.col-span-12 > .flex').first().click();
  await page.locator('.col-span-12 > .flex').first().fill('Tp. Hồ Chí Minh');
  await page.locator('.col-span-12 > .flex').first().press('Enter');

  await page.waitForTimeout(2000);

  // Đảo số điện thoại, random 4 số cuối cho 09222221111
  const randomPhoneSuffix = Math.floor(1000 + Math.random() * 9000); // random 4 số cuối
  const phoneNumber = `0922222${randomPhoneSuffix}`;
  await page.getByTestId('admission-patientInfo-phoneInput').fill(phoneNumber.split('').reverse().join(''));
  await page.getByTestId('admission-patientInfo-phoneInput').press('Tab');
  await page.getByTestId('admission-vaccineConsul-selectRoomDropdown').click();
  await page.getByRole('cell', { name: 'PHÒNG KHÁM 3' }).click();
  await page.getByTestId('admission-vaccineConsul-section').getByRole('button', { name: 'Thêm' }).click();
  await page.getByRole('button', { name: 'Lưu' }).click();

  // // Chờ page lưu và load xong
  // await page.waitForSelector('text=Tiếp nhận thành công', { timeout: 10000 });

  // await page.getByRole('button', { name: 'NGOẠI TRÚ' }).click();
  // await page.getByRole('button', { name: 'Khám Bệnh' }).click();
  // await page.getByTestId('chon-phong-kham').click();
  // await page.getByText('PHÒNG KHÁM 3').click();
  // await page.getByRole('cell', { name: 'TEST P3' }).dblclick();
  // await page.getByRole('button', { name: 'Ok' }).click();
  // await page.getByRole('tab', { name: 'Chỉ định Vắc-xin' }).click();
  // await page.getByTestId('nhom-benh-select').click();
  // await page.getByRole('cell', { name: 'Bạch Hầu', exact: true }).click();
  // await page.getByTestId('vaccine-select').click();
  // await page.getByRole('cell', { name: 'Boostrix (BỈ - GSK)' }).locator('div').click();
  // await page.getByTestId('phac-do-select').click();
  // await page.getByRole('cell', { name: 'Từ 4 tuổi đến dưới 65 tuổi (Boostrix không giới hạn trên)', exact: true }).click();
  // await page.getByTestId('them-vaccine-button').click();
  // await page.locator('.border.rounded-md.overflow-auto').first().click();
  // await page.getByLabel('', { exact: true }).nth(1).click();
  // await page.getByRole('tab', { name: 'Theo dõi phác đồ' }).click();
  // await page.getByRole('tab', { name: 'Phác đồ nhóm bệnh' }).click();
  // await page.getByRole('button', { name: 'Đóng phác đồ' }).click();
  // await page.getByRole('cell', { name: 'Ho gà' }).click();
  // await page.getByRole('button', { name: 'Đóng phác đồ' }).click();
  // await page.getByRole('cell', { name: 'Uốn ván' }).click();
  // await page.getByRole('button', { name: 'Đóng phác đồ' }).click();
  // await page.getByRole('tab', { name: 'Phác đồ vaccine' }).click();
  // await page.getByRole('tab', { name: 'Chỉ định Vắc-xin' }).click();
  // await page.getByTestId('nhom-benh-select').click();
  // await page.getByRole('cell', { name: 'Ho gà', exact: true }).click();
  // await page.getByTestId('vaccine-select').click();
  // await page.getByRole('cell', { name: 'ADACEL 0,5ml (CANADA - Sanofi' }).click();
  // await page.getByTestId('phac-do-select').click();
  // await page.getByRole('row', { name: 'Từ 4 tuổi đến dưới 65 tuổi (Boostrix không giới hạn trên)', exact: true }).getByRole('cell').click();
  // await page.getByTestId('them-vaccine-button').click();
  // await page.getByRole('button', { name: 'Có' }).click();
  // await page.getByTestId('chi-dinh-table').locator('label').first().click();
  // await page.getByRole('button', { name: 'Ok' }).click();
  // await page.getByRole('button', { name: 'Close', exact: true }).click();
  // await page.getByTestId('chi-dinh-table').locator('label').first().click();
  // await page.getByText('Bạch Hầu,Ho gà,Uốn ván').first().click();
  // await page.getByRole('tab', { name: 'Theo dõi phác đồ' }).click();
  // await page.getByRole('tab', { name: 'Phác đồ nhóm bệnh' }).click();
  // await page.getByRole('cell', { name: 'Uốn ván' }).first().click();
  // await page.getByRole('button', { name: 'Mở phác đồ' }).click();
  // await page.getByRole('cell', { name: 'Ho gà' }).first().click();
  // await page.getByRole('button', { name: 'Mở phác đồ' }).click();
  // await page.getByRole('cell', { name: 'Bạch Hầu' }).first().click();
  // await page.getByRole('button', { name: 'Mở phác đồ' }).click();
  // await page.getByRole('tab', { name: 'Chỉ định Vắc-xin' }).click();
  // await page.getByText('Bạch Hầu,Ho gà,Uốn ván').nth(1).click();
  // await page.getByLabel('', { exact: true }).first().click();
  // await page.getByText('Khách hàng đang có 2 phác đồ').click();
  // await page.getByText('Khách hàng đang có 2 phác đồ').click();
});