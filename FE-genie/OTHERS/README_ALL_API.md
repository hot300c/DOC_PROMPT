# Tổng hợp tất cả API calls từ Frontend đến Backend

## Tổng quan
Tài liệu này liệt kê tất cả các API calls được sử dụng trong project Genie frontend để giao tiếp với backend.

## Cấu trúc API
- **Endpoint chính**: `/DataAccess` (sử dụng httpService.post)
- **Endpoint phụ**: `/Login`, `/api/*` (sử dụng axios, fetch)
- **Cấu trúc request**: `{ category, command, parameters }`

## 1. API DataAccess (httpService.post)

### 1.1 QAHosGenericDB Category

#### Patient Management
- `ws_MDM_Patient_Get` - Lấy thông tin bệnh nhân
- `ws_MDM_Patient_SaveV2` - Lưu thông tin bệnh nhân
- `ws_MDM_Patient_SaveV3` - Lưu thông tin bệnh nhân (v3)
- `ws_MDM_Patient_SaveV4` - Lưu thông tin bệnh nhân (v4)
- `ws_MDM_Patient_CheckExists` - Kiểm tra bệnh nhân tồn tại
- `ws_MDM_Patient_GetInfoFromBarCodeForOP` - Lấy thông tin từ barcode
- `ws_MDM_PersonReferredNotification_Today_ByFacID` - Thông báo giới thiệu hôm nay
- `ws_MDM_Person_Referred_ForReception_Check` - Kiểm tra giới thiệu cho tiếp nhận

#### Contract Management
- `ws_L_Customer_ByFacIDForContractPostfix_List` - Danh sách hậu tố hợp đồng
- `ws_Vaccine_HopDong_ListByPatientIDV2` - Danh sách hợp đồng vaccine theo bệnh nhân
- `ws_TaoSoHopDongVaccine` - Tạo số hợp đồng vaccine
- `ws_KTTrungHopDong` - Kiểm tra trùng hợp đồng
- `ws_KTHopDongTruocKhiXoa` - Kiểm tra hợp đồng trước khi xóa
- `ws_VNVCContractBeforeAddBeforeSave` - Kiểm tra hợp đồng VNVC trước khi lưu

#### Vaccine Management
- `ws_Vaccine_LayChiDinh_PhacDo_V2` - Lấy chỉ định phác đồ vaccine
- `ws_Vaccine_PhacDoBenhNhan_List` - Danh sách phác đồ bệnh nhân
- `ws_Vaccine_LichSuTiemVaccine` - Lịch sử tiêm vaccine
- `ws_Vaccine_ChiDinhVaccine` - Chỉ định vaccine
- `ws_Vaccine_LuuMuiTiem` - Lưu mũi tiêm
- `ws_Vaccine_Random_ALL_V2` - Random vaccine tất cả
- `ws_Vaccine_Update_IsDuocTiem` - Cập nhật trạng thái được tiêm
- `ws_Vaccine_KiemTraDuocTiem` - Kiểm tra được tiêm
- `ws_Vaccine_KiemTraChiDinhCoPhong` - Kiểm tra chỉ định có phòng
- `ws_Vaccine_KiemTraDongPhacDo` - Kiểm tra đóng phác đồ
- `ws_Vaccine_DanhSachChoKham_DaGoi_Save` - Lưu danh sách chờ khám đã gọi
- `ws_Vaccine_TaoSoThuThu_PhongTiem` - Tạo số thứ tự phòng tiêm
- `ws_Vaccine_DanhSachBnTapTrung_Tiem_V2` - Danh sách bệnh nhân tập trung tiêm
- `ws_Vaccine_ChonPhongTiem_PhongKham_V3` - Chọn phòng tiêm phòng khám
- `ws_Vaccine_DanhSachChoKham_Update_DangGoi_WEB` - Cập nhật danh sách chờ khám đang gọi
- `ws_VaccineTooltip_HTML` - Tooltip vaccine HTML

