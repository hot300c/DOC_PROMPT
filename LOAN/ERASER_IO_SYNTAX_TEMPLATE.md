# Eraser.io Syntax Template - Loan Management System

## Eraser.io Syntax cho Loan Management System

```eraser
direction right
// loan-management-system-architecture

Client [icon: users] {
    Mobile Apps [icon: mobile] {
        iOS App [icon: apple]
        Android App [icon: android]
    }
    Web Admin [icon: browser] {
        Admin Dashboard [icon: monitor]
        Staff Portal [icon: laptop]
    }
    Web Browser [icon: browser] {
        Customer Portal [icon: globe]
    }
}

group AWS Infrastructure {
    // Edge & CDN Layer
    CloudFront [icon: aws-cloudfront, note: "Global CDN"]
    Route53 [icon: aws-route53, note: "DNS Service"]
    WAF [icon: aws-waf, note: "Web Application Firewall"]
    
    // API Gateway Layer
    ALB [icon: aws-alb, note: "Application Load Balancer"]
    APIGW [icon: aws-api-gateway, note: "REST & WebSocket APIs"]
    Cognito [icon: aws-cognito, note: "Authentication Service"]
    
    // Compute Layer
    ECS [icon: aws-ecs, note: "Container Orchestration"]
    Lambda [icon: aws-lambda, note: "Serverless Functions"]
    EC2 [icon: aws-ec2, note: "Virtual Servers"]
    
    // Core Services
    BACKEND {
        User Service [icon: k8s-pod, note: "Spring Boot", color: blue]
        Loan Service [icon: k8s-pod, note: "Spring Boot", color: green]
        Payment Service [icon: k8s-pod, note: "Spring Boot", color: orange]
        Notification Service [icon: k8s-pod, note: "Spring Boot", color: purple]
        Document Service [icon: k8s-pod, note: "Spring Boot", color: red]
        Analytics Service [icon: k8s-pod, note: "Spring Boot", color: teal]
    }
    
    // Data Layer
    DATABASE {
        RDS PostgreSQL [icon: aws-rds, note: "Primary Database", color: blue]
        ElastiCache Redis [icon: aws-elasticache, note: "Cache & Sessions", color: red]
        DynamoDB [icon: aws-dynamodb, note: "NoSQL Database", color: green]
    }
    
    // Storage Layer
    STORAGE {
        S3 [icon: aws-s3, note: "File Storage", color: orange]
        S3 Glacier [icon: aws-s3, note: "Archive Storage", color: gray]
    }
    
    // Messaging Layer
    MESSAGING {
        SQS [icon: aws-sqs, note: "Message Queues"]
        SNS [icon: aws-sns, note: "Notification Service"]
        EventBridge [icon: aws-eventbridge, note: "Event Routing"]
    }
    
    // Monitoring Layer
    MONITORING {
        CloudWatch [icon: aws-cloudwatch, note: "Metrics & Logs"]
        X-Ray [icon: aws-xray, note: "Distributed Tracing"]
        CloudTrail [icon: aws-cloudtrail, note: "API Auditing"]
    }
    
    // Security Layer
    SECURITY {
        KMS [icon: aws-kms, note: "Key Management"]
        IAM [icon: aws-iam, note: "Access Control"]
        Secrets Manager [icon: aws-secrets-manager, note: "Credential Storage"]
    }
}

group External Services {
    Firebase [icon: firebase, note: "Auth & Analytics"]
    SES [icon: aws-ses, note: "Email Service"]
    SNS SMS [icon: aws-sns, note: "SMS Service"]
    VNPay [icon: credit-card, note: "Payment Gateway"]
    MoMo [icon: mobile, note: "Payment Gateway"]
    CIC API [icon: bank, note: "Credit Bureau"]
    loan.com.us [icon: building, note: "Sandbox API"]
}

// Client to AWS connections
Client > CloudFront
CloudFront > WAF
WAF > ALB
ALB > APIGW
APIGW > Cognito

// API Gateway to Services
APIGW > User Service
APIGW > Loan Service
APIGW > Payment Service
APIGW > Notification Service
APIGW > Document Service
APIGW > Analytics Service

// Services to Database
User Service > RDS PostgreSQL
Loan Service > RDS PostgreSQL
Payment Service > RDS PostgreSQL
Notification Service > RDS PostgreSQL
Document Service > RDS PostgreSQL
Analytics Service > DynamoDB

// Services to Cache
User Service > ElastiCache Redis
Loan Service > ElastiCache Redis
Payment Service > ElastiCache Redis

// Services to Storage
Document Service > S3
Analytics Service > S3 Glacier

// Services to Messaging
Notification Service > SQS
Notification Service > SNS
Loan Service > EventBridge

// Services to External
User Service > Firebase
Loan Service > CIC API
Loan Service > loan.com.us
Payment Service > VNPay
Payment Service > MoMo
Notification Service > SES
Notification Service > SNS SMS
Notification Service > Firebase

// Monitoring connections
User Service > CloudWatch
Loan Service > CloudWatch
Payment Service > CloudWatch
Notification Service > CloudWatch
Document Service > CloudWatch
Analytics Service > CloudWatch

// Security connections
User Service > KMS
Loan Service > KMS
Payment Service > KMS
Notification Service > KMS
Document Service > KMS

// Compute to Services
ECS > User Service
ECS > Loan Service
ECS > Payment Service
ECS > Notification Service
ECS > Document Service
ECS > Analytics Service

Lambda > User Service
Lambda > Loan Service
Lambda > Payment Service
```

