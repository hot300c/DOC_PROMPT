# Git Flow Automation Script
# PowerShell script to automate Git Flow operations

param(
    [Parameter(Mandatory=$false)]
    [string]$BranchName = "",
    
    [Parameter(Mandatory=$false)]
    [string]$CommitMessage = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$NewFeature = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$ContinueFeature = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$Push = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$Rebase = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$ShowHelp = $false
)

# Function to show help
function Show-Help {
    Write-Host "🚀 Git Flow Automation Script" -ForegroundColor Green
    Write-Host "=============================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\git-flow.ps1 [Options]" -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -NewFeature branch_name message         Tạo feature mới (commit lần đầu)" -ForegroundColor White
    Write-Host "  -ContinueFeature message                 Tiếp tục feature (commit --amend)" -ForegroundColor White
    Write-Host "  -Push                                   Push branch lên remote" -ForegroundColor White
    Write-Host "  -Rebase                                 Rebase với main" -ForegroundColor White
    Write-Host "  -ShowHelp                               Hiển thị help" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  # Tạo feature mới" -ForegroundColor White
    Write-Host "  .\git-flow-simple.ps1 -NewFeature feature/login 'Add login feature'" -ForegroundColor White
    Write-Host ""
    Write-Host "  # Tiếp tục feature hiện tại" -ForegroundColor White
    Write-Host "  .\git-flow-simple.ps1 -ContinueFeature 'Fix login bug'" -ForegroundColor White
    Write-Host ""
    Write-Host "  # Push branch" -ForegroundColor White
    Write-Host "  .\git-flow-simple.ps1 -Push" -ForegroundColor White
    Write-Host ""
    Write-Host "  # Rebase với main" -ForegroundColor White
    Write-Host "  .\git-flow-simple.ps1 -Rebase" -ForegroundColor White
    Write-Host ""
    Write-Host "Git Flow Rules:" -ForegroundColor Cyan
    Write-Host "  • Feature mới: git commit (lần đầu)" -ForegroundColor White
    Write-Host "  • Feature cũ: git commit --amend (tiếp tục)" -ForegroundColor White
    Write-Host "  • Luôn rebase với main trước khi push" -ForegroundColor White
}

# Function to find git repository
function Find-GitRepository {
    $currentDir = Get-Location
    
    # Check if we're already in a git repository
    if (Test-Path ".git") {
        Write-Host "✅ Already in git repository" -ForegroundColor Green
        return "."
    }
    
    # Check if we're in DOCS_PROMPT/RUN and need to go up
    $parentGitPath = "$currentDir\..\..\.git"
    if (Test-Path $parentGitPath) {
        Write-Host "Found git repository in parent directory..." -ForegroundColor Cyan
        return "..\.."
    }
    
    # Check if we're in DOCS_PROMPT and need to go up
    $parentGitPath = "$currentDir\..\.git"
    if (Test-Path $parentGitPath) {
        Write-Host "Found git repository in parent directory..." -ForegroundColor Cyan
        return ".."
    }
    
    # Try to find git repository in C:\PROJECTS
    $projectsGitPath = "C:\PROJECTS\.git"
    if (Test-Path $projectsGitPath) {
        Write-Host "Found git repository in C:\PROJECTS..." -ForegroundColor Cyan
        return "C:\PROJECTS"
    }
    
    # Try to find git repository in subdirectories
    $subdirs = @("aladdin", "genie", "qas-db", "qas-db-dev")
    foreach ($subdir in $subdirs) {
        $subdirGitPath = "$currentDir\$subdir\.git"
        if (Test-Path $subdirGitPath) {
            Write-Host "Found git repository in $subdir..." -ForegroundColor Cyan
            return $subdir
        }
    }
    
    # Try to find git repository in parent subdirectories
    foreach ($subdir in $subdirs) {
        $subdirGitPath = "$currentDir\..\$subdir\.git"
        if (Test-Path $subdirGitPath) {
            Write-Host "Found git repository in ..\$subdir..." -ForegroundColor Cyan
            return "..\$subdir"
        }
    }
    
    Write-Host "❌ Cannot find git repository." -ForegroundColor Red
    Write-Host "Current directory: $currentDir" -ForegroundColor Yellow
    Write-Host "Please ensure git repository exists in one of these locations:" -ForegroundColor Yellow
    Write-Host "  - Current directory or subdirectory" -ForegroundColor White
    Write-Host "  - Parent directories" -ForegroundColor White
    Write-Host "  - C:\PROJECTS" -ForegroundColor White
    exit 1
}

