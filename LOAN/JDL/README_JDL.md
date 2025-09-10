# LOAN 3-Application Architecture JDL

This folder contains a JHipster JDL to generate 3 applications in a single file:
1. **Notification Service** (Microservice) - Notifications & reminders
2. **Loan Management Service** (Microservice) - Core business logic
3. **Gateway** (Gateway) - User Management + NextJS frontend

## Sources Analyzed

Derived from:
- https://github.com/PNTSOL/LMA_BACKEND/issues/7: unique email as login, Google sign-in metadata, registered vs. guest users.
- https://github.com/PNTSOL/LMA_BACKEND/issues/4: campaigns, multi-channel (Email | Push | In-app), templates, activation, send-now flows, history logging, device tokens with platform.
- https://github.com/PNTSOL/LMA_BACKEND/issues/5: daily scheduled reminder before due date, configurable schedule and limits, template caching, logging history.

## Model Overview

Key enums:
- `NotificationChannel`: EMAIL, PUSH, IN_APP
- `SendStatus`: PENDING, SUCCESS, FAILED
- `Platform`: ANDROID, IOS, WEB
- `AudienceType`: REGISTERED, UNREGISTERED
- `LeadStatus`: NEW, IN_PROGRESS, PENDING_INFO, SUBMITTED, APPROVED, DECLINED, WITHDRAWN
- `LoanStatus`: PENDING, APPROVED, ACTIVE, PAID_OFF, DEFAULTED, CANCELLED
- `PaymentStatus`: PENDING, PAID, OVERDUE, PARTIAL
- `PaymentMethod`: BANK_TRANSFER, CASH, CHEQUE, CARD
- `LoanType`: PERSONAL, BUSINESS, MORTGAGE, AUTO, EQUIPMENT
- `InterestType`: FIXED, VARIABLE

Key entities and relations:
- `CustomerProfile` 1–1 `User` (JHipster built-in user), holds profile and registration markers.
- `DeviceToken` many per `CustomerProfile`, stores device/platform and optional email/username/loanCode snapshots to detect registration per rules.
- `Broker` manages lead applications and loan applications.
- `LeadApplication` core lead data with comprehensive customer information and status tracking.
- `LoanApplication` created from approved LeadApplication with contract details and snapshot data.
- `RepaymentSchedule` and `Payment` entities for loan management.
- `NotificationCampaign` with activation flags per channel and template fields per channel, 1–many `NotificationBatch`.
- `NotificationBatch` groups sends using specific content.
- `NotificationDelivery` stores per-send record with recipient snapshots and channel/status.
- `ReminderConfig` stores scheduler parameters (enabled, run time, daysBeforeDue, maxReminders).
- `ReminderHistory` stores reminder sends with template snapshots, linked to `CustomerProfile` and `NotificationCampaign`.

See `loan-management-application.jdl` for full spec.

## Generation Instructions

### Single JDL File with 3 Applications
```bash
jhipster import-jdl loan-management-application.jdl
jhipster import-jdl C:\PROJECTS\DOCS_PROMPT\LOAN\JDL\loan-management-application.jdl
```

This will generate 3 applications:
1. **notificationService** (Microservice, Port 8083)
2. **loanManagementService** (Microservice, Port 8082)
3. **loanGateway** (Gateway with NextJS Frontend, Port 8080)

Notes:
- **Notification Service**: `skipClient true` - Backend-only microservice
- **Loan Management Service**: `skipClient true` - Backend-only microservice
- **Gateway Service**: `skipClient false` - Gateway with NextJS frontend
- Authentication set to `jwt` by default; adjust if using OAuth2
- Database defaults to MySQL for all applications
- Service Discovery: Consul for all applications
- Each application runs on its own port

## Database Configuration

### Development Environment
Each application will use its own MySQL database:
- **Notification Service**: `notification_service` database
- **Loan Management Service**: `loan_management_service` database  
- **Gateway**: `loan_gateway` database

