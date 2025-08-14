# Cursor AI Logout Script

[CmdletBinding()]
param(
	[ValidateSet('1','2')]
	[string] $Mode,
	[switch] $SkipPause,
	[switch] $DryRun
)

Write-Host "=== CURSOR AI LOGOUT ===" -ForegroundColor Cyan
if ($DryRun) { Write-Host "DRY RUN: No changes will be made" -ForegroundColor Yellow }

# Close Cursor AI if running
$cursorProcesses = Get-Process -Name "Cursor" -ErrorAction SilentlyContinue
if ($cursorProcesses) {
	if ($DryRun) {
		Write-Host "Would close Cursor AI processes" -ForegroundColor DarkYellow
	} else {
		Write-Host "Closing Cursor AI..." -ForegroundColor Yellow
		$cursorProcesses | Stop-Process -Force
		Start-Sleep -Seconds 2
		Write-Host "Cursor AI closed." -ForegroundColor Green
	}
}

# Ask user for logout mode (if not provided via -Mode)
if (-not $Mode) {
Write-Host "" 
Write-Host "Select logout mode:" -ForegroundColor Cyan
Write-Host "1) Logout (keep cache)" -ForegroundColor White
Write-Host "2) Logout and delete cache" -ForegroundColor White
$Mode = Read-Host "Enter choice (1 or 2, default 1)"
}
if ($Mode -ne '1' -and $Mode -ne '2') { $Mode = '1' }

# Remove configuration data but preserve cache directories
$paths = @(
    "$env:APPDATA\Cursor",
    "$env:LOCALAPPDATA\Cursor",
    "$env:APPDATA\Cursor User Data",
    "$env:LOCALAPPDATA\Cursor User Data"
)

# Treat any directory whose name ends with "Cache" (case-insensitive) as cache

function Remove-NonCacheItems {
    param(
        [Parameter(Mandatory = $true)]
        [string] $RootPath,

        [Parameter(Mandatory = $true)]
        [ref] $RemovedCounter,

        [Parameter(Mandatory = $true)]
        [bool] $IsDryRun
    )

    if (-not (Test-Path -LiteralPath $RootPath)) { return }

    $children = @()
    try {
        $children = Get-ChildItem -LiteralPath $RootPath -Force -ErrorAction Stop
    } catch {
        Write-Host "Cannot enumerate: $RootPath" -ForegroundColor Red
        return
    }

	foreach ($item in $children) {
        $full = $item.FullName
        $leaf = Split-Path -Path $full -Leaf

        # Skip cache directories/files
        if ($leaf -match '(?i)cache$') {
            Write-Host "Preserved (cache): $full" -ForegroundColor DarkGray
            continue
        }

        if ($item.PSIsContainer) {
            # Recurse into non-cache directories first
            Remove-NonCacheItems -RootPath $full -RemovedCounter $RemovedCounter -IsDryRun:$IsDryRun

            # If directory is empty after cleanup, remove it
            try {
                $isEmpty = -not (Get-ChildItem -LiteralPath $full -Force -ErrorAction SilentlyContinue)
                if ($isEmpty) {
                    if ($IsDryRun) {
                        Write-Host "Would delete empty dir: $full" -ForegroundColor DarkGray
                        $RemovedCounter.Value++
                    } else {
                        Remove-Item -LiteralPath $full -Force -ErrorAction Stop
                        $RemovedCounter.Value++
                        Write-Host "Deleted empty dir: $full" -ForegroundColor Green
                    }
                }
            } catch {
                Write-Host "Cannot delete dir: $full" -ForegroundColor Red
            }
		} else {
            # Remove file
            try {
                if ($IsDryRun) {
                    Write-Host "Would delete file: $full" -ForegroundColor DarkGray
                    $RemovedCounter.Value++
                } else {
                    Remove-Item -LiteralPath $full -Force -ErrorAction Stop
                    $RemovedCounter.Value++
                    Write-Host "Deleted file: $full" -ForegroundColor Green
                }
            } catch {
                Write-Host "Cannot delete file: $full" -ForegroundColor Red
            }
        }
    }
}

if ($Mode -eq '2') {
	# Full removal including caches
	$deletedCount = 0
	foreach ($path in $paths) {
		if (Test-Path -LiteralPath $path) {
            Write-Host ("Deleting all (including cache): {0}" -f $path) -ForegroundColor Yellow
			try {
				if ($DryRun) {
					Write-Host "Would delete: $path" -ForegroundColor DarkGray
					$deletedCount++
				} else {
					Remove-Item -LiteralPath $path -Recurse -Force -ErrorAction Stop
					$deletedCount++
					Write-Host "Deleted: $path" -ForegroundColor Green
				}
			} catch {
				Write-Host "Cannot delete: $path" -ForegroundColor Red
			}
		}
	}

	Write-Host ""
	Write-Host "Deleted $deletedCount configuration directories" -ForegroundColor White

	if ($deletedCount -gt 0) {
		Write-Host "LOGOUT SUCCESSFUL!" -ForegroundColor Green
	} else {
		Write-Host "No Cursor AI data found" -ForegroundColor Yellow
	}
} else {
	# Preserve caches; remove only non-cache items
	$deletedCount = 0
	foreach ($path in $paths) {
		if (Test-Path -LiteralPath $path) {
            Write-Host ("Cleaning (preserving caches): {0}" -f $path) -ForegroundColor Yellow
            Remove-NonCacheItems -RootPath $path -RemovedCounter ([ref]$deletedCount) -IsDryRun:$DryRun
		}
	}

	Write-Host ""
	Write-Host "Removed $deletedCount items (caches preserved)" -ForegroundColor White

	if ($deletedCount -gt 0) {
		Write-Host "LOGOUT SUCCESSFUL!" -ForegroundColor Green
	} else {
		Write-Host "No Cursor AI data found" -ForegroundColor Yellow
	}
}

if (-not $SkipPause) {
	Write-Host "Press any key to exit..." -ForegroundColor Gray
	try { $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") } catch { }
}
