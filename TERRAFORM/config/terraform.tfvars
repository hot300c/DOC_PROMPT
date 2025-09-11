aws_region         = "ap-southeast-2"
project_name       = "LOAN_MANAGEMENT_APPLICATION"
environment        = "dev"
use_default_vpc    = true

# Điền đúng tên key pair bạn đã tạo trong AWS EC2 → Key Pairs
key_pair_name      = "pnt-ec2-lma-key"

# Nên đổi thành IP văn phòng của bạn theo dạng x.x.x.x/32 thay vì 0.0.0.0/0
allow_ssh_cidr     = "0.0.0.0/0"

# EC2
ec2_instance_type  = "t3.small"
ec2_ebs_size_gb    = 50
ec2_ebs_type       = "gp3"
open_http_80       = true
open_https_443     = false

# RDS MySQL
rds_engine         = "mysql"
rds_engine_version = "8.0.39"
rds_instance_class = "db.t3.micro"
rds_allocated_storage = 20
rds_db_name        = "lma"
rds_username       = "lma_root"
rds_password       = "123457Abc"
rds_public_access  = false
