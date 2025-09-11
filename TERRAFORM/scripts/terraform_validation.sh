#!/bin/bash

# Terraform Configuration Validation Script
# Kiểm tra cấu hình Terraform và so sánh với AWS thực tế

echo "=== TERRAFORM CONFIGURATION VALIDATION ==="
echo "Date: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
if ! command_exists terraform; then
    echo -e "${RED}Error: Terraform not found. Please install Terraform first.${NC}"
    exit 1
fi

if ! command_exists aws; then
    echo -e "${RED}Error: AWS CLI not found. Please install AWS CLI first.${NC}"
    exit 1
fi

# Change to script directory
cd "$(dirname "$0")/.."

echo -e "${GREEN}✓ Prerequisites check passed${NC}"
echo ""

# Initialize Terraform if needed
if [ ! -d ".terraform" ]; then
    echo "Initializing Terraform..."
    terraform init
    echo ""
fi

echo "=== TERRAFORM SYNTAX VALIDATION ==="
echo "Validating Terraform configuration syntax..."
terraform validate
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Terraform configuration syntax is valid${NC}"
else
    echo -e "${RED}✗ Terraform configuration has syntax errors${NC}"
    exit 1
fi
echo ""

echo "=== TERRAFORM FORMAT CHECK ==="
echo "Checking Terraform formatting..."
terraform fmt -check
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Terraform files are properly formatted${NC}"
else
    echo -e "${YELLOW}⚠ Some Terraform files need formatting. Run 'terraform fmt' to fix.${NC}"
fi
echo ""

echo "=== TERRAFORM PLAN VALIDATION ==="
echo "Running Terraform plan to check for changes..."
terraform plan -detailed-exitcode > plan_output.txt 2>&1
PLAN_EXIT_CODE=$?

if [ $PLAN_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ No changes needed. Infrastructure matches configuration.${NC}"
elif [ $PLAN_EXIT_CODE -eq 2 ]; then
    echo -e "${YELLOW}⚠ Changes detected. Infrastructure differs from configuration.${NC}"
    echo "Plan output:"
    cat plan_output.txt
else
    echo -e "${RED}✗ Terraform plan failed with errors.${NC}"
    echo "Error output:"
    cat plan_output.txt
    exit 1
fi
echo ""

echo "=== RESOURCE COUNT VALIDATION ==="
echo "Counting resources in Terraform state..."
EC2_COUNT=$(terraform state list | grep aws_instance | wc -l)
RDS_COUNT=$(terraform state list | grep aws_db_instance | wc -l)
SG_COUNT=$(terraform state list | grep aws_security_group | wc -l)
EIP_COUNT=$(terraform state list | grep aws_eip | wc -l)

echo "Resources in Terraform state:"
echo "  EC2 Instances: $EC2_COUNT"
echo "  RDS Instances: $RDS_COUNT"
echo "  Security Groups: $SG_COUNT"
echo "  Elastic IPs: $EIP_COUNT"
echo ""

echo "=== AWS RESOURCE VERIFICATION ==="
echo "Verifying resources exist in AWS..."

# Check EC2 instances
if [ $EC2_COUNT -gt 0 ]; then
    echo "EC2 instances in AWS:"
    aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table
    echo ""
fi

# Check RDS instances
if [ $RDS_COUNT -gt 0 ]; then
    echo "RDS instances in AWS:"
    aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceStatus,Engine]' --output table
    echo ""
fi

# Check Security Groups
if [ $SG_COUNT -gt 0 ]; then
    echo "Security Groups in AWS:"
    aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupId,GroupName,Description]' --output table
    echo ""
fi

# Check Elastic IPs
if [ $EIP_COUNT -gt 0 ]; then
    echo "Elastic IPs in AWS:"
    aws ec2 describe-addresses --query 'Addresses[*].[AllocationId,PublicIp,InstanceId]' --output table
    echo ""
fi

echo "=== CONFIGURATION DRIFT DETECTION ==="
echo "Checking for configuration drift..."

# Get current outputs
echo "Current Terraform outputs:"
terraform output
echo ""

# Check if resources are running
echo "Resource status check:"
for instance in $(terraform state list | grep aws_instance); do
    instance_id=$(terraform state show $instance | grep -o 'id = "[^"]*"' | cut -d'"' -f2)
    if [ ! -z "$instance_id" ]; then
        state=$(aws ec2 describe-instances --instance-ids $instance_id --query 'Reservations[0].Instances[0].State.Name' --output text)
        echo "  $instance: $state"
    fi
done
echo ""

echo "=== SECURITY CONFIGURATION CHECK ==="
echo "Checking security configurations..."

# Check for overly permissive security groups
echo "Security groups with SSH (port 22) open to 0.0.0.0/0:"
aws ec2 describe-security-groups --filters "Name=ip-permission.from-port,Values=22" --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]' --output table
echo ""

# Check RDS public access
echo "RDS instances with public access:"
aws rds describe-db-instances --query 'DBInstances[?PubliclyAccessible==`true`].[DBInstanceIdentifier,PubliclyAccessible]' --output table
echo ""

echo "=== COST OPTIMIZATION CHECK ==="
echo "Checking for cost optimization opportunities..."

# Check for stopped instances
echo "Stopped EC2 instances:"
aws ec2 describe-instances --filters "Name=instance-state-name,Values=stopped" --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table
echo ""

# Check for unattached EIPs
echo "Unattached Elastic IPs:"
aws ec2 describe-addresses --query 'Addresses[?InstanceId==null].[AllocationId,PublicIp]' --output table
echo ""

echo "=== VALIDATION SUMMARY ==="
if [ $PLAN_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All validations passed. Infrastructure is consistent with configuration.${NC}"
else
    echo -e "${YELLOW}⚠ Some issues detected. Review the output above for details.${NC}"
fi

# Cleanup
rm -f plan_output.txt

echo ""
echo "=== NEXT STEPS ==="
echo "1. Review any warnings or errors above"
echo "2. Run './audit_aws_resources.sh' for detailed AWS resource audit"
echo "3. Check AWS_AUDIT_CHECKLIST.md for manual verification steps"
echo "4. Consider running 'terraform apply' if changes are needed"
