# HỢP ĐỒNG GIA CÔNG PHẦN MỀM
## LOAN MANAGEMENT APP (LMA)

---

**Số hợp đồng:** PTN-LMA-2024-001  
**Ngày ký:** [Ngày] tháng [Tháng] năm [Năm]  
**Địa điểm ký:** [Địa điểm]

---

## BÊN A (BÊN THUÊ GIA CÔNG): [TÊN CÔNG TY ĐỐI TÁC]
- **Tên công ty:** [Tên công ty đối tác]
- **Địa chỉ:** [Địa chỉ đầy đủ]
- **Mã số thuế:** [MST]
- **Đại diện:** [Tên đại diện]
- **Chức vụ:** [Chức vụ]
- **Điện thoại:** [SĐT]
- **Email:** [Email]
- **Tài khoản ngân hàng:** [Số tài khoản]

## BÊN B (BÊN GIA CÔNG): CÔNG TY TNHH PT&N SOLUTION
- **Tên công ty:** Công ty TNHH PT&N Solution
- **Địa chỉ:** [Địa chỉ công ty PT&N Solution]
- **Mã số thuế:** [MST]
- **Đại diện:** [Tên đại diện]
- **Chức vụ:** [Chức vụ]
- **Điện thoại:** [SĐT]
- **Email:** [Email]
- **Tài khoản ngân hàng:** [Số tài khoản]

---

## ĐIỀU 1: ĐỊNH NGHĨA VÀ GIẢI THÍCH

### 1.1 Định nghĩa
- **"Dự án"** có nghĩa là Ứng dụng Quản lý Khoản vay (Loan Management App - LMA) được mô tả trong tài liệu kỹ thuật đính kèm.
- **"Giai đoạn 1"** có nghĩa là giai đoạn phát triển các tính năng cơ bản của ứng dụng LMA theo phạm vi công việc đã thỏa thuận.
- **"Yêu cầu phát sinh"** có nghĩa là bất kỳ yêu cầu bổ sung, thay đổi hoặc mở rộng nào ngoài phạm vi công việc ban đầu đã được thỏa thuận.
- **"Deliverables"** có nghĩa là tất cả các sản phẩm, tài liệu và dịch vụ mà Bên B phải cung cấp theo hợp đồng này.
- **"Source Code"** có nghĩa là mã nguồn của phần mềm, bao gồm tất cả các file code, database schema, configuration files và documentation.

### 1.2 Tài liệu tham chiếu
- Tài liệu "COST_BREAKDOWN_AND_REQUIREMENTS.md" được đính kèm và là một phần không tách rời của hợp đồng này.
- Tất cả các yêu cầu kỹ thuật, chi phí và timeline được mô tả trong tài liệu đính kèm sẽ được áp dụng cho hợp đồng này.

---

## ĐIỀU 2: PHẠM VI CÔNG VIỆC

### 2.1 Giai đoạn 1 - Phát triển cơ bản
Bên B sẽ phát triển ứng dụng LMA với các tính năng sau:

#### 2.1.1 Ứng dụng di động đa nền tảng
- **Flutter Framework** cho cross-platform development
- **iOS:** Hỗ trợ iOS 13.0+ (iPhone, iPad)
- **Android:** Hỗ trợ Android 8.0+ (API level 26)
- **Web:** Progressive Web App (PWA) support

#### 2.1.3 Core Features
- **User Account Management**
  - Registration, Login/Logout
  - Password Reset
  - Profile Edit
  - Secure access với dashboard entry point

- **Dashboard (Home)**
  - Loan summary cards
  - Total balance display
  - Active loans count
  - Quick action buttons
  - Central hub showing high-level loan status & actions

- **Loan Application & Approval**
  - Application form
  - Status tracking
  - Document upload (optional)
  - Approval updates
  - Submission + feedback loop
  - UI flow matches Credora style

- **Repayment Schedule**
  - Repayment calendar
  - Upcoming installments
  - Total due display
  - Visual calendar hoặc list user-friendly view
  - Mirror Credora styling

- **Repayment Reminder**
  - Email/SMS reminders
  - Alert banners in dashboard for due dates
  - Keep users on track with due repayment alerts

- **Push Notifications**
  - Loan approval updates
  - Repayment due reminders
  - General alerts
  - Enhances UX, instant feedback to user

- **Admin Panel**
  - User/loan management
  - View status
  - Reports
  - CSV export
  - Dashboard-like view với clear tables/cards

