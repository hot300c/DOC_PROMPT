output "admin_backend_public_ip" {
  description = "Public IP of the Admin Backend EC2 instance (Elastic IP)"
  value       = aws_eip.admin_eip.public_ip
}

output "admin_backend_instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.admin_backend.id
}

output "rds_endpoint" {
  description = "RDS MySQL endpoint"
  value       = aws_db_instance.mysql.address
}

output "rds_port" {
  description = "RDS port"
  value       = aws_db_instance.mysql.port
}


