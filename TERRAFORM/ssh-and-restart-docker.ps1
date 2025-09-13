# Script to SSH into EC2 and restart Docker services
# This script will help you connect to EC2 and manage Docker containers

Write-Host "=== EC2 Connection and Docker Management ===" -ForegroundColor Green

# EC2 Information
$EC2_PUBLIC_IP = "13.211.100.36"
$EC2_PUBLIC_DNS = "ec2-13-211-100-36.ap-southeast-2.compute.amazonaws.com"
$EC2_USER = "ec2-user"
$EC2_PASSWORD = "MySecurePassword123!"

Write-Host "`n📋 EC2 Instance Information:" -ForegroundColor Yellow
Write-Host "   Instance ID: i-01e34ea2551c53c55" -ForegroundColor White
Write-Host "   Instance Type: t3.medium (4GB RAM)" -ForegroundColor White
Write-Host "   Public IP: $EC2_PUBLIC_IP" -ForegroundColor White
Write-Host "   Public DNS: $EC2_PUBLIC_DNS" -ForegroundColor White
Write-Host "   Username: $EC2_USER" -ForegroundColor White

Write-Host "`n🔧 Docker Management Commands:" -ForegroundColor Yellow
Write-Host "   The following commands will be executed on EC2:" -ForegroundColor White

$DOCKER_COMMANDS = @"
# Check Docker status
sudo systemctl status docker

# Restart Docker service
sudo systemctl restart docker

# Check running containers
docker ps -a

# Check Docker images
docker images

# Check system resources
free -h
df -h

# Check if any containers are running
docker ps

# If you have specific containers, you can restart them:
# docker restart <container_name>

# Check Docker logs if needed:
# docker logs <container_name>
"@

Write-Host $DOCKER_COMMANDS -ForegroundColor Cyan

Write-Host "`n🚀 SSH Connection Options:" -ForegroundColor Yellow
Write-Host "`nOption 1: Using SSH with password (if SSH client supports it):" -ForegroundColor White
Write-Host "   ssh $EC2_USER@$EC2_PUBLIC_IP" -ForegroundColor Green
Write-Host "   Password: $EC2_PASSWORD" -ForegroundColor Green

Write-Host "`nOption 2: Using SSH with private key:" -ForegroundColor White
Write-Host "   ssh -i ./config/github_actions_key.pem $EC2_USER@$EC2_PUBLIC_IP" -ForegroundColor Green

Write-Host "`nOption 3: Using PowerShell SSH (if available):" -ForegroundColor White
Write-Host "   ssh $EC2_USER@$EC2_PUBLIC_IP" -ForegroundColor Green

Write-Host "`n🌐 Web Access URLs:" -ForegroundColor Yellow
Write-Host "   HTTP: http://$EC2_PUBLIC_IP" -ForegroundColor Green
Write-Host "   HTTP: http://$EC2_PUBLIC_DNS" -ForegroundColor Green
Write-Host "   Consul UI: http://$EC2_PUBLIC_IP:8500" -ForegroundColor Green
Write-Host "   Portainer: https://$EC2_PUBLIC_IP:9443" -ForegroundColor Green

Write-Host "`n📝 Quick Docker Commands to Run:" -ForegroundColor Yellow
Write-Host "   1. sudo systemctl restart docker" -ForegroundColor White
Write-Host "   2. docker ps -a" -ForegroundColor White
Write-Host "   3. docker images" -ForegroundColor White
Write-Host "   4. free -h" -ForegroundColor White

Write-Host "`n⚠️  Note: After restarting Docker, you may need to:" -ForegroundColor Yellow
Write-Host "   - Restart your application containers" -ForegroundColor White
Write-Host "   - Check if services are running properly" -ForegroundColor White
Write-Host "   - Verify network connectivity" -ForegroundColor White

Write-Host "`n=== Ready to Connect ===" -ForegroundColor Green
Write-Host "Choose your preferred SSH method above and run the commands!" -ForegroundColor White
