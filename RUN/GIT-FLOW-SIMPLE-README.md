# Git Flow Simple - Hướng dẫn sử dụng

Script đơn giản để tự động hóa Git Flow theo quy trình fast-forward merge.

## 📁 Files

- `git-flow-simple.ps1` - PowerShell script chính
- `git-flow-simple.bat` - Batch script để chạy
- `GIT-FLOW-SIMPLE-README.md` - File hướng dẫn này

## 🚀 Cách sử dụng

### 1. Tạo Feature Mới (Commit lần đầu)

```bash
# Tạo feature mới với branch name và commit message
.\git-flow-simple.bat -NewFeature feature/login "Add login feature"

# Script sẽ tự động:
# - Update main branch
# - Tạo branch mới từ main
# - Add tất cả changes
# - Commit lần đầu tiên
```

### 2. Tiếp Tục Feature (Commit --amend)

```bash
# Tiếp tục feature hiện tại với commit message mới
.\git-flow-simple.bat -ContinueFeature "Fix login bug"

# Script sẽ tự động:
# - Add tất cả changes
# - Amend commit (không tạo commit mới)
```

### 3. Push Branch

```bash
# Push branch lên remote
.\git-flow-simple.bat -Push

# Script sẽ tự động:
# - Force push nếu branch đã tồn tại
# - Normal push nếu branch mới
```

### 4. Rebase với Main

```bash
# Rebase branch hiện tại với main
.\git-flow-simple.bat -Rebase

# Script sẽ tự động:
# - Fetch latest changes từ main
# - Rebase branch hiện tại
```

## 📋 Quy trình đầy đủ

### Feature Mới

```bash
# 1. Làm thay đổi và add files
git add -p

# 2. Tạo feature mới
.\git-flow-simple.bat -NewFeature feature/my-feature "Initial implementation"

# 3. Push branch
.\git-flow-simple.bat -Push

# 4. Tạo Merge Request trên GitLab
```

### Tiếp Tục Feature

```bash
# 1. Làm thay đổi và add files
git add -p

# 2. Tiếp tục feature
.\git-flow-simple.bat -ContinueFeature "Fix bugs"

# 3. Force push
.\git-flow-simple.bat -Push
```

### Cập Nhật từ Main

```bash
# 1. Rebase với main
.\git-flow-simple.bat -Rebase

# 2. Force push sau khi rebase
.\git-flow-simple.bat -Push
```

## ⚙️ Parameters

| Parameter         | Type   | Description                           |
| ----------------- | ------ | ------------------------------------- |
| `BranchName`      | string | Tên branch (chỉ dùng với -NewFeature) |
| `CommitMessage`   | string | Message cho commit                    |
| `NewFeature`      | switch | Tạo feature mới (commit lần đầu)      |
| `ContinueFeature` | switch | Tiếp tục feature (commit --amend)     |
| `Push`            | switch | Push branch lên remote                |
| `Rebase`          | switch | Rebase với main                       |
| `ShowHelp`        | switch | Hiển thị help message                 |

## 🔧 Tính năng

Script sẽ tự động:

1. ✅ Kiểm tra Git installation và repository
2. ✅ Update main branch trước khi tạo feature mới
3. ✅ Tạo branch mới từ main đã được update
4. ✅ Add tất cả changes
5. ✅ Commit lần đầu cho feature mới
6. ✅ Amend commit cho feature cũ
7. ✅ Push branch (force push nếu cần)
8. ✅ Rebase với main
9. ✅ Hướng dẫn next steps

## 🛠️ Requirements

- Windows 10/11
- PowerShell 5.1+
- Git 2.0+
- Git repository với remote origin

## 🚨 Troubleshooting

### Lỗi Git không được install

Tải và cài đặt Git từ: https://git-scm.com/

### Lỗi Rebase Conflict

Nếu gặp conflict khi rebase:

1. Resolve conflicts trong files
2. `git add <resolved-files>`
3. `git rebase --continue`
4. Hoặc `git rebase --abort` để cancel

### Lỗi Force Push

Force push sẽ overwrite remote branch. Chỉ dùng sau khi rebase hoặc khi chắc chắn.

## 💡 Tips

- **Feature mới**: Luôn dùng `-NewFeature` với branch name và message
- **Feature cũ**: Luôn dùng `-ContinueFeature` với message mới
- **Push**: Script sẽ tự động force push nếu cần
- **Rebase**: Luôn rebase trước khi push để tránh conflict

## 📞 Support

Nếu gặp vấn đề, hãy kiểm tra:

1. PowerShell execution policy
2. Git installation
3. Đảm bảo chạy script từ git repository
4. Kiểm tra remote origin đã setup chưa
