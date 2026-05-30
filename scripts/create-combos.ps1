#requires -Version 5.1
<#
.SYNOPSIS
    Create combo models in 9Router for auto-routing.
.DESCRIPTION
    Creates auto-berat, auto-sedang, and auto-ringan combo models with
    ordered fallback chains. Skips combos that already exist.
.NOTES
    Uses $env:NINEROUTER_KEY for API auth. Falls back to unauthenticated
    requests if the endpoint does not require API keys.
#>

function Main {
    $prevEAP = $global:ErrorActionPreference
    $global:ErrorActionPreference = "Stop"

    try {
        # ── Configuration ───────────────────────────────────────────────────────────
        $BaseUrl = "http://localhost:20128"

        # API key: use env var, otherwise prompt interactively.
        if (-not $env:NINEROUTER_KEY) {
            $secureKey = Read-Host "Enter NINEROUTER_KEY" -AsSecureString
            $env:NINEROUTER_KEY = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
                [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
            )
        }

        $AuthHeaders = @{
            "Authorization" = "Bearer $env:NINEROUTER_KEY"
            "Content-Type"  = "application/json"
        }

        $NoAuthHeaders = @{
            "Content-Type" = "application/json"
        }

        # ── Header ──────────────────────────────────────────────────────────────────
        Write-Host ""
        Write-Host "=== 9Router Combo Model Creation ===" -ForegroundColor Cyan
        Write-Host ""

        # ── Health Check ────────────────────────────────────────────────────────────
        Write-Host "[*] Checking 9Router health..." -ForegroundColor Cyan

        try {
            $null = Invoke-RestMethod -Uri "$BaseUrl/api/health" -TimeoutSec 5 -ErrorAction Stop
            Write-Host "      9Router is healthy" -ForegroundColor Green
        }
        catch {
            Write-Host "      ERROR: 9Router health check failed ($($_.Exception.Message))" -ForegroundColor Red
            Write-Host "      Ensure 9Router is running on port 20128." -ForegroundColor Yellow
            exit 1
        }

        # ── Detect Auth Mode ────────────────────────────────────────────────────────
        # Test whether the combos endpoint accepts API key auth or needs no auth.
        Write-Host "[*] Detecting auth mode..." -ForegroundColor Cyan

        $Headers = $AuthHeaders
        try {
            $null = Invoke-RestMethod -Uri "$BaseUrl/api/combos" -Headers $AuthHeaders -TimeoutSec 5 -ErrorAction Stop
            Write-Host "      Using API key auth" -ForegroundColor Green
        }
        catch {
            # Distinguish "server unreachable" from "wrong credentials".
            if (-not $_.Exception.Response) {
                Write-Host "      ERROR: 9Router unreachable ($($_.Exception.Message))" -ForegroundColor Red
                exit 1
            }

            $statusCode = [int]$_.Exception.Response.StatusCode

            if ($statusCode -eq 401) {
                # API key not accepted for dashboard API; try without auth.
                try {
                    $null = Invoke-RestMethod -Uri "$BaseUrl/api/combos" -Headers $NoAuthHeaders -TimeoutSec 5 -ErrorAction Stop
                    $Headers = $NoAuthHeaders
                    Write-Host "      Using no auth (requireApiKey disabled)" -ForegroundColor Yellow
                }
                catch {
                    $statusCode2 = $null
                    if ($_.Exception.Response) {
                        $statusCode2 = [int]$_.Exception.Response.StatusCode
                    }

                    if ($statusCode2 -eq 401) {
                        # Dashboard session auth required — can't proceed without login.
                        Write-Host "      WARNING: Dashboard session auth required" -ForegroundColor Yellow
                        Write-Host "      Create combos via Dashboard → Combos → Create New" -ForegroundColor Yellow
                        Write-Host "      Or disable requireLogin in 9Router settings." -ForegroundColor Yellow
                        exit 2
                    }
                    # Some other error — still try with no-auth and let per-combo errors surface.
                    $Headers = $NoAuthHeaders
                    Write-Host "      Using no auth (trying anyway)" -ForegroundColor Yellow
                }
            }
            else {
                # Non-401 error — probably no combos exist yet or endpoint issue.
                Write-Host "      Using API key auth" -ForegroundColor Green
            }
        }

        # ── Combo Definitions ───────────────────────────────────────────────────────
        $Combos = @(
            @{
                Name   = "auto-berat"
                Models = @("kr/claude-sonnet-4.5", "kr/deepseek-3.2", "gc/gemini-3-pro-preview")
            },
            @{
                Name   = "auto-sedang"
                Models = @("openrouter/moonshotai/kimi-k2.6:free", "gemini/gemini-3-flash-preview", "kr/minimax-m2.5")
            },
            @{
                Name   = "auto-ringan"
                Models = @("openrouter/deepseek/deepseek-v4-flash:free", "openrouter/google/gemma-4-26b-a4b-it:free", "openrouter/qwen/qwen3-next-80b-a3b:free")
            }
        )

        # ── Create Combos ───────────────────────────────────────────────────────────
        foreach ($combo in $Combos) {
            Write-Host ""
            Write-Host "[*] Processing combo: $($combo.Name)" -ForegroundColor Cyan

            # Check if combo already exists via GET /api/combos and filter by name.
            $exists = $false
            try {
                $allCombos = Invoke-RestMethod -Uri "$BaseUrl/api/combos" -Headers $Headers -TimeoutSec 5 -ErrorAction Stop
                if ($allCombos -and $allCombos.combos -is [array]) {
                    $exists = $null -ne ($allCombos.combos | Where-Object { $_.name -eq $combo.Name })
                }
            }
            catch {
                # If we can't list combos, fall back to checking /v1/models for the combo ID.
                try {
                    $models = Invoke-RestMethod -Uri "$BaseUrl/v1/models" -TimeoutSec 5 -ErrorAction Stop
                    if ($models -and $models.data) {
                        [array]$modelIds = $models.data.id
                        $exists = $modelIds -contains $combo.Name
                    }
                }
                catch {
                    # Can't verify existence — attempt creation anyway.
                    $exists = $false
                }
            }

            if ($exists) {
                Write-Host "      Already exists — skipping" -ForegroundColor Yellow
                continue
            }

            # Build request body as hashtable → JSON
            $Body = @{
                name   = $combo.Name
                models = @($combo.Models)
            }

            $JsonBody = $Body | ConvertTo-Json -Depth 3

            try {
                $result = Invoke-RestMethod `
                    -Uri "$BaseUrl/api/combos" `
                    -Headers $Headers `
                    -Method Post `
                    -Body $JsonBody `
                    -TimeoutSec 10 `
                    -ErrorAction Stop

                # Check for API-level error in response body.
                if ($result.error) {
                    throw $result.error
                }

                Write-Host "      Created successfully" -ForegroundColor Green
            }
            catch {
                $statusCode = $null
                if ($_.Exception.Response) {
                    $statusCode = [int]$_.Exception.Response.StatusCode
                }

                if ($statusCode -eq 400) {
                    # 400 often means "already exists" from the combo API.
                    Write-Host "      Already exists — skipping" -ForegroundColor Yellow
                }
                else {
                    Write-Host "      ERROR creating combo: $($_.Exception.Message)" -ForegroundColor Red
                }
            }
        }

        # ── Summary ─────────────────────────────────────────────────────────────────
        Write-Host ""
        Write-Host "Combo model creation complete." -ForegroundColor Cyan
        Write-Host ""
    }
    finally {
        $global:ErrorActionPreference = $prevEAP
    }
}

Main
