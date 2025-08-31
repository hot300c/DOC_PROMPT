FE: [FE-genie/TASK12_INIT_Integrating/README_FOUND.md](../FE-genie/TASK12_INIT_Integrating/README_FOUND.md)

BE: [BE-aladdin/TASK/TASK12_REVIEWING](../BE-aladdin/TASK/TASK12_REVIEWING)

GIT:
cd C:\PROJECTS\aladdin
git checkout feat/Convert_ws_Vaccine_KiemTraTrungNhomBenhDangMo



Kiểm tra lại request và response khi gọi API BE mà tôi đã test thành công qua các test case trong thư mục này:
C:\PROJECTS\aladdin\WebService.Handlers.Tests\TestCases\QAHosGenericDB\ws_Vaccine_KiemTraTrungNhomBenhDangMo

Hãy tham thảo và kiểm tra code FE cho đúng.


Done:
https://git.vnvc.info/vnvc-qas/aladdin/-/merge_requests/738


cd C:\PROJECTS\genie
git checkout -b feat/Convert_ws_Vaccine_KiemTraTrungNhomBenhDangMo


git push origin feat/Convert_ws_Vaccine_KiemTraTrungNhomBenhDangMo --force-with-lease

C:\PROJECTS\genie\app\lib\services\detailCheckup.ts
C:\PROJECTS\genie\app\(main)\ngoai-tru\kham-benh\hooks\useChiDinhVaccine.ts



Convert SP to handle ws_Vaccine_KiemTraTrungNhomBenhDangMo:
Dũng đã duyệt, nhờ Sơn xem để cùng merge vào main sau đó anh tạo ticket cho anh Nguyên testing.
BE: https://git.vnvc.info/vnvc-qas/aladdin/-/merge_requests/738
FE: https://git.vnvc.info/vnvc-qas/genie/-/merge_requests/3597