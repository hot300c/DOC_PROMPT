# Script to setup environment variables for Terraform and AWS CLI
# Run this script before using Terraform or AWS CLI

Write-Host "=== Setting up Development Environment ===" -ForegroundColor Green

# Terraform path
$TERRAFORM_PATH = "C:\Users\ADMIN\AppData\Local\Microsoft\WinGet\Packages\Hashicorp.Terraform_Microsoft.Winget.Source_8wekyb3d8bbwe"

# AWS CLI path
$AWS_CLI_PATH = "C:\Program Files\Amazon\AWSCLIV2"

# Check if paths exist
if (Test-Path $TERRAFORM_PATH) {
    Write-Host "✅ Found Terraform at: $TERRAFORM_PATH" -ForegroundColor Green
} else {
    Write-Host "❌ Terraform not found at: $TERRAFORM_PATH" -ForegroundColor Red
    Write-Host "   Please install Terraform first" -ForegroundColor Yellow
    exit 1
}

if (Test-Path $AWS_CLI_PATH) {
    Write-Host "✅ Found AWS CLI at: $AWS_CLI_PATH" -ForegroundColor Green
} else {
    Write-Host "❌ AWS CLI not found at: $AWS_CLI_PATH" -ForegroundColor Red
    Write-Host "   Please install AWS CLI first" -ForegroundColor Yellow
    exit 1
}

# Add to PATH for current session
Write-Host "`nAdding tools to PATH for current session..." -ForegroundColor Yellow
$env:PATH += ";$TERRAFORM_PATH;$AWS_CLI_PATH"

# Verify installations
Write-Host "`nVerifying installations..." -ForegroundColor Yellow

Write-Host "`nTerraform version:" -ForegroundColor Cyan
terraform version

Write-Host "`nAWS CLI version:" -ForegroundColor Cyan
aws --version

Write-Host "`n=== Environment Setup Complete ===" -ForegroundColor Green
Write-Host "✅ Terraform and AWS CLI are now available in this session" -ForegroundColor Green
Write-Host "`nTo make this permanent, add these paths to your system PATH:" -ForegroundColor Yellow
Write-Host "   $TERRAFORM_PATH" -ForegroundColor White
Write-Host "   $AWS_CLI_PATH" -ForegroundColor White

Write-Host "`nYou can now run:" -ForegroundColor Yellow
Write-Host "   terraform plan" -ForegroundColor White
Write-Host "   terraform apply" -ForegroundColor White
Write-Host "   aws ec2 describe-instances" -ForegroundColor White
