#!/bin/bash

# Script để cập nhật GitHub Secrets với RDS endpoint từ Terraform
# Usage: ./update-github-secrets.sh [repository-owner/repository-name]

set -e

# Điều hướng đến thư mục terraform
cd "$(dirname "$0")/.."

# Kiểm tra terraform state file
if [ ! -f "terraform.tfstate" ]; then
    echo "Error: terraform.tfstate not found"
    exit 1
fi

# Lấy repository từ argument hoặc sử dụng default
REPO=${1:-"pntsol/lma_backend"}

# Lấy RDS endpoint từ terraform state
RDS_ENDPOINT=$(terraform output -raw rds_endpoint 2>/dev/null || echo "")
RDS_PORT=$(terraform output -raw rds_port 2>/dev/null || echo "")

if [ -z "$RDS_ENDPOINT" ]; then
    echo "Error: Could not get RDS endpoint from terraform state"
    echo "Make sure terraform has been applied successfully"
    exit 1
fi

echo "Updating GitHub Secrets for repository: $REPO"
echo "RDS Endpoint: $RDS_ENDPOINT"
echo "RDS Port: $RDS_PORT"
echo ""

# Kiểm tra GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed"
    echo "Please install GitHub CLI first: https://cli.github.com/"
    exit 1
fi

# Cập nhật GitHub Secrets
echo "Setting RDS_PRIVATE_ENDPOINT secret..."
gh secret set RDS_PRIVATE_ENDPOINT --body "$RDS_ENDPOINT" --repo "$REPO"

echo "Setting RDS_PORT secret..."
gh secret set RDS_PORT --body "$RDS_PORT" --repo "$REPO"

echo ""
echo "✅ GitHub Secrets updated successfully!"
echo ""
echo "Secrets set:"
echo "- RDS_PRIVATE_ENDPOINT: $RDS_ENDPOINT"
echo "- RDS_PORT: $RDS_PORT"
echo ""
echo "You can now use these secrets in your CI/CD pipeline."
