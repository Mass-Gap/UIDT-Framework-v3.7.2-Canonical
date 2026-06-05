powershell
<#
.SYNOPSIS
    UIDT Verification Wrapper: Block B3 (BMW Gamma Flow)
.DESCRIPTION
    Führt das verifizierte Blueprint-Skript BMW_gamma_flow.py aus, 
    überprüft die Integrität der Umgebung (Git Branch, Python-Module) 
    und generiert einen formatierten Issue-Kommentar-Block.
.NOTES
    Author: P. Rietz (via Canonical Assistant)
    Target Issue: #536
#>

# 1. Konfiguration
$ScriptPath = "verification\scripts\BMW_gamma_flow.py"
$LogFile = "B3_Execution_Audit.txt"
$RequiredBranch = "research/L4-BMW-gamma-derivation"

Clear-Host
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host " UIDT VERIFICATION AUDIT: Block B3 (BMW Gamma Flow)" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# 2. Umgebungsprüfung (Git Status)
Write-Host "`n[1/3] Checking environment integrity..."
$CurrentBranch = git rev-parse --abbrev-ref HEAD
if ($CurrentBranch -ne $RequiredBranch) {
    Write-Host "[WARNING] You are on branch '$CurrentBranch', but B3 requires '$RequiredBranch'." -ForegroundColor Yellow
    Write-Host "Press 'Y' to continue anyway (if merged), or any other key to abort." -ForegroundColor Yellow
    $response = Read-Host
    if ($response -notmatch "^[Yy]$") {
        Write-Host "Aborting." -ForegroundColor Red
        exit
    }
} else {
    Write-Host "[OK] Correct branch: $CurrentBranch" -ForegroundColor Green
}

$GitHash = git rev-parse --short HEAD
Write-Host "[OK] Current Commit: $GitHash" -ForegroundColor Green

# 3. Python & Dependency Check
try {
    $PythonVersion = python --version 2>&1
    Write-Host "[OK] Found $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    exit
}

$MpmathCheck = python -c "import mpmath; print(mpmath.__version__)" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Missing dependency: mpmath. Run 'pip install mpmath' first." -ForegroundColor Red
    exit
} else {
    Write-Host "[OK] mpmath module available (v$MpmathCheck)" -ForegroundColor Green
}

# 4. Skript-Ausführung
if (-not (Test-Path $ScriptPath)) {
    Write-Host "`n[ERROR] Script not found at: $ScriptPath" -ForegroundColor Red
    exit
}

Write-Host "`n[2/3] Executing BMW Flow Integration (mp.dps=80)..." -ForegroundColor Cyan
Write-Host "      This may take a moment depending on the ODE solver step size." -ForegroundColor DarkGray

$StartTime = Get-Date
# Ausführung und Capturing der Standardausgabe
$Output = & python $ScriptPath 2>&1
$EndTime = Get-Date
$ExecutionTime = ($EndTime - $StartTime).TotalSeconds

Write-Host "[OK] Execution completed in $($ExecutionTime.ToString('0.00')) seconds.`n" -ForegroundColor Green

# 5. Protokoll-Generierung für Issue #536
Write-Host "[3/3] Generating Audit Log for Issue #536..." -ForegroundColor Cyan

$IssueFormat = @"
**[PI EXECUTION AUDIT] Block B3 (BMW Gamma Flow)**

**Environment Context:**
* **Date:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ssZ')
* **Commit:** `$CurrentBranch` (`$GitHash`)
* **Execution Time:** $($ExecutionTime.ToString('0.00')) s

**Terminal Output (Raw 80-digit mpmath data):**
```text
$($Output | Out-String)

```

"@

# In Datei speichern und auf der Konsole ausgeben

$IssueFormat | Out-File -FilePath $LogFile -Encoding utf8
Write-Host $IssueFormat -ForegroundColor Gray

Write-Host "`n======================================================" -ForegroundColor Cyan
Write-Host " [SUCCESS] Audit log saved to: $LogFile" -ForegroundColor Green
Write-Host " Please copy the block above and paste it as a comment in Issue #536." -ForegroundColor Yellow
Write-Host "======================================================" -ForegroundColor Cyan


