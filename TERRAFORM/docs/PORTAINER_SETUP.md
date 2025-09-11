# 🐳 Portainer Setup & Usage Guide

## ✅ **Portainer đã được cài đặt thành công!**

### 🌐 **Truy cập Portainer:**
- **URL**: `https://54.66.35.243:9443`
- **Protocol**: HTTPS (SSL)
- **Status**: ✅ **Đang chạy**

## 🔧 **Thông tin Container:**

```bash
Container ID: 7a081d9e2b68
Image: portainer/portainer-ce:latest
Status: Up and running
Ports: 
  - 8000:8000 (API)
  - 9443:9443 (Web UI)
  - 9000 (Internal)
```

## 🚀 **Cách sử dụng Portainer:**

### 1. **Truy cập Web UI:**
```
https://54.66.35.243:9443
```

### 2. **Setup lần đầu:**
1. Mở trình duyệt và truy cập URL trên
2. Tạo admin user mới:
   - **Username**: `admin` (hoặc tùy chọn)
   - **Password**: Tạo password mạnh
   - **Confirm Password**: Nhập lại password

### 3. **Chọn Environment:**
- Chọn **"Docker"** (Local Docker environment)
- Portainer sẽ tự động detect Docker socket

## 📋 **Tính năng Portainer:**

### 🐳 **Container Management:**
- Xem danh sách containers
- Start/Stop/Restart containers
- Xem logs real-time
- Execute commands trong container
- Monitor resource usage

### 🖼️ **Image Management:**
- Pull images từ Docker Hub
- Build images từ Dockerfile
- Xóa images không cần thiết
- Xem image history

### 🌐 **Network Management:**
- Tạo custom networks
- Quản lý port mappings
- Monitor network traffic

### 💾 **Volume Management:**
- Tạo và quản lý volumes
- Mount volumes vào containers
- Backup/restore data

## 🔧 **Docker Commands qua Portainer:**

### **Chạy container mới:**
```bash
# Nginx web server
docker run -d --name nginx-web -p 8080:80 nginx

# MySQL database
docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 mysql

# Redis cache
docker run -d --name redis-cache -p 6379:6379 redis
```

### **Docker Compose (nếu cần):**
```bash
# Cài Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Chạy docker-compose
docker-compose up -d
```

## 🛡️ **Security Best Practices:**

### 1. **Thay đổi default password:**
- Đăng nhập Portainer
- Settings → Users → Change Password

### 2. **Tạo user riêng:**
- Settings → Users → Add User
- Phân quyền theo role

### 3. **Backup Portainer data:**
```bash
# Backup volume
sudo docker run --rm -v portainer_data:/data -v $(pwd):/backup alpine tar czf /backup/portainer_backup.tar.gz -C /data .
```

## 📊 **Monitoring & Logs:**

### **Xem container logs:**
1. Vào **Containers** tab
2. Click vào container name
3. Chọn **Logs** tab
4. Xem logs real-time

### **Monitor resources:**
1. Vào **Dashboard**
2. Xem CPU, Memory, Network usage
3. Set up alerts nếu cần

## 🔧 **Troubleshooting:**

### **Portainer không truy cập được:**
```bash
# Kiểm tra container status
ssh -i config/pnt-ec2-lma-key.pem ec2-user@54.66.35.243 "sudo docker ps"

# Restart Portainer
ssh -i config/pnt-ec2-lma-key.pem ec2-user@54.66.35.243 "sudo docker restart portainer"
```

### **Docker daemon issues:**
```bash
# Restart Docker service
ssh -i config/pnt-ec2-lma-key.pem ec2-user@54.66.35.243 "sudo systemctl restart docker"
```

### **Port conflicts:**
```bash
# Kiểm tra ports đang sử dụng
ssh -i config/pnt-ec2-lma-key.pem ec2-user@54.66.35.243 "sudo netstat -tlnp"
```

## 📝 **Useful Commands:**

### **SSH vào EC2:**
```bash
ssh -i config/pnt-ec2-lma-key.pem ec2-user@54.66.35.243
```

### **Docker commands:**
```bash
# List containers
sudo docker ps -a

# List images
sudo docker images

# Remove unused containers
sudo docker container prune

# Remove unused images
sudo docker image prune

# System cleanup
sudo docker system prune -a
```

## 🎯 **Next Steps:**

1. **Truy cập Portainer**: `https://54.66.35.243:9443`
2. **Setup admin user**
3. **Deploy applications** qua Portainer UI
4. **Monitor resources** và performance
5. **Setup backups** cho important data

## 📞 **Support:**

- **Portainer Docs**: https://docs.portainer.io/
- **Docker Docs**: https://docs.docker.com/
- **EC2 Instance**: `i-0016db3d37417eb79`
- **Public IP**: `54.66.35.243`
