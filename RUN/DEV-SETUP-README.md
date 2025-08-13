# Aladdin Development Environment Setup

Scripts để tự động setup và chạy môi trường development cho dự án Aladdin.

## 📁 Files

### Frontend (Genie)

- `run-dev.ps1` - PowerShell script chính cho frontend
- `run-dev.bat` - Batch script để chạy với test API
- `run-fe-dev-local.bat` - Batch script để chạy với local API
- `clear-cache.ps1` - PowerShell script để clear cache
- `clear-cache.bat` - Batch script để clear cache

### Backend (Aladdin WebService)

- `run-be-dev.ps1` - PowerShell script chính cho backend
- `run-be-dev.bat` - Batch script để chạy backend
- `run-be-tests.ps1` - PowerShell script để chạy tests
- `run-be-tests.bat` - Batch script để chạy tests

### Documentation

- `DEV-SETUP-README.md` - File hướng dẫn này

## 🚀 Cách sử dụng

### Frontend (Genie)

#### Option 1: Sử dụng Test API (Mặc định)

```bash
# Double-click file
run-dev.bat

# Hoặc chạy từ command line
.\run-dev.bat
```

#### Option 2: Sử dụng Local API

```bash
# Double-click file
run-fe-dev-local.bat

# Hoặc chạy từ command line
.\run-fe-dev-local.bat
```

#### Option 3: Chạy trực tiếp PowerShell

```powershell
# Với test API
.\run-dev.ps1

# Với local API
.\run-dev.ps1 -UseLocalApi

# Với custom API URL
.\run-dev.ps1 -ApiUrl "http://localhost:3000" -ApiPrefix "/api"
```

#### Option 4: Clear Cache (nếu gặp lỗi webpack)

```bash
# Double-click file
clear-cache.bat

# Hoặc chạy từ command line
.\clear-cache.bat
```

### Backend (Aladdin WebService)

#### Option 1: Chạy Backend Development Server

```bash
# Double-click file
run-be-dev.bat

# Hoặc chạy từ command line
.\run-be-dev.bat
```

#### Option 2: Chạy Tests

```bash
# Chạy tất cả tests
.\run-be-tests.bat

# Chạy tests với filter
.\run-be-tests.bat -Filter "ws_QuanLyTapTrung"

# Chạy tests với verbose output
.\run-be-tests.bat -Verbose

# Chạy tests trong watch mode
.\run-be-tests.bat -Watch
```

#### Option 3: Chạy trực tiếp PowerShell

```powershell
# Chạy backend
.\run-be-dev.ps1

# Chạy backend với custom port
.\run-be-dev.ps1 -Port 5000

# Chạy backend với Docker
.\run-be-dev.ps1 -UseDocker

# Chỉ build không chạy
.\run-be-dev.ps1 -BuildOnly

# Chạy tests
.\run-be-tests.ps1

# Chạy tests với filter
.\run-be-tests.ps1 -Filter "ws_QuanLyTapTrung" -Verbose
```

### 📁 Vị trí chạy script

Scripts có thể chạy từ:

#### Frontend (Genie)

- **C:\PROJECTS\genie** (thư mục genie trực tiếp)
- **C:\PROJECTS** (thư mục gốc có chứa thư mục genie)

#### Backend (Aladdin)

- **C:\PROJECTS\aladdin** (thư mục aladdin trực tiếp)
- **C:\PROJECTS** (thư mục gốc có chứa thư mục aladdin)

Script sẽ tự động phát hiện và chuyển đến thư mục tương ứng nếu cần.

## ⚙️ Parameters

### Frontend Parameters

