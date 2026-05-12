# boot.ps1 - Document OS 1.0 Boot Script

Clear-Host

Write-Host ""
Write-Host "   DDDDDD   OOOOO   CCCCC   U     U  M     M  EEEEEEE  N     N  TTTTTTT " -ForegroundColor Cyan
Write-Host "   D     D O     O C     C U     U  MM   MM  E        NN    N    T    " -ForegroundColor Cyan
Write-Host "   D     D O     O C       U     U  M M M M  EEEE     N N   N    T    " -ForegroundColor Cyan
Write-Host "   D     D O     O C       U     U  M  M  M  E        N  N  N    T    " -ForegroundColor Cyan
Write-Host "   DDDDDD   OOOOO   CCCCC   UUUUU   M     M  EEEEEEE  N   N N    T    " -ForegroundColor Cyan
Write-Host ""

Write-Host "                    Official Company System v1.0" -ForegroundColor Green
Write-Host "                    ==================================" -ForegroundColor Yellow
Write-Host ""

# Python Detection
$pythonCmd = $null
if (Get-Command py -ErrorAction SilentlyContinue) { 
    $pythonCmd = "py" 
} elseif (Get-Command python -ErrorAction SilentlyContinue) { 
    $pythonCmd = "python" 
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) { 
    $pythonCmd = "python3" 
} else {
    Write-Host "Python not found!" -ForegroundColor Red
    Write-Host "Please install Python and add it to PATH." -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Initializing Document OS Kernel..." -ForegroundColor Magenta
Start-Sleep -Milliseconds 800

Write-Host "Loading Business Filesystem..." -ForegroundColor Magenta
Start-Sleep -Milliseconds 600

Write-Host "Mounting Company Documents..." -ForegroundColor Magenta
Start-Sleep -Milliseconds 500

Write-Host "Starting Secure Session..." -ForegroundColor Green
Start-Sleep -Milliseconds 700

Write-Host ""
Write-Host "=============================================================" -ForegroundColor Green
Write-Host "          DOCUMENT OS 1.0 IS NOW READY                      " -ForegroundColor Green
Write-Host "=============================================================" -ForegroundColor Green
Write-Host ""

# Launch Document OS
& $pythonCmd docos.py

Write-Host ""
Write-Host "Document OS shutdown completed." -ForegroundColor Cyan