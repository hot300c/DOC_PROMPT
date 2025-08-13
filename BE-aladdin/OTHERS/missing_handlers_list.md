# DANH SÁCH STORED PROCEDURES CHƯA CÓ HANDLERS

## 1. BILLING & INVOICING (Ưu tiên cao)

### Invoice Management
- ws_BIL_Invoice_Save
- ws_BIL_Invoice_Get
- ws_BIL_Invoice_List
- ws_BIL_Invoice_Delete
- ws_BIL_Invoice_Update
- ws_BIL_Invoice_ListByFacAdmissionID
- ws_BIL_Invoice_ListByCondition
- ws_BIL_Invoice_List_IP

### Invoice Details
- ws_BIL_InvoiceDetail_Save
- ws_BIL_InvoiceDetail_Get
- ws_BIL_InvoiceDetail_List
- ws_BIL_InvoiceDetail_ListByInvoiceID
- ws_BIL_InvoiceDetail_Delete
- ws_BIL_InvoiceDetail_Update

### Payment Methods
- ws_BIL_Invoice_Cash_Save
- ws_BIL_Invoice_Credit_Save
- ws_BIL_Invoice_VNPAY_Save
- ws_BIL_Invoice_QAPAY_Save
- ws_BIL_Invoice_MB_Save
- ws_BIL_Invoice_Techcom_Save

### Advanced Payment
- ws_BIL_AdvancedPayment_Save
- ws_BIL_AdvancedPayment_Get
- ws_BIL_AdvancedPayment_List
- ws_BIL_AdvancedPayment_Delete

### Refunds
- ws_BIL_InvoiceRefund_Save
- ws_BIL_InvoiceRefund_Get
- ws_BIL_InvoiceRefund_List
- ws_BIL_InvoiceRefund_Delete

## 2. PATIENT MANAGEMENT (Ưu tiên cao)

### Patient CRUD
- ws_MDM_Patient_Save
- ws_MDM_Patient_List
- ws_MDM_Patient_Delete
- ws_MDM_Patient_SearchByName
- ws_MDM_Patient_SearchByPhoneNumber_List
- ws_MDM_Patient_ListForBilling
- ws_MDM_Patient_ListForReception

### Patient Information
- ws_MDM_Patient_GetAllInfo
- ws_MDM_Patient_GetAllInfo_Ver2
- ws_MDM_Patient_GetBy
- ws_MDM_Patient_GetByPatientHospitalID
- ws_MDM_Patient_GetByPatientID
- ws_MDM_Patient_GetByInvoiceID

### Patient History
- ws_MDM_Patient_GetLichSuKham
- ws_MDM_Patient_GetNgayTaiKhamGanNhat
- ws_MDM_Patient_GetMaxPatientHospitalID

### Patient Search
- ws_MDM_Patient_SearchCriteria
- ws_MDM_Patient_SearchV2
- ws_MDM_Patient_TimKiemBenhNhan
- ws_MDM_Patient_TimKiemTheoMaTiemChung

## 3. CLINICAL SESSIONS (Ưu tiên cao)

### Clinical Sessions CRUD
- ws_CN_ClinicalSessions_Save
- ws_CN_ClinicalSessions_Get
- ws_CN_ClinicalSessions_List
- ws_CN_ClinicalSessions_Delete
- ws_CN_ClinicalSessions_UpdateComplete

### Clinical Sessions by Patient
- ws_CN_ClinicalSessions_ListByPatientID
- ws_CN_ClinicalSessions_GetByFac
- ws_CN_ClinicalSessions_GetByNgayChiDinh

### Clinical Sessions Services
- ws_CN_ClinicalSessions_ListServicesByPA
- ws_CN_ClinicalSessions_ListServicesByFacAdmission
- ws_CN_ClinicalSessions_ListServicesByParentClinicalSessionID

### Clinical Sessions Materials
- ws_CN_ClinicalSessions_GetMaterialIP
- ws_CN_ClinicalSessions_GetExportedMaterialOP
- ws_CN_ClinicalSessions_ListWaitingExportByRoomID

## 4. VACCINE MANAGEMENT (Ưu tiên trung bình)

### Vaccine CRUD
- ws_Vaccine_List
- ws_Vaccine_Save
- ws_Vaccine_Get
- ws_Vaccine_Delete
- ws_Vaccine_Update

### Vaccine Contracts
- ws_Vaccine_HopDong_Save
- ws_Vaccine_HopDong_Get
- ws_Vaccine_HopDong_List
- ws_Vaccine_HopDong_Delete
- ws_Vaccine_HopDong_ListByPatientID

### Vaccine Schedules
- ws_Vaccine_DanhSachChoKham_WEB
- ws_Vaccine_DanhSachChoTiem_WEB
- ws_Vaccine_LichSuTiem
- ws_Vaccine_LichSuTiemVaccine

