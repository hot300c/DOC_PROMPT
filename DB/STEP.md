Khi thêm 1 cột mới vào DB. 
Thì nên theo các bước sau để cho đồng bộ DB:

1. Pull toàn bộ source code từ qas-db (production) về local.
2. Copy file thay đổi vào cùng cấp thư mục: C:\PROJECTS\qas-db-dev

3. chạy lệnh theo README :
C:\PROJECTS\qas-db-dev\README.md

3.1: 
.\CreateSchemas.ps1 -db QAHosGenericDB

3.2 
docker build -t registry.vnvc.info/vnvc-qas/qas-db-dev:0.25 .

3.3 
docker run --rm -d -p 1433:1433 --name mssql registry.vnvc.info/vnvc-qas/qas-db-dev:0.25

3.4 
docker tag registry.vnvc.info/vnvc-qas/qas-db-dev:0.25 registry.vnvc.info/vnvc-qas/qas-db-dev:0.25

3.5 
docker push registry.vnvc.info/vnvc-qas/qas-db-dev:0.25




git checkout main
git pull
git checkout fix/ws_QuanLyTapTrung_vnvcshop
git rebase main