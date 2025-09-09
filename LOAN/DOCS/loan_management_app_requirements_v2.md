# Loan Management App - User Requirements Document

## 1. Executive Summary

### 1.1 Project Overview
The Loan Management App is a comprehensive mobile application designed to streamline both lead management and loan management processes for brokers and customers. The app serves multiple user types including customers, brokers, and administrators, providing a secure, efficient, and user-friendly platform for lead capture, loan application, tracking, and management. The system integrates seamlessly with the existing Dealer Admin Portal to maintain data consistency and provide a unified experience.

### 1.2 Business Objectives
- **Streamline Lead Management**: Efficiently capture and manage customer leads from initial contact to loan application
- **Streamline Loan Processing**: Reduce loan application and approval processing time
- **Improve Broker Efficiency**: Provide brokers with efficient tools for lead and loan management
- **Enhance Customer Experience**: Provide real-time lead and loan status tracking with comprehensive notifications
- **Reduce Manual Work**: Automate lead processing, loan status updates, and notifications
- **Ensure Data Accuracy**: Maintain single source of truth through Dealer Admin Portal integration
- **Optimize Conversion**: Convert leads to successful loan applications through streamlined processes

### 1.3 Success Metrics
- Loan application completion rate: > 85%
- Customer satisfaction score: > 4.5/5
- Average loan processing time: < 24 hours
- Broker productivity improvement: > 30%
- System uptime: > 99.5%

## 2. User Personas

### 2.1 Primary Users

#### 2.1.1 Customer (Borrower/LeadApplication)
**Profile**: Individual seeking loans through broker network, can be either a new lead application or existing customer
**Goals**:
- Submit loan inquiries and applications easily
- Track lead application and loan application status in real-time
- Receive timely notifications about status updates
- View repayment schedules and due dates
- Access loan application information and history
- Complete profile information efficiently

**Pain Points**:
- Lack of transparency in lead application and loan application status
- Difficulty tracking application progress
- Poor communication from brokers
- Complex repayment tracking
- Repetitive form filling for lead application capture

#### 2.1.2 Broker
**Profile**: Loan broker managing lead applications, customer applications and loan applications
**Goals**:
- Efficiently manage lead applications and convert them to loan applications
- Track and update lead application and loan application statuses
- Access comprehensive customer information quickly
- Export data for reporting and analysis
- Communicate with customers effectively
- Manage workload and lead application assignments

**Pain Points**:
- Manual data entry and lead application processing
- Difficulty managing multiple lead applications and loan applications
- Lack of centralized customer information
- Time-consuming status updates
- Poor lead application qualification and scoring
- Inefficient lead application assignment processes

#### 2.1.3 Administrator
**Profile**: System administrator managing the platform and data integration
**Goals**:
- Monitor system performance and usage
- Manage user accounts and permissions
- Generate comprehensive reports and analytics
- Configure system settings and integrations
- Ensure data integrity and synchronization
- Monitor lead application and loan application processing metrics

**Pain Points**:
- Complex system administration
- Limited reporting capabilities
- User management overhead
- Data synchronization issues
- Integration monitoring complexity

## 3. Functional Requirements

### 3.1 Authentication & User Management

#### 3.1.1 User Registration and Login
**REQ-AUTH-001**: Customer Registration
- Users can register using email/phone and password
- Email/phone verification required (OTP)
- Profile completion with personal information
- Integration with Dealer Admin Portal for customer data

**REQ-AUTH-002**: Broker Authentication
- Secure broker login with role-based access
- Multi-factor authentication for sensitive operations
- Session management and timeout
- Integration with existing broker credentials

**REQ-AUTH-003**: Password Management
- Password reset functionality
- Strong password requirements
- Account lockout after failed attempts
- Secure password storage

#### 3.1.2 Profile Management
**REQ-PROF-001**: Customer Profile
- Personal information (name, address, contact details)
- Employment and income information
- Bank account details
- Profile picture upload
- Integration with Dealer Admin Portal data

**REQ-PROF-002**: Profile Updates
- Real-time profile updates
- Broker can edit customer information
- Changes persist to master data
- Audit trail for profile changes

### 3.2 Dashboard & Navigation

#### 3.2.1 Customer Dashboard
**REQ-DASH-001**: Home Dashboard
- Loan summary cards showing active loans
- Total balance display
- Active loans count
- Quick action buttons for common tasks
- Navigation to key features

**REQ-DASH-002**: Loan Status Overview
- Visual loan status indicators
- Recent activity feed
- Upcoming payment reminders
- Quick access to loan details

#### 3.2.2 Broker Dashboard
**REQ-BROKER-001**: Broker Worklist
- Default pending queue view
- Filter by status (Approved/Assigned to me)
- Case assignment functionality
- Customer data management interface

### 3.3 LeadApplication Management

