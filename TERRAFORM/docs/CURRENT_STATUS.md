# LMA Infrastructure - Current Status

## Quick Status (post-terraform apply)

- EC2: Public 13.211.100.36, Private 172.31.13.93
- EC2 Open Ports: 22, 80, 8080, 8082, 8500, 9443 (all 0.0.0.0/0)
- RDS: loan-management-application-dev-mysql.cfiocsmsoith.ap-southeast-2.rds.amazonaws.com:3306

Links:
- Loan Gateway: http://13.211.100.36:8080
- Loan Management: http://13.211.100.36:8082
- Consul UI: http://13.211.100.36:8500
- Portainer: https://13.211.100.36:9443

Server Specs:
- EC2: t3.small, Amazon Linux 2023, 50GB gp3, key `github_actions_key`
- RDS: MySQL 8.0.39, db.t3.micro, 20GB, single-AZ
