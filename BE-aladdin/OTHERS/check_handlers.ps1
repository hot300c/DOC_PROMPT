# Script PowerShell to check stored procedures and handlers

Write-Host "=== CHECKING STORED PROCEDURES AND HANDLERS ===" -ForegroundColor Green
Write-Host ""

# Read stored procedures from README_LISTSP.md
Write-Host "Reading stored procedures list..." -ForegroundColor Yellow
$spFile = "DOCS\README_LISTSP.md"
$storedProcedures = @()

if (Test-Path $spFile) {
    $content = Get-Content $spFile -Encoding UTF8
    foreach ($line in $content) {
        $line = $line.Trim()
        if ($line -and -not $line.StartsWith("#")) {
            $storedProcedures += $line
        }
    }
    Write-Host "Found $($storedProcedures.Count) stored procedures" -ForegroundColor Green
} else {
    Write-Host "File $spFile not found" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Find handlers in WebService.Handlers directory
Write-Host "Finding handlers..." -ForegroundColor Yellow
$handlersDir = "WebService.Handlers"
$handlers = @()

if (Test-Path $handlersDir) {
    $csFiles = Get-ChildItem -Path $handlersDir -Recurse -Filter "*.cs"
    foreach ($file in $csFiles) {
        try {
            $content = Get-Content $file.FullName -Encoding UTF8 -Raw
            # Find ws_ProcedureName patterns
            $matches = [regex]::Matches($content, 'ws_[A-Za-z0-9_]+')
            foreach ($match in $matches) {
                $handlers += $match.Value
            }
        } catch {
            Write-Host "Error reading file $($file.FullName): $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    # Remove duplicates
    $handlers = $handlers | Sort-Object | Get-Unique
    Write-Host "Found $($handlers.Count) handlers" -ForegroundColor Green
} else {
    Write-Host "Directory $handlersDir not found" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Compare stored procedures with handlers
Write-Host "Comparing..." -ForegroundColor Yellow

# Convert to HashSet for efficient comparison
$spSet = [System.Collections.Generic.HashSet[string]]::new($storedProcedures)
$handlerSet = [System.Collections.Generic.HashSet[string]]::new($handlers)

# Find stored procedures that have handlers
$haveHandlers = @()
foreach ($sp in $storedProcedures) {
    if ($handlerSet.Contains($sp)) {
        $haveHandlers += $sp
    }
}

# Find stored procedures without handlers
$missingHandlers = @()
foreach ($sp in $storedProcedures) {
    if (-not $handlerSet.Contains($sp)) {
        $missingHandlers += $sp
    }
}

# Find handlers not in stored procedures list
$extraHandlers = @()
foreach ($handler in $handlers) {
    if (-not $spSet.Contains($handler)) {
        $extraHandlers += $handler
    }
}

# Display results
Write-Host "=== RESULTS ===" -ForegroundColor Green
Write-Host ""

Write-Host "SUMMARY:" -ForegroundColor Cyan
Write-Host "   - Total stored procedures: $($storedProcedures.Count)" -ForegroundColor White
Write-Host "   - Total handlers: $($handlers.Count)" -ForegroundColor White
Write-Host "   - Stored procedures with handlers: $($haveHandlers.Count)" -ForegroundColor Green
Write-Host "   - Stored procedures missing handlers: $($missingHandlers.Count)" -ForegroundColor Red
Write-Host "   - Handlers not in SP list: $($extraHandlers.Count)" -ForegroundColor Yellow
Write-Host ""

Write-Host "STORED PROCEDURES WITH HANDLERS ($($haveHandlers.Count)):" -ForegroundColor Green
$displayCount = [Math]::Min(20, $haveHandlers.Count)
for ($i = 0; $i -lt $displayCount; $i++) {
    Write-Host "   [OK] $($haveHandlers[$i])" -ForegroundColor Green
}
if ($haveHandlers.Count -gt 20) {
    Write-Host "   ... and $($haveHandlers.Count - 20) more stored procedures" -ForegroundColor Gray
}
Write-Host ""

Write-Host "STORED PROCEDURES MISSING HANDLERS ($($missingHandlers.Count)):" -ForegroundColor Red
$displayCount = [Math]::Min(20, $missingHandlers.Count)
for ($i = 0; $i -lt $displayCount; $i++) {
    Write-Host "   [MISSING] $($missingHandlers[$i])" -ForegroundColor Red
}
if ($missingHandlers.Count -gt 20) {
    Write-Host "   ... and $($missingHandlers.Count - 20) more stored procedures" -ForegroundColor Gray
}
Write-Host ""

Write-Host "HANDLERS NOT IN SP LIST ($($extraHandlers.Count)):" -ForegroundColor Yellow
$displayCount = [Math]::Min(20, $extraHandlers.Count)
for ($i = 0; $i -lt $displayCount; $i++) {
    Write-Host "   [EXTRA] $($extraHandlers[$i])" -ForegroundColor Yellow
}
if ($extraHandlers.Count -gt 20) {
    Write-Host "   ... and $($extraHandlers.Count - 20) more handlers" -ForegroundColor Gray
}
Write-Host ""

# Save detailed results to file
$outputFile = "handler_analysis_result.txt"
Write-Host "Saving detailed results to: $outputFile" -ForegroundColor Cyan

$output = @"
=== STORED PROCEDURES AND HANDLERS ANALYSIS ===

Total stored procedures: $($storedProcedures.Count)
Total handlers: $($handlers.Count)
Stored procedures with handlers: $($haveHandlers.Count)
Stored procedures missing handlers: $($missingHandlers.Count)
Handlers not in SP list: $($extraHandlers.Count)

=== STORED PROCEDURES WITH HANDLERS ===
"@

foreach ($sp in $haveHandlers) {
    $output += "`n[OK] $sp"
}

$output += @"

=== STORED PROCEDURES MISSING HANDLERS ===
"@

foreach ($sp in $missingHandlers) {
    $output += "`n[MISSING] $sp"
}

$output += @"

=== HANDLERS NOT IN SP LIST ===
"@

foreach ($handler in $extraHandlers) {
    $output += "`n[EXTRA] $handler"
}

$output | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host "Analysis completed!" -ForegroundColor Green
