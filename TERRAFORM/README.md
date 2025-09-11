# LMA Terraform (Minimal Infra)

Provision minimal AWS infra:
- 1 EC2 (Admin Backend)
- 1 RDS PostgreSQL (single-AZ)

## Prerequisites
- AWS credentials configured (e.g., `aws configure`)
- Terraform >= 1.5
- Existing EC2 key pair name for SSH (optional)

## Quick start
```bash
cd TERRAFORM
terraform init
terraform plan -var "key_pair_name=YOUR_KEYPAIR" -out tfplan
terraform apply "tfplan"
```

## Variables
- `aws_region` (default `ap-southeast-2`)
- `ec2_instance_type` (default `t3.medium`)
- `rds_instance_class` (default `db.t3.micro`)
- `rds_password` (optional; random if omitted)
- `key_pair_name` (for SSH)

## Outputs
- `admin_backend_public_ip`
- `admin_backend_instance_id`
- `rds_endpoint`
- `rds_port`

Notes: Uses default VPC; RDS is private (connect from EC2).
