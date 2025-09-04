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



### 2. Add các file đã thay đổi
```bash
# git add .
# hoặc add từng file cụ thể, 
git add -A
```

### 3. Commit với amend (cập nhật commit cuối cùng)
```bash
git commit --amend -m "upgrade code"
# git commit --amend -m "Adjust parameters to match the values and names sent from the Front-end"
```

### 4. Push code lên remote (force push vì đã amend)
```bash
#git push origin <tên_nhánh> --force
# hoặc
git push origin feat/ws_L_NhomBenhVaccine_ListByMaChung_handler --force-with-lease
```

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
