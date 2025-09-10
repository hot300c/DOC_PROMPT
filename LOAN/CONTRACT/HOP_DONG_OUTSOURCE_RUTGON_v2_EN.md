# SOFTWARE OUTSOURCING CONTRACT
## LOAN MANAGEMENT APP (LMA)

---

**Contract No.:** PTN-Dealer-LMA-2025-002
**Date:** September 10, 2025  
**Place of Signing:** [Location]

---

## PARTY A (HIRING PARTY): [PARTNER COMPANY NAME]
- **Company name:** [Partner company name]
- **Address:** [Full address]
- **Tax ID:** [Tax ID]
- **Representative:** [Representative name]
- **Position:** [Position]
- **Phone:** [Phone]
- **Email:** [Email]
- **Bank account:** [Account number]

## PARTY B (OUTSOURCING PROVIDER): PT&N COMPANY LIMITED
- **Company name:** PN&T COMPANY LIMITED
- **Address:** 0314786024
- **Tax ID:** [Tax ID]
- **Representative:** Nguyen Ngo Duy Phuc
- **Position:** Chief Technology Officer (CTO)
- **Phone:** +84 974 554 565
- **Email:** phucng2001@gmail.com
- **Bank name:** Tien Phong Bank
- **Bank account:** 0974554565
- **Account holder name:** NGUYEN  
---

## ARTICLE 1: DEFINITIONS AND INTERPRETATION

### 1.1 Definitions
- "Project" means the Loan Management App (LMA) described in the attached technical documentation.
- "Phase 1" means the development of core features within the agreed scope.
- "Change Request" means any additional, modified, or expanded request outside the original scope agreed by the parties.
- "Deliverables" means all products, documents, and services that Party B must provide under this Contract.


### 1.2 Reference Documents
- All technical requirements, costs, and timelines described in the attached documentation apply to this Contract.

---

## ARTICLE 2: SCOPE OF WORK

### 2.1 Phase 1 – Core Development
Party B will develop the LMA with the following features:

#### 2.1.1 Cross-Platform Mobile Application
- **Flutter Framework** for cross-platform development
- **iOS:** Support iOS 13.0+ (iPhone, iPad)
- **Android:** Support Android 8.0+ (API level 26)

#### 2.1.3 Core Features
- **User Account Management**
  - Registration, Login/Logout, Password Reset, Profile Edit
  - Secure access with a dashboard entry point

- **Dashboard (Home)**
  - Loan summary cards, Total balance, Active loans count
  - Quick action buttons
  - Central hub showing high-level loan status & actions

- **Loan Application & Approval**
  - Application form, Status tracking, Optional document upload
  - Approval updates
  - Submission + feedback loop; UI flow follows Credora style

- **Repayment Schedule & Reminders**
  - Basic repayment calendar, Upcoming installments, Total due overview
  - Email/SMS reminders, Dashboard alert banners for due dates
  - Keep users on track with due repayment alerts

- **Push Notifications**
  - Loan approval updates, Repayment due reminders, General alerts
  - Enhances UX, instant feedback to users

- **Admin Panel**
  - User/loan management, Status view, Reports, CSV export (web-based admin system)
  - Dashboard-like view; clear tables/cards for backend management