### Vaccine Validation
- ws_Vaccine_CheckValidation
- ws_Vaccine_KiemTraChiDinh
- ws_Vaccine_KiemTraTuongTac

## 5. INVENTORY MANAGEMENT (Ưu tiên trung bình)

### Product Management
- ws_INV_Product_Get
- ws_INV_Product_Save
- ws_INV_Product_List
- ws_INV_Product_Delete
- ws_INV_Product_UpdateQty

### Stock Management
- ws_INV_Product_LayTonKho
- ws_INV_Product_LayTonKhoHienTai
- ws_INV_Product_LayXuatNhapTon
- ws_INV_Product_XemTonKhoToanHeThong

### Approved In/Out
- ws_INV_ApprovedIn_Save
- ws_INV_ApprovedIn_Get
- ws_INV_ApprovedIn_List
- ws_INV_ApprovedOut_Save
- ws_INV_ApprovedOut_Get
- ws_INV_ApprovedOut_List

### Request In/Out
- ws_INV_RequestIn_Save
- ws_INV_RequestIn_Get
- ws_INV_RequestIn_List
- ws_INV_RequestOut_Save
- ws_INV_RequestOut_Get
- ws_INV_RequestOut_List

## 6. FACILITY ADMISSIONS (Ưu tiên trung bình)

### Admissions CRUD
- ws_CN_FacAdmissions_Save
- ws_CN_FacAdmissions_Get
- ws_CN_FacAdmissions_List
- ws_CN_FacAdmissions_Delete
- ws_CN_FacAdmissions_UpdateComplete

### Admissions by Patient
- ws_CN_FacAdmissions_GetByPatientID
- ws_CN_FacAdmissions_ListByPatientID
- ws_CN_FacAdmissions_GetCurrentFacAdmissionID

### Admissions by Date
- ws_CN_FacAdmissions_ListInDay
- ws_CN_FacAdmissions_Get_ToDay
- ws_CN_FacAdmissions_List_ByAdmitOn

## 7. PHYSICIAN ADMISSIONS (Ưu tiên trung bình)

### Physician Admissions CRUD
- ws_CN_PhysicianAdmissions_Save
- ws_CN_PhysicianAdmissions_Get
- ws_CN_PhysicianAdmissions_List
- ws_CN_PhysicianAdmissions_Delete
- ws_CN_PhysicianAdmissions_UpdateComplete

### Physician Admissions by Patient
- ws_CN_PhysicianAdmissions_ListByPatientID
- ws_CN_PhysicianAdmissions_GetByFacAdmissionID

### Physician Admissions by Date
- ws_CN_PhysicianAdmissions_ListInDay
- ws_CN_PhysicianAdmissions_GetPhysInDay_List

## 8. DIAGNOSIS & CONSULTATIONS (Ưu tiên thấp)

### Diagnosis CRUD
- ws_CN_Diagnosis_Save
- ws_CN_Diagnosis_Get
- ws_CN_Diagnosis_List
- ws_CN_Diagnosis_Delete
- ws_CN_Diagnosis_Update_Mota

### Physician Consultations
- ws_CN_PhysicianConsultations_Save
- ws_CN_PhysicianConsultations_Get
- ws_CN_PhysicianConsultations_List
- ws_CN_PhysicianConsultations_SavePractice

## 9. REPORTS (Đã có một số handlers)

### Billing Reports
- ws_rep_BaoCaoDoanhThu
- ws_rep_BaoCaoKiemKe
- ws_rep_BaoCaoThongKeTongHopDichVu

### Patient Reports
- ws_rep_KhamBenhTheoNgay
- ws_rep_PhieuLinhThuocNoiTru
- ws_rep_ToaThuocForYHCT

### Vaccine Reports
- ws_rep_Report_BienBanGiaoNhanVaccineV2
- ws_rep_PhuLucHopDongVaccine

## 10. UTILITIES & CONFIGURATION (Ưu tiên thấp)

### Settings & Configuration
- ws_L_SettingUsage_List
- ws_L_SettingUsage_Save
- ws_L_SettingUsage_Delete

### Lookup Data
- ws_L_ICD10_List
- ws_L_Service_List
- ws_L_Department_List
- ws_L_Product_List

### System Utilities
- ws_GetDateTimeServer
- ws_GetSequentialGuids
- ws_ValidateDataControl

## TỔNG KẾT

### Theo ưu tiên:

**Ưu tiên cao (Core Business):**
- Billing & Invoicing: ~50 SPs
- Patient Management: ~30 SPs  
- Clinical Sessions: ~40 SPs

**Ưu tiên trung bình:**
- Vaccine Management: ~60 SPs
- Inventory Management: ~80 SPs
- Facility/Physician Admissions: ~40 SPs

**Ưu tiên thấp:**
- Diagnosis & Consultations: ~20 SPs
- Reports: ~30 SPs
- Utilities: ~50 SPs

**Tổng cộng:** Khoảng 400 stored procedures cần handlers ưu tiên cao và trung bình
