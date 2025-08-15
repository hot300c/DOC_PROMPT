### APIs used by trang Tiep Nhan Moi (`/tiep-nhan/tiep-nhan-moi`)

This page documents how the page calls backend APIs and inventories all commands/endpoints referenced by the route and its nested components.

### Overview

- Transport: central Axios layer posting to one backend endpoint.
- Base URL: `process.env.ALADDIN_API_URL`
- Endpoint: `POST /DataAccess`
- Body shape: an array of objects `{ category, command, parameters }`
- Typical categories: `QAHosGenericDB`, `QA_Pay`, `Integration`, `Security`
- Some external calls use plain axios/fetch (e.g., Immunization code lookup, TTS proxy)

### How to read this inventory

- “Service” is the function used in code, often inside `app/lib/services/*`.
- “Command” is the `ws_*` backend procedure executed through `/DataAccess`.
- “Type”: Read = query; Write = mutation/transaction.

### Core request helpers

- Client axios: `app/lib/network/client-axios.ts`
- Server axios: `app/lib/network/server-axios.ts`
- Shared instance: `app/lib/network/axios-instance.ts`
- HTTP wrapper: `app/lib/network/http.ts` (`post("/DataAccess", …)`)
- Batched transactions: `SystemService.executeTransaction` (sends multiple `{ category, command, parameters }` items)

### External (non-/DataAccess) calls

- Immunization code lookup search (axios GET with Bearer):
  - File: `app/(main)/tiep-nhan/tiep-nhan-moi/immunization-code-lookup/_utils/services/search-MTC.ts`
  - Type: Read
- TTS proxy route (server → external TTS API):
  - File: `app/api/tts/route.ts` (axios POST to `ttsApiUrl`)
  - Type: Read

### Inventory table (grouped by domain)

Note: file references indicate where the service/command is used within the `tiep-nhan/tiep-nhan-moi` route and its direct utilities.


