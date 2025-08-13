# Clear Next.js Cache Script
# PowerShell script to clear Next.js cache and node_modules

param(
    [switch]$ClearAll = $false
)

Write-Host "🧹 Next.js Cache Cleaner" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green

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

# Clear Next.js cache
Write-Host "Clearing Next.js cache..." -ForegroundColor Cyan
if (Test-Path ".next") {
    try {
        Remove-Item -Path ".next" -Recurse -Force
        Write-Host "✅ Next.js cache cleared" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Warning: Could not clear cache completely: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ No .next cache to clear" -ForegroundColor Green
}

# Clear npm cache if requested
if ($ClearAll) {
    Write-Host "Clearing npm cache..." -ForegroundColor Cyan
    try {
        npm cache clean --force
        Write-Host "✅ NPM cache cleared" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Warning: Could not clear npm cache: $_" -ForegroundColor Yellow
    }
    
    Write-Host "Removing node_modules..." -ForegroundColor Cyan
    if (Test-Path "node_modules") {
        try {
            Remove-Item -Path "node_modules" -Recurse -Force
            Write-Host "✅ node_modules removed" -ForegroundColor Green
            Write-Host "Run 'npm install' to reinstall dependencies" -ForegroundColor Yellow
        } catch {
            Write-Host "⚠️ Warning: Could not remove node_modules completely: $_" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✅ No node_modules to remove" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "🎉 Cache clearing completed!" -ForegroundColor Green
if ($ClearAll) {
    Write-Host "Next time you run the development server, it will reinstall dependencies." -ForegroundColor Yellow
}
