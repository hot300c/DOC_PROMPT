# LOAN MANAGEMENT APP (LMA) - COST BREAKDOWN & REQUIREMENTS V2
## Tài liệu cơ sở cho hợp đồng outsource - Phiên bản 2

---

## 📊 TỔNG QUAN DỰ ÁN

**Tên dự án:** Loan Management App (LMA)  
**Loại dự án:** P2P Lending Platform  
**Mục tiêu:** Phát triển ứng dụng quản lý khoản vay toàn diện  
**Thời gian dự kiến:** 2-3 tháng  

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

### 2. YÊU CẦU TỪ ĐỐI TÁC (KHÔNG TÍNH VÀO CHI PHÍ VENDOR)

| STT | Danh mục | Cung cấp bởi | Ghi chú | Yêu cầu | Tác động chi phí |
|-----|----------|--------------|---------|---------|------------------|
| 1 | **Domain & SSL** | Partner | Cung cấp subdomain (app.company.com) và cấu hình DNS trỏ đến backend server | Phải setup trước khi release app | Không tính vào chi phí vendor |
| 2 | **Email Service (SMTP/API)** | Partner | Cung cấp API key từ email service (SendGrid, Mailgun, AWS SES) | Cần thiết cho gửi transactional emails | Không tính vào chi phí vendor |
| 3 | **License API Key (Lend.com.au)** | Partner | Sandbox API key cho development/testing | Phải có sẵn để tích hợp và test loan workflows | Không tính vào chi phí vendor |

---

## 🎯 YÊU CẦU KỸ THUẬT

### 1. CAPACITY REQUIREMENTS

| Danh mục | Số lượng người dùng | Ghi chú |
|----------|-------------------|---------|
| **Admin Backend** | ~20 admin users | Hệ thống quản lý nội bộ |
| **App Users** | Unlimited | Không giới hạn người dùng ứng dụng |
| **Concurrent Users** | 10,000+ | Hệ thống phải hỗ trợ đồng thời |
| **Daily Applications** | 1,000+ | Xử lý đơn vay mỗi ngày |
| **Hourly Payments** | 5,000+ | Xử lý thanh toán mỗi giờ |

### 2. TECHNICAL SPECIFICATIONS

#### 2.1 Performance Requirements
- **App launch time:** < 3 giây
- **Page load time:** < 2 giây  
- **API response time:** < 1 giây
- **Image upload:** < 30 giây cho file 10MB
- **Payment processing:** < 10 giây

#### 2.2 Scalability Requirements
- **Database storage:** 1TB+ documents
- **Uptime requirement:** 99.9%
- **Concurrent connections:** 10,000+
- **Data processing:** Real-time

#### 2.3 Security Requirements
- **Data encryption:** End-to-end
- **Compliance:** PCI DSS, GDPR
- **Authentication:** Multi-factor
- **Audit logging:** Complete trail

---

## 📱 PLATFORM REQUIREMENTS

### 1. Mobile Platforms
- **iOS:** 13.0+ (iPhone, iPad)
- **Android:** 8.0+ (API level 26)
- **Web:** Progressive Web App (PWA)
- **Cross-platform:** Flutter framework

### 2. Backend Requirements
- **Database:** MySQL/PostgreSQL (RDS)
- **API:** RESTful + GraphQL
- **Authentication:** JWT + OAuth2
- **Real-time:** WebSocket connections

---

## 🔧 INTEGRATION REQUIREMENTS

### 1. Third-Party Services
- **Credit Bureau APIs:** Experian, Equifax, TransUnion
- **Payment Gateways:** Stripe, PayPal, VNPay
- **Banking APIs:** Account verification
- **Document Services:** OCR, verification
- **Communication:** SMS, Email services

### 2. Development Tools
- **Version Control:** Git
- **CI/CD:** Automated deployment
- **Testing:** Unit, Integration, E2E
- **Monitoring:** Performance, Security

---


## 🚀 DEPLOYMENT REQUIREMENTS

### 1. Development Environment
- **Staging:** Pre-production testing
- **Production:** Live environment
- **Backup:** Disaster recovery
- **Monitoring:** 24/7 system health

### 2. Maintenance
- **Bug Fixes:** Immediate response
- **Updates:** Regular releases
- **Security Patches:** Critical updates
- **Performance Optimization:** Continuous improvement

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

## 📝 CONTRACT CONSIDERATIONS

### 1. Payment Structure
- **Development Phase:** Milestone-based payments
- **Maintenance Phase:** Monthly retainer
- **Additional Features:** Time & materials
- **Emergency Support:** Priority response

### 2. Deliverables
- **Source Code:** Complete codebase
- **Documentation:** Technical & user manuals
- **Testing:** Comprehensive test suite
- **Training:** Team knowledge transfer

### 3. Timeline
- **Phase 1:** Project setup (4 weeks)
- **Phase 2:** Core development (12 weeks)
- **Phase 3:** Testing & deployment (4 weeks)
- **Phase 4:** Maintenance (ongoing)

---

## ⚠️ RISK CONSIDERATIONS

### 1. Technical Risks
- **Third-party Dependencies:** API changes, Service outages
- **Scalability:** Performance under load
- **Security:** Data breaches, Vulnerabilities
- **Integration:** Complex system connections

### 2. Business Risks
- **Regulatory Changes:** Compliance updates
- **Market Competition:** Feature differentiation
- **User Adoption:** Market acceptance
- **Economic Factors:** Budget constraints

### 3. Mitigation Strategies
- **Backup Plans:** Alternative solutions
- **Regular Updates:** Security patches
- **Performance Monitoring:** Proactive optimization
- **User Feedback:** Continuous improvement

---

## 📞 NEXT STEPS

### 1. Immediate Actions
- [ ] Review and approve cost breakdown V2
- [ ] Finalize technical requirements
- [ ] Prepare contract documentation
- [ ] Set up project timeline

### 2. Pre-Development
- [ ] Secure third-party API access
- [ ] Set up development environment
- [ ] Establish communication protocols
- [ ] Create project repository

### 3. Development Phase
- [ ] Weekly progress reports
- [ ] Regular milestone reviews
- [ ] Quality assurance testing
- [ ] User acceptance testing

---

## 🔄 VERSION HISTORY

**V1 (Original):** $242/tháng - Basic infrastructure setup
**V2 (Current):** $480-490/tháng - Enhanced infrastructure with dedicated database and improved performance

**Tài liệu này cung cấp cơ sở hoàn chỉnh để tạo hợp đồng outsource cho dự án Loan Management App V2, bao gồm tất cả chi phí cập nhật, yêu cầu kỹ thuật và rủi ro cần xem xét.**