Default connection strings:
```
jdbc:mysql://localhost:3306/notification_service?useUnicode=true&characterEncoding=utf8&useSSL=false&useLegacyDatetimeCode=false&serverTimezone=UTC&createDatabaseIfNotExist=true

jdbc:mysql://localhost:3306/loan_management_service?useUnicode=true&characterEncoding=utf8&useSSL=false&useLegacyDatetimeCode=false&serverTimezone=UTC&createDatabaseIfNotExist=true

jdbc:mysql://localhost:3306/loan_gateway?useUnicode=true&characterEncoding=utf8&useSSL=false&useLegacyDatetimeCode=false&serverTimezone=UTC&createDatabaseIfNotExist=true
```

### Production Environment
For production deployment with Docker, use separate MySQL containers:
```
jdbc:mysql://mysql-notification:3306/notification_service?useUnicode=true&characterEncoding=utf8&useSSL=true&serverTimezone=UTC

jdbc:mysql://mysql-loan:3306/loan_management_service?useUnicode=true&characterEncoding=utf8&useSSL=true&serverTimezone=UTC

jdbc:mysql://mysql-gateway:3306/loan_gateway?useUnicode=true&characterEncoding=utf8&useSSL=true&serverTimezone=UTC
```

### Custom Database Configuration
You can override database settings by modifying the generated `application.yml` files in each service:
- `src/main/resources/config/application-dev.yml` (Development)
- `src/main/resources/config/application-prod.yml` (Production)

## 3-Application Architecture

### Application Overview:

#### 1. **Notification Service** (`notificationService`)
- **Type**: Microservice (Backend-only)
- **Port**: 8083
- **Frontend**: None (separate)
- **Entities**: Notification-related entities
  - NotificationCampaign, NotificationContent, NotificationBatch, NotificationDelivery, NotificationContentVariant
  - ReminderConfig, ReminderHistory, ApiAuditLog
- **Responsibility**: Notifications, reminders, campaign management

#### 2. **Loan Management Service** (`loanManagementService`)
- **Type**: Microservice (Backend-only)
- **Port**: 8082
- **Frontend**: None (separate)
- **Entities**: All core business entities
  - CustomerProfile, DeviceToken, Broker
  - LeadApplication, LeadOwner, LeadOwnerEmployment, LeadOwnerIncome, LeadOwnerAddress, LeadAssetFinance, LeadMarketing, LeadNote, CommercialProfile, LeadStatusHistory, LeadRevision
  - LoanApplication, RepaymentSchedule, Payment
  - Industry, LoanPurpose, LoanTerm, OwnerType, HomeOwnerOption, ProductType, EquipmentType, Occupation, EmploymentType
- **Responsibility**: Core business logic, lead/loan processing, reference data

#### 3. **Gateway** (`loanGateway`)
- **Type**: Gateway with Frontend
- **Port**: 8080
- **Frontend**: NextJS (included)
- **Entities**: All entities (for routing and orchestration)
- **Responsibility**: User Management, API Gateway, Frontend, Service orchestration

### Application Communication:
- **Gateway** → **Loan Management Service**: REST API calls for business operations
- **Gateway** → **Notification Service**: REST API calls for sending notifications
- **Service Discovery**: Consul for service registration and discovery
- **JWT Token Propagation**: Secure inter-service communication
- **Database Separation**: Each application has its own database
- **Independent Deployment**: Applications can be deployed separately

### Benefits of 3-Application Architecture:
- **Clear Separation**: Business logic vs. notification logic vs. gateway
- **Scalability**: Each service can be scaled independently
- **Technology Flexibility**: Different services can use different technologies
- **Frontend Integration**: Gateway includes NextJS frontend for modern development
- **API Gateway**: Single entry point for all services
- **Service Discovery**: Consul enables dynamic service discovery and load balancing