| Category       | Service/Usage                                                                       | Command (if via /DataAccess)                                    | Type  | Files (examples)                                                                                     |
| ---------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------ |
| QAHosGenericDB | SettingService.fetchEthnicity                                                       | ws_MDM_Ethnicity_List                                           | Read  | `admissionPatientDetailModal.tsx`, `app/lib/services/setting.ts`                                     |
| QAHosGenericDB | SettingService.fetchOccupation                                                      | ws_MDM_Occupation_List                                          | Read  | `admissionPatientDetailModal.tsx`, `app/lib/services/setting.ts`                                     |
| QAHosGenericDB | SettingService.fetchProvince                                                        | ws_MDM_Province_Get                                             | Read  | `admissionPatientDetailModal.tsx`, `app/lib/services/setting.ts`                                     |
| QAHosGenericDB | SettingService.fetchCountry                                                         | ws_L_Country_ListV2                                             | Read  | `admissionPatientDetailModal.tsx`, `app/lib/services/setting.ts`                                     |
| QAHosGenericDB | SettingService.fetch_ws_L_DepartmentRoom_DanhsachTangList                           | ws_L_DepartmentRoom_DanhsachTangList                            | Read  | `floorSettingUI.tsx`, `app/lib/services/setting.ts`                                                  |
| QAHosGenericDB | SettingService.ws_L_API_Config_Load                                                 | ws_L_API_Config_Load (Integration)                              | Read  | `contractDetailUI.tsx`, `app/lib/services/setting.ts`                                                |
| QAHosGenericDB | PatientService.fetchListPatientToday                                                | ws_… (see`app/lib/services/patient.ts`)                        | Read  | `admissionListPatient.tsx`                                                                           |
| QAHosGenericDB | PatientService.fetchPatientExaminationHistory                                       | ws_…                                                           | Read  | `admissionExaminationHistoryModal.tsx`                                                               |
| QAHosGenericDB | PatientService.fetchPatientClinicalSession                                          | ws_…                                                           | Read  | `admissionExaminationHistoryModal.tsx`                                                               |
| QAHosGenericDB | PatientService.fetch_ws_CN_MDM_Patient_Age_Get                                      | ws_CN_MDM_Patient_Age_Get                                       | Read  | `admissionNotificationUI.tsx`, `app/lib/services/patient.ts`                                         |
| QAHosGenericDB | PatientService.fetch_ws_MDM_PersonReferredNotification_Today_ByFacID_List           | ws_MDM_PersonReferredNotification_Today_ByFacID_List            | Read  | `admissionNotificationUI.tsx`, `app/lib/services/patient.ts`                                         |
| QAHosGenericDB | PatientService.fetch_ws_Vaccine_LichSuTiem                                          | ws_Vaccine_LichSuTiem                                           | Read  | `patientHistoryUI.tsx`, `app/lib/services/patient.ts`                                                |
| QAHosGenericDB | PatientService.fetch_ws_Vaccine_LichSuTiemVaccine                                   | ws_Vaccine_LichSuTiemVaccine                                    | Read  | `patientHistoryUI.tsx`, `app/lib/services/patient.ts`                                                |
| QAHosGenericDB | PatientService.fetch_ws_BIL_Invoice_PatientContractPayment_List                     | ws_BIL_Invoice_PatientContractPayment_List                      | Read  | `patientHistoryUI.tsx`                                                                               |
| QAHosGenericDB | PatientService.fetch_ws_CN_ClinicalSessionID_AnotherSource_Vaccine_ByPatientID_List | ws_CN_ClinicalSessionID_AnotherSource_Vaccine_ByPatientID_List  | Read  | `patientHistoryUI.tsx`                                                                               |
| QAHosGenericDB | PatientService.fetchCarrier                                                         | ws_…                                                           | Read  | `admissionUpdateCarrierModal.tsx`                                                                    |
| QAHosGenericDB | ConsultationRoomService.fetchConsultationRoom                                       | ws_L_DepartmentRoom_ListForReception                            | Read  | `consultationFeeUI.tsx`, `consultationFeeComboboxRoomUI.tsx`, `app/lib/services/consultationRoom.ts` |
| QAHosGenericDB | ConsultationGridService.fetchConsultationGrid (new pricing)                         | ws_CN_PhysicianAdmissions_GetVIPPhysInDay_List                  | Read  | `consultationFeeUI.tsx`, `app/lib/services/consultationGrid.ts`                                      |
| QAHosGenericDB | ConsultationGridService.fetchConsultationGrid (legacy)                              | ws_LayDotKhamGanNhatTrongNgay                                   | Read  | `consultationFeeUI.tsx`, `app/lib/services/consultationGrid.ts`                                      |
| QAHosGenericDB | VaccineService.fetchVaccinationHistory                                              | ws_…                                                           | Read  | `admissionSearchPatientHistory.tsx`                                                                  |
| QAHosGenericDB | VaccineService.fetchVaccineRegimenGroup                                             | ws_Vaccine_PhacDoBenhNhan… (see`app/lib/services/vaccine*.ts`) | Read  | `contractDetailUI.tsx`, `contractVaccineDetailUI.tsx`                                                |
| QAHosGenericDB | VaccineService.fetchVaccineRegimenDetail                                            | ws_Vaccine_Phacdo_Detail…                                      | Read  | `contractRegimenDetails.tsx`, `contractVaccineDetailUI.tsx`                                          |
| QAHosGenericDB | VaccineService.fetchVaccineRegimenByAge                                             | ws_Vaccine_Phacdo_XepTheoTuoi / or age variant                  | Read  | `contractVaccineDetailUI.tsx`                                                                        |
| QAHosGenericDB | VaccineService.fetchVaccineLimitedByPackage                                         | ws_…                                                           | Read  | `contractVaccineDetailUI.tsx`                                                                        |
| QAHosGenericDB | VaccineService.fetchActiveVaccineRegimen                                            | ws_…                                                           | Read  | `contractVaccineDiseaseGroupUI.tsx`, `add-template-modal/index.tsx`                                  |
| QAHosGenericDB | VaccineService.fetchVaccinePackageTemplate                                          | ws_…                                                           | Read  | `contractVaccineTemplateModal.tsx`                                                                   |
| QAHosGenericDB | VaccineService.fetchVaccinePackageTemplateDetail                                    | ws_…                                                           | Read  | `contractVaccineTemplateModal.tsx`, `template-configuration/*`                                       |
| QAHosGenericDB | ContractService.fetchContractDetailV2                                               | ws_…                                                           | Read  | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | ContractService.fetchContractDetailRoot                                             | ws_Vaccine_HopDong_Detail_Root_ByHopDongID_List                 | Read  | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | ContractService.fetch_ws_Vaccine_HopDong_ListByPatientIDV2                          | ws_Vaccine_HopDong_ListByPatientIDV2                            | Read  | `contractListUI.tsx`, `contract-history/*`                                                           |
| QAHosGenericDB | Contract-history utils                                                              | ws_ws_L_ServicePackage_ListByServicePackageIDForHDVaccine_V2    | Read  | `contract-history/_utils/services/contract-history-api.ts`                                           |
| QAHosGenericDB | Contract-history utils                                                              | ws_LayDanhSachVaccineTheoHopDongDaDatTruoc_V3                   | Read  | same as above                                                                                        |
| QAHosGenericDB | Contract-history utils                                                              | ws_L_Vaccine_Phacdo_List_ByMaChungForTiepNhan_V2                | Read  | same as above                                                                                        |
| QAHosGenericDB | Contract-history utils                                                              | ws_LayDanhSachPhacDoTheoHopDongDaDatTruoc_V2                    | Read  | same as above                                                                                        |
| QAHosGenericDB | Contract-history utils                                                              | ws_L_Vaccine_Phacdo_Detail_ListWithPrice                        | Read  | same as above                                                                                        |
| QAHosGenericDB | Contract-history utils                                                              | ws_LayDanhSachMuiTiemTheoHopDongDaDatTruoc                      | Read  | same as above                                                                                        |
| QAHosGenericDB | PreOrderService.fetchListNhomBenhVaccine                                            | ws_…                                                           | Read  | `preorder-vaccine-table.tsx`, `patientPreOrder` logic                                                |
| QAHosGenericDB | PreOrderService.fetchListVaccineTab                                                 | ws_…                                                           | Read  | `preorder-vaccine-table.tsx`                                                                         |
| QAHosGenericDB | Address suggestion                                                                  | ws_GoiYListDiaChiMoiByPatient                                   | Read  | `_components/goi-y-dia-chi-moi-model.tsx`, `_utils/services/api.ts`                                  |
| QAHosGenericDB | Template configuration list                                                         | ws_L_DanhSachMau_ByFacID_List                                   | Read  | `template-configuration/_utils/services/template-configuration.api.ts`                               |
| QAHosGenericDB | Template configuration detail                                                       | ws_L_DanhSachMau_Detail_List                                    | Read  | `template-configuration/_utils/services/template-configuration.api.ts`                               |
| QAHosGenericDB | Product vaccine list                                                                | ws_L_Product_Vaccine_List                                       | Read  | `template-configuration/_utils/services/api.ts`                                                      |
| QAHosGenericDB | Vaccine regimen by age                                                              | ws_L_Vaccine_Phacdo_XepTheoTuoi                                 | Read  | `template-configuration/_utils/services/api.ts`                                                      |
| QAHosGenericDB | DanhSachMau KT                                                                      | ws_L_DanhSachMau_KT                                             | Read  | `template-configuration/_utils/services/api.ts`                                                      |
| QAHosGenericDB | Immunization country info                                                           | ws_LayThongTinMaQuocGia                                         | Read  | `immunization-code-lookup/_utils/services/immunization-code-lookup.api.ts`                           |
| QAHosGenericDB | Search patient by immunization code                                                 | ws_MDM_Patient_TimKiemTheoMaTiemChung                           | Read  | `immunization-code-lookup/_utils/services/immunization-code-lookup.api.ts`                           |
| QA_Pay         | QAPay.fetchAccountOwner                                                             | ws_AccountOwner_GetByCondition                                  | Read  | `qa-pay-check/*`, `app/lib/services/qa-pay-services.ts`                                              |
| QA_Pay         | QAPay.fetchCardInfo                                                                 | ws_L_Card_Get                                                   | Read  | `qa-pay-check/*`                                                                                     |
| QA_Pay         | QAPay.fetchNTransactionListByAccount                                                | ws_NTransaction_ListByAccount                                   | Read  | `qa-pay-check/*`                                                                                     |
| QAHosGenericDB | Save patient (search modal)                                                         | ws_MDM_Patient_SaveV2                                           | Write | `admissionSearchPatientModal.tsx`                                                                    |
| QAHosGenericDB | Save person referred with patient                                                   | ws_MDM_Person_ForReferredWithPatient_Save                       | Write | `admissionSearchPatientModal.tsx`                                                                    |
| QAHosGenericDB | Save patient identity                                                               | ws_MDM_Patient_ThongTinGiayToTuyThan_Save                       | Write | `admissionSearchPatientModal.tsx`                                                                    |
| QAHosGenericDB | Warn just discharged patient                                                        | ws_CN_FacAdmissions_WarnJustDischargedPatient                   | Read  | `admissionSearchPatientModal.tsx`                                                                    |
| QAHosGenericDB | Get admission exist today                                                           | ws_CN_FacAdmissions_GetExistTodayV2                             | Read  | `admissionSearchPatientModal.tsx`, `consultationRoom.ts`                                             |
| QAHosGenericDB | Re-exam warning                                                                     | ws_CN_PatientScheduledVisits_CanhBaoTaiKham                     | Read  | `admissionSearchPatientModal.tsx`                                                                    |
| QAHosGenericDB | Check update service                                                                | ws_CN_FacAdmissions_CheckUpdateService                          | Read  | `admissionSearchPatientModal.tsx`                                                                    |
| QAHosGenericDB | Get referral source                                                                 | ws_CN_FacAdmission_NoiGioiThieu_Get                             | Read  | `admissionSearchPatientModal.tsx`                                                                    |
| QAHosGenericDB | Save contact person                                                                 | ws_CN_NguoiLienHe_Savev2                                        | Write | `page.tsx` (saving flow)                                                                             |
| QAHosGenericDB | Save exam fee info                                                                  | ws_KTThongTinCongKhamVaccine                                    | Write | `consultationFeeUI.tsx`                                                                              |
| QAHosGenericDB | Update exam fee info                                                                | ws_CapNhatThongTinCongKhamVaccine                               | Write | `consultationFeeUI.tsx`                                                                              |
| QAHosGenericDB | Verify before deleting accompany                                                    | ws_MDM_Accompany_Customers_VerifyBeforeDeleting                 | Read  | `consultationFeeUI.tsx`                                                                              |
| QAHosGenericDB | Delete accompany by facAdmissionId                                                  | ws_MDM_Accompany_Customers_ByFacAdmissionID_Delete              | Write | `consultationFeeUI.tsx`                                                                              |
| QAHosGenericDB | Save regimen                                                                        | ws_CN_ClinicalSessions_SavePhacDo                               | Write | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | Save regimen schedule                                                               | ws_CN_ClinicalSessions_Schedule_Save                            | Write | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | Save patient regimen detail                                                         | ws_Vaccine_PhacDoBenhNhan_Detail_Save                           | Write | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | Save contract root detail                                                           | ws_Vaccine_HopDong_Detail_Root_Save                             | Write | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | Update contract duration                                                            | ws_Vaccine_HopDong_CapNhatThoiHanHD                             | Write | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | Update outside-shot pre-order                                                       | ws_Vaccine_HopDong_TiemNgoaiTemp_DatTruoc_Update                | Write | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | Update shot of contract detail                                                      | ws_Vaccine_HopDong_Detail_CapNhatMuiTiem                        | Write | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | Save patient regimen                                                                | ws_Vaccine_PhacDoBenhNhan_Save                                  | Write | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | Save patient regimen by disease group                                               | ws_Vaccine_PhacDo_NhomBenh_BenhNhan_SaveByNhomBenh              | Write | `contractRegimenDetails.tsx`                                                                         |
| QAHosGenericDB | Template config save                                                                | ws_L_DanhSachMau_Save                                           | Write | `template-configuration/_components/*`                                                               |
| QAHosGenericDB | Template config activate                                                            | ws_L_DanhSachMau_Active_Update                                  | Write | `template-configuration/_components/*`                                                               |
| QAHosGenericDB | Template config delete by goiId                                                     | ws_L_DanhSachMau_ByGoiID_Delete                                 | Write | `template-configuration/_components/*`                                                               |
| QAHosGenericDB | Template detail save                                                                | ws_L_DanhSachMau_Detail_Save                                    | Write | `template-configuration/_components/*`                                                               |

If you need a HAR/runtime capture to ensure no interactions are missed (e.g., buttons opening modals or contextual actions), consider using Playwright to visit `/tiep-nhan/tiep-nhan-moi`, perform key interactions, and l


| col1 | col2 | col3 |
| ------ | ------ | ------ |
|      |      |      |
|      |      |      |

og all requests that match `/DataAccess`, `/api/*`, or external hosts.
