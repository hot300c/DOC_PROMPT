# LMA Terraform Infrastructure

Minimal AWS infrastructure for Loan Management Application.

## 📁 Directory Structure

```
TERRAFORM/
├── README.md                    # This file
├── main.tf                      # Main infrastructure configuration
├── variables.tf                 # Variable definitions
├── outputs.tf                   # Output definitions
├── providers.tf                 # Provider configurations
├── versions.tf                  # Version constraints
├── terraform.tfstate           # Terraform state file
├── terraform.tfstate.backup    # State backup
├── tfplan                      # Terraform plan file
├── config/                     # Configuration files
│   ├── terraform.tfvars       # Variable values
│   ├── terraform-user_accessKeys.csv  # AWS credentials
│   ├── pnt-ec2-lma-key.pem    # EC2 private key
│   └── vnvc-ec2-key.pem       # Alternative EC2 key
├── docs/                       # Documentation
│   ├── README.md              # Detailed documentation
│   ├── CONFIG_SURVEY.md       # Configuration survey
│   └── AWS_AUDIT_CHECKLIST.md # Audit checklist
└── scripts/                    # Utility scripts
    ├── audit_aws_resources.sh # AWS resource audit
    └── terraform_validation.sh # Terraform validation
```

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured
- Terraform >= 1.5
- EC2 Key Pair created

### Deploy Infrastructure
```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var-file="config/terraform.tfvars" -out tfplan

# Apply changes
terraform apply "tfplan"
```

### Connect to EC2
```bash
# Using Terraform output (now accurate)
ssh -i config/github_actions_key.pem ec2-user@$(terraform output -raw admin_backend_public_ip)

# Or directly with IP
ssh -i config/github_actions_key.pem ec2-user@13.211.100.36
```

## 🔧 Configuration

All configuration is in `config/terraform.tfvars`:
- **EC2**: t3.small, 50GB gp3, Docker pre-installed
- **RDS**: MySQL 8.0.39, db.t3.micro, private access
- **Network**: Default VPC, HTTP enabled, HTTPS disabled
- **Key Pair**: `pnt-ec2-lma-key`

## 📋 Validation & Audit

### Terraform Validation
```bash
./scripts/terraform_validation.sh
```

### AWS Resource Audit
```bash
./scripts/audit_aws_resources.sh
```

### Manual Checklist
See `docs/AWS_AUDIT_CHECKLIST.md` for detailed manual verification steps.

## 📊 Outputs

- `admin_backend_public_ip` - EC2 public IP (13.211.100.36)
- `admin_backend_instance_id` - EC2 instance ID (i-01e34ea2551c53c55)
- `rds_endpoint` - RDS MySQL endpoint
- `rds_port` - RDS port (3306)
- `github_actions_private_key` - SSH private key for GitHub Actions
- `github_actions_public_key` - SSH public key for GitHub Actions
- `ssh_key_file_path` - Path to private key file

## 🌐 Application Access

- **Loan Gateway**: http://13.211.100.36:8080
- **Loan Management Service**: http://13.211.100.36:8082
- **Consul UI**: http://13.211.100.36:8500
- **Portainer**: https://13.211.100.36:9443

## 🔒 Security

- **RDS**: Private access only (accessible from EC2 security group)
- **SSH**: Key pair authentication only (`github_actions_key`)
- **Security Groups**: 
  - EC2 SG: Ports 22, 80, 8080, 8082, 8500, 9443
  - RDS SG: Port 3306 (MySQL) from EC2 SG only
- **Network**: Default VPC with public subnet
- **IAM**: EC2 instance profile for Systems Manager access

## 💰 Cost Optimization

- t3.small EC2 instance
- db.t3.micro RDS instance
- 50GB gp3 storage
- No backup retention (dev environment)

## 📚 Documentation

- `docs/README.md` - Detailed setup instructions
- `docs/CONFIG_SURVEY.md` - Configuration survey
- `docs/AWS_AUDIT_CHECKLIST.md` - Audit procedures

## 🛠️ Maintenance

### Update Infrastructure
```bash
terraform plan -var-file="config/terraform.tfvars"
terraform apply
```

### Destroy Infrastructure
```bash
terraform destroy -var-file="config/terraform.tfvars"
```

### Backup State
```bash
cp terraform.tfstate terraform.tfstate.backup.$(date +%Y%m%d_%H%M%S)
```