# Function to check if git repository exists and change to it
function Test-GitRepository {
    $gitDir = Find-GitRepository
    
    # Change to git repository if needed
    if ($gitDir -ne ".") {
        Write-Host "Changing to git repository: $gitDir" -ForegroundColor Cyan
        Set-Location $gitDir
    }
}

# Function to check if git is installed
function Test-GitInstallation {
    try {
        $gitVersion = git --version
        Write-Host "✅ Git version: $gitVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
        exit 1
    }
}

# Function to get current branch
function Get-CurrentBranch {
    $currentBranch = git branch --show-current
    return $currentBranch
}

# Function to show git status
function Show-GitStatus {
    Write-Host "📊 Git Status:" -ForegroundColor Cyan
    Write-Host "Current branch: $(Get-CurrentBranch)" -ForegroundColor White
    Write-Host ""
    git status --short
}

# Function to create new branch from main
function New-FeatureBranch {
    param([string]$BranchName)
    
    Write-Host "🔄 Creating new branch: $BranchName" -ForegroundColor Cyan
    
    # Check if branch name is provided
    if ([string]::IsNullOrWhiteSpace($BranchName)) {
        Write-Host "❌ Branch name is required. Use -NewFeature branch_name message" -ForegroundColor Red
        exit 1
    }
    
    # Check if branch already exists
    $existingBranch = git branch --list $BranchName
    if ($existingBranch) {
        Write-Host "⚠️ Branch '$BranchName' already exists. Switching to it..." -ForegroundColor Yellow
        git checkout $BranchName
        return
    }
    
    # Update main branch
    Write-Host "Updating main branch..." -ForegroundColor Cyan
    git checkout main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to checkout main branch" -ForegroundColor Red
        exit 1
    }
    
    git pull
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to pull latest changes from main" -ForegroundColor Red
        exit 1
    }
    
    # Create new branch
    Write-Host "Creating new branch from main..." -ForegroundColor Cyan
    git checkout -b $BranchName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create new branch" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Successfully created and switched to branch: $BranchName" -ForegroundColor Green
    Write-Host "💡 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Make your changes" -ForegroundColor White
    Write-Host "   2. Add files: git add -p" -ForegroundColor White
    Write-Host "   3. Initial commit: .\git-flow.ps1 -Commit 'Your message'" -ForegroundColor White
}

# Function to make initial commit
function New-InitialCommit {
    param([string]$CommitMessage)
    
    Write-Host "💾 Making initial commit..." -ForegroundColor Cyan
    
    # Check if commit message is provided
    if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
        Write-Host "❌ Commit message is required. Use -ContinueFeature message" -ForegroundColor Red
        exit 1
    }
    
    # Check if there are staged changes
    $stagedChanges = git diff --cached --name-only
    if (-not $stagedChanges) {
        Write-Host "⚠️ No staged changes found. Please add files first:" -ForegroundColor Yellow
        Write-Host "   git add -p" -ForegroundColor White
        exit 1
    }
    
    # Make commit
    git commit -m $CommitMessage
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to commit changes" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Successfully committed changes" -ForegroundColor Green
    Write-Host "💡 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Push branch: .\git-flow.ps1 -Push" -ForegroundColor White
    Write-Host "   2. Create Merge Request on GitLab" -ForegroundColor White
}

# Function to amend last commit
function Update-LastCommit {
    Write-Host "📝 Amending last commit..." -ForegroundColor Cyan
    
    # Check if there are changes to commit
    $unstagedChanges = git diff --name-only
    $stagedChanges = git diff --cached --name-only
    
    if (-not $unstagedChanges -and -not $stagedChanges) {
        Write-Host "⚠️ No changes to commit" -ForegroundColor Yellow
        return
    }
    
    # Add all changes
    git add .
    
    # Amend commit
    git commit --amend --no-edit
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to amend commit" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Successfully amended last commit" -ForegroundColor Green
    Write-Host "💡 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Force push: .\git-flow.ps1 -ForcePush" -ForegroundColor White
}