## Mapping from Business Rules
- Unique email as login: handled by `User`; `CustomerProfile` links 1–1 to `User`.
- Registered vs. unregistered: `AudienceType` in campaigns; `DeviceToken` includes `email/username/loanCode` to infer registration.
- Channels and template constraints: per-channel fields in `NotificationCampaign`; `imageUrl` supports media when applicable.
- Send history and reminder history: `NotificationHistory` and `ReminderHistory` capture channel, status, timestamps, and snapshots.
- Scheduler parameters: `ReminderConfig` holds schedule and limits.

## Next Steps
- Implement schedulers and messaging/integration logic in service layer after generation.
- Integrate Firebase/APNs for push and email provider for email.
- Expose APIs required by separate frontend.

## LeadApplication Management (Consumer & Commercial)

Entities added to support submitting and managing Lend lead applications:
- `LeadApplication`: core lead application data, amounts, requested terms/purpose/product, industry, notes, and audit fields.
  - Status tracking: `status` (enum `LeadStatus`), `statusReason`, `statusUpdatedAt`, `statusUpdatedBy`.
  - Generic audit: `createdAt`, `updatedAt`, `updatedBy`.
  - Owner/Finance/Marketing/Notes via 1–1 or 1–many relations.
- `LeadOwner`: consumer owner profile and KYC fields (name, contact, DOB, gender, marital status, IDs).
- `LeadOwnerEmployment`, `LeadOwnerIncome`, `LeadOwnerAddress`: arrays from API mapped to separate entities.
- `LeadAssetFinance`: vehicle/equipment details and finance parameters.
- `LeadMarketing`: GA/UTM tracking fields.
- `LeadNote`: arbitrary notes.
- `CommercialProfile`: business profile for commercial lead applications.

Status and backup flow:
1. Before updating a lead application, create `LeadRevision` with a full JSON snapshot.
2. Apply changes to `LeadApplication` and set `updatedBy/updatedAt`.
3. If status changes, set `status/statusReason/statusUpdatedBy/statusUpdatedAt` and insert `LeadStatusHistory`.

Related entities:
- `LeadStatusHistory`: who/when/why a status changed.
- `LeadRevision`: `JsonBlob` snapshot (backup) before modifications.
- `ApiAuditLog`: API-level audit for all actions (endpoint, method, request/response, user, IP, UA, success/status).

Field validations (key examples):
- Owner: `firstName/lastName (≤60)`, `contactNumber (≤10)`, `email (≤254)`.
- IDs: licence/medicare/passport fields have reasonable max lengths; `medicareExpiry` stored as string for mm-yy.
- Asset finance: VIN/rego/state and supplier contact fields sized to match API samples.
- Amounts: `amountRequested min(1)`, income amounts `min(0)`.

References:
- Submit New Consumer Lead and Commercial Lead specs at the Lend Broker API docs.
  - Consumer: https://broker-api-docs.lend.com.au/api/#submit-new-consumer-lead
  - Commercial: https://broker-api-docs.lend.com.au/api/#submit-new-commercial-lead

## LoanApplication Management

Entities for managing approved loan applications and contracts:
- `LoanApplication`: created from approved LeadApplication with contract details and snapshot data.
  - Contract fields: `loanNumber`, `amount`, `interestRate`, `termMonths`, `loanType`, `interestType`.
  - Status tracking: `status` (enum `LoanStatus`), `approvedAt`, `disbursedAt`, `maturityDate`.
  - Snapshot strategy: `leadSnapshotJson` contains complete LeadApplication data at creation time.
  - Denormalized fields: `customerName`, `customerEmail`, `customerPhone`, `brokerName`, `leadType`, `purpose` for easy querying.
- `RepaymentSchedule`: installment schedule for each loan application.
  - Fields: `installmentNumber`, `dueDate`, `principalAmount`, `interestAmount`, `totalAmount`, `status`.
  - Payment tracking: `paidAt`, `paidAmount`, `lateFee`.
