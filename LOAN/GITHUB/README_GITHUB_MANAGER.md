# LOAN GitHub Project Manager

Scripts để quản lý GitHub project cho LOAN notification system.

## Yêu cầu

1. **GitHub CLI (gh)** - Cài đặt từ: https://cli.github.com/
2. **Authentication** - Chạy `gh auth login` để đăng nhập
3. **PowerShell** - Đã có sẵn trên Windows

## Cài đặt

1. Cài đặt GitHub CLI:
   ```bash
   winget install GitHub.cli
   ```

2. Đăng nhập GitHub:
   ```bash
   gh auth login
   ```

3. Kiểm tra kết nối:
   ```bash
   gh auth status
   ```

## Sử dụng

### Cách 1: Batch Script (Đơn giản)

```bash
# Xem danh sách projects
loan-git.bat status

# Xem tasks đang in-progress
loan-git.bat inprogress 1

# Thêm task mới
loan-git.bat add "Implement notification service" 1

# Xem project board
loan-git.bat board 1
```

### Cách 2: PowerShell Script (Chi tiết)

```powershell
# Xem danh sách projects
.\github-project-manager.ps1 -Action status

# Xem tasks đang in-progress
.\github-project-manager.ps1 -Action inprogress -ProjectNumber 1

# Thêm task mới
.\github-project-manager.ps1 -Action add -Title "Implement notification service" -ProjectNumber 1

# Xem project board
.\github-project-manager.ps1 -Action board -ProjectNumber 1
```

## Tính năng

### 1. Xem Projects
- Liệt kê tất cả projects trong repository
- Hiển thị project number và URL

### 2. Xem In-Progress Tasks
- Hiển thị tasks đang được thực hiện
- Thông tin assignee và URL

### 3. Thêm Task Mới
- Tạo issue mới trong repository
- Tự động thêm vào project
- Hỗ trợ title và description

### 4. Xem Project Board
- Hiển thị toàn bộ project board
- Nhóm tasks theo status
- Thông tin assignees

## Repository

Mặc định kết nối với: `hot300c/DOC_PROMPT_VNVC`

## Troubleshooting

### Lỗi "GitHub CLI not found"
```bash
# Cài đặt GitHub CLI
winget install GitHub.cli

# Hoặc download từ: https://cli.github.com/
```

### Lỗi "Not authenticated"
```bash
# Đăng nhập lại
gh auth login

# Kiểm tra trạng thái
gh auth status
```

### Lỗi "Execution Policy"
```powershell
# Cho phép chạy PowerShell script
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Workflow Đề Xuất

1. **Hàng ngày**: `loan-git.bat status` để xem projects
2. **Check progress**: `loan-git.bat inprogress [PROJECT_NUMBER]`
3. **Thêm task**: `loan-git.bat add "Task description" [PROJECT_NUMBER]`
4. **Review board**: `loan-git.bat board [PROJECT_NUMBER]`

## Tích hợp với Git

Có thể kết hợp với `git-sync.bat` ở thư mục gốc:

```bash
# Đồng bộ code
cd ..
git-sync.bat

# Quản lý tasks
cd LOAN
loan-git.bat status
```
