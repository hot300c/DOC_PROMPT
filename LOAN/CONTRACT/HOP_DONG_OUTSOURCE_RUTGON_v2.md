# HỢP ĐỒNG GIA CÔNG PHẦN MỀM
## LOAN MANAGEMENT APP (LMA)

---

**Số hợp đồng:** PTN-Dealer-LMA-2025-002
**Ngày ký:** 10 tháng 9 năm 2025  
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

## BÊN B (BÊN GIA CÔNG): CÔNG TY TNHH PT&N COMPANY LIMITED
- **Tên công ty:** PN&T COMPANY LIMITED
- **Địa chỉ:** 0314786024
- **Mã số thuế:** [MST]
- **Đại diện:** Nguyễn Ngô Duy Phúc
- **Chức vụ:** Giám đốc Công nghệ (CTO)
- **Điện thoại:** 0974554565
- **Email:** phucng2001@gmail.com
- **Tên ngân hàng:** Tiên Phong bank
- **Tài khoản ngân hàng:** 0974554565
- **Tên Chủ tài khoản:** NGUYỄN  
---

## ĐIỀU 1: ĐỊNH NGHĨA VÀ GIẢI THÍCH

### 1.1 Định nghĩa
- **"Dự án"** có nghĩa là Ứng dụng Quản lý Khoản vay (Loan Management App - LMA) được mô tả trong tài liệu kỹ thuật đính kèm.
- **"Giai đoạn 1"** có nghĩa là giai đoạn phát triển các tính năng cơ bản của ứng dụng LMA theo phạm vi công việc đã thỏa thuận.
- **"Yêu cầu phát sinh"** có nghĩa là bất kỳ yêu cầu bổ sung, thay đổi hoặc mở rộng nào ngoài phạm vi công việc ban đầu đã được thỏa thuận.
- **"Deliverables"** có nghĩa là tất cả các sản phẩm, tài liệu và dịch vụ mà Bên B phải cung cấp theo hợp đồng này.


### 1.2 Tài liệu tham chiếu
- Tất cả các yêu cầu kỹ thuật, chi phí và timeline được mô tả trong tài liệu đính kèm sẽ được áp dụng cho hợp đồng này.

---

## ĐIỀU 2: PHẠM VI CÔNG VIỆC

### 2.1 Giai đoạn 1 - Phát triển cơ bản
Bên B sẽ phát triển ứng dụng LMA với các tính năng sau:

#### 2.1.1 Ứng dụng di động đa nền tảng
- **Flutter Framework** cho cross-platform development
- **iOS:** Hỗ trợ iOS 13.0+ (iPhone, iPad)
- **Android:** Hỗ trợ Android 8.0+ (API level 26)

#### 2.1.3 Core Features
- **User Account Management**
  - Registration, Login/Logout, Password Reset, Profile Edit
  - Secure access với dashboard entry point

- **Dashboard (Home)**
  - Loan summary cards, Total balance, Active loans count
  - Quick action buttons
  - Central hub showing high-level loan status & actions

- **Loan Application & Approval**
  - Application form, Status tracking, Document upload (optional)
  - Approval updates
  - Submission + feedback loop; UI flow matches Credora style

- **Repayment Schedule & Reminders**
  - Repayment calendar basics, Upcoming installments, Total due overview
  - Email/SMS reminders, Alert banners in dashboard for due dates
  - Keep users on track with due repayment alerts

- **Push Notifications**
  - Loan approval updates, Repayment due reminders, General alerts
  - Enhances UX, instant feedback to user

- **Admin Panel**
  - User/loan management, View status, Reports, CSV export (web-based admin system)
  - Dashboard-like view; clear tables/cards for managing backend

