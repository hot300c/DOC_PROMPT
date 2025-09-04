# GitHub Project Management Guide - MCP Commands

## 📋 Project #6 - Loan Management App Backend

**Repository**: `PNTSOL/LMA_BACKEND`  
**Project URL**: https://github.com/orgs/PNTSOL/projects/6  
**Current Status**: 6 tasks active (all linked to Project #6)

---

## ⚠️ MCP Status Notice

**Current Status**: MCP GitHub Projects server may be temporarily unavailable  
**Last Working**: 2025-09-04  
**Alternative**: ✅ GitHub CLI is working perfectly

---

## 🚀 Quick Commands Reference

### **1. Xem trạng thái Project #6**

```bash
# Xem tất cả tasks trong LMA_BACKEND
gh issue list --repo PNTSOL/LMA_BACKEND --state open

# Xem tasks đã hoàn thành
gh issue list --repo PNTSOL/LMA_BACKEND --state closed

# Xem tất cả tasks (cả open và closed)
gh issue list --repo PNTSOL/LMA_BACKEND
```

### **2. Tạo Task mới**

```bash
# Tạo task mới với title và body
gh issue create --repo PNTSOL/LMA_BACKEND --title "Tên task" --body "Mô tả chi tiết task"

# Ví dụ tạo task với labels
gh issue create --repo PNTSOL/LMA_BACKEND --title "Implement User Authentication" --body "Tạo hệ thống xác thực người dùng" --label enhancement
```

### **3. Cập nhật Task**

```bash
# Cập nhật trạng thái task (open/closed)
gh issue close --repo PNTSOL/LMA_BACKEND 1

# Cập nhật nội dung task
gh issue edit --repo PNTSOL/LMA_BACKEND 1 --body "Nội dung mới"

# Gán assignee cho task
gh issue edit --repo PNTSOL/LMA_BACKEND 1 --add-assignee hot300c
```

### **4. Xem chi tiết Task**

```bash
# Xem chi tiết task cụ thể
gh issue view --repo PNTSOL/LMA_BACKEND 1
```

### **5. Quản lý Project**

```bash
# Xem danh sách projects
gh project list --owner PNTSOL

# Xem chi tiết project
gh project view 6 --owner PNTSOL

# Thêm issue vào project
gh project item-add 6 --owner PNTSOL --url https://github.com/PNTSOL/LMA_BACKEND/issues/1

# Refresh authentication với quyền project
gh auth refresh -s project
```

---

## 📝 Current Tasks Status (Project #6)

### **Active Tasks (6 tasks):**

1. **Issue #1**: "Meeting Notes – Loan Management App (Phase 1)"
   - 🏷️ Label: documentation
   - 👤 Assignee: hot300c
   - 📅 Created: 2025-09-04
   - 🔗 URL: https://github.com/PNTSOL/LMA_BACKEND/issues/1
   - 📋 Project: ✅ Added to Project #6

2. **Issue #2**: "Xây dựng kiến trúc Admin"
   - 🏷️ Label: enhancement
   - 👤 Assignee: hot300c
   - 📅 Created: 2025-09-04
   - 🔗 URL: https://github.com/PNTSOL/LMA_BACKEND/issues/2
   - 📋 Project: ✅ Added to Project #6

3. **Issue #3**: "Dựng bản mô tả đầy đủ các chức năng"
   - 🏷️ Label: documentation
   - 👤 Assignee: hot300c
   - 📅 Created: 2025-09-04
   - 🔗 URL: https://github.com/PNTSOL/LMA_BACKEND/issues/3
   - 📋 Project: ✅ Added to Project #6

4. **Issue #4**: "Tài liệu nghiệp vụ người dùng - chức năng Gửi thông báo"
   - 🏷️ Label: enhancement
   - 👤 Assignee: hot300c
   - 📅 Created: 2025-09-04
   - 🔗 URL: https://github.com/PNTSOL/LMA_BACKEND/issues/4
   - 📋 Project: ✅ Added to Project #6

5. **Issue #5**: "Tài liệu nghiệp vụ người dùng - Chức năng nhắc nợ định kỳ"
   - 🏷️ Label: enhancement
   - 👤 Assignee: hot300c
   - 📅 Created: 2025-09-04
   - 🔗 URL: https://github.com/PNTSOL/LMA_BACKEND/issues/5
   - 📋 Project: ✅ Added to Project #6

6. **Issue #6**: "Xây dựng file JDL để tạo source code thông qua JHipster - Kiến trúc Monolith"
   - 🏷️ Label: enhancement
   - 👤 Assignee: hot300c
   - 📅 Created: 2025-09-04
   - 🔗 URL: https://github.com/PNTSOL/LMA_BACKEND/issues/6
   - 📋 Project: ✅ Added to Project #6

---

## 🎯 Common Use Cases

### **A. Kiểm tra trạng thái project hàng ngày**
```bash
gh issue list --repo PNTSOL/LMA_BACKEND --state open
```

### **B. Tạo task mới cho feature**
```bash
gh issue create --repo PNTSOL/LMA_BACKEND --title "Implement Payment Gateway Integration" --body "Tích hợp cổng thanh toán cho hệ thống loan" --label enhancement
```

### **C. Đánh dấu task hoàn thành**
```bash
gh issue close --repo PNTSOL/LMA_BACKEND 2
```

### **D. Cập nhật tiến độ task**
```bash
gh issue edit --repo PNTSOL/LMA_BACKEND 3 --body "Task đã hoàn thành 50%. Đang implement phần user management..."
```

### **E. Gán task cho team member**
```bash
gh issue edit --repo PNTSOL/LMA_BACKEND 4 --add-assignee username
```

### **F. Thêm task mới vào project**
```bash
# Tạo task mới
gh issue create --repo PNTSOL/LMA_BACKEND --title "New Task" --body "Description"

# Thêm vào project (thay issue_number bằng số thực tế)
gh project item-add 6 --owner PNTSOL --url https://github.com/PNTSOL/LMA_BACKEND/issues/7
```

---

## 📊 Project Statistics

- **Total Tasks**: 6
- **Open Tasks**: 6
- **Closed Tasks**: 0
- **Documentation Tasks**: 2
- **Enhancement Tasks**: 4
- **Assignee**: hot300c (100%)
- **Project Items**: 11 (all issues linked)

---

## 🔧 Troubleshooting

### **Nếu MCP không hoạt động:**
1. **Kiểm tra MCP server status**: Thử lệnh `@mcp_GitHub-Projects-hot300c_get_me`
2. **Restart MCP server**: Có thể cần restart MCP GitHub Projects
3. **Use alternative methods**:
   - GitHub CLI: `gh issue list --repo PNTSOL/LMA_BACKEND`
   - Web interface: https://github.com/PNTSOL/LMA_BACKEND/issues
   - PowerShell script: `github-project-manager-fixed.ps1`

### **Nếu không thêm được issue vào project:**
1. **Refresh authentication**: `gh auth refresh -s project`
2. **Kiểm tra quyền**: Đảm bảo có quyền project trong organization
3. **Kiểm tra project ID**: Sử dụng `gh project list --owner PNTSOL`

### **Nếu không thấy tasks:**
1. Kiểm tra repository name: `LMA_BACKEND`
2. Kiểm tra organization: `PNTSOL`
3. Thử lệnh: `gh issue list --repo PNTSOL/LMA_BACKEND`

### **Nếu không tạo được task:**
1. Kiểm tra quyền truy cập repository
2. Đảm bảo repository tồn tại
3. Kiểm tra format của title và body

### **Nếu không cập nhật được task:**
1. Kiểm tra issue_number có đúng không
2. Đảm bảo task chưa bị đóng
3. Kiểm tra quyền edit

---

## 📞 Quick Help Commands

```bash
# Xem thông tin user hiện tại
gh auth status

# Tìm kiếm repositories trong organization
gh repo list --owner PNTSOL

# Xem project details
gh project view 6 --owner PNTSOL

# List all projects
gh project list --owner PNTSOL
```

---

## 🔄 Alternative Methods

### **GitHub CLI Commands:**
```bash
# List issues
gh issue list --repo PNTSOL/LMA_BACKEND

# Create issue
gh issue create --repo PNTSOL/LMA_BACKEND --title "Task Title" --body "Description"

# Close issue
gh issue close --repo PNTSOL/LMA_BACKEND 1

# Add to project
gh project item-add 6 --owner PNTSOL --url https://github.com/PNTSOL/LMA_BACKEND/issues/1
```

### **PowerShell Script:**
```bash
# Run PowerShell script
.\github-project-manager-fixed.ps1 -Action status
```

---

## 📅 Last Updated: 2025-09-04

**Note**: Sử dụng các lệnh GitHub CLI này để quản lý Project #6 một cách hiệu quả. Tất cả issues đã được liên kết với Project #6. Copy và paste các lệnh vào terminal để thực hiện các thao tác tương ứng.
