## 📋 Project #6 - Loan Management App Backend

**Repository**: `PNTSOL/LMA_BACKEND`
**Project URL**: https://github.com/orgs/PNTSOL/projects/6  
**Git Repo**: https://github.com/PNTSOL/VNVC_DOCS.git


### Cài đặt git cli

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


## ✅ Quy tắc an toàn ký tự & định dạng khi tạo Task/Issue

- **Không dùng emoji/biểu tượng đặc biệt** trong Title (tránh lỗi mã hóa khi dùng PowerShell/CLI). Dùng ASCII thuần: A–Z, 0–9, khoảng trắng, dấu gạch nối.
- **Body** nên là Markdown thuần. Tránh ký tự điều khiển ẩn, copy-paste từ Word/Excel.
- Nếu cần dùng emoji trong body, ưu tiên dán trực tiếp trên GitHub Web sau khi issue đã tạo xong.
- Trên Windows PowerShell, tránh paste tiêu đề có emoji vào tham số `--title`. Nếu bắt buộc, cập nhật lại Title bằng GitHub Web sau khi tạo.
- **Labels**: chỉ gán nhãn đã tồn tại. Nếu `gh` báo "label not found", tạo nhãn trước hoặc bỏ gán nhãn khi tạo.

### Mẫu Title an toàn
- Main: `Task 17: CompanyB2B Management System - Complete Implementation`
- Sub: `Task 17.2: Frontend Implementation - CompanyB2B Management`

### Mẫu Heading trong body
- Dùng `##`, `###` theo Markdown. Không dùng ký tự đặc biệt trong heading.


## 📝 Task Completion Documentation Requirements

### Khi hoàn tất hoặc đóng task/issues, BẮT BUỘC phải có các ghi chú chi tiết:

#### 1. **Giải pháp thực hiện (Solution)**
- Mô tả cách tiếp cận và phương pháp giải quyết
- Các bước thực hiện chính
- Lý do lựa chọn giải pháp này

#### 2. **Kỹ thuật sử dụng (Technical Implementation)**
- Công nghệ, framework, thư viện được sử dụng
- Cấu trúc code, pattern áp dụng
- API endpoints, database schema (nếu có)

#### 3. **Yêu cầu đặc biệt (Special Requirements)**
- Dependencies cần thiết
- Cấu hình môi trường
- Permissions, credentials cần thiết

#### 4. **Các vấn đề gặp phải và cách khắc phục (Issues & Fixes)**
- Bug, lỗi trong quá trình thực hiện
- Cách debug và troubleshoot
- Workarounds tạm thời (nếu có)

#### 5. **Bổ sung và cải tiến (Enhancements)**
- Tính năng mở rộng đã thêm
- Optimizations, performance improvements
- Code refactoring, best practices áp dụng

#### 6. **Testing & Validation**
- Cách test tính năng
- Test cases, scenarios
- Kết quả validation

#### 7. **Deployment & Configuration**
- Hướng dẫn deploy
- Environment variables
- Configuration changes

### 📋 Template ghi chú hoàn tất task:

```
## ✅ Task Completed: [TASK_NAME]

### 🔧 Solution
- [Mô tả giải pháp chính]

### 🛠️ Technical Implementation
- [Chi tiết kỹ thuật]

### ⚙️ Requirements
- [Yêu cầu đặc biệt]

### 🐛 Issues & Fixes
- [Vấn đề và cách khắc phục]

### 🚀 Enhancements
- [Cải tiến đã thực hiện]

### 🧪 Testing
- [Cách test và validate]

### 🚀 Deployment
- [Hướng dẫn deploy]
```

### ⚠️ Lưu ý quan trọng:
- **KHÔNG** đóng task mà không có ghi chú chi tiết
- Ghi chú phải đủ chi tiết để người khác có thể hiểu và tiếp tục phát triển
- Luôn cập nhật documentation khi có thay đổi
- Sử dụng markdown formatting để dễ đọc

