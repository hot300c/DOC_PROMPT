#!/bin/bash

# Script để lấy RDS private endpoint từ Terraform state
# Usage: ./get-rds-endpoint.sh

set -e

# Điều hướng đến thư mục terraform
cd "$(dirname "$0")/.."

# Kiểm tra terraform state file
if [ ! -f "terraform.tfstate" ]; then
    echo "Error: terraform.tfstate not found"
    exit 1
fi

# Lấy RDS endpoint từ terraform state
RDS_ENDPOINT=$(terraform output -raw rds_endpoint 2>/dev/null || echo "")

if [ -z "$RDS_ENDPOINT" ]; then
    echo "Error: Could not get RDS endpoint from terraform state"
    echo "Make sure terraform has been applied successfully"
    exit 1
fi

echo "RDS Private Endpoint: $RDS_ENDPOINT"
echo ""
echo "Add this to your GitHub Secrets:"
echo "Secret Name: RDS_PRIVATE_ENDPOINT"
echo "Secret Value: $RDS_ENDPOINT"
echo ""
echo "Or run this command to add to GitHub CLI (if you have gh installed):"
echo "gh secret set RDS_PRIVATE_ENDPOINT --body \"$RDS_ENDPOINT\""