#### 3.3.1 Lead Capture & Processing
**REQ-LEAD-001**: LeadApplication Creation
- Capture lead application information from multiple sources (web forms, phone calls, referrals)
- Support both Consumer and Commercial lead application types
- Real-time lead application validation and data quality checks
- Integration with external lead sources (Google Ads, Facebook, etc.)
- Automatic lead application assignment to brokers based on criteria

**REQ-LEAD-002**: LeadApplication Information Management
- Comprehensive lead application profile with personal, employment, and financial details
- Support for multiple addresses and employment history
- Asset finance information for commercial lead applications
- Marketing attribution tracking (UTM parameters, Google Analytics)
- Lead application notes and communication history

**REQ-LEAD-003**: LeadApplication Status Management
- Lead application status workflow: NEW → IN_PROGRESS → PENDING_INFO → SUBMITTED → APPROVED → DECLINED → WITHDRAWN
- Status change notifications to relevant parties
- Lead application status history and audit trail
- Automatic status updates based on actions
- Lead application conversion tracking to loan applications

#### 3.3.2 LeadApplication Qualification & Assessment
**REQ-LEAD-004**: LeadApplication Scoring
- Automated lead application scoring based on predefined criteria
- Risk assessment for lead application qualification
- Priority assignment for lead application follow-up
- Lead application quality indicators and metrics

**REQ-LEAD-005**: LeadApplication Assignment
- Automatic broker assignment based on lead application type, location, or capacity
- Manual lead application reassignment capabilities
- Broker workload balancing
- Lead application assignment history tracking

### 3.4 LoanApplication Management

#### 3.4.1 LoanApplication Process
**REQ-LOAN-001**: LoanApplication Creation
- Streamlined loan application form
- Integration with Dealer Admin Portal
- Real-time form validation
- Loan application submission and confirmation

**REQ-LOAN-002**: LoanApplication Status Tracking
- Real-time loan application status updates
- Status change notifications
- Timeline view of loan application progress
- Communication history with brokers

#### 3.4.2 LoanApplication Status Management
**REQ-STATUS-001**: LoanApplication Status Updates
- Broker can update loan application status (Active → Paid-off)
- Automatic customer notifications
- Status change audit trail
- Integration with Dealer Admin Portal

### 3.5 Repayment Management

#### 3.5.1 Repayment Schedule
**REQ-REPAY-001**: Schedule Display
- Visual repayment calendar
- Upcoming installments list
- Total amount due display
- Payment history tracking

**REQ-REPAY-002**: Payment Reminders
- Email/SMS reminders for due dates
- Dashboard alert banners
- Configurable reminder settings
- Escalation for overdue payments

### 3.6 Communication & Notifications

#### 3.6.1 Push Notifications
**REQ-NOTIFY-001**: System Notifications
- Loan approval updates
- Repayment due reminders
- Status change notifications
- General system alerts

**REQ-NOTIFY-002**: In-App Notifications
- Dashboard notification banners
- Notification center
- Read/unread status tracking
- Notification history

### 3.7 Data Management & Reporting

#### 3.7.1 Data Export
**REQ-EXPORT-001**: Export Functionality
- CSV/Excel export by status (All/Active/Paid-off)
- Export by broker or all brokers
- Filtered data export
- Scheduled report generation

#### 3.7.2 Admin Panel
**REQ-ADMIN-001**: Administrative Functions
- User and loan management
- System status monitoring
- Report generation
- Configuration management

## 4. Non-Functional Requirements

### 4.1 Performance Requirements

#### 4.1.1 Response Time
**REQ-PERF-001**: Application Performance
- App launch time: < 3 seconds
- Page load time: < 2 seconds
- API response time: < 1 second
- Real-time updates: < 5 seconds
- Data export: < 30 seconds

#### 4.1.2 Scalability
**REQ-SCALE-001**: System Capacity
- Support 1,000+ concurrent users
- Handle 500+ loan applications per day
- Process 1,000+ status updates per hour
- 99.5% uptime requirement

### 4.2 Security Requirements

#### 4.2.1 Data Protection
**REQ-SEC-001**: Data Security
- End-to-end encryption for sensitive data
- Secure API communication
- Regular security audits
- Compliance with financial data standards
- Secure integration with Dealer Admin Portal

#### 4.2.2 Access Control
**REQ-SEC-002**: Authentication Security
- Role-based access control
- Session timeout and management
- Audit trail for all actions
- Secure broker authentication

### 4.3 Usability Requirements

#### 4.3.1 User Interface
**REQ-UI-001**: Design Standards
- Modern, intuitive interface design
- Consistent with Credora styling
- Mobile-first responsive design
- Accessibility compliance
- Multi-language support

