# GitHub Project Manager for LOAN - FIXED VERSION
# Requires GitHub CLI (gh) to be installed and authenticated

param(
    [string]$Action = "status",
    [string]$Title = "",
    [string]$Body = ""
)

# Project configuration - PNTSOL Project #6
$PROJECT_NUMBER = "6"
$ORGANIZATION = "PNTSOL"
$REPOSITORY = "PNTSOL/DOC_PROMPT_VNVC"

# Colors for output
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"
$WarningColor = "Yellow"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Test-GitHubCLI {
    try {
        $null = gh --version
        return $true
    }
    catch {
        Write-ColorOutput "GitHub CLI (gh) is not installed or not in PATH." $ErrorColor
        Write-ColorOutput "Please install from: https://cli.github.com/" $InfoColor
        return $false
    }
}

function Test-GitHubAuth {
    try {
        $null = gh auth status 2>$null
        return $true
    }
    catch {
        Write-ColorOutput "Not authenticated with GitHub CLI." $ErrorColor
        Write-ColorOutput "Run: gh auth login" $InfoColor
        return $false
    }
}

function Get-ProjectInfo {
    Write-ColorOutput "`n=== PNTSOL Project #$PROJECT_NUMBER ===" $InfoColor
    
    try {
        # Get project details
        $project = gh project view $PROJECT_NUMBER --owner $ORGANIZATION --format json | ConvertFrom-Json
        
        Write-ColorOutput "`n📊 Project: $($project.title)" $SuccessColor
        Write-ColorOutput "   Description: $($project.description)" $InfoColor
        Write-ColorOutput "   URL: $($project.url)" $InfoColor
        Write-ColorOutput "   Status: $($project.state)" $InfoColor
        
        # Get project statistics
        $items = gh project item-list $PROJECT_NUMBER --owner $ORGANIZATION --format json | ConvertFrom-Json
        
        $totalItems = $items.Count
        $inProgressItems = ($items | Where-Object { $_.status -and $_.status.name -eq "In Progress" }).Count
        $todoItems = ($items | Where-Object { $_.status -and $_.status.name -eq "Todo" }).Count
        $doneItems = ($items | Where-Object { $_.status -and $_.status.name -eq "Done" }).Count
        
        Write-ColorOutput "`n📈 Statistics:" $InfoColor
        Write-ColorOutput "   Total Items: $totalItems" $SuccessColor
        Write-ColorOutput "   Todo: $todoItems" $WarningColor
        Write-ColorOutput "   In Progress: $inProgressItems" $InfoColor
        Write-ColorOutput "   Done: $doneItems" $SuccessColor
        
    }
    catch {
        Write-ColorOutput "Error fetching project info: $($_.Exception.Message)" $ErrorColor
    }
}

function Get-InProgressTasks {
    Write-ColorOutput "`n=== In-Progress Tasks ===" $InfoColor
    
    try {
        # Get project items
        $items = gh project item-list $PROJECT_NUMBER --owner $ORGANIZATION --format json | ConvertFrom-Json
        
        $inProgressItems = $items | Where-Object { 
            $_.status -and $_.status.name -eq "In Progress" 
        }
        
        if ($inProgressItems.Count -eq 0) {
            Write-ColorOutput "No tasks currently in progress." $WarningColor
        }
        else {
            Write-ColorOutput "Found $($inProgressItems.Count) in-progress tasks:" $SuccessColor
            foreach ($item in $inProgressItems) {
                Write-ColorOutput "`n📋 $($item.title)" $SuccessColor
                if ($item.content) {
                    Write-ColorOutput "   Content: $($item.content.title)" $InfoColor
                }
                if ($item.assignees) {
                    $assignees = $item.assignees | ForEach-Object { $_.login } | Join-String -Separator ", "
                    Write-ColorOutput "   👥 Assignees: $assignees" $InfoColor
                }
                Write-ColorOutput "   🔗 URL: $($item.url)" $InfoColor
            }
        }
    }
    catch {
        Write-ColorOutput "Error fetching project items: $($_.Exception.Message)" $ErrorColor
    }
}

function Add-NewTask {
    param([string]$Title, [string]$Body)
    
    if ([string]::IsNullOrEmpty($Title)) {
        Write-ColorOutput "Please provide a title with -Title parameter" $ErrorColor
        return
    }
    
    Write-ColorOutput "`n=== Adding New Task ===" $InfoColor
    
    try {
        # Create issue first
        $issueBody = if ([string]::IsNullOrEmpty($Body)) { "Task for LOAN project" } else { $Body }
        
        $issue = gh issue create --title $Title --body $issueBody --repo $REPOSITORY --format json | ConvertFrom-Json
        
        Write-ColorOutput "✅ Created issue: $($issue.title)" $SuccessColor
        Write-ColorOutput "   Issue #$($issue.number)" $InfoColor
        Write-ColorOutput "   URL: $($issue.url)" $InfoColor
        
        # Add to project
        gh project item-add $PROJECT_NUMBER --owner $ORGANIZATION --url $issue.url
        
        Write-ColorOutput "✅ Added to PNTSOL Project #$PROJECT_NUMBER" $SuccessColor
        
    }
    catch {
        Write-ColorOutput "Error creating task: $($_.Exception.Message)" $ErrorColor
    }
}

# Main execution
Write-ColorOutput "🚀 LOAN GitHub Project Manager" $InfoColor
Write-ColorOutput "Organization: $ORGANIZATION" $InfoColor
Write-ColorOutput "Project: #$PROJECT_NUMBER" $InfoColor
Write-ColorOutput "Repository: $REPOSITORY" $InfoColor

# Check prerequisites
if (-not (Test-GitHubCLI)) { exit 1 }
if (-not (Test-GitHubAuth)) { exit 1 }

# Execute based on action
switch ($Action.ToLower()) {
    "status" {
        Get-ProjectInfo
    }
    "inprogress" {
        Get-InProgressTasks
    }
    "add" {
        Add-NewTask -Title $Title -Body $Body
    }
    default {
        Write-ColorOutput "`nAvailable Actions:" $InfoColor
        Write-ColorOutput "  status      - Show project overview and statistics" $SuccessColor
        Write-ColorOutput "  inprogress  - Show in-progress tasks" $SuccessColor
        Write-ColorOutput "  add         - Add new task (requires -Title)" $SuccessColor
        Write-ColorOutput "`nExamples:" $InfoColor
        Write-ColorOutput "  .\github-project-manager-fixed.ps1 -Action status" $SuccessColor
        Write-ColorOutput "  .\github-project-manager-fixed.ps1 -Action inprogress" $SuccessColor
        Write-ColorOutput "  .\github-project-manager-fixed.ps1 -Action add -Title \"Implement notification service\"" $SuccessColor
    }
}