- **Wallet / Balance View**
  - Wallet balance, Fund disbursal tracking, Transaction history
  - Balance card & transactions (similar to Credora's wallet card)

#### 2.1.4 Integration Requirements
- **Dealer Admin Portal**: Đồng bộ dữ liệu real-time (profile, leads, loans), 2 chiều với audit log và xử lý xung đột
- **Loan/Lead APIs** theo yêu cầu nghiệp vụ
- **Email services**
- **Firebase** cho authentication, analytics và push notification (FCM)

### 2.2 Phạm vi không bao gồm
- **Server Infrastructure:** Bên B không chịu trách nhiệm cung cấp, quản lý hoặc duy trì server infrastructure
- **Third-party Service Costs:** Chi phí các dịch vụ bên thứ ba (ngoài free tier)
- **Domain & SSL:** Bên A tự cung cấp domain và SSL certificate
---

## ĐIỀU 3: TIMELINE VÀ MILESTONE

### 3.1 Tổng thời gian dự án: **2,5 tháng**

### 3.2 Các giai đoạn chính:

#### **Project Setup & Core Infrastructure (3 tuần)**
- Thiết lập project structure
- Cài đặt development environment
- Database design và migration
- Basic authentication system
- User Account Management (Registration, Login/Logout, Password Reset)

**Deliverables:**
- Project structure hoàn chỉnh
- Development environment setup
- Basic authentication system
- Database schema
- User Account Management features

#### **Core Features & Loan Management (4 tuần)**
- Profile Edit và dashboard entry point
- Dashboard (Home) với loan summary cards, total balance, active loans count
- Quick action buttons
- Loan Application & Approval workflow
- Document upload system
- Status tracking
- Approval updates
- Upcoming installments display

**Deliverables:**
- Complete dashboard system
- Loan application & approval system
- 50% progress completion

#### **Phase 3: Advanced Features & Finalization (3 tuần)**
- Repayment Reminder system (Email/SMS)
- Alert banners in dashboard
- Push Notifications (Firebase FCM)
- Admin Panel với user/loan management
- Reports và CSV export
- Transaction history
- Mobile app development
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
- Complete mobile applications
- Fully tested application
- Production deployment
- Complete documentation
- 80% progress completion

### 3.3 Milestone Payments (MVP - Version 2)

Tổng giá trị: 4,000 AUD (hoặc USD tương đương theo tỷ giá tại thời điểm xuất hóa đơn)

| Phase | Payment % | Amount (AUD) | Condition / Deliverable | Notes |
|-------|-----------|--------------|-------------------------|-------|
| Phase 1 | 60% | 2,400 AUD | Project setup & core infra; User Account Management; Dashboard; Loan Application cơ bản; Repayment cơ bản; Notifications setup | Nghiệm thu tạm thời |
| Phase 2 | 20% | 800 AUD | Hoàn thiện core workflows: lead/loan status tracking & updates; timeline/progress; integration hooks | Tiến độ 50% |
| Phase 3 | 20% | 800 AUD | Advanced & finalization: reminders, admin panel essentials, CSV export, QA, deployment | Nghiệm thu cuối |

---

## ĐIỀU 4: CHI PHÍ VÀ THANH TOÁN

### 4.1 Tổng giá trị hợp đồng (MVP - Version 2): **4,000 AUD**

### 4.2 Chi phí breakdown:

#### **4.2.1 Development Cost: 4,000 AUD**
- User Account Management & Core App: 3,000 AUD
- Lead/Loan workflows (LeadApplication, LoanApplication), cập nhật trạng thái loan, và quản trị bộ danh mục (picklists/reference data), kèm Export Excel: 1,000 AUD

#### **4.2.2 Chi phí không bao gồm trong hợp đồng:**
- **Server Infrastructure:** Bên A tự chịu trách nhiệm
- **Third-party Services:** Ngoài free tier
- **Domain & SSL:** Bên A tự cung cấp
- **API Keys:** Bên A tự cung cấp

### 4.3 Chi phí hạ tầng (Bên A tự chịu) - Theo Version 2 (USD)

| STT | Danh mục | Chi phí | Ghi chú | Khuyến nghị |
|-----|----------|---------|---------|-------------|
| 1 | **AWS EC2 (Admin Backend)** | ~$200/tháng | 4 vCPU, 16 GiB RAM, 100 GB gp3 | Cân bằng chi phí/hiệu suất |
| 2 | **Database (Amazon RDS - MySQL)** | ~$85-95/tháng | db.t3.medium, Single-AZ, 100 GB gp3 | Lưu trữ dữ liệu khách hàng |
| 3 | **Push Notification (Firebase FCM)** | $0 | Free tier | Bắt đầu với free tier |

**Tổng chi phí hạ tầng hàng tháng:** ~$480-490/tháng  
**Tổng chi phí hạ tầng năm đầu:** ~$5,760-5,880/năm

Các chi phí tài khoản:
- **Apple Developer Program (Organization):** ~$99/năm  
- **Google Play Developer Account:** ~$25 (một lần)

### 4.4 Chi phí vận hành & hỗ trợ (Bên A tự chịu)

| STT | Danh mục | Chi phí | Ghi chú |
|-----|----------|---------|---------|
| 1 | **Maintenance & Support** | $195/tháng | Bug fixing, updates, working-hour monitoring. Khuyến nghị tối thiểu 12 tháng |

**Tổng chi phí vận hành & hỗ trợ:** $195/tháng  
**Tổng chi phí vận hành & hỗ trợ năm đầu:** $2,340/năm

### 4.5 Phương thức thanh toán:
- **Bank transfer** hoặc **PayPal**
- Thanh toán theo milestone
- Invoice sẽ được gửi trước 7 ngày làm việc
- Thanh toán trong vòng 15 ngày kể từ ngày nhận invoice
- **Late payment fee:** 1.5%/tháng cho các khoản thanh toán quá hạn

### 4.6 Chi phí phát sinh:
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
- **Thay đổi UI/UX design:** Nếu Bên A thay đổi design sau khi đã cung cấp, sẽ tính phí phát sinh

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
- **UI/UX redesign:** $150/giờ (thay đổi hoàn toàn design)
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

#### 6.1.2 Cung cấp giao diện và design:
- Cung cấp design files (Figma)
- Cung cấp UI/UX guidelines và style guide
- Cung cấp assets (icons, images, fonts, colors)
- Cung cấp responsive design cho mobile và web
- Phê duyệt mockups và prototypes trước khi development

#### 6.1.3 Hỗ trợ và phản hồi:
- Phản hồi yêu cầu feedback trong vòng 3 ngày làm việc
- Cung cấp test data và user accounts
- Tham gia testing và UAT
- Cung cấp business requirements clarification

#### 6.1.4 Thanh toán:
- Thanh toán đúng hạn theo milestone
- Cung cấp thông tin thanh toán chính xác
- Thông báo sớm nếu có vấn đề về thanh toán

#### 6.1.5 Server Infrastructure:
- Tự chịu trách nhiệm cung cấp và quản lý server
- Đảm bảo server đáp ứng performance requirements
- Cung cấp access cho Bên B để deployment
- Chịu trách nhiệm backup và security của server

### 6.2 Trách nhiệm của Bên B (Bên gia công):

#### 6.2.1 Phát triển phần mềm:
- Phát triển đúng theo yêu cầu kỹ thuật
- Implement UI/UX theo design Bên A cung cấp
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
- Cung cấp documentation và user manuals
- Training cho team Bên A
- 3 tháng warranty support sau delivery
- **Lưu ý:** Source code không được bàn giao theo thỏa thuận

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
- **Source code** thuộc sở hữu của Bên B và không được bàn giao
- **Documentation** và **user manuals** thuộc sở hữu của Bên A sau khi thanh toán đầy đủ
- Bên B được quyền sử dụng **open-source libraries** và **frameworks**
- **Third-party licenses** phải tuân thủ terms of use


### 7.3 Confidentiality Agreement:
- Bên B ký NDA riêng biệt
- Thông tin dự án được classify là "Confidential"
- Cam kết không reverse engineering hoặc decompile
- Return tất cả materials sau khi hoàn thành dự án

### 7.4 Work Product:
- **Source code** thuộc sở hữu của Bên B
- **Documentation** và **user manuals** thuộc về Bên A

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

### 10.1 Quản lý rủi ro:
- **Rủi ro kỹ thuật:** Có phương án dự phòng và giải pháp thay thế
- **Rủi ro tiến độ:** Dự phòng thời gian và phân bổ nguồn lực hợp lý
- **Rủi ro chất lượng:** Áp dụng chiến lược kiểm thử toàn diện
- **Rủi ro bảo mật:** Kiểm tra, đánh giá bảo mật và giám sát thường xuyên

### 10.2 Bất khả kháng:
- **Thiên tai, chiến tranh, đại dịch**
- **Thay đổi quy định của nhà nước**
- **Sự cố dịch vụ bên thứ ba**
- **Khủng hoảng kinh tế** ảnh hưởng đến hoạt động

### 10.3 Chiến lược giảm thiểu rủi ro:
- **Giao tiếp thường xuyên** và cập nhật tiến độ
- **Đánh giá rủi ro** hàng tuần
- **Kế hoạch dự phòng** cho các vấn đề nghiêm trọng
- **Giải pháp thay thế** cho các phụ thuộc quan trọng

### 10.4 Bảo hiểm:
- Bên B có bảo hiểm trách nhiệm nghề nghiệp
- Bảo hiểm bao gồm lỗi và thiếu sót
- Mức bảo hiểm tối thiểu: $1,000,000

---

## ĐIỀU 11: CHẤM DỨT HỢP ĐỒNG

### 11.1 Chấm dứt theo thỏa thuận:
- Hai bên cùng đồng ý chấm dứt hợp đồng
- Thanh toán dựa trên khối lượng công việc đã hoàn thành
- Trả lại toàn bộ tài liệu và dữ liệu
- Nghĩa vụ bảo mật vẫn tiếp tục có hiệu lực

### 11.2 Chấm dứt do vi phạm:
- **Bên A:** Không thanh toán sau 30 ngày kể từ khi nhận được thông báo
- **Bên B:** Không bàn giao đúng tiến độ sau 15 ngày kể từ khi nhận được thông báo
- **Vi phạm nghiêm trọng** nghĩa vụ bảo mật thông tin
- **Vấn đề chất lượng** không được khắc phục sau 30 ngày

### 11.3 Quy trình chấm dứt hợp đồng:
1. **Thông báo bằng văn bản** trước 30 ngày
2. **Thời gian khắc phục** là 15 ngày (nếu có thể)
3. **Thanh toán, quyết toán cuối cùng** trong vòng 30 ngày
4. **Trả lại tài liệu** và dữ liệu
5. **Nghĩa vụ bảo mật** tiếp tục có hiệu lực

### 11.4 Phí chấm dứt hợp đồng:
- **Bên A chấm dứt sớm:** Phải thanh toán 50% giá trị hợp đồng còn lại
- **Bên B chấm dứt:** Hoàn trả 100% phần phí chưa thực hiện
- **Trường hợp bất khả kháng:** Không áp dụng phí chấm dứt

---

## ĐIỀU 12: GIẢI QUYẾT TRANH CHẤP

### 12.1 Thương lượng:
- Nỗ lực giải quyết thông qua **thương lượng trực tiếp**
- **Chuyển cấp** lên ban lãnh đạo nếu cần
- **Hòa giải** nếu không đạt được thỏa thuận

### 12.2 Trọng tài:
- **Trọng tài** theo quy định của Trung tâm Trọng tài Quốc tế Việt Nam (VIAC)
- **Ngôn ngữ:** Tiếng Việt
- **Địa điểm:** Hồ Chí Minh
- **Chi phí:** Hai bên chia đều

### 12.3 Luật điều chỉnh:
- **Luật Việt Nam** được áp dụng
- **Giải quyết tranh chấp** theo quy định pháp luật Việt Nam
- **Thẩm quyền:** Tòa án có thẩm quyền tại Hồ Chí Minh

---

## ĐIỀU 13: ĐIỀU KHOẢN CHUNG

### 13.1 Sửa đổi hợp đồng:
- Mọi sửa đổi, bổ sung hợp đồng chỉ có giá trị khi được lập thành văn bản.
- Hai bên phải cùng ký tên xác nhận vào văn bản sửa đổi.
- Thời điểm hiệu lực của sửa đổi là từ ngày ký văn bản đó.

### 13.2 Hiệu lực từng điều khoản:
- Nếu bất kỳ điều khoản nào của hợp đồng này bị tuyên bố vô hiệu, các điều khoản còn lại vẫn giữ nguyên hiệu lực.
- Các bên sẽ thay thế điều khoản vô hiệu bằng một điều khoản hợp lệ có giá trị tương đương.

### 13.3 Toàn bộ thỏa thuận:
- Hợp đồng này thay thế tất cả các thỏa thuận, cam kết trước đây giữa hai bên liên quan đến nội dung hợp đồng.
- Đây là thỏa thuận đầy đủ và duy nhất giữa hai bên về nội dung hợp đồng này.
- Mọi sửa đổi miệng đều không có giá trị pháp lý.

### 13.4 Thông báo:
- Mọi thông báo liên quan đến hợp đồng phải được thực hiện bằng văn bản, gửi qua email và thư bảo đảm.
- Thời điểm thông báo có hiệu lực là sau 3 ngày kể từ ngày gửi.
- Địa chỉ nhận thông báo là địa chỉ ghi trong hợp đồng này.

### 13.5 Chuyển nhượng:
- Không bên nào được chuyển nhượng hợp đồng này cho bên thứ ba nếu không có sự đồng ý bằng văn bản của bên còn lại.
- Người kế thừa và bên nhận chuyển nhượng (nếu có) phải tuân thủ các điều khoản của hợp đồng này.

### 13.6 Bất khả kháng:
- Các bên được miễn trừ trách nhiệm thực hiện nghĩa vụ hợp đồng trong trường hợp xảy ra sự kiện bất khả kháng.
- Bên gặp sự kiện bất khả kháng phải thông báo cho bên còn lại trong vòng 48 giờ kể từ khi xảy ra sự kiện.
- Các bên phải nỗ lực tối đa để giảm thiểu thiệt hại và khắc phục hậu quả do sự kiện bất khả kháng gây ra.

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

### Phụ lục A: Architecture Diagrams
- System architecture overview
- Architecture diagram (tham chiếu: `LOAN/diagram/diagram-export-10-09-2025-14_42_42.png`)

### Phụ lục B: Cost Breakdown
- Detailed cost analysis
- Third-party service costs
- Infrastructure requirements

### Phụ lục C: User Manuals
- Ghi chú: Cung cấp gần giai đoạn triển khai
- Phạm vi: User guide (mobile app), Admin guide (web-based admin)
- Định dạng: PDF (tiếng Việt/tiếng Anh theo thỏa thuận)

---

**Lưu ý:** Hợp đồng này được soạn thảo dựa trên tài liệu kỹ thuật và yêu cầu chi tiết của dự án Loan Management App. Tất cả các điều khoản đều có thể được điều chỉnh theo thỏa thuận giữa hai bên.

**Công ty TNHH PT&N Solution cam kết cung cấp dịch vụ gia công phần mềm chất lượng cao với giá cả cạnh tranh và hỗ trợ kỹ thuật tận tình.**