## 🆕 Tạo Task/Issues Mới

### Khi tạo task/issues mới, BẮT BUỘC phải có:

#### 1. **Thông tin cơ bản (Basic Information)**
- **Title**: Mô tả ngắn gọn, rõ ràng
- **Description**: Chi tiết yêu cầu, mục tiêu
- **Labels**: Phân loại (bug, feature, enhancement, etc.)
- **Priority**: High, Medium, Low
- **Assignee**: Người thực hiện

#### 2. **Yêu cầu chi tiết (Detailed Requirements)**
- **Acceptance Criteria**: Tiêu chí hoàn thành
- **User Story**: Từ góc độ người dùng
- **Technical Requirements**: Yêu cầu kỹ thuật cụ thể
- **Dependencies**: Task/issues liên quan

#### 3. **Thông tin kỹ thuật (Technical Information)**
- **Component/Module**: Phần nào của hệ thống
- **Technology Stack**: Công nghệ sử dụng
- **API Endpoints**: Nếu có API liên quan
- **Database Changes**: Thay đổi database (nếu có)

#### 4. **Testing & Validation**
- **Test Scenarios**: Các trường hợp test
- **Expected Results**: Kết quả mong đợi
- **Test Data**: Dữ liệu test cần thiết

### 📋 Template tạo task/issues mới:

```
## 🎯 New Task/Issue: [TASK_TITLE]

### 📝 Description
[Chi tiết yêu cầu và mục tiêu]

### 🎯 Acceptance Criteria
- [ ] [Tiêu chí 1]
- [ ] [Tiêu chí 2]
- [ ] [Tiêu chí 3]

### 📖 User Story
As a [user type], I want [functionality] so that [benefit]

### 🛠️ Technical Requirements
- **Component**: [Module/Component name]
- **Technology**: [Tech stack]
- **API**: [Endpoints if applicable]
- **Database**: [Changes if any]

### 🔗 Dependencies
- Depends on: [Task/Issue #]
- Blocks: [Task/Issue #]

### 🧪 Testing
- **Test Scenarios**: [List scenarios]
- **Expected Results**: [Expected outcomes]
- **Test Data**: [Required test data]

### 📊 Priority & Labels
- **Priority**: [High/Medium/Low]
- **Labels**: [bug/feature/enhancement/documentation]
- **Assignee**: [@username]
```

### 🔗 **Mapping vào Project**

#### Bước 1: Tạo Issue/Task
1. Sử dụng template trên để điền đầy đủ thông tin
2. Gán labels và assignee phù hợp

#### Bước 2: Thêm vào Project #8
1. Sử dụng GitHub CLI: `gh project item-add 8 --owner PNTSOL --url https://github.com/PNTSOL/VNVC_DOCS/issues/[ISSUE_NUMBER]`
2. Hoặc click "Add items" hoặc "+" button trên GitHub UI
3. Search và chọn issue/task vừa tạo
4. Drag & drop vào cột phù hợp (To do, In Progress, etc.)

#### Bước 3: Cập nhật Project Status
- **To do**: Task mới tạo, chưa bắt đầu
- **In Progress**: Đang thực hiện
- **In Review**: Đang review code
- **Done**: Hoàn thành (có ghi chú chi tiết)

## 🏗️ **Tạo Sub-Issues (Sub-Tasks)**

### Quy trình tạo Sub-Issues:

#### Khi nào cần tạo Sub-Issues?
- **Bắt buộc** khi task bao gồm từ 2 nhóm công việc độc lập trở lên (ví dụ: Frontend + Backend, hoặc Backend + Database, hoặc kèm theo SQL Scripts/DevOps).
- Khi cần phân công cho nhiều người/nhóm khác nhau.
- Khi cần theo dõi tiến độ chi tiết theo module (FE/BE/DB/QA/Docs).