- **Wallet / Balance View**
  - Wallet balance
  - Fund disbursal tracking
  - Transaction history
  - Balance card & transactions (similar to Credora's wallet card)

#### 2.1.4 Integration Requirements
- **Loan APIs** (loan.com.au)
- **Email services**
- **Firebase** cho authentication và analytics

### 2.2 Phạm vi không bao gồm
- **Server Infrastructure:** Bên B không chịu trách nhiệm cung cấp, quản lý hoặc duy trì server infrastructure
- **Third-party Service Costs:** Chi phí các dịch vụ bên thứ ba (ngoài free tier)
- **Domain & SSL:** Bên A tự cung cấp domain và SSL certificate
- **API Keys:** Bên A tự cung cấp các API keys cần thiết

---

## ĐIỀU 3: TIMELINE VÀ MILESTONE

### 3.1 Tổng thời gian dự án: **2,5 tháng**

### 3.2 Các giai đoạn chính:

#### **Phase 1: Project Setup & Core Infrastructure (3 tuần)**
- Thiết lập project structure
- Cài đặt development environment
- Implement Clean Architecture
- Setup CI/CD pipeline
- Database design và migration
- Basic authentication system
- User Account Management (Registration, Login/Logout, Password Reset)

**Deliverables:**
- Project structure hoàn chỉnh
- Development environment setup
- Basic authentication system
- Database schema
- Core infrastructure ready
- User Account Management features

#### **Phase 2: Core Features & Loan Management (4 tuần)**
- Profile Edit và dashboard entry point
- Dashboard (Home) với loan summary cards, total balance, active loans count
- Quick action buttons
- Loan Application & Approval workflow
- Document upload system
- Status tracking
- Approval updates
- Repayment Schedule với calendar view
- Upcoming installments display
- Total due calculation

**Deliverables:**
- Complete dashboard system
- Loan application & approval system
- Repayment schedule functionality
- Document management
- 50% progress completion

#### **Phase 3: Advanced Features & Finalization (3 tuần)**
- Repayment Reminder system (Email/SMS)
- Alert banners in dashboard
- Push Notifications (Firebase FCM)
- Admin Panel với user/loan management
- Reports và CSV export
- Wallet / Balance View
- Fund disbursal tracking
- Transaction history
- Mobile app development
- Responsive web interface
- UI/UX implementation (Credora style)
- Cross-platform testing
- Performance optimization
- Comprehensive testing
- Security testing
- Production deployment
- Documentation

**Deliverables:**
- Complete notification & reminder system
- Admin panel functionality
- Wallet & balance features
- Complete mobile applications
- Web application
- Fully tested application
- Production deployment
- Complete documentation
- 80% progress completion

### 3.3 Milestone Payments

| Phase | Payment % | Amount (AUD) | Condition / Deliverable | Notes |
|-------|-----------|--------------|------------------------|-------|
| Phase 1 | 60% | 1,800 AUD | Agreement on scope & requirements; project kick-off | Initial development begins |
| Phase 2 | 20% | 600 AUD | 50% progress OR completion of User Management & Loan modules | Core features in place |
| Phase 3 | 20% | 600 AUD | 80% progress and delivery of remaining functionalities | Final handover, testing & closure |

---

## ĐIỀU 4: CHI PHÍ VÀ THANH TOÁN

### 4.1 Tổng giá trị hợp đồng: **3,000 AUD**

### 4.2 Chi phí breakdown:

#### **4.2.1 Development Cost: 3,000 AUD**
- Backend development: 1,500 AUD
- Mobile app development: 1,000 AUD
- Web application: 300 AUD
- Integration & testing: 200 AUD

#### **4.2.2 Chi phí không bao gồm trong hợp đồng:**
- **Server Infrastructure:** Bên A tự chịu trách nhiệm
- **Third-party Services:** Ngoài free tier
- **Domain & SSL:** Bên A tự cung cấp
- **API Keys:** Bên A tự cung cấp

### 4.3 Chi phí server (Bên A tự chịu):

| STT | Danh mục | Chi phí | Ghi chú |
|-----|----------|---------|---------|
| 1 | **AWS EC2 t3.large (Admin Backend)** | ~$47/tháng | 2 vCPU, 8 GiB RAM |
| 2 | **Apple Developer Program (Organization)** | ~$99/năm | Bắt buộc cho iOS |
| 3 | **Google Play Developer Account** | ~$25 (một lần) | Bắt buộc cho Android |
| 4 | **Push Notification (Firebase FCM)** | $0 | Free tier |
| 5 | **Maintenance & Support (10%)** | ~$195/tháng | Sau khi bàn giao |

**Tổng chi phí server hàng tháng:** ~$242/tháng  
**Tổng chi phí server năm đầu:** ~$2,904/năm

### 4.4 Phương thức thanh toán:
- **Bank transfer** hoặc **PayPal**
- Thanh toán theo milestone
- Invoice sẽ được gửi trước 7 ngày làm việc
- Thanh toán trong vòng 15 ngày kể từ ngày nhận invoice
- **Late payment fee:** 1.5%/tháng cho các khoản thanh toán quá hạn

### 4.5 Chi phí phát sinh:
- **Yêu cầu thay đổi:** $150/giờ cho development work
- **Additional features:** Báo giá riêng theo complexity
- **Emergency support:** $200/giờ (ngoài giờ làm việc)
- **Training sessions:** $100/giờ

---

## ĐIỀU 5: YÊU CẦU PHÁT SINH

### 5.1 Định nghĩa yêu cầu phát sinh
- Bất kỳ yêu cầu nào ngoài phạm vi công việc ban đầu
- Thay đổi thiết kế sau khi đã approved
- Thêm tính năng mới không có trong specification
- Thay đổi integration requirements

### 5.2 Quy trình xử lý yêu cầu phát sinh
1. **Bên A gửi yêu cầu bằng văn bản**
2. **Bên B phân tích và báo giá trong 3 ngày làm việc**
3. **Bên A xem xét và chấp thuận bằng văn bản**
4. **Bên B thực hiện sau khi nhận được approval**
5. **Thanh toán theo thỏa thuận riêng**

### 5.3 Bảng giá yêu cầu phát sinh
- **Minor changes:** $150/giờ
- **Major features:** Báo giá riêng
- **UI/UX changes:** $120/giờ
- **Backend changes:** $180/giờ
- **Integration work:** $200/giờ

---

## ĐIỀU 6: TRÁCH NHIỆM CỦA CÁC BÊN

### 6.1 Trách nhiệm của Bên A (Bên thuê gia công):

#### 6.1.1 Cung cấp thông tin và tài liệu:
- Cung cấp đầy đủ tài liệu yêu cầu kỹ thuật
- Cung cấp access đến các hệ thống hiện tại (nếu có)
- Cung cấp API keys cho third-party services
- Cung cấp domain và SSL certificate
- Cung cấp email service (SMTP/API)

#### 6.1.2 Hỗ trợ và phản hồi:
- Phản hồi yêu cầu feedback trong vòng 3 ngày làm việc
- Cung cấp test data và user accounts
- Tham gia testing và UAT
- Cung cấp business requirements clarification

#### 6.1.3 Thanh toán:
- Thanh toán đúng hạn theo milestone
- Cung cấp thông tin thanh toán chính xác
- Thông báo sớm nếu có vấn đề về thanh toán

#### 6.1.4 Server Infrastructure:
- Tự chịu trách nhiệm cung cấp và quản lý server
- Đảm bảo server đáp ứng performance requirements
- Cung cấp access cho Bên B để deployment
- Chịu trách nhiệm backup và security của server

### 6.2 Trách nhiệm của Bên B (Bên gia công):

#### 6.2.1 Phát triển phần mềm:
- Phát triển đúng theo yêu cầu kỹ thuật
- Đảm bảo chất lượng code và performance
- Implement security best practices
- Tuân thủ coding standards và conventions

#### 6.2.2 Testing và Quality Assurance:
- Thực hiện unit testing, integration testing
- Performance testing và security testing
- Bug fixing và optimization
- Code review và documentation

#### 6.2.3 Delivery và Support:
- Delivery đúng hạn theo timeline
- Cung cấp source code và documentation
- Training cho team Bên A
- 3 tháng warranty support sau delivery

#### 6.2.4 Communication:
- Báo cáo tiến độ hàng tuần
- Thông báo sớm nếu có delay hoặc issues
- Cung cấp demo và testing environment
- Hỗ trợ troubleshooting

---

## ĐIỀU 7: BẢO MẬT VÀ SỞ HỮU TRÍ TUỆ

### 7.1 Bảo mật thông tin:
- Bên B cam kết bảo mật tuyệt đối thông tin của Bên A
- Không được tiết lộ thông tin cho bên thứ ba
- Implement security measures theo industry standards
- Regular security audits và penetration testing

### 7.2 Sở hữu trí tuệ:
- **Source code** và **documentation** thuộc sở hữu của Bên A sau khi thanh toán đầy đủ
- Bên B được quyền sử dụng **open-source libraries** và **frameworks**
- **Third-party licenses** phải tuân thủ terms of use
- Bên B không được sử dụng code cho dự án khác mà không có sự đồng ý

### 7.3 Confidentiality Agreement:
- Bên B ký NDA riêng biệt
- Thông tin dự án được classify là "Confidential"
- Cam kết không reverse engineering hoặc decompile
- Return tất cả materials sau khi hoàn thành dự án

### 7.4 Work Product:
- Tất cả work product (code, designs, documentation) thuộc về Bên A
- Bên B không được claim ownership hoặc license rights
- Bên B có quyền sử dụng trong portfolio với sự đồng ý của Bên A

---

## ĐIỀU 8: TESTING VÀ ACCEPTANCE

### 8.1 Testing Process:

#### 8.1.1 Development Testing:
- Unit testing với coverage > 80%
- Integration testing cho tất cả APIs
- Performance testing theo requirements
- Security testing và vulnerability scanning

#### 8.1.2 User Acceptance Testing (UAT):
- Bên A thực hiện UAT trong 2 tuần
- Test trên tất cả supported platforms
- Test tất cả features và workflows
- Performance testing với expected load

### 8.2 Acceptance Criteria:

#### 8.2.1 Functional Requirements:
- [ ] Tất cả features hoạt động đúng specification
- [ ] Performance đạt requirements
- [ ] Security requirements được implement
- [ ] Cross-platform compatibility
- [ ] Integration với third-party services

#### 8.2.2 Quality Requirements:
- [ ] Zero critical bugs
- [ ] Code quality standards met
- [ ] Documentation complete
- [ ] User training completed
- [ ] Production deployment successful

### 8.3 Acceptance Process:
1. Bên B deliver final version
2. Bên A có 2 tuần để UAT
3. Báo cáo bugs/issues (nếu có)
4. Bên B fix bugs trong 1 tuần
5. Final acceptance và sign-off

### 8.4 Rejection Process:
- Nếu Bên A reject deliverables, phải nêu rõ lý do
- Bên B có 1 tuần để fix issues
- Nếu vẫn không đạt, có thể terminate hợp đồng
- Chi phí đã thanh toán sẽ được hoàn trả theo tỷ lệ work completed

---

## ĐIỀU 9: WARRANTY VÀ SUPPORT

### 9.1 Warranty Period: **3 tháng** sau delivery

### 9.2 Warranty Coverage:
- **Bug fixing** cho tất cả bugs phát hiện
- **Performance optimization** nếu cần
- **Security updates** và patches
- **Minor enhancements** (không thay đổi scope)

### 9.3 Support Services:
- **Email support** trong 24 giờ
- **Remote support** cho critical issues
- **Documentation updates**
- **Training sessions** nếu cần

### 9.4 Exclusions:
- **Major feature changes** (sẽ tính phí riêng)
- **Third-party service issues**
- **Hardware hoặc infrastructure problems**
- **Issues do Bên A gây ra**

### 9.5 Post-Warranty Support:
- **Maintenance contract:** $195/tháng
- **Emergency support:** $200/giờ
- **Feature updates:** Báo giá riêng
- **Security patches:** $100/giờ

---

## ĐIỀU 10: RỦI RO VÀ BẢO HIỂM

### 10.1 Risk Management:
- **Technical risks:** Backup plans và fallback options
- **Timeline risks:** Buffer time và resource allocation
- **Quality risks:** Comprehensive testing strategy
- **Security risks:** Regular audits và monitoring

### 10.2 Force Majeure:
- **Natural disasters, war, pandemic**
- **Government regulations changes**
- **Third-party service outages**
- **Economic crisis** affecting operations

### 10.3 Mitigation Strategies:
- **Regular communication** và status updates
- **Risk assessment** hàng tuần
- **Contingency plans** cho critical issues
- **Alternative solutions** cho key dependencies

### 10.4 Insurance:
- Bên B có bảo hiểm trách nhiệm nghề nghiệp
- Coverage cho errors và omissions
- Minimum coverage: $1,000,000

---

## ĐIỀU 11: CHẤM DỨT HỢP ĐỒNG

### 11.1 Termination by Mutual Agreement:
- Cả hai bên đồng ý chấm dứt
- Thanh toán theo work completed
- Return tất cả materials và data
- Confidentiality obligations vẫn có hiệu lực

### 11.2 Termination for Breach:
- **Bên A:** Không thanh toán sau 30 ngày notice
- **Bên B:** Không deliver theo timeline sau 15 ngày notice
- **Material breach** của confidentiality agreement
- **Quality issues** không được fix sau 30 ngày

### 11.3 Termination Process:
1. **Written notice** 30 ngày trước
2. **Cure period** 15 ngày (nếu có thể)
3. **Final settlement** trong 30 ngày
4. **Return materials** và data
5. **Confidentiality** obligations continue

### 11.4 Termination Fees:
- **Early termination by Bên A:** 50% của remaining contract value
- **Termination by Bên B:** Hoàn trả 100% của unearned fees
- **Force majeure:** No termination fees

---

## ĐIỀU 12: GIẢI QUYẾT TRANH CHẤP

### 12.1 Negotiation:
- Cố gắng giải quyết qua **direct negotiation**
- **Escalation** lên management level
- **Mediation** nếu cần thiết

### 12.2 Arbitration:
- **Arbitration** theo quy định của Trung tâm Trọng tài Quốc tế Việt Nam
- **Language:** Tiếng Việt
- **Location:** Hà Nội
- **Costs:** Chia đều giữa hai bên

### 12.3 Governing Law:
- **Vietnamese Law** áp dụng
- **Dispute resolution** theo pháp luật Việt Nam
- **Jurisdiction:** Tòa án có thẩm quyền tại Hà Nội

---

## ĐIỀU 13: ĐIỀU KHOẢN CHUNG

### 13.1 Amendment:
- Chỉ được sửa đổi bằng **written agreement**
- **Both parties** phải ký tên
- **Effective date** từ ngày ký

### 13.2 Severability:
- Nếu điều khoản nào **invalid**, các điều khoản khác vẫn có hiệu lực
- **Replacement** với điều khoản hợp lệ tương đương

### 13.3 Entire Agreement:
- Hợp đồng này **supersedes** tất cả agreements trước đó
- **Complete agreement** giữa hai bên
- **No oral modifications** được chấp nhận

### 13.4 Notices:
- **Written notices** gửi qua email và registered mail
- **Effective date:** 3 ngày sau khi gửi
- **Addresses** như trong hợp đồng

### 13.5 Assignment:
- **Không được assign** hợp đồng mà không có written consent
- **Successors** và **assigns** bị ràng buộc bởi hợp đồng

### 13.6 Force Majeure:
- **Excuse performance** trong trường hợp force majeure
- **Notice requirement** trong 48 giờ
- **Mitigation efforts** required

---

## ĐIỀU 14: KÝ KẾT

Hợp đồng này có hiệu lực từ ngày ký và được lập thành **02 (hai) bản** có giá trị pháp lý như nhau, mỗi bên giữ **01 (một) bản**.

**BÊN A (BÊN THUÊ GIA CÔNG)**  
[Tên đại diện]  
[Chức vụ]  
[Ký tên và đóng dấu]

**BÊN B (BÊN GIA CÔNG)**  
[Tên đại diện]  
[Chức vụ]  
[Ký tên và đóng dấu]

---

**Ngày:** [Ngày]  
**Tháng:** [Tháng]  
**Năm:** [Năm]

---

## PHỤ LỤC

### Phụ lục A: Technical Specifications
- Detailed technical requirements
- Architecture diagrams
- Database schema
- API specifications

### Phụ lục B: Project Timeline
- Detailed milestone breakdown
- Resource allocation
- Dependencies và critical path

### Phụ lục C: Cost Breakdown
- Detailed cost analysis
- Third-party service costs
- Infrastructure requirements

### Phụ lục D: Testing Plan
- Test cases và scenarios
- Performance benchmarks
- Security testing procedures

### Phụ lục E: Documentation Requirements
- User manuals
- Technical documentation
- API documentation
- Deployment guides

### Phụ lục F: Server Infrastructure Requirements
- AWS EC2 specifications
- Database requirements
- Security configurations
- Backup procedures

---

**Lưu ý:** Hợp đồng này được soạn thảo dựa trên tài liệu kỹ thuật và yêu cầu chi tiết của dự án Loan Management App. Tất cả các điều khoản đều có thể được điều chỉnh theo thỏa thuận giữa hai bên.

**Công ty TNHH PT&N Solution cam kết cung cấp dịch vụ gia công phần mềm chất lượng cao với giá cả cạnh tranh và hỗ trợ kỹ thuật tận tình.**