- `Payment`: actual payment records.
  - Fields: `paymentNumber`, `amount`, `paymentDate`, `paymentMethod`, `reference`, `status`, `notes`.

Business workflow:
1. LeadApplication status: NEW → IN_PROGRESS → PENDING_INFO → SUBMITTED → APPROVED → DECLINED → WITHDRAWN
2. When LeadApplication status = APPROVED, create LoanApplication with:
   - Complete snapshot of LeadApplication data (leadSnapshotJson)
   - Denormalized key fields for querying
   - Loan-specific contract details
3. LoanApplication status: PENDING → APPROVED → ACTIVE → PAID_OFF/DEFAULTED/CANCELLED
4. When LoanApplication becomes ACTIVE, generate RepaymentSchedule
5. Record actual payments in Payment entity

Data optimization strategy:
- `leadSnapshotJson`: Complete JSON snapshot of LeadApplication + all related entities at loan creation
- Denormalized fields: Key fields extracted for easy querying and reporting
- Benefits: Data integrity + Query performance + No redundancy
- Flexible constraints: Removed required constraints for better user experience

## Picklist Caches (from Lend Broker API)

Entities used to cache and validate picklist values returned by Lend:
- `Industry` (self-referencing parent/children)
- `LoanPurpose`
- `LoanTerm`
- `OwnerType`
- `HomeOwnerOption`
- `ProductType` (self-referencing parent/children)
- `EquipmentType`
- `Occupation` (flags `isAu`, `isNz`)
- `EmploymentType`

Mapping guidelines:
- Use `externalId` to store the Lend ID (string-safe if API returns numeric as string).
- Use `name` or `description` to store display text (matching `industry`, `purpose`, `loan_term`, `product_type_name`, `description`, etc.).
- In `LeadApplication`, the following fields map to picklists:
  - `purposeId` → `LoanPurpose.externalId`
  - `loanTermRequested` → `LoanTerm.externalId`
  - `productTypeId` → `ProductType.externalId`
  - `industryId` → `Industry.externalId`
  - `LeadOwner.homeOwnerOptionId` → `HomeOwnerOption.externalId`
  - `LeadOwnerEmployment.occupationId` → `Occupation.externalId`
  - `LeadOwnerEmployment.employmentType` → `EmploymentType.name`

Sync strategy (recommended):
- Scheduled job calls the picklist APIs and upserts by `externalId`.
- Preserve existing values in use; avoid destructive deletes; mark obsolete rows inactive if needed.
- Validate incoming `LeadApplication` data against cached picklists and return precise errors if mismatched.

References:
- Picklist APIs: https://broker-api-docs.lend.com.au/api/#picklist-apis
- Industries: https://broker-api-docs.lend.com.au/api/#industries
- Loan Purposes: https://broker-api-docs.lend.com.au/api/#loan-purposes
- Loan Terms: https://broker-api-docs.lend.com.au/api/#loan-terms
- Owner Types: https://broker-api-docs.lend.com.au/api/#owner-types
- Home Owner Options: https://broker-api-docs.lend.com.au/api/#home-owner-options
- Product Types: https://broker-api-docs.lend.com.au/api/#product-types
- Equipment Types: https://broker-api-docs.lend.com.au/api/#equipment-types
- Occupations: https://broker-api-docs.lend.com.au/api/#occupations
- Employment Types: https://broker-api-docs.lend.com.au/api/#employment-types

## Campaign Actors, Sending Flow, and Audit

Actors captured across entities:
- Campaign creator: who created/edited the campaign definition (use `ApiAuditLog` and campaign `updatedBy/updatedAt` if present).
- Sender (who pressed send): stored on `NotificationBatch` via `changedBy`/`createdBy` in audit (use `ApiAuditLog` to persist the exact user and request context; optionally add `triggeredBy` on batch if needed).
- Distributor/worker: the background job identity can also be recorded in `ApiAuditLog` when the job executes the send.
- Recipient: stored per-row on `NotificationDelivery` (recipientEmail/recipientUsername/recipientLoanCode); this is the authoritative per-user receipt history.

