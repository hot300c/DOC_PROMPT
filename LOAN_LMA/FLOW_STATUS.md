# Loan Application Flow Status Diagram

## Overview
This diagram shows the complete flow of a loan application.

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> DRAFT: Bắt đầu soạn đơn

    state "Khởi tạo" as ORIGINATION {
        state DRAFT
        state SUBMITTED
        state PENDING_VERIFICATION
        state PRE_APPROVED

        DRAFT --> SUBMITTED: Nộp đơn
        SUBMITTED --> PENDING_VERIFICATION: Xác nhận đơn
        SUBMITTED --> REJECTED: Thiếu tài liệu
        PENDING_VERIFICATION --> PRE_APPROVED: KYC hoàn tất
        PENDING_VERIFICATION --> REJECTED: KYC thất bại
        PRE_APPROVED --> IN_REVIEW: Bắt đầu thẩm định
        PRE_APPROVED --> REJECTED: Không đủ điều kiện
    }

    state "Thẩm định" as UNDERWRITING {
        state IN_REVIEW
        state UNDERWRITING_ACTIVE
        state APPROVED
        state CONDITIONALLY_APPROVED

        IN_REVIEW --> UNDERWRITING_ACTIVE: Phân tích rủi ro
        UNDERWRITING_ACTIVE --> APPROVED: Đạt tiêu chí
        UNDERWRITING_ACTIVE --> CONDITIONALLY_APPROVED: Cần bổ sung
        UNDERWRITING_ACTIVE --> REJECTED: Không đạt tiêu chí
        CONDITIONALLY_APPROVED --> APPROVED: Thỏa điều kiện
        CONDITIONALLY_APPROVED --> REJECTED: Không thỏa điều kiện
    }

    state "Quản lý Vay" as SERVICING {
        state DISBURSED
        state ACTIVE
        state OVERDUE
        state IN_COLLECTION

        APPROVED --> DISBURSED: Giải ngân
        DISBURSED --> ACTIVE: Vay bắt đầu
        ACTIVE --> OVERDUE: Quá hạn 5 ngày
        ACTIVE --> PAID_OFF: Trả hết sớm
        OVERDUE --> IN_COLLECTION: Quá hạn 30 ngày
        OVERDUE --> PAID_OFF: Thanh toán muộn
        IN_COLLECTION --> PAID_OFF: Thu hồi thành công
        IN_COLLECTION --> DEFAULTED: Không thu hồi được
    }

    state "Kết thúc" as CLOSURE {
        state PAID_OFF
        state CLOSED
        state DEFAULTED
        state REJECTED
        state ARCHIVED

        PAID_OFF --> CLOSED: Hoàn tất hồ sơ
        CLOSED --> ARCHIVED: Lưu trữ 5 năm
        DEFAULTED --> ARCHIVED: Lưu trữ nợ xấu
        REJECTED --> ARCHIVED: Lưu trữ từ chối
    }

    ARCHIVED --> [*]: Kết thúc
```

## State Descriptions

### 1. Khởi tạo (Origination)
- **DRAFT**: Đơn vay đang được soạn thảo
- **SUBMITTED**: Đơn đã được nộp
- **PENDING_VERIFICATION**: Đang chờ xác minh KYC
- **PRE_APPROVED**: Sơ bộ được chấp thuận

### 2. Thẩm định (Underwriting)
- **IN_REVIEW**: Đang trong quá trình xem xét
- **UNDERWRITING_ACTIVE**: Đang thẩm định tích cực
- **APPROVED**: Được chấp thuận hoàn toàn
- **CONDITIONALLY_APPROVED**: Chấp thuận có điều kiện

### 3. Quản lý Vay (Servicing)
- **DISBURSED**: Đã giải ngân
- **ACTIVE**: Khoản vay đang hoạt động
- **OVERDUE**: Quá hạn thanh toán
- **IN_COLLECTION**: Đang trong quá trình thu hồi

### 4. Kết thúc (Closure)
- **PAID_OFF**: Đã trả hết nợ
- **CLOSED**: Hồ sơ đã đóng
- **DEFAULTED**: Vỡ nợ
- **REJECTED**: Bị từ chối
- **ARCHIVED**: Đã lưu trữ

## Transition Rules

### Khởi tạo → Thẩm định
- Chỉ khi KYC hoàn tất và sơ bộ được chấp thuận
- Có thể bị từ chối nếu thiếu tài liệu hoặc không đủ điều kiện

### Thẩm định → Quản lý Vay
- Chỉ khi được chấp thuận hoàn toàn
- Có thể cần bổ sung tài liệu trước khi chấp thuận

### Quản lý Vay → Kết thúc
- Khi trả hết nợ hoặc vỡ nợ
- Tất cả hồ sơ cuối cùng đều được lưu trữ

## Business Rules

1. **KYC Verification**: Bắt buộc trước khi thẩm định
2. **Document Requirements**: Phải đầy đủ trước khi xem xét
3. **Payment Tracking**: Theo dõi chặt chẽ các khoản thanh toán
4. **Collection Process**: Bắt đầu sau 30 ngày quá hạn
5. **Archive Policy**: Lưu trữ tối thiểu 5 năm