#### Room Management
- `ws_L_DepartmentRoom_ListForReception` - Danh sách phòng tiếp nhận
- `ws_L_DepartmentRoom_Reception_Random` - Random phòng tiếp nhận
- `ws_L_DepartmentRoom_Get` - Lấy thông tin phòng
- `ws_DepartmentRoomIsUsing_Update` - Cập nhật trạng thái sử dụng phòng

#### Admission Management
- `ws_CN_PhysicianAdmissions_CongKham_CheckExisted` - Kiểm tra khám tồn tại
- `ws_CN_FacAdmissions_GetExistTodayV2` - Lấy khám hôm nay
- `ws_CN_FacAdmissions_SaveV2` - Lưu thông tin khám
- `ws_CN_PhysicianAdmissions_UpdateIsPracticed` - Cập nhật trạng thái thực hành
- `ws_CN_PhysicianAdmissions_UpdatePrimaryDoctor` - Cập nhật bác sĩ chính
- `ws_CN_PhysicanAdmissions_FinishPractice` - Hoàn thành thực hành

#### Customer Management
- `ws_L_Customer_GetByFacID` - Lấy khách hàng theo cơ sở

### 1.2 Security Category

#### User Management
- `ws_User_Get` - Lấy thông tin user
- `ws_User_SetPassword` - Đặt mật khẩu user
- `ws_UserPermissions_List` - Danh sách quyền user
- `ws_Permissions_List` - Danh sách quyền
- `ws_UserRoomPermissions_Get` - Quyền phòng của user
- `ws_UserLoginRoom_Save` - Lưu đăng nhập phòng
- `ws_UserLoginRoom_GetLastRoomID` - Lấy phòng cuối cùng đăng nhập

#### Menu Management
- `ws_Menu_Get` - Lấy menu

### 1.3 Settings Category
- `ws_Settings_ListByFacID` - Danh sách cài đặt theo cơ sở
- `ws_GetSetting` - Lấy cài đặt

### 1.4 Reports Category
- `ws_L_Reports_GetByID` - Lấy báo cáo theo ID
- `ws_ReportQueue_Push` - Đẩy báo cáo vào queue
- `ws_ReportOutput_Get` - Lấy output báo cáo

### 1.5 Documents Category
- `ws_Docs_HbsAg_Test_BangKiem_Get` - Lấy bảng kiểm HbsAg
- `ws_Docs_HbsAg_Test_BangKiem_Save` - Lưu bảng kiểm HbsAg

### 1.6 Clinical Sessions Category
- `ws_CN_ClinicalSessions_CongKhamTrongNgay_ByPatientID` - Phiên khám trong ngày theo bệnh nhân

### 1.7 Vital Signs Category
- `ws_CN_VitalSign_Save` - Lưu dấu hiệu sinh tồn
- `ws_CN_VitalSign_Get` - Lấy dấu hiệu sinh tồn

### 1.8 Affiliate Facility Category
- `ws_L_AffiliateFacility_List` - Danh sách cơ sở liên kết

### 1.9 Content Introduction Category
- `ws_L_NoiDungGioiThieu_List` - Danh sách nội dung giới thiệu
- `ws_CN_GioiThieuDichVu_ByFacAdmisionID_List` - Giới thiệu dịch vụ theo khám
- `ws_CN_GhiChu_GioiThieuDichVu_Get` - Ghi chú giới thiệu dịch vụ

### 1.10 Facility Category
- `ws_L_Facility_BVTamAnh_List` - Danh sách cơ sở BV Tâm Anh

## 2. API Login
- `/Login` - Đăng nhập

## 3. API External Services

### 3.1 TTS Service
- `/api/tts` - Text-to-Speech

### 3.2 QAS Service
- `/api/qas/login` - Đăng nhập QAS
- `/api/qas/question/department` - Câu hỏi phòng ban
- `/api/qas/question/other` - Câu hỏi khác
- `/api/qas/log/create` - Tạo log