Best-practice audit:
- Record user/API context in `ApiAuditLog` for campaign create/update, schedule/send actions.
- Use `NotificationBatch` for per-send grouping and counters.
- Use `NotificationDelivery` for per-recipient status and optional render parameters.

## Deduplication via contentHash

- `NotificationContent.contentHash` is a deterministic hash built from the channel and content fields (e.g., email: `channel|subject|body`).
- Purpose:
  - Deduplicate static content: 1 content sent to N recipients → only one `NotificationContent` row reused across batches.
  - Reuse and analytics: group sends by identical content for reporting and idempotency.
- Personalized templates: store template at campaign level; keep per-recipient parameters in `NotificationDelivery.parametersJson`. Avoid exploding `NotificationContent` for each recipient.

## Delivery vs History (and why Delivery wins)

- `NotificationDelivery` is the authoritative per-recipient log. It holds status, error, recipient snapshot, timestamps, and (optionally) `parametersJson` and rendered subject/body for audit.
- `NotificationHistory` was the original per-send-per-recipient log. Given the introduction of batches and dedup content, it overlaps with `NotificationDelivery`.

Recommendation:
- Consolidate on `NotificationDelivery` for per-recipient records and deprecate `NotificationHistory`.
- Keep `NotificationBatch` to aggregate a send execution (per channel) and connect to `NotificationContent`.
- Migration approach:
  1) Stop writing to `NotificationHistory` in new code paths.
  2) Backfill or alias existing history views to read from `NotificationDelivery`.
  3) Remove `NotificationHistory` once no longer used (or keep for backward compatibility if required by legacy reports).

## Multi-channel, Audience-based Sending (How it works)

- One `NotificationCampaign` defines audience targeting (REGISTERED/UNREGISTERED) and enables channels (email/push/in-app) with their templates.
- When sending:
  1) System resolves the recipient list according to audience and filters.
  2) For each enabled channel, create one `NotificationBatch` linked to the campaign.
  3) Content handling:
     - Static: upsert `NotificationContent` by `contentHash`, point the batch to it, and create `NotificationDelivery` rows per recipient.
     - Personalized: keep template in campaign; store per-recipient `parametersJson` (and optional rendered fields) on `NotificationDelivery`.
  4) Execute send, update each delivery's `status/error/sentAt` and batch counters.
- Reporting/UI:
  - Join `NotificationDelivery → NotificationBatch → NotificationContent → NotificationCampaign` and sort by `COALESCE(delivery.sentAt, batch.sentAt, batch.plannedAt)` for a user's timeline.

This model supports: reusing campaigns, sending to both audiences, multi-channel in one click, dedup static content, personalized parameters, and complete audit and history.

## Content Model: RenderingStrategy, In‑app Short/Long, and Variants

Key enum:
- `RenderingStrategy`: STATIC | PER_RECIPIENT

Entities:
- `NotificationContent` (deduplicated by `contentHash`)
  - Email/push: `subject`, `body`
  - In‑app short/long: `inAppShortTitle`, `inAppShortBody` (list view), `inAppLongTitle`, `inAppLongBody`, `inAppImageUrl`, `inAppRichStyleJson`
  - Personalization: `renderingStrategy`, `paramSchemaJson`
- `NotificationContentVariant` (optional)
  - Group repeated rendered outputs for personalized templates using `variantHash`
- `NotificationBatch`
  - One per send action and per channel; links to `NotificationContent` (and optionally a variant strategy)
- `NotificationDelivery`
  - Per recipient; holds metadata only and `parametersJson` (no heavy rendered body) for fast listing

