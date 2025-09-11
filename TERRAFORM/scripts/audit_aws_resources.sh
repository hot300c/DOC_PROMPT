#!/bin/bash

# AWS Resources Audit Script
# Kiểm tra tài nguyên AWS và so sánh với Terraform state

echo "=== AWS INFRASTRUCTURE AUDIT ==="
echo "Date: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
if ! command_exists aws; then
    echo -e "${RED}Error: AWS CLI not found. Please install AWS CLI first.${NC}"
    exit 1
fi

if ! command_exists terraform; then
    echo -e "${RED}Error: Terraform not found. Please install Terraform first.${NC}"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity >/dev/null 2>&1; then
    echo -e "${RED}Error: AWS credentials not configured. Run 'aws configure' first.${NC}"
    exit 1
fi

# Change to script directory
cd "$(dirname "$0")/.."

echo -e "${GREEN}✓ AWS CLI and Terraform are available${NC}"
echo ""

# Get current AWS account and region
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
echo "AWS Account: $AWS_ACCOUNT"
echo "AWS Region: $AWS_REGION"
echo ""

# Function to get Terraform managed resources
get_terraform_resources() {
    local resource_type=$1
    terraform state list | grep "$resource_type" | sed 's/.*\.//' || echo ""
}

echo "=== TERRAFORM STATE CHECK ==="
echo "Checking Terraform state consistency..."
terraform plan -detailed-exitcode >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Terraform state is consistent${NC}"
elif [ $? -eq 2 ]; then
    echo -e "${YELLOW}⚠ Terraform state has changes${NC}"
else
    echo -e "${RED}✗ Terraform state has errors${NC}"
fi
echo ""

echo "=== EC2 INSTANCES AUDIT ==="
echo "Terraform managed EC2 instances:"
terraform state list | grep aws_instance || echo "None"
echo ""

echo "All EC2 instances in AWS:"
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0],InstanceType]' --output table
echo ""

echo "=== RDS INSTANCES AUDIT ==="
echo "Terraform managed RDS instances:"
terraform state list | grep aws_db_instance || echo "None"
echo ""

echo "All RDS instances in AWS:"
aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceStatus,Engine,DBInstanceClass]' --output table
echo ""

echo "=== SECURITY GROUPS AUDIT ==="
echo "Terraform managed Security Groups:"
terraform state list | grep aws_security_group || echo "None"
echo ""

echo "All Security Groups in AWS:"
aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupId,GroupName,Description]' --output table
echo ""

echo "=== ELASTIC IPs AUDIT ==="
echo "Terraform managed Elastic IPs:"
terraform state list | grep aws_eip || echo "None"
echo ""

echo "All Elastic IPs in AWS:"
aws ec2 describe-addresses --query 'Addresses[*].[AllocationId,PublicIp,InstanceId,AssociationId]' --output table
echo ""

echo "=== VPC & SUBNETS AUDIT ==="
echo "VPCs in AWS:"
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId,IsDefault,State,CidrBlock]' --output table
echo ""

echo "Subnets in AWS:"
aws ec2 describe-subnets --query 'Subnets[*].[SubnetId,VpcId,AvailabilityZone,State,CidrBlock]' --output table
echo ""

echo "=== SECURITY AUDIT ==="
echo "Security Groups with SSH (port 22) open to 0.0.0.0/0:"
aws ec2 describe-security-groups --filters "Name=ip-permission.from-port,Values=22" --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]' --output table
echo ""

echo "RDS instances that are publicly accessible:"
aws rds describe-db-instances --query 'DBInstances[?PubliclyAccessible==`true`].[DBInstanceIdentifier,PubliclyAccessible]' --output table
echo ""

echo "=== COST OPTIMIZATION CHECK ==="
echo "EC2 instances that are stopped:"
aws ec2 describe-instances --filters "Name=instance-state-name,Values=stopped" --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table
echo ""

echo "Unattached Elastic IPs:"
aws ec2 describe-addresses --query 'Addresses[?InstanceId==null].[AllocationId,PublicIp]' --output table
echo ""

echo "=== TERRAFORM OUTPUTS ==="
echo "Current Terraform outputs:"
terraform output
echo ""

echo "=== AUDIT COMPLETE ==="
echo "Review the above output for any orphaned resources or security issues."
echo "Use the AWS_AUDIT_CHECKLIST.md for detailed cleanup procedures."
