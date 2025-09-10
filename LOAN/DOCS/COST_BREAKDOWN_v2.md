# LOAN MANAGEMENT APP (LMA) - COST BREAKDOWN V2
## Tài liệu cơ sở cho hợp đồng outsource - Phiên bản 2 (Chỉ giữ phần chi phí)

---

## 💰 CHI PHÍ DỰ ÁN

### 1. CHI PHÍ HOSTING VÀ INFRASTRUCTURE

| STT | Danh mục | Chi phí | Ghi chú | Khuyến nghị | Sức chứa người dùng |
|-----|----------|---------|---------|-------------|-------------------|
| 1 | **AWS EC2 t3.large (Admin Backend)** | ~$200/tháng | 4 vCPU, 16 GiB RAM, 100 GB gp3 - Thêm tài nguyên để xử lý Application, Export Excel, traffic 20 user Update Form, Status,... | Cân bằng chi phí vs hiệu suất | ~20 admin users |
| 2 | **Database (RDS)** | ~$85-95/tháng | db.t3.medium, Single-AZ, 100 GB gp3 | Lưu trữ dữ liệu khách hàng | Toàn bộ hệ thống |
| 3 | **Apple Developer Program (Organization)** | ~$99/năm | Bắt buộc để publish iOS apps dưới tên công ty. Yêu cầu: D-U-N-S Number, Legal Entity Status, Apple ID với 2FA | Khuyến nghị cho thương hiệu công ty | Unlimited app users |
| 4 | **Google Play Developer Account** | ~$25 (một lần) | Phí một lần để upload Android apps | Bắt buộc cho triển khai Android | Unlimited app users |
| 5 | **Push Notification (Firebase FCM)** | $0 | Free tier có sẵn | Sử dụng free tier ban đầu | Unlimited app users |
| 6 | **Maintenance & Support (10%)** | ~$195/tháng | Bug fixing, updates, working-hour monitoring | Khuyến nghị tối thiểu 12 tháng | Toàn bộ hệ thống |

**Tổng chi phí infrastructure hàng tháng:** ~$480-490/tháng  
**Tổng chi phí infrastructure năm đầu:** ~$5,760-5,880/năm

---

## 📊 COST SUMMARY

### 1. One-time Costs
- **Google Play Developer:** $25
- **Apple Developer Program:** $99
- **Development Setup:** $0 (included)

### 2. Monthly Costs
- **AWS EC2:** $200
- **Database (RDS):** $85-95
- **Maintenance & Support:** $195
- **Firebase FCM:** $0 (free tier)
- **Total Monthly:** $480-490

### 3. Annual Costs
- **Infrastructure:** $5,760-5,880
- **Apple Developer:** $99
- **Total Annual:** $5,859-5,979

---

## 📈 COST COMPARISON V1 vs V2

| Danh mục | V1 (USD/tháng) | V2 (USD/tháng) | Thay đổi |
|----------|----------------|----------------|----------|
| **AWS EC2** | $47 | $200 | +$153 (+325%) |
| **Database** | $0 | $85-95 | +$85-95 (mới) |
| **Maintenance** | $195 | $195 | Không đổi |
| **Tổng cộng** | $242 | $480-490 | +$238-248 (+98-102%) |

**Lý do tăng chi phí:**
- Nâng cấp AWS EC2 từ t3.large (2 vCPU, 8 GiB) lên t3.large (4 vCPU, 16 GiB) để xử lý tốt hơn
- Thêm RDS database riêng biệt để lưu trữ dữ liệu khách hàng
- Hỗ trợ traffic cao hơn với 20 admin users đồng thời
- Tăng khả năng xử lý Excel export và form updates

---

## 📑 PAYMENT MILESTONES (AUD)

| Phase   | Payment % | Amount (AUD) | Condition / Deliverable                                            | Notes                         |
|---------|-----------|--------------|---------------------------------------------------------------------|-------------------------------|
| Phase 1 | 60%       | 2,400        | Agreement on scope & requirements; project kick-off                 | Initial development begins    |
| Phase 2 | 20%       | 800          | 50% progress OR completion of User Management & Loan modules        | Core features in place        |
| Phase 3 | 20%       | 800          | 80% progress and delivery of remaining functionalities              | Final handover, testing & closure |

---

## Addendum (English, concise)

- Clarify scope: Customer record and loan status are managed directly in the Dealer Admin Portal (source of truth), not via lend.com.au.
- New capability: Brokers can update customer profiles and change loan status (e.g., Active → Paid‑off) within the portal.
- Data export: Support exports by status (All/Active/Paid‑off) and by broker or all brokers.
- Notifications: “Request for statement” notifies brokers; status updates trigger in‑app/push alerts to customers.

---

## 🔒 Scope Alignment with Requirements (Concise)

- Source of truth: Customer and loan data are mastered in the Dealer Admin Portal; mobile app integrates and reflects portal updates in real time.
- MVP Core (Phase 1): Authentication, Dashboard (Home), Loan Application & Approval, Repayment Schedule, Repayment Reminder, Push Notifications, Broker Worklist & Filtering, Assignment, Customer Data Management, Loan Status Update, Data Export.
- Phase 2 (Enhancements): Admin Panel, Wallet/Balance view, Advanced reporting, Enhanced notifications, Performance optimizations.

### Currency & Units
- Infrastructure costs: priced in USD (approximate, monthly/annual as listed above).
- Development: priced in AUD (see Budget & Phasing; milestones table also in AUD).

### Development Budget & Phasing (AUD)

| Phase   | Scope (summary)                                                                 | Budget (AUD) |
|---------|----------------------------------------------------------------------------------|--------------|
| Phase 1 | MVP Core features listed above                                                   | 2,400        |
| Phase 2 | Core completion checkpoints (workflows, integration hooks, 50% progress)        | 800          |
| Phase 3 | Advanced & finalization (reminders, admin essentials, export, QA, deploy)       | 800          |

Total Development Budget (MVP): 4,000 AUD

### Key Non-Functional Requirements (from Requirements Document)
- Performance: App launch < 3s, page load < 2s, API < 1s, exports < 30s; real-time updates < 5s.
- Security: End-to-end encryption, secure APIs, RBAC, MFA for sensitive ops, full audit logs.
- Scalability & Reliability: ≥1,000 concurrent users (MVP), 99.5% uptime target, robust sync with portal.
- Integration: Real-time synchronization with Dealer Admin Portal; conflict resolution and retries.

### Assumptions
- Continuous access to Dealer Admin Portal APIs for real-time sync and updates.
- Notification services (Firebase/Email/SMS) credentials provided and configured by partner where needed.
- Data export requirements limited to CSV/Excel by status (All/Active/Paid-off) and by broker/all brokers.

### Out of Scope (for current cost and MVP)
- Document upload/management, advanced document workflows.
- Wallet/payment processing and settlement flows.
- Complex reporting beyond basic exports and listed Phase 2 enhancements.
