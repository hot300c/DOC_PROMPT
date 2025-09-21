# Terraform variables for Loan Management Application
# This file contains sensitive configuration - do not commit to version control

# Project Configuration
project_name = "LOAN_MANAGEMENT_APPLICATION"
environment  = "dev"
aws_region   = "ap-southeast-2"

# EC2 Configuration
ec2_instance_type = "t3.medium"
ec2_ebs_size_gb   = 50
ec2_ebs_type      = "gp3"

# Security Configuration - Restrict access to specific IPs
allow_ssh_cidr    = "0.0.0.0/0"  # Open public per request
allow_http_cidr   = "0.0.0.0/0"  # Open public per request
allow_https_cidr  = "0.0.0.0/0"  # Open public per request

# RDS Configuration
rds_engine         = "mysql"
rds_engine_version = "8.0.39"
rds_instance_class = "db.t3.micro"
rds_allocated_storage = 20
rds_username       = "lma_root"
rds_password       = "123457Abc"  # Match with your application config
rds_db_name        = "lma"

# Security: Keep public access but restrict to specific IPs only
rds_public_access = true   # Keep public access but restrict via Security Group
rds_allowed_ips = [
  "0.0.0.0/0",  # Open public per request
]

# Network Configuration
use_default_vpc = true

# Web Access Configuration
open_http_80  = true
open_https_443 = false

# Required Tags
required_tags = {
  Owner      = "DevOps Team"
  Project    = "LMA"
  Env        = "dev"
  CostCenter = "IT"
}