#### 4.3.2 User Experience
**REQ-UX-001**: Ease of Use
- Intuitive navigation
- Clear error messages
- Offline functionality for critical features
- Progressive web app capabilities
- Consistent user journey flows

### 4.4 Integration Requirements

#### 4.4.1 System Integration
**REQ-INTEG-001**: Dealer Admin Portal Integration
- Real-time data synchronization for customer profiles, leads, and loans
- Single source of truth for customer data with master-slave architecture
- Bi-directional data updates with conflict resolution
- API-based integration with RESTful endpoints
- Data mapping and transformation between systems
- Error handling and retry mechanisms for failed synchronizations
- Audit logging for all integration activities
- Data validation and integrity checks before synchronization

**REQ-INTEG-002**: LeadApplication Data Integration
- Automatic lead application import from Dealer Admin Portal
- Lead application status synchronization between systems
- Customer profile updates from portal changes
- Lead application assignment and broker information sync
- Marketing attribution data integration

**REQ-INTEG-003**: LoanApplication Data Integration
- Loan application status synchronization
- Customer loan application history import
- Repayment schedule and payment data sync
- Loan application document and attachment integration
- Financial data and calculation synchronization

#### 4.4.2 Third-Party Services
**REQ-INTEG-004**: External Services
- SMS/email notification services (Twilio, SendGrid)
- Push notification providers (Firebase, OneSignal)
- Data export services (CSV, Excel, PDF generation)
- Authentication services (OAuth, JWT)
- Payment gateway integration (for future payment processing)
- Document management services (for loan documents)
- Analytics and tracking services (Google Analytics, marketing attribution)

## 5. Technical Requirements

### 5.1 Platform Requirements

#### 5.1.1 Mobile Platforms
**REQ-PLAT-001**: Device Support
- iOS 13.0 and above
- Android 8.0 (API level 26) and above
- Progressive Web App (PWA) support
- Cross-platform consistency
- Tablet support

#### 5.1.2 Backend Integration
**REQ-BACKEND-001**: API Architecture
- RESTful API design
- Real-time WebSocket connections
- API versioning and backward compatibility
- Rate limiting and throttling
- Secure API authentication

### 5.2 Data Management

#### 5.2.1 Data Synchronization
**REQ-SYNC-001**: Data Management
- Real-time synchronization with Dealer Admin Portal
- Offline data caching for critical functionality
- Conflict resolution strategies with last-write-wins and manual resolution
- Data backup and recovery with point-in-time restoration
- Comprehensive audit logging for all data changes
- Data versioning and change tracking
- Incremental synchronization to minimize bandwidth usage

#### 5.2.2 Database Requirements
**REQ-DB-001**: Database Architecture
- MySQL database with JPA/Hibernate ORM
- Support for complex relationships between leads, customers, and loans
- Optimized indexing for lead and loan queries
- Data partitioning for large datasets
- Connection pooling and performance optimization
- Database replication for high availability

**REQ-DB-002**: Data Models
- Lead application management entities (LeadApplication, LeadOwner, LeadAssetFinance, etc.)
- Customer profile management (CustomerProfile, DeviceToken)
- Loan application management entities (LoanApplication, RepaymentSchedule, Payment)
- Notification system entities (NotificationCampaign, NotificationDelivery)
- Audit and logging entities (ApiAuditLog, LeadStatusHistory)
- Picklist and reference data entities (Industry, ProductType, etc.)

## 6. User Stories

### 6.1 Customer User Stories

#### 6.1.1 LeadApplication Submission
**As a potential customer, I want to:**
- Submit my loan inquiry through the mobile app
- Provide my personal and financial information easily
- Track my lead application status and progress
- Receive updates about my inquiry

**Acceptance Criteria:**
- Lead application form is intuitive and easy to complete
- Information is validated in real-time
- Lead application status is clearly communicated
- Follow-up communications are timely

#### 6.1.2 LoanApplication Management
**As a customer, I want to:**
- Apply for a loan through the mobile app
- Track my loan application status in real-time
- Receive notifications about status changes
- View my loan application details and repayment schedule

**Acceptance Criteria:**
- Loan application form is easy to complete
- Status updates are real-time and accurate
- Notifications are timely and informative
- Loan application information is clearly displayed

#### 6.1.3 Repayment Management
**As a customer, I want to:**
- View my repayment schedule
- Receive reminders for upcoming payments
- Track my payment history
- Access loan information anytime

**Acceptance Criteria:**
- Repayment schedule is clear and accurate
- Reminders are sent at appropriate times
- Payment history is complete
- Information is easily accessible

### 6.2 Broker User Stories

#### 6.2.1 LeadApplication Management
**As a broker, I want to:**
- View and manage my assigned lead applications
- Update lead application information and status
- Convert lead applications to loan applications
- Track lead application conversion metrics