Recommended usage:
- STATIC content (no parameters):
  - Upsert `NotificationContent` by `contentHash`; `NotificationBatch` → `NotificationContent`
  - Create many `NotificationDelivery` rows (recipient snapshots, status/timestamps)
- PER_RECIPIENT (personalized):
  - Keep template at campaign/content; store per‑recipient `parametersJson` on `NotificationDelivery`
  - Only use `NotificationContentVariant` if you detect many identical rendered results and want extra dedup

Examples
- Static email campaign (REGISTERED audience):
  1) Create `NotificationBatch` for channel EMAIL
  2) Upsert `NotificationContent` with `subject/body`, `renderingStrategy=STATIC`
  3) Insert deliveries for N recipients; send; update statuses
- Personalized push (UNREGISTERED audience) with name variable:
  1) Batch for PUSH, `NotificationContent` has `pushTitle/pushBody`, `renderingStrategy=PER_RECIPIENT`, `paramSchemaJson` describes `fullName`
  2) For each recipient, set `{ "fullName": "Nguyen Van A" }` in `parametersJson` on delivery; render at send time
  3) Deliver and update status; listing stays fast since bodies live in content (not per delivery)
- In‑app short/long content:
  - Short fields show in notification lists; long fields show on detail screen with image/style (`inAppImageUrl`, `inAppRichStyleJson`)

Query/UI tips:
- User inbox: join `NotificationDelivery → NotificationBatch → NotificationContent` to show channel, subject/short body, and sent time; fetch long content only on detail screen.
- Index deliveries by recipient identifiers and `(sent_at desc)`; batches by `(campaign_id, sent_at)`.

## Practical Examples (Records and Flow)

### Example records

- NotificationCampaign (UNREGISTERED audience, enable email + in-app)
```json
{
  "name": "Promo Aug Week 1",
  "active": true,
  "audience": "UNREGISTERED",
  "channelActiveEmail": true,
  "channelActivePush": false,
  "channelActiveInApp": true,
  "emailSubject": "Ưu đãi tháng 8",
  "emailBody": "Nhanh tay nhận ưu đãi...",
  "inAppTitle": "Ưu đãi tháng 8",
  "inAppBody": "Ưu đãi mới cho bạn...",
  "imageUrl": "https://cdn.example.com/banner-aug.png"
}
```

- NotificationContent (STATIC email + in-app short/long)
```json
{
  "channel": "EMAIL",
  "subject": "Ưu đãi 20% tuần này",
  "body": "Mua ngay...",
  "inAppShortTitle": "Ưu đãi 20%",
  "inAppShortBody": "Xem ngay",
  "inAppLongTitle": "Ưu đãi 20% tuần này",
  "inAppLongBody": "Chi tiết ưu đãi...",
  "inAppImageUrl": "https://cdn.example.com/offer.png",
  "renderingStrategy": "STATIC",
  "paramSchemaJson": "{}",
  "contentHash": "sha256:email|Ưu đãi 20% tuần này|Mua ngay...",
  "createdAt": "2025-08-10T01:00:00Z"
}
```

- NotificationBatch (email channel)
```json
{
  "name": "Batch-EMAIL-2025-08-10T01:05Z",
  "plannedAt": "2025-08-10T01:05:00Z",
  "sentAt": null,
  "status": "PENDING",
  "totalRecipients": 100000,
  "successCount": 0,
  "failureCount": 0,
  "campaign": "Promo Aug Week 1",
  "content": "sha256:email|Ưu đãi 20% tuần này|Mua ngay..."
}
```

- NotificationDelivery (per user, lightweight)
```json
{
  "recipientEmail": "[email protected]",
  "status": "PENDING",
  "parametersJson": "{}"
}
```