### 3.3 Patient API
- `/api/patient/PatientInfo` - Thông tin bệnh nhân

### 3.4 Printer API
- `/Printer/printers` - Danh sách máy in
- `/Printer/configurations` - Cấu hình máy in
- `/outputNumber` - Số output

### 3.5 Smart POS API
- `/SmartPos/get-pos-config` - Lấy cấu hình POS
- `/SmartPos/update-pos-config` - Cập nhật cấu hình POS
- `/SmartPos/show-qrcode` - Hiển thị QR code
- `/SmartPos/cancel-qrcode` - Hủy QR code

### 3.6 Viettel Integration
- IP fetch API - Lấy IP từ Viettel
- Token management APIs - Quản lý token Viettel

### 3.7 National Vaccination System
- Vaccination history upload APIs - Upload lịch sử tiêm chủng
- Vaccination statistics APIs - Thống kê tiêm chủng
- Vaccination code creation APIs - Tạo mã tiêm chủng

### 3.8 Drug Database Integration
- Drug search APIs - Tìm kiếm thuốc
- Drug login APIs - Đăng nhập hệ thống thuốc

### 3.9 QA Pay Integration
- Card validation APIs - Xác thực thẻ
- Transaction APIs - Giao dịch thanh toán
- Invoice APIs - Hóa đơn

## 4. File Download APIs
- `/templates/*.xlsx` - Tải template Excel

## 5. Fetch APIs
- External address APIs - API địa chỉ bên ngoài
- Bill info APIs - API thông tin hóa đơn
- Chi dinh phong kham APIs - API chỉ định phòng khám

## 6. Các Service Files chính

### 6.1 Core Services
- `patient.ts` - Quản lý bệnh nhân
- `contract.ts` - Quản lý hợp đồng
- `vaccine.ts` - Quản lý vaccine
- `vaccineService.ts` - Dịch vụ vaccine
- `nurse.ts` - Quản lý điều dưỡng
- `system.ts` - Hệ thống
- `setting.ts` - Cài đặt

### 6.2 Business Services
- `admissionBusiness.ts` - Nghiệp vụ tiếp nhận
- `consultationService.ts` - Dịch vụ tư vấn
- `payment.ts` - Thanh toán
- `room.ts` - Quản lý phòng
- `keVaccinTabServices.ts` - Dịch vụ tab vaccine

### 6.3 External Services
- `promotion-api.ts` - API khuyến mãi
- `qa-pay-services.ts` - Dịch vụ QA Pay
- `patientsNutri.ts` - Dịch vụ dinh dưỡng

## 7. Network Configuration

### 7.1 HTTP Service
- `http.ts` - Service HTTP chính
- `axios-instance.ts` - Instance axios
- `cache-axios.ts` - Axios với cache
- `client-axios.ts` - Axios client
- `server-axios.ts` - Axios server

### 7.2 External APIs
- `rajah-apis.ts` - API Rajah
- `promotion-api.ts` - API khuyến mãi

## 8. Tổng kết

### 8.1 Số lượng API calls
- **DataAccess APIs**: ~200+ commands
- **External APIs**: ~50+ endpoints
- **File APIs**: ~10+ endpoints
- **Total**: ~260+ API calls

### 8.2 Categories chính
1. **Patient Management** - Quản lý bệnh nhân
2. **Vaccine Management** - Quản lý vaccine
3. **Contract Management** - Quản lý hợp đồng
4. **Room Management** - Quản lý phòng
5. **Admission Management** - Quản lý tiếp nhận
6. **User Management** - Quản lý người dùng
7. **Payment Management** - Quản lý thanh toán
8. **External Integrations** - Tích hợp bên ngoài

### 8.3 Patterns sử dụng
- **httpService.post("/DataAccess", [...])** - API chính
- **axiosInstance.post/get** - API bên ngoài
- **fetch()** - File download và API đơn giản
- **userLocalAxios** - API local

---

*Tài liệu này được tạo tự động bằng cách quét toàn bộ codebase frontend Genie.*