**Acceptance Criteria:**
- Lead application worklist is organized and efficient
- Lead application data can be updated easily
- Lead application status updates are tracked
- Conversion tracking is accurate

#### 6.2.2 LoanApplication Management
**As a broker, I want to:**
- View and manage my assigned loan applications
- Update customer information
- Change loan application statuses
- Export data for reporting

**Acceptance Criteria:**
- Worklist is organized and efficient
- Customer data can be updated easily
- Status updates trigger customer notifications
- Export functionality works correctly

#### 6.2.3 Customer Communication
**As a broker, I want to:**
- Access customer information quickly
- Update customer profiles
- Track communication history
- Manage multiple cases efficiently

**Acceptance Criteria:**
- Customer information is easily accessible
- Profile updates are saved correctly
- Communication history is maintained
- Case management is streamlined

### 6.3 Administrator User Stories

#### 6.3.1 System Management
**As an administrator, I want to:**
- Monitor system performance
- Manage user accounts
- Generate reports
- Configure system settings

**Acceptance Criteria:**
- System monitoring is comprehensive
- User management is efficient
- Reports are accurate and timely
- Configuration is flexible

## 7. Acceptance Criteria

### 7.1 Functional Acceptance Criteria

#### 7.1.1 Core Functionality
- [ ] Users can register and authenticate successfully
- [ ] Loan applications can be submitted and tracked
- [ ] Brokers can manage customer data and loan statuses
- [ ] Notifications are sent appropriately
- [ ] Data export functionality works correctly

#### 7.1.2 User Experience
- [ ] App is intuitive and easy to navigate
- [ ] All features work on supported devices
- [ ] Performance meets specified requirements
- [ ] Error handling is user-friendly
- [ ] Integration with Dealer Admin Portal is seamless

### 7.2 Non-Functional Acceptance Criteria

#### 7.2.1 Performance
- [ ] Response times meet specified requirements
- [ ] System can handle expected load
- [ ] Real-time updates work correctly
- [ ] Data synchronization is reliable
- [ ] App performance is consistent

#### 7.2.2 Security
- [ ] All security requirements are implemented
- [ ] Data is encrypted appropriately
- [ ] Authentication is secure
- [ ] Audit logging is complete
- [ ] Integration security is maintained

## 8. Implementation Phases

### 8.1 Phase 1 (MVP) - Core Features
**Budget: 4,000 AUD**
- User Account Management (3,000 AUD)
- Dashboard (Home)
- Loan Application & Approval
- Repayment Schedule
- Repayment Reminder
- Push Notifications
- Broker Worklist & Filtering (1,000 AUD)
- Assignment
- Customer Data Management
- Loan Status Update
- Data Export

### 8.2 Phase 2 (MVP) - Enhanced Features
- Admin Panel
- Wallet / Balance View
- Advanced reporting
- Enhanced notifications
- Performance optimizations

## 9. Constraints and Assumptions

### 9.1 Technical Constraints
- Must integrate with existing Dealer Admin Portal
- Limited to mobile platforms initially
- Must maintain data consistency across systems
- Budget constraints for development phases
- Timeline constraints for MVP delivery

### 9.2 Business Constraints
- Must comply with financial regulations
- Limited to broker network initially
- Must support existing customer base
- Budget limitations for development
- Resource constraints for testing

### 9.3 Assumptions
- Users have basic smartphone literacy
- Internet connectivity is generally available
- Dealer Admin Portal integration is stable
- Users are willing to provide personal information
- Third-party services are reliable

## 10. Risk Assessment

### 10.1 Technical Risks
- **Integration Failures**: Plan for fallback mechanisms with Dealer Admin Portal
- **System Performance Issues**: Conduct thorough performance testing
- **Data Synchronization Problems**: Implement robust conflict resolution
- **Security Vulnerabilities**: Implement comprehensive security measures

### 10.2 Business Risks
- **User Adoption**: Conduct user research and testing
- **Broker Workflow Disruption**: Ensure smooth transition
- **Data Accuracy**: Maintain single source of truth
- **Regulatory Compliance**: Monitor regulatory requirements

### 10.3 Mitigation Strategies
- Regular integration testing with Dealer Admin Portal
- Comprehensive user acceptance testing
- Phased rollout approach
- Continuous monitoring and feedback collection
- Regular security audits and updates

## 11. Out of Scope Features

### 11.1 Excluded Features
- Document upload functionality
- Data import capabilities
- Wallet/payment processing
- Advanced document management
- Complex reporting features (beyond basic export)

### 11.2 Future Considerations
- Document management system
- Advanced analytics and reporting
- Payment gateway integration
- Enhanced customer communication tools
- Advanced workflow automation

This user requirements document provides a comprehensive foundation for developing a successful loan management application that meets the needs of customers, brokers, and administrators while ensuring seamless integration with the existing Dealer Admin Portal system.