- NotificationContent (PER_RECIPIENT push)
```json
{
  "channel": "PUSH",
  "subject": null,
  "body": "Xin chào {{fullName}}, ưu đãi chờ bạn!",
  "renderingStrategy": "PER_RECIPIENT",
  "paramSchemaJson": "{\"type\":\"object\",\"properties\":{\"fullName\":{\"type\":\"string\"}}}",
  "contentHash": "sha256:push|Xin chào {{fullName}}|ưu đãi chờ bạn!",
  "createdAt": "2025-08-10T01:00:00Z"
}
```

- LeadApplication (core)
```json
{
  "ref": "22nPwwU",
  "leadType": "CONSUMER",
  "amountRequested": 56000,
  "loanTermRequested": 12,
  "purposeId": 2,
  "productTypeId": 1,
  "industryId": 189,
  "status": "NEW",
  "createdAt": "2025-08-10T00:00:00Z"
}
```

- LoanApplication (created from approved LeadApplication)
```json
{
  "loanNumber": "LOAN-2025-001",
  "leadApplicationId": 123,
  "customerId": 456,
  "brokerId": 789,
  "amount": 56000,
  "interestRate": 8.5,
  "termMonths": 12,
  "status": "ACTIVE",
  "loanType": "PERSONAL",
  "interestType": "FIXED",
  "customerName": "Nguyen Van A",
  "customerEmail": "[email protected]",
  "brokerName": "John Smith",
  "leadSnapshotJson": "{\"leadApplication\": {...}, \"leadOwner\": {...}}",
  "createdAt": "2025-08-10T01:00:00Z"
}
```

- ApiAuditLog (send request)
```json
{
  "action": "SEND_CAMPAIGN",
  "httpMethod": "POST",
  "endpoint": "/api/campaigns/{id}/send",
  "correlationId": "req-01JABC...",
  "success": true,
  "statusCode": 202,
  "userId": "admin",
  "username": "admin",
  "ipAddress": "203.0.113.10",
  "performedAt": "2025-08-10T01:05:00Z"
}
```

### Send flow (Static email + In‑app, UNREGISTERED)
1) Pick recipients per AudienceType (UNREGISTERED list).
2) For each enabled channel:
   - Upsert NotificationContent (STATIC) by contentHash.
   - Create NotificationBatch linked to campaign + content.
   - Bulk insert NotificationDelivery for N recipients (parametersJson = {}).
3) Dispatch send job per batch; update each delivery status/sentAt and batch counters.
4) UI list joins Delivery → Batch → Content → Campaign; show short fields (subject/inAppShort*). Detail loads long fields.

### LeadApplication to LoanApplication Flow
1) Customer submits LeadApplication (status: NEW).
2) Broker reviews and updates LeadApplication (status: IN_PROGRESS → PENDING_INFO → SUBMITTED).
3) LeadApplication approved (status: APPROVED).
4) System creates LoanApplication with:
   - Complete snapshot of LeadApplication data (leadSnapshotJson)
   - Denormalized fields for querying
   - Contract-specific details
5) LoanApplication activated (status: ACTIVE) and RepaymentSchedule generated.
6) Customer makes payments tracked in Payment entity.

### Admin UI
- Enabled via `withAdminUi true` in JDL. After generation, use the JHipster admin to CRUD campaigns, contents, batches, deliveries, lead applications, loan applications, picklists, and audit logs.

### Index/partition suggestions (for large scale)
- Delivery: (recipient_email), (recipient_username), (recipient_loan_code), (batch_id), (status, sent_at desc), (sent_at desc)
- Batch: (campaign_id), (content_id), (sent_at desc)
- Content: (content_hash unique)
- ApiAuditLog: (performed_at desc), (user_id), (endpoint)
- LeadApplication: (status), (broker_id), (created_at desc), (ref unique)
- LoanApplication: (status), (broker_id), (customer_id), (created_at desc), (loan_number unique)
- RepaymentSchedule: (loan_application_id), (due_date), (status)
- Payment: (loan_application_id), (payment_date desc), (status)
- Partition Delivery/ApiAuditLog/LeadApplication/LoanApplication by time if volume is very large.
