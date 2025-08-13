import pandas as pd

# Danh sách các file trong thư mục QAHosGenericDB
files_data = [
    {"STT": 1, "Tên File": "ws_MDM_Patient_SaveV2.cs", "Kích thước": "25KB", "Số dòng": 503},
    {"STT": 2, "Tên File": "ws_Vaccine_CapNhatNgayHenTiem.cs", "Kích thước": "14KB", "Số dòng": 322},
    {"STT": 3, "Tên File": "ws_L_PatientCompanyAffiliation_Get_ByFacAdmission.cs", "Kích thước": "1.3KB", "Số dòng": 39},
    {"STT": 4, "Tên File": "ws_MDM_Patient_CheckExists.cs", "Kích thước": "7.3KB", "Số dòng": 191},
    {"STT": 5, "Tên File": "ws_Vaccine_KTChiDinhVaccineCungNhomBenh.cs", "Kích thước": "4.9KB", "Số dòng": 96},
    {"STT": 6, "Tên File": "ws_QuanLyTapTrung.cs", "Kích thước": "61KB", "Số dòng": 1183},
    {"STT": 7, "Tên File": "ws_Vaccine_CheckValidation.cs", "Kích thước": "2.6KB", "Số dòng": 61},
    {"STT": 8, "Tên File": "ws_Vaccine_ChiDinhVaccine.cs", "Kích thước": "33KB", "Số dòng": 660},
    {"STT": 9, "Tên File": "ws_Vaccine_DanhSachBnTapTrung_GetByName.cs", "Kích thước": "2.6KB", "Số dòng": 68},
    {"STT": 10, "Tên File": "ws_Vaccine_DanhSachChoKham_Update_DangGoi_WEB.cs", "Kích thước": "2.4KB", "Số dòng": 57},
    {"STT": 11, "Tên File": "ws_Vaccine_DanhSachChoKham_WEB.cs", "Kích thước": "6.5KB", "Số dòng": 127},
    {"STT": 12, "Tên File": "ws_Vaccine_DanhSachChoTiem_WEB.cs", "Kích thước": "6.1KB", "Số dòng": 153},
    {"STT": 13, "Tên File": "ws_Vaccine_GetByMaDungChung.cs", "Kích thước": "3.9KB", "Số dòng": 96},
    {"STT": 14, "Tên File": "ws_Vaccine_HanCheKhuyenKhich_ByFacID_List.cs", "Kích thước": "2.4KB", "Số dòng": 74},
    {"STT": 15, "Tên File": "ws_Vaccine_HopDong_Detail_KiemTraSLMui.cs", "Kích thước": "6.9KB", "Số dòng": 180},
    {"STT": 16, "Tên File": "ws_Vaccine_HopDong_ListByPatientID.cs", "Kích thước": "10KB", "Số dòng": 243},
    {"STT": 17, "Tên File": "ws_Vaccine_HopDong_ListByPatientIDV2.cs", "Kích thước": "16KB", "Số dòng": 332},
    {"STT": 18, "Tên File": "ws_Vaccine_KiemTra_CapNhat_NgayHenTiem.cs", "Kích thước": "14KB", "Số dòng": 311},
    {"STT": 19, "Tên File": "ws_Vaccine_LayChiDinh.cs", "Kích thước": "3.1KB", "Số dòng": 82},
    {"STT": 20, "Tên File": "ws_Vaccine_LayChiDinh_PhacDo_TrongNgay.cs", "Kích thước": "2.7KB", "Số dòng": 62},
    {"STT": 21, "Tên File": "ws_Vaccine_LichSuTiem.cs", "Kích thước": "12KB", "Số dòng": 274},
    {"STT": 22, "Tên File": "ws_Vaccine_LichSuTiemVaccine.cs", "Kích thước": "6.5KB", "Số dòng": 160},
    {"STT": 23, "Tên File": "ws_Vaccine_PhacDoBenhNhan_List.cs", "Kích thước": "17KB", "Số dòng": 372},
    {"STT": 24, "Tên File": "ws_Vaccine_TheoDoiSauTiem_Get.cs", "Kích thước": "16KB", "Số dòng": 357},
    {"STT": 25, "Tên File": "ws_Vaccine_TheoDoiSauTiem_List.cs", "Kích thước": "9.8KB", "Số dòng": 233},
    {"STT": 26, "Tên File": "ws_Vaccine_TiepNhan_TabVaccine_List.cs", "Kích thước": "20KB", "Số dòng": 457},
    {"STT": 27, "Tên File": "ws_Vaccine_VaccineSuDungThucTe_List.cs", "Kích thước": "4.0KB", "Số dòng": 94},
    {"STT": 28, "Tên File": "ws_Vaccine_VatTuLe_List.cs", "Kích thước": "1.7KB", "Số dòng": 43},
    {"STT": 29, "Tên File": "ws_LayDotKhamGanNhatTrongNgay.cs", "Kích thước": "1.6KB", "Số dòng": 46},
    {"STT": 30, "Tên File": "ws_LoadTenBacSiDieuDuong.cs", "Kích thước": "1.4KB", "Số dòng": 43},
    {"STT": 31, "Tên File": "ws_L_DepartmentRoom_ListForReception.cs", "Kích thước": "5.4KB", "Số dòng": 138},
    {"STT": 32, "Tên File": "ws_L_DoiTuongTinhTien_List.cs", "Kích thước": "1.4KB", "Số dòng": 45},
    {"STT": 33, "Tên File": "ws_L_DoiTuongTinhTien_ListByKhuTiepNhan.cs", "Kích thước": "2.7KB", "Số dòng": 75},
    {"STT": 34, "Tên File": "ws_L_DoiTuongUuTien_List.cs", "Kích thước": "1.1KB", "Số dòng": 32},
    {"STT": 35, "Tên File": "ws_L_Facility_BVTamAnh_List.cs", "Kích thước": "855B", "Số dòng": 25},
    {"STT": 36, "Tên File": "ws_L_Hospital_List.cs", "Kích thước": "2.1KB", "Số dòng": 65},
    {"STT": 37, "Tên File": "ws_L_ICD10_Version.cs", "Kích thước": "744B", "Số dòng": 22},
    {"STT": 38, "Tên File": "ws_L_InjuredTime_List.cs", "Kích thước": "797B", "Số dòng": 26},
    {"STT": 39, "Tên File": "ws_L_LieuLuong_Vaccine_Get.cs", "Kích thước": "1.9KB", "Số dòng": 52},
    {"STT": 40, "Tên File": "ws_L_LoaiBenhNhan_Get.cs", "Kích thước": "381B", "Số dòng": 14},
    {"STT": 41, "Tên File": "ws_L_LoaiTiepNhan_ListByKhuTiepNhan.cs", "Kích thước": "1.5KB", "Số dòng": 42},
    {"STT": 42, "Tên File": "ws_L_MoiQuanHe_Get.cs", "Kích thước": "1.1KB", "Số dòng": 34},
    {"STT": 43, "Tên File": "ws_L_NganHang_Get.cs", "Kích thước": "618B", "Số dòng": 20},
    {"STT": 44, "Tên File": "ws_L_NoiDungGioiThieu_List.cs", "Kích thước": "881B", "Số dòng": 25},
    {"STT": 45, "Tên File": "ws_L_PatientCompanyAffiliation_Save.cs", "Kích thước": "2.6KB", "Số dòng": 69},
    {"STT": 46, "Tên File": "ws_L_PayType_List_Reception.cs", "Kích thước": "660B", "Số dòng": 22},
    {"STT": 47, "Tên File": "ws_L_PKN_LichSuDonThuocChiTiet_Get.cs", "Kích thước": "2.4KB", "Số dòng": 65},
    {"STT": 48, "Tên File": "ws_L_PKN_LichSuDonThuoc_Get.cs", "Kích thước": "2.1KB", "Số dòng": 62},
    {"STT": 49, "Tên File": "ws_L_Province_Version.cs", "Kích thước": "944B", "Số dòng": 25},
    {"STT": 50, "Tên File": "ws_L_ServicePackage_ListChiLayGoi.cs", "Kích thước": "1.7KB", "Số dòng": 42},
    {"STT": 51, "Tên File": "ws_L_Service_VIPExamination_List.cs", "Kích thước": "3.1KB", "Số dòng": "N/A"},
    {"STT": 52, "Tên File": "ws_L_ShiftDaily_LayCaHienTaiLamViec.cs", "Kích thước": "1.8KB", "Số dòng": "N/A"},
    {"STT": 53, "Tên File": "ws_L_UnitDinhNghiaQuyDoi_Get_List.cs", "Kích thước": "1.2KB", "Số dòng": "N/A"},
    {"STT": 54, "Tên File": "ws_L_Utilities_Get.cs", "Kích thước": "1.2KB", "Số dòng": "N/A"},
    {"STT": 55, "Tên File": "ws_L_Vaccine_List.cs", "Kích thước": "4.9KB", "Số dòng": "N/A"},
    {"STT": 56, "Tên File": "ws_L_Vaccine_Phacdo_Detail_Get_KhamBenh.cs", "Kích thước": "16KB", "Số dòng": "N/A"},
    {"STT": 57, "Tên File": "ws_L_Vaccine_ViTriTiem_List.cs", "Kích thước": "1.1KB", "Số dòng": "N/A"},
    {"STT": 58, "Tên File": "ws_MDM_Accompany_Customers_ByPersonReferredID_Save.cs", "Kích thước": "5.5KB", "Số dòng": "N/A"},
    {"STT": 59, "Tên File": "ws_MDM_Accompany_Customers_MainPatient_Check.cs", "Kích thước": "1.8KB", "Số dòng": "N/A"},
    {"STT": 60, "Tên File": "ws_MDM_Accompany_Customers_Save.cs", "Kích thước": "2.9KB", "Số dòng": "N/A"},
    {"STT": 61, "Tên File": "ws_MDM_District_ListAll.cs", "Kích thước": "1.4KB", "Số dòng": "N/A"},
    {"STT": 62, "Tên File": "ws_MDM_Ethnicity_List.cs", "Kích thước": "834B", "Số dòng": "N/A"},
    {"STT": 63, "Tên File": "ws_MDM_Occupation_List.cs", "Kích thước": "975B", "Số dòng": "N/A"},
    {"STT": 64, "Tên File": "ws_MDM_Patient_Get.cs", "Kích thước": "5.6KB", "Số dòng": "N/A"},
    {"STT": 65, "Tên File": "ws_MDM_Patient_GetInfoFromBarCodeForOP.cs", "Kích thước": "23KB", "Số dòng": "N/A"},
    {"STT": 66, "Tên File": "ws_MDM_Patient_GetLichSuKham.cs", "Kích thước": "2.4KB", "Số dòng": "N/A"},
    {"STT": 67, "Tên File": "ws_MDM_Patient_Get_NewPractice.cs", "Kích thước": "9.9KB", "Số dòng": "N/A"},
    {"STT": 68, "Tên File": "ws_MDM_Patient_LayDanhSachBNNgoaiTru_NewScreen.cs", "Kích thước": "30KB", "Số dòng": "N/A"},
    {"STT": 69, "Tên File": "ws_MDM_Patient_MaTiemChung_Save.cs", "Kích thước": "2.5KB", "Số dòng": "N/A"},
    {"STT": 70, "Tên File": "ws_MDM_Patient_NLH_Get.cs", "Kích thước": "6.0KB", "Số dòng": "N/A"},
    {"STT": 71, "Tên File": "ws_MDM_Patient_SearchByNameListForNgoaiTru.cs", "Kích thước": "1.6KB", "Số dòng": "N/A"},
    {"STT": 72, "Tên File": "ws_MDM_Patient_SearchByName_List.cs", "Kích thước": "1.5KB", "Số dòng": "N/A"},
    {"STT": 73, "Tên File": "ws_MDM_Patient_SearchByPhoneNumber_List.cs", "Kích thước": "22KB", "Số dòng": "N/A"},
    {"STT": 74, "Tên File": "ws_MDM_Patient_ThongTinGiayToTuyThan_Save.cs", "Kích thước": "3.1KB", "Số dòng": "N/A"},
    {"STT": 75, "Tên File": "ws_MDM_Patient_TimKiemTheoMaTiemChung.cs", "Kích thước": "1.1KB", "Số dòng": "N/A"},
    {"STT": 76, "Tên File": "ws_MDM_PersonReferredCustomerID_Save.cs", "Kích thước": "1.4KB", "Số dòng": "N/A"},
    {"STT": 77, "Tên File": "ws_MDM_PersonReferredNotification_Today_ByFacID_List.cs", "Kích thước": "2.3KB", "Số dòng": "N/A"},
    {"STT": 78, "Tên File": "ws_MDM_Person_Delete.cs", "Kích thước": "1.8KB", "Số dòng": "N/A"},
    {"STT": 79, "Tên File": "ws_MDM_Person_ForReferredWithPatient_Save.cs", "Kích thước": "2.9KB", "Số dòng": "N/A"},
    {"STT": 80, "Tên File": "ws_MDM_Person_SearchByFullName_List.cs", "Kích thước": "9.9KB", "Số dòng": "N/A"},
    {"STT": 81, "Tên File": "ws_MDM_Person_SearchByPhoneNumber_List.cs", "Kích thước": "9.5KB", "Số dòng": "N/A"},
    {"STT": 82, "Tên File": "ws_MDM_Person_SearchForPatientByFullName_List.cs", "Kích thước": "9.8KB", "Số dòng": "N/A"},
    {"STT": 83, "Tên File": "ws_MDM_Province_Get.cs", "Kích thước": "1.4KB", "Số dòng": "N/A"},
    {"STT": 84, "Tên File": "ws_MDM_Province_ListAll.cs", "Kích thước": "1.6KB", "Số dòng": "N/A"},
    {"STT": 85, "Tên File": "ws_MDM_Ward_ListAll.cs", "Kích thước": "852B", "Số dòng": "N/A"},
    {"STT": 86, "Tên File": "ws_NguonTiepNhan_ListAll.cs", "Kích thước": "921B", "Số dòng": "N/A"},
    {"STT": 87, "Tên File": "ws_PatientHub_Getdata.cs", "Kích thước": "19KB", "Số dòng": "N/A"},
    {"STT": 88, "Tên File": "ws_PhacDoGoiY_List_Get.cs", "Kích thước": "10KB", "Số dòng": "N/A"},
    {"STT": 89, "Tên File": "ws_PhongTiemVaccine_List.cs", "Kích thước": "2.8KB", "Số dòng": "N/A"},
    {"STT": 90, "Tên File": "ws_PKN_BNThongTinSoSinh_Save.cs", "Kích thước": "2.0KB", "Số dòng": "N/A"},
    {"STT": 91, "Tên File": "ws_PKN_DeletePatientServiceAssignment.cs", "Kích thước": "1.7KB", "Số dòng": "N/A"},
    {"STT": 92, "Tên File": "ws_PKN_Diagnosis_Get_Latest.cs", "Kích thước": "1.2KB", "Số dòng": "N/A"},
    {"STT": 93, "Tên File": "ws_PKN_GetBenhNhanKhamBenhId.cs", "Kích thước": "2.6KB", "Số dòng": "N/A"},
    {"STT": 94, "Tên File": "ws_PKN_GetPatientServicesAssignment.cs", "Kích thước": "4.6KB", "Số dòng": "N/A"},
    {"STT": 95, "Tên File": "ws_PKN_GetServiceList.cs", "Kích thước": "5.6KB", "Số dòng": "N/A"},
    {"STT": 96, "Tên File": "ws_PKN_HenTaiKham_Delete.cs", "Kích thước": "2.8KB", "Số dòng": "N/A"},
    {"STT": 97, "Tên File": "ws_PKN_HenTaiKham_Save.cs", "Kích thước": "6.9KB", "Số dòng": "N/A"},
    {"STT": 98, "Tên File": "ws_PKN_ICD_get.cs", "Kích thước": "806B", "Số dòng": "N/A"},
    {"STT": 99, "Tên File": "ws_PKN_KhamBenh_Get.cs", "Kích thước": "4.0KB", "Số dòng": "N/A"},
    {"STT": 100, "Tên File": "ws_PKN_KhamBenh_Save.cs", "Kích thước": "12KB", "Số dòng": "N/A"}
]

# Tạo DataFrame
df = pd.DataFrame(files_data)

# Tạo file Excel
with pd.ExcelWriter('QAHosGenericDB_Files_List.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Danh sách Files', index=False)
    
    # Lấy worksheet để format
    worksheet = writer.sheets['Danh sách Files']
    
    # Điều chỉnh độ rộng cột
    worksheet.column_dimensions['A'].width = 8
    worksheet.column_dimensions['B'].width = 60
    worksheet.column_dimensions['C'].width = 15
    worksheet.column_dimensions['D'].width = 12

print("Đã tạo file Excel: QAHosGenericDB_Files_List.xlsx")
print(f"Tổng số file: {len(files_data)}")
