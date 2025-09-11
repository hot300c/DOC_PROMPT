locals {
  name_prefix       = "${var.project_name}-${var.environment}"
  safe_project_name = replace(lower(var.project_name), "_", "-")
  safe_environment  = replace(lower(var.environment), "_", "-")
  id_prefix         = "${local.safe_project_name}-${local.safe_environment}"
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_vpc" "selected" {
  default = var.use_default_vpc
}

data "aws_subnets" "selected" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }
}

resource "aws_security_group" "admin_ec2_sg" {
  name        = "${local.name_prefix}-admin-ec2-sg"
  description = "Security group for Admin Backend EC2"
  vpc_id      = data.aws_vpc.selected.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allow_ssh_cidr]
  }

  dynamic "ingress" {
    for_each = var.open_http_80 ? [1] : []
    content {
      description = "HTTP"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = [var.allow_http_cidr]
    }
  }

  dynamic "ingress" {
    for_each = var.open_https_443 ? [1] : []
    content {
      description = "HTTPS"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = [var.allow_https_cidr]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_ami" "amazon_linux" {
  owners      = ["amazon"]
  most_recent = true
  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "admin_backend" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = var.ec2_instance_type
  subnet_id                   = data.aws_subnets.selected.ids[0]
  vpc_security_group_ids      = [aws_security_group.admin_ec2_sg.id]
  key_name                    = var.key_pair_name
  associate_public_ip_address = true
  user_data                   = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl enable docker
    systemctl start docker
    usermod -aG docker ec2-user
  EOF

  root_block_device {
    volume_size = var.ec2_ebs_size_gb
    volume_type = var.ec2_ebs_type
    delete_on_termination = true
  }

  tags = {
    Name        = "${local.name_prefix}-admin-backend"
    Environment = var.environment
    Project     = var.project_name
  }
}

locals {
  effective_rds_password = var.rds_password
}

resource "aws_security_group" "rds_sg" {
  name        = "${local.name_prefix}-rds-sg"
  description = "Security group for RDS"
  vpc_id      = data.aws_vpc.selected.id

  ingress {
    description = "MySQL from EC2 SG"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    security_groups = [aws_security_group.admin_ec2_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "rds_subnets" {
  name       = "${local.id_prefix}-rds-subnet-group"
  subnet_ids = slice(data.aws_subnets.selected.ids, 0, 2)
}

resource "aws_db_instance" "mysql" {
  identifier                 = "${local.id_prefix}-mysql"
  engine                     = var.rds_engine
  engine_version             = var.rds_engine_version
  instance_class             = var.rds_instance_class
  allocated_storage          = var.rds_allocated_storage
  db_subnet_group_name       = aws_db_subnet_group.rds_subnets.name
  vpc_security_group_ids     = [aws_security_group.rds_sg.id]
  username                   = var.rds_username
  password                   = local.effective_rds_password
  db_name                    = var.rds_db_name
  publicly_accessible        = var.rds_public_access
  skip_final_snapshot        = true
  backup_retention_period    = 0
  deletion_protection        = false
  multi_az                   = false
  apply_immediately          = true
  auto_minor_version_upgrade = true
}

resource "aws_eip" "admin_eip" {
  instance = aws_instance.admin_backend.id
  domain   = "vpc"
  tags = {
    Name        = "${local.name_prefix}-admin-eip"
    Environment = var.environment
    Project     = var.project_name
  }
}


