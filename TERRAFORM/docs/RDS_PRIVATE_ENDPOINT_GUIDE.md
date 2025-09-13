# Hướng dẫn sử dụng RDS Private Endpoint trong CI/CD

## Vấn đề

Khi deploy ứng dụng trên EC2 cùng VPC với RDS, bạn nên sử dụng private endpoint thay vì public endpoint để:
- Tối ưu hiệu suất (traffic không đi qua internet)
- Tăng cường bảo mật
- Giảm chi phí data transfer

## Giải pháp

### 1. Sử dụng GitHub Secrets (Đơn giản nhất)

#### Bước 1: Lấy RDS endpoint từ Terraform
```bash
cd /path/to/terraform
./scripts/get-rds-endpoint.sh
```

#### Bước 2: Thêm vào GitHub Secrets
- Vào GitHub repository → Settings → Secrets and variables → Actions
- Thêm secret mới:
  - Name: `RDS_PRIVATE_ENDPOINT`
  - Value: `loan-management-application-dev-mysql.cfiocsmsoith.ap-southeast-2.rds.amazonaws.com`

#### Bước 3: Cập nhật CI/CD pipeline
```yaml
script: |
  RDS_ENDPOINT='${{ secrets.RDS_PRIVATE_ENDPOINT }}'
  RDS_USERNAME='lma_root'
  RDS_PASSWORD='${{ secrets.RDS_PASSWORD }}'
  # ... rest of the script
```

### 2. Sử dụng AWS Systems Manager Parameter Store (Tự động)

#### Bước 1: Apply Terraform để tạo Parameter Store
```bash
cd /path/to/terraform
terraform apply
```

#### Bước 2: Cập nhật GitHub Secrets tự động
```bash
./scripts/update-github-secrets.sh pntsol/lma_backend
```

#### Bước 3: CI/CD sẽ tự động lấy endpoint từ Parameter Store
```yaml
script: |
  RDS_ENDPOINT=$(aws ssm get-parameter \
    --name "/loan-management-application-dev/rds/endpoint" \
    --query 'Parameter.Value' \
    --output text \
    --region ap-southeast-2)
```

### 3. Sử dụng AWS CLI trực tiếp (Cần IAM permissions)

#### Bước 1: Đảm bảo EC2 có IAM role với quyền truy cập RDS
Terraform đã tự động tạo IAM role và policy cần thiết.

#### Bước 2: CI/CD sẽ tự động lấy endpoint
```yaml
script: |
  RDS_ENDPOINT=$(aws rds describe-db-instances \
    --db-instance-identifier loan-management-application-dev-mysql \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text \
    --region ap-southeast-2)
```

## Lợi ích của từng giải pháp

### GitHub Secrets
- ✅ Đơn giản, dễ hiểu
- ✅ Không cần AWS permissions trên EC2
- ❌ Cần cập nhật thủ công khi RDS thay đổi

### Systems Manager Parameter Store
- ✅ Tự động đồng bộ với Terraform
- ✅ Có thể cập nhật tự động
- ✅ Audit trail và versioning
- ❌ Cần AWS permissions trên EC2

### AWS CLI trực tiếp
- ✅ Luôn lấy được thông tin mới nhất
- ✅ Không cần lưu trữ secrets
- ❌ Cần AWS permissions trên EC2
- ❌ Phụ thuộc vào AWS CLI

## Khuyến nghị

**Sử dụng giải pháp 1 (GitHub Secrets)** nếu:
- Bạn muốn giải pháp đơn giản
- RDS endpoint ít khi thay đổi
- Không muốn phức tạp hóa infrastructure

**Sử dụng giải pháp 2 (Parameter Store)** nếu:
- Bạn muốn tự động hóa hoàn toàn
- Có nhiều environments cần quản lý
- Muốn có audit trail

## Troubleshooting

### Lỗi: "Could not get RDS endpoint"
```bash
# Kiểm tra terraform state
terraform state list | grep aws_db_instance

# Kiểm tra outputs
terraform output rds_endpoint
```

### Lỗi: "Access denied to Parameter Store"
```bash
# Kiểm tra IAM role
aws sts get-caller-identity

# Kiểm tra permissions
aws ssm get-parameter --name "/loan-management-application-dev/rds/endpoint"
```

### Lỗi: "GitHub CLI not authenticated"
```bash
# Login GitHub CLI
gh auth login

# Kiểm tra authentication
gh auth status
```
