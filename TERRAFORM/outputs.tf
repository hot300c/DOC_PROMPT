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

output "github_actions_private_key" {
  description = "Private key for GitHub Actions SSH access"
  value       = tls_private_key.github_actions_key.private_key_pem
  sensitive   = true
}

output "github_actions_public_key" {
  description = "Public key for GitHub Actions SSH access"
  value       = tls_private_key.github_actions_key.public_key_openssh
}

output "ssh_key_file_path" {
  description = "Path to the private key file"
  value       = local_file.github_actions_private_key.filename
}


