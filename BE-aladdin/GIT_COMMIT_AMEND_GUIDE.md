# HƯỚNG DẪN GIT COMMIT VÀ PUSH VỚI AMEND

## Mục đích
Tài liệu này ghi nhớ cách xử lý khi cần commit và push code với amend để giữ chỉ 1 commit trong nhánh.

## Các bước thực hiện

### 1. Kiểm tra trạng thái hiện tại
```bash
# để kiểm tra nhánh
cd aladdin
git checkout fix/ws_QuanLyTapTrung

git branch
git status
git log --oneline
```

Convert SP to handle ws_BIL_Invoice_Save_Vaccine: DONE
feat/Convert_ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh: DONE
https://git.vnvc.info/vnvc-qas/aladdin/-/tree/feat/Convert_ws_Vaccine_ThongBaoKhongchan: 



review code giúp tôi theo rule trong task template. Nếu code chưa tuân thủ đúng thì cập nhật lại nhưng vẫn đảm bảo logic code đúng đắn vì tôi đã testing passed nó rồi.

review lại code trang này mà phải tuân thủ theo rule của task template. Và cập nhật nó khi chưa tuân thủ đầy đủ. Cũng test lại test case luôn.


### 2. Add các file đã thay đổi
```bash
# git add .
# hoặc add từng file cụ thể, 
git add -A
```

### 3. Commit với amend (cập nhật commit cuối cùng)
```bash
git commit --amend -m "Refactor code to follow coding conventions"
# git commit --amend -m "Adjust parameters to match the values and names sent from the Front-end"
```

### 4. Push code lên remote (force push vì đã amend)
```bash
#git push origin <tên_nhánh> --force
# hoặc
git push origin feat/Convert_ws_Vaccine_KiemTraCanhBaoTiemVaccineTrungNhomBenh --force-with-lease
```

### 5. Check
https://git.vnvc.info/vnvc-qas/aladdin/-/merge_requests



## Lưu ý quan trọng

- **--force-with-lease** an toàn hơn --force vì nó kiểm tra xem có ai khác đã push code mới lên chưa
- Chỉ sử dụng amend khi commit chưa được push lên remote hoặc chỉ có mình làm việc trên nhánh đó
- Nếu đã push commit lên remote và có người khác đã pull về, KHÔNG nên dùng amend

## Trường hợp cần dùng

- Sửa lỗi typo trong commit message
- Thêm file quên vào commit trước đó
- Sửa lỗi nhỏ trong code đã commit
- Muốn giữ lịch sử commit sạch sẽ với chỉ 1 commit

## Lệnh backup (để phòng hờ)

```bash
# Tạo backup branch trước khi amend
git branch backup-before-amend

# Nếu cần quay lại
git reset --hard backup-before-amend
```

## Ví dụ thực tế

```bash
# 1. Kiểm tra status
git status

# 2. Add files
git add .

# 3. Commit với amend
git commit --amend -m "Fix bug và cải thiện performance"

# 4. Push force
git push origin main --force-with-lease
```

---
*Tài liệu này được tạo để ghi nhớ cách xử lý git commit và push với amend. Cập nhật khi cần thiết.*