# Function to push branch
function Push-Branch {
    Write-Host "🚀 Pushing branch to origin..." -ForegroundColor Cyan
    
    $currentBranch = Get-CurrentBranch
    
    # Check if we're on main branch
    if ($currentBranch -eq "main") {
        Write-Host "⚠️ You're on main branch. Are you sure you want to push to main?" -ForegroundColor Yellow
        $confirm = Read-Host "Type 'yes' to continue"
        if ($confirm -ne "yes") {
            Write-Host "Push cancelled" -ForegroundColor Yellow
            return
        }
    }
    
    # Push branch
    git push origin $currentBranch
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to push branch" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Successfully pushed branch: $currentBranch" -ForegroundColor Green
    Write-Host "💡 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Create Merge Request on GitLab" -ForegroundColor White
    Write-Host "   2. Or continue working and use -Amend for changes" -ForegroundColor White
}

# Function to force push branch
function Force-PushBranch {
    Write-Host "💪 Force pushing branch to origin..." -ForegroundColor Cyan
    
    $currentBranch = Get-CurrentBranch
    
    # Check if we're on main branch
    if ($currentBranch -eq "main") {
        Write-Host "⚠️ You're on main branch. Force pushing to main is dangerous!" -ForegroundColor Red
        $confirm = Read-Host "Type 'yes' to continue"
        if ($confirm -ne "yes") {
            Write-Host "Force push cancelled" -ForegroundColor Yellow
            return
        }
    }
    
    # Force push branch
    git push origin -f $currentBranch
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to force push branch" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Successfully force pushed branch: $currentBranch" -ForegroundColor Green
}

# Function to rebase with main
function Update-RebaseMain {
    Write-Host "🔄 Rebasing with main..." -ForegroundColor Cyan
    
    $currentBranch = Get-CurrentBranch
    
    # Check if we're on main branch
    if ($currentBranch -eq "main") {
        Write-Host "⚠️ You're on main branch. No need to rebase." -ForegroundColor Yellow
        return
    }
    
    # Fetch latest changes from main
    Write-Host "Fetching latest changes from main..." -ForegroundColor Cyan
    git fetch origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to fetch from origin main" -ForegroundColor Red
        exit 1
    }
    
    # Rebase with main
    Write-Host "Rebasing current branch with main..." -ForegroundColor Cyan
    git rebase origin/main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Rebase failed. Please resolve conflicts manually:" -ForegroundColor Red
        Write-Host "   1. Resolve conflicts in the files" -ForegroundColor White
        Write-Host "   2. git add resolved-files" -ForegroundColor White
        Write-Host "   3. git rebase --continue" -ForegroundColor White
        Write-Host "   4. Or git rebase --abort to cancel" -ForegroundColor White
        exit 1
    }
    
    Write-Host "✅ Successfully rebased with main" -ForegroundColor Green
    Write-Host "💡 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Force push: .\git-flow.ps1 -ForcePush" -ForegroundColor White
}

# Main script logic
if ($ShowHelp) {
    Show-Help
    exit 0
}

# Check git installation and repository
Test-GitInstallation
Test-GitRepository

# Show status if requested
if ($ShowStatus) {
    Show-GitStatus
    exit 0
}

# Execute requested operations
if ($NewFeature) {
    New-FeatureBranch -BranchName $BranchName
    New-InitialCommit -CommitMessage $CommitMessage
}

if ($ContinueFeature) {
    Update-LastCommit
}

if ($Push) {
    Push-Branch
}

if ($Rebase) {
    Update-RebaseMain
}

# If no operation specified, show help
if (-not ($NewFeature -or $ContinueFeature -or $Push -or $Rebase -or $ShowHelp)) {
    Write-Host "⚠️ No operation specified" -ForegroundColor Yellow
    Show-Help
}
