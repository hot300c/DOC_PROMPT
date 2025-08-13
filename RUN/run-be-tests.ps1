# Aladdin Backend Tests Runner Script
# PowerShell script to run backend tests

param(
    [string]$TestProject = "WebService.Handlers.Tests",
    [string]$Filter = "",
    [switch]$Verbose = $false,
    [switch]$Watch = $false
)

Write-Host "🧪 Aladdin Backend Tests Runner" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

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

# Check if test project exists
$testProjectPath = "$TestProject\$TestProject.csproj"
if (-not (Test-Path $testProjectPath)) {
    Write-Host "❌ Test project not found: $testProjectPath" -ForegroundColor Red
    Write-Host "Available test projects:" -ForegroundColor Yellow
    Get-ChildItem -Path "." -Filter "*.Tests.csproj" -Recurse | ForEach-Object {
        Write-Host "  - $($_.FullName)" -ForegroundColor White
    }
    exit 1
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

# Build test arguments
$testArgs = @("test", $testProjectPath, "--configuration", "Debug")

if ($Filter) {
    $testArgs += "--filter", $Filter
}

if ($Verbose) {
    $testArgs += "--verbosity", "normal"
} else {
    $testArgs += "--verbosity", "minimal"
}

if ($Watch) {
    $testArgs += "--watch"
}

# Run tests
Write-Host "Running tests..." -ForegroundColor Cyan
Write-Host "Test project: $TestProject" -ForegroundColor White
if ($Filter) {
    Write-Host "Filter: $Filter" -ForegroundColor White
}
if ($Watch) {
    Write-Host "Watch mode: enabled" -ForegroundColor White
}
Write-Host ""

try {
    dotnet $testArgs
} catch {
    Write-Host "❌ Failed to run tests" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}
