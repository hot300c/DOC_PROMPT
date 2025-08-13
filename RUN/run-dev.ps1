# Aladdin Development Environment Setup Script
# PowerShell script to automatically setup and run the development environment

param(
    [string]$ApiUrl = "https://test-aladdin.vnvc.info",
    [string]$ApiPrefix = "/aladdin",
    [switch]$UseLocalApi = $false
)

Write-Host "🚀 Aladdin Development Environment Setup" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Set API URL based on parameter
if ($UseLocalApi) {
    $ApiUrl = "http://localhost:5272"
    Write-Host "Using local API: $ApiUrl" -ForegroundColor Yellow
} else {
    Write-Host "Using test API: $ApiUrl" -ForegroundColor Yellow
}

# Set environment variables
Write-Host "Setting environment variables..." -ForegroundColor Cyan
$env:ALADDIN_API_URL = $ApiUrl
$env:NEXT_PUBLIC_API_PREFIX = $ApiPrefix

Write-Host "ALADDIN_API_URL: $env:ALADDIN_API_URL" -ForegroundColor White
Write-Host "NEXT_PUBLIC_API_PREFIX: $env:NEXT_PUBLIC_API_PREFIX" -ForegroundColor White

# Find genie directory from current location
$currentDir = Get-Location
$genieDir = $null

# Check if we're already in genie directory
$packageJsonPath = Join-Path $currentDir "package.json"
if (Test-Path $packageJsonPath) {
    Write-Host "✅ Already in genie directory" -ForegroundColor Green
    $genieDir = "."
}

# Check if genie is in current directory
if (-not $genieDir) {
    $geniePackageJsonPath = Join-Path $currentDir "genie" "package.json"
    if (Test-Path $geniePackageJsonPath) {
        Write-Host "Found genie in current directory..." -ForegroundColor Cyan
        $genieDir = "genie"
    }
}

# Check if we're in DOCS_PROMPT/RUN and need to go up
if (-not $genieDir) {
    $parentGeniePath = Join-Path $currentDir ".." ".." "genie" "package.json"
    if (Test-Path $parentGeniePath) {
        Write-Host "Found genie in parent directory..." -ForegroundColor Cyan
        $genieDir = "..\..\genie"
    }
}

# Check if we're in DOCS_PROMPT and need to go up
if (-not $genieDir) {
    $parentGeniePath = Join-Path $currentDir ".." "genie" "package.json"
    if (Test-Path $parentGeniePath) {
        Write-Host "Found genie in parent directory..." -ForegroundColor Cyan
        $genieDir = "..\genie"
    }
}

# Try to find genie in C:\PROJECTS
if (-not $genieDir) {
    $projectsGeniePath = "C:\PROJECTS\genie\package.json"
    if (Test-Path $projectsGeniePath) {
        Write-Host "Found genie in C:\PROJECTS\genie..." -ForegroundColor Cyan
        $genieDir = "C:\PROJECTS\genie"
    }
}

if (-not $genieDir) {
    Write-Host "❌ Cannot find genie project." -ForegroundColor Red
    Write-Host "Current directory: $currentDir" -ForegroundColor Yellow
    Write-Host "Please ensure genie project exists in one of these locations:" -ForegroundColor Yellow
    Write-Host "  - C:\PROJECTS\genie" -ForegroundColor White
    Write-Host "  - Current directory or subdirectory" -ForegroundColor White
    Write-Host "  - Parent directories" -ForegroundColor White
    exit 1
}

# Change to genie directory if needed
if ($genieDir -ne ".") {
    Write-Host "Changing to genie directory: $genieDir" -ForegroundColor Cyan
    Set-Location $genieDir
}

# Create .env.development file if it doesn't exist
$envFile = ".env.development"
if (-not (Test-Path $envFile)) {
    Write-Host "Creating .env.development file..." -ForegroundColor Cyan
    @"
NEXT_PUBLIC_API_PREFIX=$ApiPrefix
ALADDIN_API_URL=$ApiUrl
"@ | Out-File -FilePath $envFile -Encoding UTF8
    Write-Host "✅ Created $envFile" -ForegroundColor Green
} else {
    Write-Host "✅ $envFile already exists" -ForegroundColor Green
}

# Check if npm is installed
Write-Host "Checking npm installation..." -ForegroundColor Cyan
try {
    $npmVersion = npm --version
    Write-Host "✅ NPM version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ NPM is not installed. Please install Node.js first:" -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check if node_modules exists, if not run npm install
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
}

# Clear Next.js cache to prevent webpack cache issues
Write-Host "Clearing Next.js cache..." -ForegroundColor Cyan
if (Test-Path ".next") {
    try {
        Remove-Item -Path ".next" -Recurse -Force
        Write-Host "✅ Next.js cache cleared" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Warning: Could not clear cache completely: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ No cache to clear" -ForegroundColor Green
}

# Start the development server
Write-Host "Starting development server..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

try {
    yarn dev
} catch {
    Write-Host "❌ Failed to start development server" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}