#### Bước 1: Tạo Main Issue
1. Tạo issue chính với title: `Task [NUMBER]: [MAIN_TASK_NAME] - Complete Implementation`
2. Sử dụng template chuẩn với đầy đủ thông tin
3. Thêm vào Project #8

#### Bước 2: Tạo Sub-Issues
1. Tạo từng sub-issue với title: `Task [NUMBER].[X]: [SUB_TASK_NAME] - [COMPONENT]`
2. Ví dụ: `Task 17.1: Backend Implementation - CompanyB2B Management`
3. Mỗi sub-issue có template riêng phù hợp với component

#### Bước 3: Link Sub-Issues
1. Cập nhật main issue body để thêm checklist sub-issues:
```markdown
## Sub-issues
- [ ] #[NUMBER] [SUB_TASK_NAME]
- [ ] #[NUMBER] [SUB_TASK_NAME]
- [ ] #[NUMBER] [SUB_TASK_NAME]
- [ ] #[NUMBER] [SUB_TASK_NAME]
```

Ghi chú:
- Dùng cú pháp `#[ISSUE_NUMBER]` để GitHub tự nhận diện liên kết.
- Sau khi Sub-Issue đóng, tick checklist trong Main Issue để đồng bộ trạng thái.

#### Bước 4: Map tất cả vào Project
1. Thêm main issue vào Project #8
2. Thêm tất cả sub-issues vào Project #8
3. Cập nhật status phù hợp cho từng issue

### 📋 Template Sub-Issue:

```markdown
# 🎯 Task [NUMBER].[X]: [SUB_TASK_NAME] - [COMPONENT]

## 📝 Description
[Chi tiết yêu cầu cho component cụ thể]

## 🎯 Acceptance Criteria
- [ ] [Tiêu chí 1]
- [ ] [Tiêu chí 2]
- [ ] [Tiêu chí 3]

## 📖 User Story
As a [user type], I want [functionality] so that [benefit]

## 🛠️ Technical Requirements
- **Component**: [Component name]
- **Technology**: [Tech stack]
- **API**: [Endpoints if applicable]
- **Database**: [Changes if any]

## 🔗 Dependencies
- Depends on: [Task/Issue #]
- Blocks: [Task/Issue #]

## 🧪 Testing
- **Test Scenarios**: [List scenarios]
- **Expected Results**: [Expected outcomes]
- **Test Data**: [Required test data]

## 📊 Priority & Labels
- **Priority**: [High/Medium/Low]
- **Labels**: [component-specific labels]
- **Assignee**: [@username]

## 🏗️ Sub-Tasks
[Chi tiết các sub-tasks nếu có]

---

**Parent Issue**: #[NUMBER] - [MAIN_TASK_NAME]
**Repository**: PNTSOL/VNVC_DOCS
**Project**: #8 - VNVC Documentation
```

### ⚠️ Lưu ý khi tạo Sub-Issues:
- **LUÔN** map tất cả issues vào Project #8
- **KHÔNG** tạo task mà không có đủ thông tin
- **KIỂM TRA** dependencies trước khi tạo
- **CẬP NHẬT** project status khi có thay đổi
- **SỬ DỤNG** template chuẩn để đảm bảo consistency
- **LINK** sub-issues với main issue thông qua checklist

## 🔍 Checklist trước khi chạy lệnh tạo Issue (Pre-flight)

- [ ] Title dùng ASCII, không emoji/ký tự đặc biệt.
- [ ] Body soạn sẵn trong file `.md` (Markdown thuần).
- [ ] Labels đã tồn tại (nếu cần gán). Nếu chưa có, tạo sau.
- [ ] Xác định có cần Sub-Issues (FE/BE/DB/QA/Docs) không.
- [ ] Copy sẵn URL Project (#8) để map ngay sau khi tạo.
- [ ] Nếu dùng Windows PowerShell: kiểm tra encoding, hạn chế emoji trong tham số CLI.