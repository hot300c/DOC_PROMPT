# LMA Terraform - Configuration Survey (Fill This File)

Trả lời ngắn gọn theo từng mục (1→9). Mình sẽ cập nhật Terraform tương ứng.

## 1) Khu vực & Dự án
- aws_region: ap-southeast-2
- project_name: LOAN_MANAGEMENT_APPLICATION
- environment: dev

## 2) VPC & Mạng
- use_default_vpc: true
- subnets: (dùng default VPC)

## 3) Truy cập EC2
- access_method: ssh
- key_pair_name (nếu ssh): TODO: điền tên key pair AWS EC2 đã tạo (ví dụ: LMA-Key)
- allow_ssh_cidr (nếu ssh): TODO: điền IP văn phòng dạng x.x.x.x/32 (tạm thời 0.0.0.0/0 nếu cần)

## 4) EC2 - Cấu hình tối thiểu
- ec2_instance_type: t3.small  # gợi ý để giữ chi phí < 60 USD (t3.medium cao hơn)
- ebs_size_gb: 50
- ebs_type: gp3  # gp3 = General Purpose SSD thế hệ mới, chi phí thấp, hiệu năng ổn định
- user_data: install docker  # sẽ cài Docker (yum install docker, enable & start)

## 5) Ứng dụng & Port
- open_http_80: true
- open_https_443: false  # để sau khi có domain/SSL
- has_domain_ssl: false

## 6) Tagging
- required_tags: { Owner: "", Project: "LMA", Env: "dev", CostCenter: "" }

## 7) RDS MySQL
- rds_engine: mysql
- rds_engine_version: TODO: xác nhận phiên bản RDS MySQL hỗ trợ (đề xuất 8.0.x; "9.2.0" không khả dụng trên RDS)
- rds_instance_class: db.t3.micro  # giữ chi phí thấp
- rds_allocated_storage_gb: 20
- rds_storage_autoscale_max_gb: none
- rds_public_access: false
- rds_db_name: lma
- rds_username: "lma_root"
- rds_password: 12347@Abc
- rds_backup_retention_days: 0  # giảm chi phí giai đoạn đầu
- rds_deletion_protection: false

## 8) Kết nối EC2 ↔ RDS
- ec2_connects_to_rds: true
- extra_sg_rules: none

## 9) Giới hạn chi phí ban đầu
- budget_cap_note: tổng chi phí hạ tầng ban đầu mục tiêu < 60 USD/tháng
- guardrails: { max_ec2: t3.small, max_rds: db.t3.micro }

---
Ghi chú thêm (optional):
- Tạo EC2 Key Pair trong AWS Console: EC2 → Key Pairs → Create key pair → đặt tên → lưu file .pem (Linux/Mac) hoặc .ppk (PuTTY/Win). Điền đúng tên key vào `key_pair_name`.
- Thông số t3.medium: 2 vCPU (burstable), ~4 GiB RAM. t3.small: 2 vCPU (burstable), ~2 GiB RAM. gp3 là ổ SSD tổng dụng chung, giá rẻ, IOPS/throughput có thể cấu hình thêm nếu cần. 
