# ============================================
# Auto-Enable Prerequisites for Skills
# ============================================
# Run this before using skills to ensure everything is ready

Write-Host "`nCHECK Checking prerequisites..." -ForegroundColor Cyan

# 1. Docker
Write-Host "`n[1/7] Docker..." -NoNewline
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK] $dockerVersion" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Not installed" -ForegroundColor Red
        Write-Host "   Install: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
    }
} catch {
    Write-Host " [FAIL] Not found" -ForegroundColor Red
}

# 2. 9Router
Write-Host "[2/7] 9Router..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "http://localhost:20128" -TimeoutSec 3 -UseBasicParsing 2>$null
    if ($response.StatusCode -eq 200 -or $response.StatusCode -eq 404) {
        Write-Host " [OK] Running on port 20128" -ForegroundColor Green
    } else {
        Write-Host " [WARN]  Running but unexpected status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host " [FAIL] Not running" -ForegroundColor Red
    Write-Host "   Start: 9Router Desktop or 'npx 9router'" -ForegroundColor Yellow
}

# 3. Node.js
Write-Host "[3/7] Node.js..." -NoNewline
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK] $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Not installed" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] Not found" -ForegroundColor Red
}

# 4. Python
Write-Host "[4/7] Python..." -NoNewline
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK] $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Not installed" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] Not found" -ForegroundColor Red
}

# 5. Git
Write-Host "[5/7] Git..." -NoNewline
try {
    $gitVersion = git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK] $gitVersion" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Not installed" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] Not found" -ForegroundColor Red
}

# 6. GitHub CLI
Write-Host "[6/7] GitHub CLI..." -NoNewline
try {
    $ghVersion = gh --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK] $ghVersion" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Not installed" -ForegroundColor Red
        Write-Host "   Install: winget install GitHub.cli" -ForegroundColor Yellow
    }
} catch {
    Write-Host " [FAIL] Not found" -ForegroundColor Red
}

# 7. pytest
Write-Host "[7/7] pytest..." -NoNewline
try {
    $pytestVersion = python -m pytest --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK] $pytestVersion" -ForegroundColor Green
    } else {
        Write-Host " [WARN] Not installed (available via pip)" -ForegroundColor Yellow
        Write-Host "   Install: pip install pytest" -ForegroundColor Yellow
    }
} catch {
    Write-Host " [FAIL] Not found" -ForegroundColor Red
}

# Obsidian Vault
Write-Host "`n[DIR] Obsidian Vault..." -NoNewline
$obsidianPath = "$env:USERPROFILE\Documents\Obsidian Vault"
if (Test-Path $obsidianPath) {
    Write-Host " [OK] Found at $obsidianPath" -ForegroundColor Green
} else {
    Write-Host " [WARN]  Not found" -ForegroundColor Yellow
}

# 9Router Auto-Routing
Write-Host "`n[ROUTE] 9Router Auto-Routing..." -NoNewline
$routerScript = Join-Path $PSScriptRoot "init-9router-routing.ps1"
$keywordRouter = Join-Path $PSScriptRoot "keyword-router.ps1"
$combosScript = Join-Path $PSScriptRoot "create-combos.ps1"

$allReady = $true
if (Test-Path $routerScript) {
    Write-Host "`n   [OK] init-9router-routing.ps1" -ForegroundColor Green
} else {
    Write-Host "`n   [FAIL] init-9router-routing.ps1 (missing)" -ForegroundColor Red
    $allReady = $false
}

if (Test-Path $keywordRouter) {
    Write-Host "   [OK] keyword-router.ps1" -ForegroundColor Green
} else {
    Write-Host "   [FAIL] keyword-router.ps1 (missing)" -ForegroundColor Red
    $allReady = $false
}

if (Test-Path $combosScript) {
    Write-Host "   [OK] create-combos.ps1" -ForegroundColor Green
} else {
    Write-Host "   [FAIL] create-combos.ps1 (missing)" -ForegroundColor Red
    $allReady = $false
}

if ($allReady) {
    Write-Host "`n   Run: .\scripts\init-9router-routing.ps1 to enable" -ForegroundColor Yellow
}

Write-Host "`n[OK] Prerequisites check complete!`n" -ForegroundColor Cyan
