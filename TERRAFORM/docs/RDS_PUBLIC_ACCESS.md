# RDS Public Access Configuration

## 🔒 Security Setup

RDS database đã được cấu hình để truy cập public với IP whitelist.

### ⚠️ **QUAN TRỌNG: Bảo mật**
- **KHÔNG** sử dụng `0.0.0.0/0` trong production
- Chỉ cho phép IP cụ thể của bạn/văn phòng
- Sử dụng SSL khi kết nối

## 📝 Cấu hình IP Whitelist

### 1. Cập nhật IP trong `config/terraform.tfvars`:

```hcl
# Thay đổi từ:
rds_allowed_ips = ["0.0.0.0/0"]

# Thành IP cụ thể của bạn:
rds_allowed_ips = [
  "203.0.113.1/32",        # IP văn phòng
  "198.51.100.0/24",       # Dải IP văn phòng
  "YOUR_HOME_IP/32"        # IP nhà riêng
]
```

### 2. Lấy IP hiện tại của bạn:
```bash
# Linux/Mac
curl ifconfig.me

# Windows
curl ipconfig.me
```

### 3. Apply thay đổi:
```bash
terraform plan -var-file="config/terraform.tfvars"
terraform apply
```

## 🔌 Kết nối Database

### Từ máy local (sau khi whitelist IP):

```bash
# Basic connection
mysql -h loan-management-application-dev-mysql.cfiocsmsoith.ap-southeast-2.rds.amazonaws.com \
      -P 3306 \
      -u lma_root \
      -p123457Abc

# With SSL (khuyến nghị)
mysql -h loan-management-application-dev-mysql.cfiocsmsoith.ap-southeast-2.rds.amazonaws.com \
      -P 3306 \
      -u lma_root \
      -p123457Abc \
      --ssl-mode=REQUIRED
```

### Connection String cho Application:

**JDBC (Java):**
```
jdbc:mysql://loan-management-application-dev-mysql.cfiocsmsoith.ap-southeast-2.rds.amazonaws.com:3306/lma?useSSL=true&requireSSL=true
```

**MySQL (Node.js, Python, etc.):**
```
mysql://lma_root:123457Abc@loan-management-application-dev-mysql.cfiocsmsoith.ap-southeast-2.rds.amazonaws.com:3306/lma?ssl=true
```

## 🛡️ Security Best Practices

### 1. IP Whitelist Management
```bash
# Thêm IP mới
rds_allowed_ips = [
  "203.0.113.1/32",        # IP cũ
  "203.0.113.2/32"         # IP mới
]

# Xóa IP cũ
rds_allowed_ips = [
  "203.0.113.2/32"         # Chỉ giữ IP cần thiết
]
```

### 2. Rotate Password
```bash
# Cập nhật password trong terraform.tfvars
rds_password = "new_secure_password"

# Apply changes
terraform apply
```

### 3. Monitor Access
```bash
# Xem logs RDS
aws rds describe-db-log-files --db-instance-identifier loan-management-application-dev-mysql

# Xem security group rules
aws ec2 describe-security-groups --group-ids sg-0270ba8d3ad36cee3
```

## 📊 Current Configuration

- **Endpoint**: `loan-management-application-dev-mysql.cfiocsmsoith.ap-southeast-2.rds.amazonaws.com`
- **Port**: `3306`
- **Database**: `lma`
- **Username**: `lma_root`
- **Password**: `123457Abc`
- **Public Access**: `true`
- **Allowed IPs**: `0.0.0.0/0` (cần thay đổi!)

## 🚨 Security Checklist

- [ ] Thay đổi `rds_allowed_ips` từ `0.0.0.0/0`
- [ ] Chỉ whitelist IP cần thiết
- [ ] Sử dụng SSL khi kết nối
- [ ] Rotate password định kỳ
- [ ] Monitor access logs
- [ ] Backup database thường xuyên

## 🔧 Troubleshooting

### Không kết nối được:
1. Kiểm tra IP có trong whitelist không
2. Kiểm tra firewall local
3. Kiểm tra RDS status: `aws rds describe-db-instances --db-instance-identifier loan-management-application-dev-mysql`

### SSL Error:
1. Download RDS CA certificate
2. Sử dụng `--ssl-ca` parameter
3. Hoặc disable SSL nếu không cần thiết

### Connection Timeout:
1. Kiểm tra security group rules
2. Kiểm tra RDS publicly accessible = true
3. Kiểm tra subnet group có public subnets không
