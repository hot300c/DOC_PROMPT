# Script PowerShell để merge FE_API.csv và Procedure.csv
# Tạo file mới với các cột từ Procedure trước, FE_API sau, và cột đánh dấu DA_CO/CHUA_CO

Write-Host "Bắt đầu merge CSV files..." -ForegroundColor Green

# Đọc file FE_API.csv
Write-Host "Đang đọc file FE_API.csv..." -ForegroundColor Yellow
$feApiContent = Get-Content "FE_API.csv" -Encoding UTF8
$feApiHeaders = $feApiContent[0] -split ','
$feApiData = $feApiContent[1..($feApiContent.Length-1)]

# Tạo dictionary để map Command -> FE_API data
$feApiDict = @{}
foreach ($line in $feApiData) {
    $values = $line -split ','
    if ($values.Length -ge 3) {
        $command = $values[2].Trim('"')
        if ($command -and $command -ne "") {
            $feApiDict[$command] = $line
        }
    }
}

Write-Host "Đã tạo $($feApiDict.Count) entries từ FE_API" -ForegroundColor Green

# Đọc file Procedure.csv
Write-Host "Đang đọc file Procedure.csv..." -ForegroundColor Yellow
$procedureContent = Get-Content "Procedure.csv" -Encoding UTF8
$procedureHeaders = $procedureContent[0] -split ','
$procedureData = $procedureContent[1..($procedureContent.Length-1)]

# Tạo headers cho file output
$outputHeaders = @()
$outputHeaders += $procedureHeaders
$outputHeaders += "Status"
foreach ($header in $feApiHeaders) {
    $outputHeaders += "FE_API_$header"
}

# Tạo content cho file output
$outputContent = @()
$outputContent += ($outputHeaders -join ',')

$daCoCount = 0
$chuaCoCount = 0

foreach ($procLine in $procedureData) {
    $procValues = $procLine -split ','
    $procName = $procValues[1].Trim('"')  # ProcedureName là cột thứ 2
    
    # Tìm kiếm trong FE_API
    $feApiMatch = $feApiDict[$procName]
    
    # Tạo row mới
    $newRow = @()
    
    # Thêm tất cả cột từ Procedure
    $newRow += $procValues
    
    # Thêm cột đánh dấu và FE_API data
    if ($feApiMatch) {
        $newRow += "DA_CO"
        $daCoCount++
        
        # Thêm tất cả cột từ FE_API
        $feApiValues = $feApiMatch -split ','
        $newRow += $feApiValues
    } else {
        $newRow += "CHUA_CO"
        $chuaCoCount++
        
        # Thêm cột trống cho FE_API
        for ($i = 0; $i -lt $feApiHeaders.Length; $i++) {
            $newRow += ""
        }
    }
    
    $outputContent += ($newRow -join ',')
}

# Lưu file kết quả
$outputFilename = "merged_procedures_fe_api.csv"
$outputContent | Out-File -FilePath $outputFilename -Encoding UTF8

Write-Host "Đã tạo file $outputFilename với $($outputContent.Length - 1) dòng" -ForegroundColor Green

# Thống kê
$totalCount = $outputContent.Length - 1
$foundPercentage = [math]::Round(($daCoCount / $totalCount) * 100, 2)

Write-Host "`nThống kê:" -ForegroundColor Cyan
Write-Host "- Tổng số procedures: $totalCount" -ForegroundColor White
Write-Host "- DA_CO (tìm thấy): $daCoCount" -ForegroundColor Green
Write-Host "- CHUA_CO (không tìm thấy): $chuaCoCount" -ForegroundColor Red
Write-Host "- Tỷ lệ tìm thấy: $foundPercentage%" -ForegroundColor Yellow

# Tạo báo cáo tóm tắt
$summaryFilename = "merge_summary_report.txt"
$summaryContent = @"
BÁO CÁO TÓM TẮT MERGE PROCEDURES VÀ FE_API
==================================================

Tổng số procedures: $totalCount
Procedures được tìm thấy (DA_CO): $daCoCount
Procedures không tìm thấy (CHUA_CO): $chuaCoCount
Tỷ lệ tìm thấy: $foundPercentage%

TOP 10 PROCEDURES KHÔNG TÌM THẤY:
"@

$summaryContent | Out-File -FilePath $summaryFilename -Encoding UTF8

Write-Host "`nĐã tạo báo cáo tóm tắt: $summaryFilename" -ForegroundColor Green
Write-Host "Hoàn thành!" -ForegroundColor Green