## Alternative Simplified Version

```eraser
direction right
// loan-management-simplified

Client [icon: users] {
    Mobile Apps [icon: mobile] {
        iOS App [icon: apple]
        Android App [icon: android]
    }
    Web Admin [icon: browser] {
        Admin Dashboard [icon: monitor]
        Staff Portal [icon: laptop]
    }
}

group PNT Infrastructure {
    APIGW Gateway [icon: aws-api-gateway]
    
    BACKEND {
        loan-backend-service [icon: k8s-pod, note: "Spring Boot", color: blue]
        database-loan [icon: database, color: red] {
            db-loan-main [icon: database]
            db-loan-analytics [icon: database]
        }
    }
    
    Cognito [icon: aws-cognito] // chứng thực người dùng
    Firebase [icon: firebase] // gửi notification
    S3 Storage [icon: aws-s3] // lưu documents
    CloudWatch [icon: aws-cloudwatch] // monitoring
}

group External Infrastructure {
    Firebase [icon: firebase, note: "external"]
    VNPay API [icon: credit-card, note: "external"]
    MoMo API [icon: mobile, note: "external"]
    CIC API [icon: bank, note: "external"]
    loan.com.us API [icon: building, note: "external"]
}

// Connections
Client > APIGW Gateway
Web Admin -> APIGW Gateway: quản trị hệ thống
loan-backend-service -> db-loan-main
APIGW Gateway > loan-backend-service

// Authentication & Services
loan-backend-service -> Cognito: xác thực người dùng
loan-backend-service -> Firebase: push notification
Mobile Apps -> loan-backend-service: REST API
Mobile Apps -> S3 Storage: tải documents

// External API connections
loan-backend-service -> VNPay API: payment processing
loan-backend-service -> MoMo API: payment processing
loan-backend-service -> CIC API: credit check
loan-backend-service -> loan.com.us API: sandbox integration

// Analytics
loan-backend-service -> db-loan-analytics: analytics data
loan-backend-service -> CloudWatch: monitoring & logs
```

## Microservices Detailed Version

```eraser
direction right
// loan-management-microservices

Client [icon: users] {
    Mobile Apps [icon: mobile] {
        iOS App [icon: apple]
        Android App [icon: android]
    }
    Web Admin [icon: browser] {
        Admin Dashboard [icon: monitor]
        Staff Portal [icon: laptop]
    }
}

group AWS Infrastructure {
    // API Gateway
    APIGW [icon: aws-api-gateway]
    ALB [icon: aws-alb]
    Cognito [icon: aws-cognito]
    
    // Microservices
    MICROSERVICES {
        User Service [icon: k8s-pod, note: "Port: 8081", color: blue]
        Loan Service [icon: k8s-pod, note: "Port: 8082", color: green]
        Payment Service [icon: k8s-pod, note: "Port: 8083", color: orange]
        Notification Service [icon: k8s-pod, note: "Port: 8084", color: purple]
        Document Service [icon: k8s-pod, note: "Port: 8085", color: red]
        Analytics Service [icon: k8s-pod, note: "Port: 8086", color: teal]
    }
    
    // Databases
    DATABASES {
        User DB [icon: aws-rds, note: "PostgreSQL", color: blue]
        Loan DB [icon: aws-rds, note: "PostgreSQL", color: green]
        Payment DB [icon: aws-rds, note: "PostgreSQL", color: orange]
        Analytics DB [icon: aws-dynamodb, note: "NoSQL", color: teal]
    }
    
    // Storage & Cache
    STORAGE {
        S3 Documents [icon: aws-s3, note: "Documents", color: red]
        Redis Cache [icon: aws-elasticache, note: "Cache", color: yellow]
    }
    
    // Messaging
    MESSAGING {
        SQS [icon: aws-sqs, note: "Queues"]
        SNS [icon: aws-sns, note: "Notifications"]
    }
}

group External Services {
    Firebase [icon: firebase, note: "Auth & Push"]
    VNPay [icon: credit-card, note: "Payment"]
    MoMo [icon: mobile, note: "Payment"]
    CIC [icon: bank, note: "Credit Check"]
    loan.com.us [icon: building, note: "Sandbox"]
}

// Client connections
Client > APIGW
APIGW > ALB
ALB > Cognito

// API Gateway to Microservices
APIGW > User Service
APIGW > Loan Service
APIGW > Payment Service
APIGW > Notification Service
APIGW > Document Service
APIGW > Analytics Service

// Service to Database connections
User Service > User DB
Loan Service > Loan DB
Payment Service > Payment DB
Analytics Service > Analytics DB

// Service to Storage connections
Document Service > S3 Documents
User Service > Redis Cache
Loan Service > Redis Cache
Payment Service > Redis Cache

// Service to Messaging connections
Notification Service > SQS
Notification Service > SNS
Loan Service > SQS

// External service connections
User Service > Firebase
Payment Service > VNPay
Payment Service > MoMo
Loan Service > CIC
Loan Service > loan.com.us
Notification Service > Firebase
```

## Cách sử dụng:

1. **Copy code** từ một trong các version trên
2. **Paste vào eraser.io** workspace
3. **Chọn direction**: right (như trong example)
4. **Customize** theo nhu cầu cụ thể
5. **Export** diagram khi hoàn thành

## Các version khác nhau:

- **Full Version**: Đầy đủ AWS services và connections
- **Simplified Version**: Tương tự như example của bạn
- **Microservices Version**: Chi tiết từng microservice với ports

Bạn có thể chọn version phù hợp với nhu cầu và customize thêm!
