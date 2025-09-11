# LMA Terraform (Minimal Infra)

Provision minimal AWS infra:
- 1 EC2 (Admin Backend)
- 1 RDS MySQL (single-AZ, private)

## Prerequisites
- AWS credentials configured (see setup below)
- Terraform >= 1.5

## Install AWS CLI (if not installed)
```bash
# macOS (using Homebrew)
brew install awscli

# macOS (using pip)
pip3 install awscli

# Verify installation
aws --version
```

## Get AWS Access Keys

### Step 1: Create IAM User
1. **AWS Console** → **IAM** → **Users** → **Create user**
2. **User name**: `terraform-user` (or any name)
3. **Access type**: ✅ Programmatic access
4. **Next**: Permissions

### Step 2: Attach Policies
1. **Attach policies directly** → Search and select:
   - `AmazonEC2FullAccess`
   - `AmazonRDSFullAccess`
   - `AmazonVPCFullAccess`
2. **Next**: Tags (optional)
3. **Next**: Review → **Create user**

### Step 3: Download Credentials
1. **Important**: Download `.csv` file or copy:
   - **Access Key ID**: `AKIA...` (20 characters)
   - **Secret Access Key**: `...` (40 characters)
2. **Save securely** - you won't see the secret key again!

## Setup AWS Credentials
```bash
# Option 1: AWS CLI
aws configure
# Enter: Access Key ID, Secret Access Key, Region (ap-southeast-2), Output format (json)

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="ap-southeast-2"
```

## Install Terraform (if not installed)

### macOS (using Homebrew)
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

### macOS (manual download)
```bash
# Download from https://developer.hashicorp.com/terraform/downloads
# Extract and move to /usr/local/bin/
sudo mv terraform /usr/local/bin/
```

### Verify installation
```bash
terraform version
```

## Create EC2 Key Pair (if not exists)
1. AWS Console → EC2 → Key Pairs → Create key pair
2. Name: `pnt-ec2-lma-key`
3. Type: RSA, Format: .pem (Linux/Mac)
4. Download and save to TERRAFORM folder
5. Set permissions: `chmod 400 pnt-ec2-lma-key.pem`

## Quick start
```bash
cd TERRAFORM

# Deploy infrastructure
terraform init
terraform plan -out tfplan
terraform apply "tfplan"
```

## Configuration
All settings are pre-configured in `terraform.tfvars` based on `CONFIG_SURVEY.md`:
- **EC2**: t3.small, 50GB gp3, Docker pre-installed
- **RDS**: MySQL 8.0.39, db.t3.micro, private access
- **Network**: Default VPC, HTTP enabled, HTTPS disabled
- **Key Pair**: `pnt-ec2-lma-key` (create in AWS Console)

## Outputs
- `admin_backend_public_ip`
- `admin_backend_instance_id`
- `rds_endpoint`
- `rds_port`

## SSH vào EC2 sau khi deploy
```bash
ssh -i pnt-ec2-lma-key.pem ec2-user@$(terraform output -raw admin_backend_public_ip)
```

Notes: Uses default VPC; RDS is private (connect from EC2). Elastic IP attached to EC2.