| Parameter     | Type   | Default                          | Description                               |
| ------------- | ------ | -------------------------------- | ----------------------------------------- |
| `ApiUrl`      | string | `https://test-aladdin.vnvc.info` | URL của API server                        |
| `ApiPrefix`   | string | `/aladdin`                       | API prefix                                |
| `UseLocalApi` | switch | `false`                          | Sử dụng local API (http://localhost:5272) |

### Backend Parameters

| Parameter     | Type   | Default                     | Description                       |
| ------------- | ------ | --------------------------- | --------------------------------- |
| `Environment` | string | `Development`               | ASP.NET Core environment          |
| `Port`        | string | `5272`                      | Port để chạy WebService           |
| `UseDocker`   | switch | `false`                     | Sử dụng Docker thay vì dotnet run |
| `BuildOnly`   | switch | `false`                     | Chỉ build không chạy server       |
| `TestProject` | string | `WebService.Handlers.Tests` | Tên project test để chạy          |
| `Filter`      | string | `""`                        | Filter để chạy tests cụ thể       |
| `Verbose`     | switch | `false`                     | Hiển thị output chi tiết          |
| `Watch`       | switch | `false`                     | Chạy tests trong watch mode       |

## 🔧 Tính năng

### Frontend Scripts sẽ tự động:

1. ✅ Set environment variables
2. ✅ Tạo file `.env.development` nếu chưa có
3. ✅ Kiểm tra npm installation
4. ✅ Tự động chuyển đến thư mục genie nếu cần
5. ✅ Install dependencies nếu cần (`npm install`)
6. ✅ Clear Next.js cache để tránh lỗi webpack
7. ✅ Chạy development server (`npm run dev`)

### Backend Scripts sẽ tự động:

1. ✅ Kiểm tra .NET installation
2. ✅ Tự động chuyển đến thư mục aladdin nếu cần
3. ✅ Tạo file `appsettings.Development.json` từ sample nếu chưa có
4. ✅ Restore NuGet packages (`dotnet restore`)
5. ✅ Build solution trong Debug mode (`dotnet build`)
6. ✅ Set environment variables (ASPNETCORE_ENVIRONMENT, ASPNETCORE_URLS)
7. ✅ Chạy WebService development server (`dotnet run`)
8. ✅ Hoặc chạy tests với các options khác nhau

## 🛠️ Requirements

### Frontend Requirements

- Windows 10/11
- PowerShell 5.1+
- Node.js 16+
- NPM package manager (có sẵn với Node.js)

### Backend Requirements

- Windows 10/11
- PowerShell 5.1+
- .NET 8.0 SDK
- SQL Server (local hoặc remote)
- Docker (tùy chọn, nếu muốn chạy với Docker)

## 📝 Environment Variables

### Frontend Environment Variables

Script sẽ set các biến môi trường:

```bash
ALADDIN_API_URL=https://test-aladdin.vnvc.info  # hoặc http://localhost:5272
NEXT_PUBLIC_API_PREFIX=/aladdin
```

### Backend Environment Variables

Script sẽ set các biến môi trường:

```bash
ASPNETCORE_ENVIRONMENT=Development
ASPNETCORE_URLS=http://localhost:5272
```

### Database Configuration

Backend cần file `WebService\appsettings.Development.json` với connection strings:

```json
{
  "ConnectionStrings": {
    "Default": "Data Source=localhost;User ID=sa;Password=Test1234;Trust Server Certificate=True",
    "HistoryCentral": "Data Source=localhost;User ID=sa;Password=Test1234;Trust Server Certificate=True"
  }
}
```

## 🚨 Troubleshooting

### Lỗi PowerShell Execution Policy

```powershell
# Chạy PowerShell as Administrator và execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Lỗi NPM không được install

```bash
# Tải và cài đặt Node.js từ: https://nodejs.org/
# NPM sẽ được cài đặt cùng với Node.js
```

### Lỗi Node.js không được install

Tải và cài đặt Node.js từ: https://nodejs.org/

### Lỗi .NET không được install

Tải và cài đặt .NET 8.0 SDK từ: https://dotnet.microsoft.com/download

### Lỗi Database Connection

Nếu gặp lỗi database connection:

1. Kiểm tra SQL Server đã chạy chưa
2. Cập nhật connection strings trong `WebService\appsettings.Development.json`
3. Đảm bảo user có quyền truy cập database
4. Kiểm tra firewall settings

### Lỗi Webpack Cache

Nếu gặp lỗi webpack cache như:

```
Error: ENOENT: no such file or directory, rename '...pack.gz_' -> '...pack.gz'
```

Chạy script clear cache:

```bash
.\clear-cache.bat
```

Hoặc xóa thủ công:

```bash
# Xóa thư mục .next
rmdir /s .next

# Hoặc xóa toàn bộ cache (bao gồm node_modules)
rmdir /s .next node_modules
npm install
```

## 📞 Support

Nếu gặp vấn đề, hãy kiểm tra:

1. PowerShell execution policy
2. NPM installation (cùng với Node.js)
3. Node.js installation
4. Network connectivity (nếu dùng test API)
5. Đảm bảo chạy script từ đúng thư mục (genie hoặc project root)
