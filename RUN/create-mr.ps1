# GitLab Merge Request Creator Script
# PowerShell script to create Merge Request on GitLab

param(
    [Parameter(Mandatory=$false)]
    [string]$Title = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Description = "",
    
    [Parameter(Mandatory=$false)]
    [string]$SourceBranch = "",
    
    [Parameter(Mandatory=$false)]
    [string]$TargetBranch = "main",
    
    [Parameter(Mandatory=$false)]
    [switch]$OpenBrowser = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$ShowHelp = $false
)

# Function to show help
function Show-Help {
    Write-Host "🔗 GitLab Merge Request Creator" -ForegroundColor Green
    Write-Host "===============================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\create-mr.ps1 [Options]" -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Title <title>                 MR title (required)" -ForegroundColor White
    Write-Host "  -Description <description>     MR description" -ForegroundColor White
    Write-Host "  -SourceBranch <branch>         Source branch (default: current branch)" -ForegroundColor White
    Write-Host "  -TargetBranch <branch>         Target branch (default: main)" -ForegroundColor White
    Write-Host "  -OpenBrowser                   Open MR in browser after creation" -ForegroundColor White
    Write-Host "  -ShowHelp                      Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  # Create MR with title" -ForegroundColor White
    Write-Host "  .\create-mr.ps1 -Title 'Add new feature'" -ForegroundColor White
    Write-Host ""
    Write-Host "  # Create MR with title and description" -ForegroundColor White
    Write-Host "  .\create-mr.ps1 -Title 'Fix bug' -Description 'Fixes issue #123'" -ForegroundColor White
    Write-Host ""
    Write-Host "  # Create MR and open in browser" -ForegroundColor White
    Write-Host "  .\create-mr.ps1 -Title 'Update docs' -OpenBrowser" -ForegroundColor White
    Write-Host ""
    Write-Host "Prerequisites:" -ForegroundColor Cyan
    Write-Host "  • Git repository with remote origin" -ForegroundColor White
    Write-Host "  • GitLab CLI (glab) installed and authenticated" -ForegroundColor White
    Write-Host "  • Current branch pushed to origin" -ForegroundColor White
}

# Function to check if git repository exists
function Test-GitRepository {
    if (-not (Test-Path ".git")) {
        Write-Host "❌ Not a git repository. Please run this script from a git repository." -ForegroundColor Red
        exit 1
    }
}

# Function to check if glab is installed
function Test-GlabInstallation {
    try {
        $glabVersion = glab --version
        Write-Host "✅ GitLab CLI version: $glabVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ GitLab CLI (glab) is not installed." -ForegroundColor Red
        Write-Host "Please install GitLab CLI from: https://gitlab.com/gitlab-org/cli" -ForegroundColor Yellow
        Write-Host "Or run: winget install GitLab.GitLabCLI" -ForegroundColor Yellow
        exit 1
    }
}

# Function to check if glab is authenticated
function Test-GlabAuthentication {
    try {
        $authStatus = glab auth status
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ GitLab CLI not authenticated." -ForegroundColor Red
            Write-Host "Please authenticate with: glab auth login" -ForegroundColor Yellow
            exit 1
        }
        Write-Host "✅ GitLab CLI authenticated" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to check GitLab CLI authentication." -ForegroundColor Red
        exit 1
    }
}

# Function to get current branch
function Get-CurrentBranch {
    $currentBranch = git branch --show-current
    return $currentBranch
}

# Function to get remote URL
function Get-RemoteUrl {
    $remoteUrl = git remote get-url origin
    return $remoteUrl
}

# Function to check if branch exists on remote
function Test-RemoteBranch {
    param([string]$BranchName)
    
    $remoteBranches = git ls-remote --heads origin $BranchName
    return $remoteBranches -ne ""
}

# Function to create Merge Request
function New-MergeRequest {
    param(
        [string]$Title,
        [string]$Description,
        [string]$SourceBranch,
        [string]$TargetBranch,
        [bool]$OpenBrowser
    )
    
    Write-Host "🔗 Creating Merge Request..." -ForegroundColor Cyan
    Write-Host "Source branch: $SourceBranch" -ForegroundColor White
    Write-Host "Target branch: $TargetBranch" -ForegroundColor White
    Write-Host "Title: $Title" -ForegroundColor White
    
    # Check if source branch exists on remote
    if (-not (Test-RemoteBranch -BranchName $SourceBranch)) {
        Write-Host "❌ Source branch '$SourceBranch' does not exist on remote." -ForegroundColor Red
        Write-Host "Please push your branch first: git push origin $SourceBranch" -ForegroundColor Yellow
        exit 1
    }
    
    # Build glab command
    $glabArgs = @("mr", "create", "--title", $Title, "--source-branch", $SourceBranch, "--target-branch", $TargetBranch)
    
    if (-not [string]::IsNullOrWhiteSpace($Description)) {
        $glabArgs += "--description", $Description
    }
    
    if ($OpenBrowser) {
        $glabArgs += "--web"
    }
    
    # Create MR
    Write-Host "Executing: glab $($glabArgs -join ' ')" -ForegroundColor Cyan
    glab $glabArgs
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create Merge Request" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Merge Request created successfully!" -ForegroundColor Green
    
    if (-not $OpenBrowser) {
        Write-Host "💡 To open MR in browser, run:" -ForegroundColor Yellow
        Write-Host "   glab mr view" -ForegroundColor White
    }
}

# Main script logic
if ($ShowHelp) {
    Show-Help
    exit 0
}

# Check prerequisites
Test-GitRepository
Test-GlabInstallation
Test-GlabAuthentication

# Get current branch if not specified
if ([string]::IsNullOrWhiteSpace($SourceBranch)) {
    $SourceBranch = Get-CurrentBranch
}

# Check if title is provided
if ([string]::IsNullOrWhiteSpace($Title)) {
    Write-Host "❌ MR title is required. Use -Title <title>" -ForegroundColor Red
    Write-Host ""
    Show-Help
    exit 1
}

# Create Merge Request
New-MergeRequest -Title $Title -Description $Description -SourceBranch $SourceBranch -TargetBranch $TargetBranch -OpenBrowser $OpenBrowser
