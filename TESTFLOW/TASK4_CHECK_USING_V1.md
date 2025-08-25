
GIT:
BE:
https://git.vnvc.info/vnvc-qas/aladdin/-/tree/feat/ws_Vaccine_KiemTraDongPhacDo


LINK TESTING:
https://dev-genie.vnvc.info/ngoai-tru/kham-benh/971646b1-2764-450c-a0b0-013117b90024?date=2025-08-20&deptID=5&roomID=1&doiTuongInPhieu=0&isPediatric=false





"Chờ review code. 
LƯU Ý: 2 SP:
ws_Vaccine_KiemTraVaDongPhacDo (đã làm cái này)
ws_Vaccine_KiemTraVaDongPhacDo_V2

https://rm.vnvc.info/issues/137323

https://git.vnvc.info/vnvc-qas/aladdin/-/merge_requests/721"






# để kiểm tra nhánh
cd aladdin
git checkout feat/ws_Vaccine_KiemTraDongPhacDo

### 2. Add các file đã thay đổi
```bash
# git add .
# hoặc add từng file cụ thể, 
git add -A
```

### 3. Commit với amend (cập nhật commit cuối cùng)
```bash
git commit --amend -m "remove sessionID in param"
# git commit --amend -m "Adjust parameters to match the values and names sent from the Front-end"
```

### 4. Push code lên remote (force push vì đã amend)
```bash
#git push origin <tên_nhánh> --force
# hoặc
git push origin feat/ws_Vaccine_KiemTraDongPhacDo --force-with-lease