- **Wallet / Balance View**
  - Wallet balance, Fund disbursal tracking, Transaction history
  - Balance card & transactions (similar to Credora's wallet card)

#### 2.1.4 Integration Requirements
- **Dealer Admin Portal**: Real-time data sync (profile, leads, loans), bidirectional with audit log and conflict handling
- **Loan/Lead APIs** as per business requirements
- **Email services**
- **Firebase** for authentication, analytics, and push notifications (FCM)

### 2.2 Out of Scope
- **Server Infrastructure:** Party B does not provide/manage/maintain server infrastructure
- **Third-party Service Costs:** Costs of third-party services (beyond free tier)
- **Domain & SSL:** Provided by Party A

---

## ARTICLE 3: TIMELINE AND MILESTONES

### 3.1 Total Project Duration: **2.5 months**

### 3.2 Main Phases:

#### Project Setup & Core Infrastructure (3 weeks)
- Project structure setup
- Development environment setup
- Database design and migration
- Basic authentication system
- User Account Management (Registration, Login/Logout, Password Reset)

**Deliverables:**
- Completed project structure
- Development environment setup
- Basic authentication system
- Database schema
- User Account Management features

#### Core Features & Loan Management (4 weeks)
- Profile Edit and dashboard entry point
- Dashboard (Home) with loan summary cards, total balance, active loans count
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

#### Phase 3: Advanced Features & Finalization (3 weeks)
- Repayment Reminder system (Email/SMS)
- Alert banners in dashboard
- Push Notifications (Firebase FCM)
- Admin Panel with user/loan management
- Reports and CSV export
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

Total value: 4,000 AUD (or USD equivalent at the invoice exchange rate)

| Phase | Payment % | Amount (AUD) | Condition / Deliverable | Notes |
|-------|-----------|--------------|-------------------------|-------|
| Phase 1 | 60% | 2,400 AUD | Project setup & core infra; User Account Management; Dashboard; basic Loan Application; basic Repayment; Notifications setup | Interim acceptance |
| Phase 2 | 20% | 800 AUD | Complete core workflows: lead/loan status tracking & updates; timeline/progress; integration hooks | 50% progress |
| Phase 3 | 20% | 800 AUD | Advanced & finalization: reminders, admin panel essentials, CSV export, QA, deployment | Final acceptance |

---

## ARTICLE 4: COSTS AND PAYMENTS

### 4.1 Total Contract Value (MVP - Version 2): **4,000 AUD**

### 4.2 Cost Breakdown:

#### 4.2.1 Development Cost: 4,000 AUD
- User Account Management & Core App: 3,000 AUD
- Lead/Loan workflows (LeadApplication, LoanApplication), loan status updates, and admin catalogs (picklists/reference data), plus Excel export: 1,000 AUD

#### 4.2.2 Excluded Costs:
- **Server Infrastructure:** Provided by Party A
- **Third-party Services:** Beyond free tier
- **Domain & SSL:** Provided by Party A
- **API Keys:** Provided by Party A

### 4.3 Infrastructure Costs (borne by Party A) – Version 2 (USD)

| No. | Category | Cost | Notes | Recommendation |
|-----|----------|------|-------|----------------|
| 1 | **AWS EC2 (Admin Backend)** | ~$200/month | 4 vCPU, 16 GiB RAM, 100 GB gp3 | Cost/performance balance |
| 2 | **Database (Amazon RDS - MySQL)** | ~$85-95/month | db.t3.medium, Single-AZ, 100 GB gp3 | Customer data storage |
| 3 | **Push Notification (Firebase FCM)** | $0 | Free tier | Start with free tier |

Monthly infra total: ~$480-490/month  
First-year infra total: ~$5,760-5,880/year

Account-related costs:
- **Apple Developer Program (Organization):** ~$99/year  
- **Google Play Developer Account:** ~$25 (one-time)

### 4.4 Operations & Support Costs (borne by Party A)

| No. | Category | Cost | Notes |
|-----|----------|------|-------|
| 1 | **Maintenance & Support** | $195/month | Bug fixing, updates, working-hour monitoring. Recommended minimum 12 months |

Monthly O&M total: $195/month  
First-year O&M total: $2,340/year

### 4.5 Payment Method:
- **Bank transfer** or **PayPal**
- Milestone-based payments
- Invoice issued 7 business days in advance
- Payment due within 15 days of invoice date
- **Late payment fee:** 1.5%/month for overdue payments

### 4.6 Additional Charges:
- **Change requests:** $150/hour for development work
- **Additional features:** Quoted based on complexity
- **Emergency support:** $200/hour (off-hours)
- **Training sessions:** $100/hour

---

## ARTICLE 5: CHANGE REQUESTS

### 5.1 Definition
- Any request outside the original scope
- Design changes after approval
- New features not in the specification
- Changes to integration requirements
- **UI/UX changes:** If Party A changes design after delivery, additional fees apply

### 5.2 Process
1. **Party A submits a written request**
2. **Party B analyzes and quotes within 3 business days**
3. **Party A reviews and approves in writing**
4. **Party B executes after receiving approval**
5. **Payment per separate agreement**

### 5.3 Pricing
- **Minor changes:** $150/hour
- **Major features:** Quoted separately
- **UI/UX changes:** $120/hour
- **UI/UX redesign:** $150/hour (complete redesign)
- **Backend changes:** $180/hour
- **Integration work:** $200/hour

---

## ARTICLE 6: RESPONSIBILITIES OF THE PARTIES

### 6.1 Party A (Hiring Party)

#### 6.1.1 Provide information and documents:
- Provide full technical requirements
- Provide access to existing systems (if any)
- Provide API keys for third-party services
- Provide domain and SSL certificate
- Provide email service (SMTP/API)

#### 6.1.2 Provide UI/UX design:
- Provide design files (Figma)
- Provide UI/UX guidelines and style guide
- Provide assets (icons, images, fonts, colors)
- Provide responsive design for mobile and web (admin)
- Approve mockups and prototypes before development

#### 6.1.3 Support & feedback:
- Respond to feedback within 3 business days
- Provide test data and user accounts
- Participate in testing and UAT
- Provide business requirement clarifications

#### 6.1.4 Payments:
- Pay on time per milestones
- Provide accurate payment information
- Notify promptly if payment issues arise

#### 6.1.5 Server Infrastructure:
- Responsible for providing and managing server
- Ensure server meets performance requirements
- Provide access to Party B for deployment
- Responsible for backups and security

### 6.2 Party B (Outsourcing Provider)

#### 6.2.1 Software Development:
- Develop according to technical requirements
- Implement UI/UX per Party A's design
- Ensure code quality and performance
- Implement security best practices
- Comply with coding standards and conventions

#### 6.2.2 Testing & Quality Assurance:
- Perform unit testing and integration testing
- Performance testing per requirements
- Security testing and vulnerability scanning
- Bug fixing and optimization
- Code review and documentation

#### 6.2.3 Delivery & Support:
- Deliver on time per timeline
- Provide documentation and user manuals
- Train Party A's team
- 3 months warranty support after delivery
- Note: **Source code is not handed over** under this agreement

#### 6.2.4 Communication:
- Weekly progress reports
- Early notice for delays or issues
- Provide demo and testing environment
- Support troubleshooting

---

## ARTICLE 7: CONFIDENTIALITY AND INTELLECTUAL PROPERTY

### 7.1 Confidentiality:
- Party B commits to strict confidentiality of Party A's information
- No disclosure to third parties
- Implement security measures per industry standards
- Regular security audits and penetration testing

### 7.2 Intellectual Property:
- **Source code** is owned by Party B and is not handed over
- **Documentation** and **user manuals** are owned by Party A upon full payment
- Party B may use **open-source libraries** and **frameworks**
- **Third-party licenses** must comply with terms of use

### 7.3 Confidentiality Agreement:
- Separate NDA to be signed by Party B
- Project information classified as "Confidential"
- No reverse engineering or decompilation
- Return all materials upon project completion

### 7.4 Work Product:
- **Source code** is owned by Party B
- **Documentation** and **user manuals** are owned by Party A

---

## ARTICLE 8: TESTING AND ACCEPTANCE

### 8.1 Testing Process:

#### 8.1.1 Development Testing:
- Unit testing with coverage > 80%
- Integration testing for all APIs
- Performance testing per requirements
- Security testing and vulnerability scanning

#### 8.1.2 User Acceptance Testing (UAT):
- Party A conducts UAT within 2 weeks
- Test on all supported platforms
- Test all features and workflows
- Performance testing under expected load

### 8.2 Acceptance Criteria:

#### 8.2.1 Functional Requirements:
- [ ] All features function per specification
- [ ] Performance meets requirements
- [ ] Security requirements implemented
- [ ] Cross-platform compatibility
- [ ] Integration with third-party services

#### 8.2.2 Quality Requirements:
- [ ] Zero critical bugs
- [ ] Code quality standards met
- [ ] Documentation complete
- [ ] User training completed
- [ ] Production deployment successful

### 8.3 Acceptance Process:
1. Party B delivers final version
2. Party A has 2 weeks for UAT
3. Report bugs/issues (if any)
4. Party B fixes within 1 week
5. Final acceptance and sign-off

### 8.4 Rejection Process:
- If Party A rejects deliverables, reasons must be specified
- Party B has 1 week to fix issues
- If still not acceptable, the Contract may be terminated
- Fees paid will be refunded proportionally to work completed

---

## ARTICLE 9: WARRANTY AND SUPPORT

### 9.1 Warranty Period: **3 months** after delivery

### 9.2 Warranty Coverage:
- **Bug fixing** for all discovered bugs
- **Performance optimization** if needed
- **Security updates** and patches
- **Minor enhancements** (no scope changes)

### 9.3 Support Services:
- **Email support** within 24 hours
- **Remote support** for critical issues
- **Documentation updates**
- **Training sessions** if needed

### 9.4 Exclusions:
- **Major feature changes** (charged separately)
- **Third-party service issues**
- **Hardware or infrastructure problems**
- **Issues caused by Party A**

### 9.5 Post-Warranty Support:
- **Maintenance contract:** $195/month
- **Emergency support:** $200/hour
- **Feature updates:** Quoted separately
- **Security patches:** $100/hour

---

## ARTICLE 10: RISKS AND INSURANCE

### 10.1 Risk Management:
- **Technical risks:** Backup plans and fallback options
- **Timeline risks:** Buffer time and resource allocation
- **Quality risks:** Comprehensive testing strategy
- **Security risks:** Regular audits and monitoring

### 10.2 Force Majeure:
- **Natural disasters, war, pandemic**
- **Government regulation changes**
- **Third-party service outages**
- **Economic crises** affecting operations

### 10.3 Mitigation Strategies:
- **Regular communication** and status updates
- **Weekly risk assessment**
- **Contingency plans** for critical issues
- **Alternative solutions** for key dependencies

### 10.4 Insurance:
- Party B carries professional liability insurance
- Coverage for errors and omissions
- Minimum coverage: $1,000,000

---

## ARTICLE 11: TERMINATION

### 11.1 Termination by Mutual Agreement:
- Both parties agree to terminate
- Payment per work completed
- Return all materials and data
- Confidentiality obligations remain in effect

### 11.2 Termination for Breach:
- **Party A:** Non-payment after 30 days' notice
- **Party B:** Failure to deliver per timeline after 15 days' notice
- **Material breach** of confidentiality
- **Quality issues** not fixed within 30 days

### 11.3 Termination Process:
1. **Written notice** 30 days in advance
2. **Cure period** 15 days (if applicable)
3. **Final settlement** within 30 days
4. **Return materials** and data
5. **Confidentiality** obligations continue

### 11.4 Termination Fees:
- **Early termination by Party A:** 50% of remaining contract value
- **Termination by Party B:** 100% refund of unearned fees
- **Force majeure:** No termination fees

---

## ARTICLE 12: DISPUTE RESOLUTION

### 12.1 Negotiation:
- Attempt to resolve via **direct negotiation**
- **Escalation** to management if needed
- **Mediation** if necessary

### 12.2 Arbitration:
- **Arbitration** under VIAC rules
- **Language:** Vietnamese
- **Location:** Ho Chi Minh City
- **Costs:** Shared equally by both parties

### 12.3 Governing Law:
- **Vietnamese Law** applies
- **Dispute resolution** per Vietnamese legal provisions
- **Jurisdiction:** Courts with jurisdiction in Ho Chi Minh City

---

## ARTICLE 13: GENERAL PROVISIONS

### 13.1 Amendment:
- Any amendment/addendum is valid only when made in writing.
- Both parties must sign the amendment document.
- Effective from the date of signature.

### 13.2 Severability:
- If any provision is deemed invalid, the remaining provisions remain effective.
- The parties will replace the invalid provision with a valid, equivalent provision.

### 13.3 Entire Agreement:
- This Contract supersedes all prior agreements and commitments between the parties on the contents herein.
- This is the full and only agreement between the parties on the contents herein.
- Oral amendments have no legal effect.

### 13.4 Notices:
- All notices must be in writing, sent via email and registered mail.
- Notices become effective 3 days after sending.
- Notice addresses are those stated in this Contract.

### 13.5 Assignment:
- Neither party may assign this Contract to a third party without written consent from the other party.
- Successors and assignees (if any) must comply with this Contract.

### 13.6 Force Majeure:
- Parties are excused from performance in the event of force majeure.
- The affected party must notify the other within 48 hours of the event.
- Parties shall use best efforts to mitigate damages and remedy consequences.

---

## ARTICLE 14: SIGNATURES

This Contract is effective from the signing date and made in **02 (two) copies** of equal legal validity, each party keeps **01 (one) copy**.

**PARTY A (HIRING PARTY)**  
[Representative name]  
[Position]  
[Signature & Seal]

**PARTY B (OUTSOURCING PROVIDER)**  
[Representative name]  
[Position]  
[Signature & Seal]

---

**Date:** [Day]  
**Month:** [Month]  
**Year:** [Year]

---

## ANNEXES

### Annex A: Architecture Diagrams
- System architecture overview
- Architecture diagram (reference: `LOAN/diagram/diagram-export-10-09-2025-14_42_42.png`)

### Annex B: Cost Breakdown
- Detailed cost analysis
- Third-party service costs
- Infrastructure requirements

### Annex C: User Manuals
- Note: To be delivered near the deployment stage
- Scope: User guide (mobile app), Admin guide (web-based admin)
- Format: PDF (Vietnamese/English as agreed)

---

**Note:** This Contract is drafted based on the technical documentation and detailed requirements of the Loan Management App project. All clauses may be adjusted by mutual agreement of the parties.

**PT&N Solution is committed to providing high-quality software outsourcing services at competitive prices with dedicated technical support.**


