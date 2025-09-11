# Generate SSH key pair for GitHub Actions
resource "tls_private_key" "github_actions_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Save private key to local file
resource "local_file" "github_actions_private_key" {
  content  = tls_private_key.github_actions_key.private_key_pem
  filename = "${path.module}/config/github_actions_key.pem"
  file_permission = "0400"
}

# Save public key to local file
resource "local_file" "github_actions_public_key" {
  content  = tls_private_key.github_actions_key.public_key_openssh
  filename = "${path.module}/config/github_actions_key.pub"
  file_permission = "0644"
}

# Add public key to EC2 instance
resource "aws_key_pair" "github_actions_key" {
  key_name   = "${local.id_prefix}-github-actions-key"
  public_key = tls_private_key.github_actions_key.public_key_openssh

  tags = merge(var.required_tags, {
    Name = "${local.id_prefix}-github-actions-key"
  })
}
