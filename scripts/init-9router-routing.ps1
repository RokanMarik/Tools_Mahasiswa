#requires -Version 5.1
<#
.SYNOPSIS
    Initialize 9Router Auto-Routing for the current session.
.DESCRIPTION
    Checks 9Router health, sets environment variables, verifies combo models,
    and loads the keyword router. Run at the start of each session.
#>

# Save and restore EAP so it doesn't leak into caller's session when dot-sourced.
$prevEAP = $global:ErrorActionPreference
$global:ErrorActionPreference = "Stop"

# Track initialization status for accurate summary.
$combosLoaded = $false
$keywordRouterLoaded = $false

try {
    # ── Header ──────────────────────────────────────────────────────────────────
    Write-Host ""
    Write-Host "=== 9Router Auto-Routing Initialization ===" -ForegroundColor Cyan
    Write-Host ""

    # ── Step 1/4: Health Check ──────────────────────────────────────────────────
    Write-Host "[1/4] Checking 9Router health..." -ForegroundColor Cyan

    try {
        $null = Invoke-RestMethod -Uri "http://localhost:20128/api/health" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "      9Router is healthy" -ForegroundColor Green
    }
    catch {
        Write-Host "      ERROR: 9Router health check failed" -ForegroundColor Red
        Write-Host "      Ensure 9Router is running on port 20128." -ForegroundColor Yellow
        exit 1
    }

    # ── Step 2/4: Environment Variables ─────────────────────────────────────────
    Write-Host "[2/4] Setting environment variables..." -ForegroundColor Cyan

    $env:NINEROUTER_URL = "http://localhost:20128"

    # Use existing key if already set in the environment; otherwise fall back
    # to a local-dev default. Never hardcode a real key in plaintext.
    if (-not $env:NINEROUTER_KEY) {
        $env:NINEROUTER_KEY = "sk-local-dev-key"
        Write-Host "      NINEROUTER_KEY = [set to local-dev default]" -ForegroundColor Green
    }
    else {
        Write-Host "      NINEROUTER_KEY = [already set in environment]" -ForegroundColor Green
    }
    Write-Host "      NINEROUTER_URL = $env:NINEROUTER_URL" -ForegroundColor Green

    # ── Step 3/4: Verify Combo Models ───────────────────────────────────────────
    Write-Host "[3/4] Verifying combo models..." -ForegroundColor Cyan

    $comboModels = @("auto-berat", "auto-sedang", "auto-ringan")
    $allModelsPresent = $true

    try {
        $modelsResponse = Invoke-RestMethod -Uri "http://localhost:20128/v1/models" -TimeoutSec 5 -ErrorAction Stop

        # Null guard: ensure data array exists before accessing properties.
        if ($null -eq $modelsResponse -or $null -eq $modelsResponse.data) {
            Write-Host "      WARNING: models endpoint returned no data" -ForegroundColor Yellow
            $allModelsPresent = $false
        }
        else {
            # Force array so -contains works correctly with a single element.
            [array]$availableIds = $modelsResponse.data.id

            foreach ($model in $comboModels) {
                if ($availableIds -contains $model) {
                    Write-Host "      $model  ✅" -ForegroundColor Green
                }
                else {
                    Write-Host "      $model  ❌" -ForegroundColor Red
                    $allModelsPresent = $false
                }
            }
        }
    }
    catch {
        Write-Host "      WARNING: Could not fetch model list ($_)" -ForegroundColor Yellow
        $allModelsPresent = $false
    }

    if (-not $allModelsPresent) {
        Write-Host ""
        Write-Host "      Run 'scripts/create-combos.ps1' to create missing combo models." -ForegroundColor Yellow
    }
    else {
        $combosLoaded = $true
    }

    # ── Step 4/4: Load Keyword Router ───────────────────────────────────────────
    Write-Host "[4/4] Loading keyword router..." -ForegroundColor Cyan

    $keywordRouterPath = Join-Path $PSScriptRoot "keyword-router.ps1"

    if (Test-Path $keywordRouterPath) {
        try {
            . $keywordRouterPath
            $keywordRouterLoaded = $true
            Write-Host "      Keyword router loaded from scripts/keyword-router.ps1" -ForegroundColor Green
        }
        catch {
            Write-Host "      ERROR: Failed to load keyword router ($_)" -ForegroundColor Red
        }
    }
    else {
        Write-Host "      WARNING: keyword-router.ps1 not found at $keywordRouterPath" -ForegroundColor Yellow
        Write-Host "      Auto-routing will not be available." -ForegroundColor Yellow
    }

    # ── Summary ─────────────────────────────────────────────────────────────────
    Write-Host ""

    if ($combosLoaded -and $keywordRouterLoaded) {
        Write-Host "✅ 9Router Auto-Routing initialized!" -ForegroundColor Green
    }
    elseif ($combosLoaded -or $keywordRouterLoaded) {
        Write-Host "⚠️  Partial initialization — some components failed to load." -ForegroundColor Yellow
    }
    else {
        Write-Host "❌ 9Router Auto-Routing initialization failed." -ForegroundColor Red
    }

    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Cyan
    Write-Host "  `$model = Get-TaskComplexity -Prompt `"`"your task description`"`"" -ForegroundColor White
    Write-Host "  Invoke-RestMethod `$env:NINEROUTER_URL/v1/chat/completions ... -Body @{ model = `$model }" -ForegroundColor White
    Write-Host ""
}
finally {
    # Restore the caller's EAP.
    $global:ErrorActionPreference = $prevEAP
}
