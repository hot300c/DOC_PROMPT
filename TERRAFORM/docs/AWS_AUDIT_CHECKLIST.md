# AWS Infrastructure Audit Checklist

## 1. Terraform State Validation
```bash
# Kiểm tra cấu hình hiện tại vs state
terraform plan

# Kiểm tra state có nhất quán không
terraform refresh

# Xem tất cả resources trong state
terraform state list
```

## 2. AWS Resources Audit

### EC2 Instances
```bash
# Liệt kê tất cả EC2 instances
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table

# Kiểm tra instances không có trong Terraform
# So sánh với: terraform state list | grep aws_instance
```

### RDS Instances
```bash
# Liệt kê tất cả RDS instances
aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceStatus,Engine]' --output table

# Kiểm tra RDS không có trong Terraform
# So sánh với: terraform state list | grep aws_db_instance
```

### Security Groups
```bash
# Liệt kê tất cả Security Groups
aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupId,GroupName,Description]' --output table

# Kiểm tra SG không có trong Terraform
# So sánh với: terraform state list | grep aws_security_group
```

### Elastic IPs
```bash
# Liệt kê tất cả Elastic IPs
aws ec2 describe-addresses --query 'Addresses[*].[AllocationId,PublicIp,InstanceId]' --output table

# Kiểm tra EIP không có trong Terraform
# So sánh với: terraform state list | grep aws_eip
```

### VPC & Subnets
```bash
# Liệt kê VPCs
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId,IsDefault,State]' --output table

# Liệt kê Subnets
aws ec2 describe-subnets --query 'Subnets[*].[SubnetId,VpcId,AvailabilityZone,State]' --output table
```

## 3. Cost Analysis
```bash
# Xem cost theo service (cần AWS Cost Explorer)
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-01-31 --granularity MONTHLY --metrics BlendedCost --group-by Type=DIMENSION,Key=SERVICE
```

## 4. Security Audit
```bash
# Kiểm tra Security Groups mở port 22/3389 cho 0.0.0.0/0
aws ec2 describe-security-groups --filters "Name=ip-permission.from-port,Values=22,3389" --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]' --output table

# Kiểm tra RDS publicly accessible
aws rds describe-db-instances --query 'DBInstances[?PubliclyAccessible==`true`].[DBInstanceIdentifier,PubliclyAccessible]' --output table
```

## 5. Resource Cleanup Checklist

### ✅ Resources Managed by Terraform
- [ ] EC2 Instance: `LOAN_MANAGEMENT_APPLICATION-dev-admin-backend`
- [ ] RDS MySQL: `loan-management-application-dev-mysql`
- [ ] Security Groups: `LOAN_MANAGEMENT_APPLICATION-dev-admin-ec2-sg`, `LOAN_MANAGEMENT_APPLICATION-dev-rds-sg`
- [ ] Elastic IP: `LOAN_MANAGEMENT_APPLICATION-dev-admin-eip`
- [ ] DB Subnet Group: `loan-management-application-dev-rds-subnet-group`

### ⚠️ Resources to Check for Orphaned
- [ ] EC2 instances not in Terraform state
- [ ] RDS instances not in Terraform state
- [ ] Security Groups not in Terraform state
- [ ] Elastic IPs not in Terraform state
- [ ] Unused VPCs (if not using default)
- [ ] Unused subnets
- [ ] Unused key pairs
- [ ] Unused IAM roles/policies

## 6. Manual Verification Steps

### SSH Access Test
```bash
# Test SSH connection
ssh -i pnt-ec2-lma-key.pem ec2-user@$(terraform output -raw admin_backend_public_ip)
```

### Database Connection Test
```bash
# From EC2 instance, test MySQL connection
mysql -h $(terraform output -raw rds_endpoint) -u lma_root -p123457Abc -e "SHOW DATABASES;"
```

### HTTP Access Test
```bash
# Test HTTP access
curl http://$(terraform output -raw admin_backend_public_ip)
```

## 7. Cleanup Commands (Use with caution!)

### Remove Orphaned Resources
```bash
# Remove specific EC2 instance (replace INSTANCE_ID)
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Remove specific Security Group (replace GROUP_ID)
aws ec2 delete-security-group --group-id sg-12345678

# Remove specific Elastic IP (replace ALLOCATION_ID)
aws ec2 release-address --allocation-id eipalloc-12345678

# Remove specific RDS instance (replace DB_INSTANCE_IDENTIFIER)
aws rds delete-db-instance --db-instance-identifier mydb --skip-final-snapshot
```

## 8. Monitoring Setup

### CloudWatch Alarms
```bash
# Create billing alarm (optional)
aws cloudwatch put-metric-alarm --alarm-name "BillingAlarm" --alarm-description "Alert when charges exceed $50" --metric-name EstimatedCharges --namespace AWS/Billing --statistic Maximum --period 86400 --threshold 50 --comparison-operator GreaterThanThreshold
```

## 9. Documentation Update
- [ ] Update README.md with actual IP addresses
- [ ] Document any manual changes made
- [ ] Update connection strings in application configs
- [ ] Save important outputs for team reference

## 10. Backup & State Management
```bash
# Backup Terraform state
cp terraform.tfstate terraform.tfstate.backup.$(date +%Y%m%d_%H%M%S)

# Backup important files
tar -czf terraform-backup-$(date +%Y%m%d_%H%M%S).tar.gz *.tf *.tfvars *.md
```

---
**Note**: Chạy các lệnh audit này định kỳ để đảm bảo không có tài nguyên dư thừa và chi phí không mong muốn.
