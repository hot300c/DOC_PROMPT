# Aladdin Backend Development Environment Setup Script
# PowerShell script to automatically setup and run the WebService backend

param(
    [string]$Environment = "Development",
    [string]$Port = "5272",
    [switch]$UseDocker = $false,
    [switch]$BuildOnly = $false
)

Write-Host "🚀 Aladdin Backend Development Environment Setup" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Find aladdin directory from current location
$currentDir = Get-Location
$aladdinDir = $null

# Check if we're already in aladdin directory
$slnPath = Join-Path $currentDir "Aladdin.sln"
if (Test-Path $slnPath) {
    Write-Host "✅ Already in aladdin directory" -ForegroundColor Green
    $aladdinDir = "."
}

# Check if aladdin is in current directory
if (-not $aladdinDir) {
    $parentSlnPath = Join-Path $currentDir "aladdin" "Aladdin.sln"
    if (Test-Path $parentSlnPath) {
        Write-Host "Found aladdin in current directory..." -ForegroundColor Cyan
        $aladdinDir = "aladdin"
    }
}

# Check if we're in DOCS_PROMPT/RUN and need to go up
if (-not $aladdinDir) {
    $parentSlnPath = Join-Path $currentDir ".." ".." "aladdin" "Aladdin.sln"
    if (Test-Path $parentSlnPath) {
        Write-Host "Found aladdin in parent directory..." -ForegroundColor Cyan
        $aladdinDir = "..\..\aladdin"
    }
}

# Check if we're in DOCS_PROMPT and need to go up
if (-not $aladdinDir) {
    $parentSlnPath = Join-Path $currentDir ".." "aladdin" "Aladdin.sln"
    if (Test-Path $parentSlnPath) {
        Write-Host "Found aladdin in parent directory..." -ForegroundColor Cyan
        $aladdinDir = "..\aladdin"
    }
}

# Try to find aladdin in C:\PROJECTS
if (-not $aladdinDir) {
    $projectsAladdinPath = "C:\PROJECTS\aladdin\Aladdin.sln"
    if (Test-Path $projectsAladdinPath) {
        Write-Host "Found aladdin in C:\PROJECTS\aladdin..." -ForegroundColor Cyan
        $aladdinDir = "C:\PROJECTS\aladdin"
    }
}

if (-not $aladdinDir) {
    Write-Host "❌ Cannot find aladdin project." -ForegroundColor Red
    Write-Host "Current directory: $currentDir" -ForegroundColor Yellow
    Write-Host "Please ensure aladdin project exists in one of these locations:" -ForegroundColor Yellow
    Write-Host "  - C:\PROJECTS\aladdin" -ForegroundColor White
    Write-Host "  - Current directory or subdirectory" -ForegroundColor White
    Write-Host "  - Parent directories" -ForegroundColor White
    exit 1
}

# Change to aladdin directory if needed
if ($aladdinDir -ne ".") {
    Write-Host "Changing to aladdin directory: $aladdinDir" -ForegroundColor Cyan
    Set-Location $aladdinDir
}

# Check if .NET is installed
Write-Host "Checking .NET installation..." -ForegroundColor Cyan
try {
    $dotnetVersion = dotnet --version
    Write-Host "✅ .NET version: $dotnetVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ .NET is not installed. Please install .NET 8.0 first:" -ForegroundColor Red
    Write-Host "Download from: https://dotnet.microsoft.com/download" -ForegroundColor Yellow
    exit 1
}

# Check if appsettings.Development.json exists, if not create from sample
$devConfigPath = "WebService\appsettings.Development.json"
$devConfigSamplePath = "WebService\appsettings.Development.json.sample"

if (-not (Test-Path $devConfigPath)) {
    if (Test-Path $devConfigSamplePath) {
        Write-Host "Creating appsettings.Development.json from sample..." -ForegroundColor Cyan
        Copy-Item $devConfigSamplePath $devConfigPath
        Write-Host "✅ Created $devConfigPath" -ForegroundColor Green
        Write-Host "⚠️ Please update database connection strings in $devConfigPath" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Cannot find appsettings.Development.json.sample" -ForegroundColor Red
        Write-Host "Please create $devConfigPath manually" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "✅ $devConfigPath already exists" -ForegroundColor Green
}

# Restore packages
Write-Host "Restoring NuGet packages..." -ForegroundColor Cyan
dotnet restore
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to restore packages" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Packages restored successfully" -ForegroundColor Green

# Build the solution
Write-Host "Building solution..." -ForegroundColor Cyan
dotnet build --configuration Debug
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to build solution" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Solution built successfully" -ForegroundColor Green

if ($BuildOnly) {
    Write-Host "Build completed. Exiting..." -ForegroundColor Green
    exit 0
}

# Set environment variables
$env:ASPNETCORE_ENVIRONMENT = $Environment
$env:ASPNETCORE_URLS = "http://localhost:$Port"

Write-Host "Environment: $env:ASPNETCORE_ENVIRONMENT" -ForegroundColor White
Write-Host "URL: $env:ASPNETCORE_URLS" -ForegroundColor White

# Check if using Docker
if ($UseDocker) {
    Write-Host "Starting with Docker..." -ForegroundColor Cyan
    if (Test-Path "docker-compose.yml") {
        docker-compose up --build
    } else {
        Write-Host "❌ docker-compose.yml not found" -ForegroundColor Red
        exit 1
    }
} else {
    # Start the development server
    Write-Host "Starting WebService development server..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""

    try {
        dotnet run --project WebService\WebService.csproj --configuration Debug
    } catch {
        Write-Host "❌ Failed to start development server" -ForegroundColor Red
        Write-Host "Error: $_" -ForegroundColor Red
        exit 1
    }
}
