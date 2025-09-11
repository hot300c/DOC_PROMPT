# Terraform Directory Structure

## 📁 Organized Structure

```
TERRAFORM/
├── README.md                    # Main documentation
├── STRUCTURE.md                 # This file - structure overview
├── .gitignore                   # Git ignore rules
├── main.tf                      # Main infrastructure configuration
├── variables.tf                 # Variable definitions
├── outputs.tf                   # Output definitions
├── providers.tf                 # Provider configurations
├── versions.tf                  # Version constraints
├── terraform.tfstate           # Terraform state file (ignored)
├── terraform.tfstate.backup    # State backup (ignored)
├── tfplan                      # Terraform plan file (ignored)
├── .terraform.lock.hcl         # Provider lock file (ignored)
├── .terraform/                  # Terraform working directory (ignored)
├── config/                      # Configuration files
│   ├── terraform.tfvars        # Variable values
│   ├── terraform-user_accessKeys.csv  # AWS credentials (ignored)
│   ├── pnt-ec2-lma-key.pem     # EC2 private key (ignored)
│   └── vnvc-ec2-key.pem        # Alternative EC2 key (ignored)
├── docs/                        # Documentation
│   ├── README.md               # Detailed setup instructions
│   ├── CONFIG_SURVEY.md        # Configuration survey
│   └── AWS_AUDIT_CHECKLIST.md  # Audit checklist
└── scripts/                     # Utility scripts
    ├── audit_aws_resources.sh  # AWS resource audit
    └── terraform_validation.sh # Terraform validation
```

## 🎯 Organization Benefits

### **Root Directory**
- Core Terraform files (`.tf`)
- State files and plans
- Main README for quick reference

### **config/**
- All configuration files
- Sensitive data (keys, credentials)
- Environment-specific settings

### **docs/**
- Detailed documentation
- Checklists and procedures
- Setup guides

### **scripts/**
- Automation scripts
- Validation tools
- Audit utilities

## 🚀 Usage Examples

### Deploy Infrastructure
```bash
terraform plan -var-file="config/terraform.tfvars" -out tfplan
terraform apply "tfplan"
```

### Run Validation
```bash
./scripts/terraform_validation.sh
```

### Run Audit
```bash
./scripts/audit_aws_resources.sh
```

### Connect to EC2
```bash
ssh -i config/pnt-ec2-lma-key.pem ec2-user@$(terraform output -raw admin_backend_public_ip)
```

## 🔒 Security Notes

- **config/** contains sensitive files
- Add `config/` to `.gitignore` in production
- Keep credentials secure
- Rotate keys regularly

## 📋 Maintenance

### Backup
```bash
# Backup state
cp terraform.tfstate terraform.tfstate.backup.$(date +%Y%m%d_%H%M%S)

# Backup entire config
tar -czf terraform-backup-$(date +%Y%m%d_%H%M%S).tar.gz config/ docs/ scripts/ *.tf
```

### Cleanup
```bash
# Remove old plans
rm tfplan

# Clean Terraform cache
rm -rf .terraform/
terraform init
```

## ✅ Best Practices

1. **Never commit sensitive files** (config/*.pem, config/*.csv)
2. **Use version control** for .tf files
3. **Backup state files** regularly
4. **Run validation scripts** before changes
5. **Document changes** in commit messages
6. **Use consistent naming** conventions
7. **Keep scripts executable** (chmod +x)
