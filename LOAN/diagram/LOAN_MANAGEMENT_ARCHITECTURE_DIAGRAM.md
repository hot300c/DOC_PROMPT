# Loan Management App 

## Tổng quan hệ thống

Đây là kiến trúc tổng thể của Loan Management App:

## 0. High-Level System Architecture
![Loan Management System Architecture](diagram/diagram-export-9-7-2025-10_27_57-AM.png)


## 1. Technology Stack

```mermaid
graph TB
    subgraph "Frontend (Mobile)"
        FLUTTER[Flutter Framework]
        GETX[GetX State Management]
        DIO[HTTP Client]
        SECURE[Secure Storage]
    end

    subgraph "Backend Services"
        SPRING[Spring Boot]
        JPA[JPA/Hibernate]
        SECURITY[Spring Security]
        GATEWAY[Spring Gateway]
    end

    subgraph "Database"
        POSTGRES[PostgreSQL<br/>Main Database]
        REDIS[Redis<br/>Cache & Session]
        MINIO[MinIO<br/>File Storage]
    end

    subgraph "External APIs"
        LOAN_API[loan.com.us API]
        EMAIL_API[Email Service API]
        SMS_API[SMS Gateway API]
        CIC_API[Credit Bureau API]
    end

    subgraph "DevOps & Monitoring"
        DOCKER[Docker Containers]
        K8S[Kubernetes]
        MONITOR[Prometheus/Grafana]
        LOGS[ELK Stack]
    end

    FLUTTER --> GETX
    GETX --> DIO
    DIO --> SECURE

    SPRING --> JPA
    SPRING --> SECURITY
    SPRING --> GATEWAY

    JPA --> POSTGRES
    SPRING --> REDIS
    SPRING --> MINIO

    SPRING --> LOAN_API
    SPRING --> EMAIL_API
    SPRING --> SMS_API
    SPRING --> CIC_API

    SPRING --> DOCKER
    DOCKER --> K8S
    K8S --> MONITOR
    K8S --> LOGS

    classDef frontend fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef backend fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef database fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef external fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef devops fill:#fce4ec,stroke:#880e4f,stroke-width:2px

    class FLUTTER,GETX,DIO,SECURE frontend
    class SPRING,JPA,SECURITY,GATEWAY backend
    class POSTGRES,REDIS,MINIO database
    class LOAN_API,EMAIL_API,SMS_API,CIC_API external
    class DOCKER,K8S,MONITOR,LOGS devops
```

## 2. Tóm tắt kiến trúc

### Các thành phần chính:

1. **Users & Client Applications**
   - **Customer**: Mobile app users (iOS & Android)
   - **Admin**: Web dashboard users
   - **Staff**: Loan officers và support staff
   - **Mobile App**: Flutter application với GetX state management
   - **Web Panel**: React/Vue.js admin interface

2. **API Layer & Gateway**
   - **Load Balancer**: Nginx/HAProxy cho traffic distribution
   - **API Gateway**: Spring Cloud Gateway cho routing và authentication
   - **Authentication Service**: JWT + OAuth2 integration

3. **Core Business Services**
   - **User Management Service**: Customer profiles, roles, permissions
   - **Loan Processing Service**: Application workflow, approval process
   - **Payment Processing Service**: Payment collection, scheduling
   - **Notification Service**: Multi-channel notifications (Push, Email, SMS)
   - **Document Management Service**: File upload, storage, verification
   - **Reporting & Analytics Service**: Business intelligence, dashboards

4. **Firebase Integration**
   - **Authentication**: User login, registration, social auth
   - **Analytics**: User behavior tracking, app performance
   - **Crashlytics**: Error monitoring và crash reporting
   - **Cloud Messaging**: Push notifications
   - **Cloud Storage**: Document và file storage

5. **External Services**
   - **loan.com.us API**: Sandbox environment integration
   - **Email Provider**: SendGrid/AWS SES cho email notifications
   - **SMS Provider**: Twilio/AWS SNS cho SMS notifications
   - **Payment Gateway**: VNPay/MoMo cho payment processing
   - **Credit Bureau**: CIC API cho credit scoring

6. **Data Storage**
   - **PostgreSQL**: Main database cho business data
   - **Redis**: Cache và session management
   - **MinIO**: File storage cho documents
   - **Elasticsearch**: Search functionality và log analysis

7. **Infrastructure**
   - **Docker**: Containerization
   - **Kubernetes**: Container orchestration
   - **Monitoring**: Prometheus + Grafana
   - **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

### Luồng xử lý chính:

1. **Loan Application Flow**: Draft → Submitted → Verification → Underwriting → Approval → Disbursement → Servicing → Closure
2. **User Management**: Guest → Member với các quyền khác nhau
3. **Notification System**: Multi-channel (Push, Email, SMS, In-app) với user preferences
4. **Data Flow**: Mobile App ↔ API Gateway ↔ Core Services ↔ Database

Kiến trúc này đảm bảo tính mở rộng, bảo mật và dễ bảo trì cho hệ thống Loan Management App.
