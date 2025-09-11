variable "project_name" {
  description = "Project name prefix for resources"
  type        = string
  default     = "LOAN_MANAGEMENT_APPLICATION"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "ap-southeast-2"
}

variable "ec2_instance_type" {
  description = "EC2 instance type for Admin Backend"
  type        = string
  default     = "t3.small"
}

variable "ec2_ebs_size_gb" {
  description = "Root EBS volume size in GB"
  type        = number
  default     = 50
}

variable "ec2_ebs_type" {
  description = "Root EBS volume type"
  type        = string
  default     = "gp3"
}

variable "key_pair_name" {
  description = "Existing AWS key pair name for SSH access"
  type        = string
  default     = null
}

variable "allow_ssh_cidr" {
  description = "CIDR block allowed to access SSH"
  type        = string
  default     = "0.0.0.0/0" # change to your office IP for security
}

variable "allow_http_cidr" {
  description = "CIDR block allowed to access HTTP"
  type        = string
  default     = "0.0.0.0/0"
}

variable "allow_https_cidr" {
  description = "CIDR block allowed to access HTTPS"
  type        = string
  default     = "0.0.0.0/0"
}

variable "rds_engine" {
  description = "RDS engine"
  type        = string
  default     = "mysql"
}

variable "rds_engine_version" {
  description = "RDS engine version"
  type        = string
  default     = "8.0.39"
}

variable "rds_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  description = "Initial RDS storage in GB"
  type        = number
  default     = 20
}

variable "rds_username" {
  description = "Master username for RDS"
  type        = string
  default     = "lma_root"
}

variable "rds_password" {
  description = "Master password for RDS"
  type        = string
  sensitive   = true
  default     = "12347@Abc"
}

variable "use_default_vpc" {
  description = "Whether to deploy into default VPC"
  type        = bool
  default     = true
}

variable "open_http_80" {
  description = "Whether to open HTTP (80) on the EC2 security group"
  type        = bool
  default     = true
}

variable "open_https_443" {
  description = "Whether to open HTTPS (443) on the EC2 security group"
  type        = bool
  default     = false
}

variable "required_tags" {
  description = "Required tags to apply to resources"
  type        = map(string)
  default     = {
    Owner      = ""
    Project    = "LMA"
    Env        = "dev"
    CostCenter = ""
  }
}

variable "rds_public_access" {
  description = "Whether the RDS instance is publicly accessible"
  type        = bool
  default     = true
}

variable "rds_allowed_ips" {
  description = "List of IP addresses/CIDR blocks allowed to access RDS"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # Change to specific IPs for security
}

variable "rds_db_name" {
  description = "Initial database name for RDS"
  type        = string
  default     = "lma"
}


