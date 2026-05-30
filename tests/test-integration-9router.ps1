#requires -Version 5.1

$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
function Write-Section {
    param([string]$Text)
    Write-Host "`n=== $Text ===" -ForegroundColor Yellow
}

function Write-Pass {
    param([string]$Prompt, [string]$Expected, [string]$Actual)
    Write-Host "  [PASS]" -ForegroundColor Green -NoNewline
    Write-Host " Prompt: $Prompt"
    Write-Host "        Expected: $Expected | Actual: $Actual" -ForegroundColor Green
}

function Write-Fail {
    param([string]$Prompt, [string]$Expected, [string]$Actual)
    Write-Host "  [FAIL]" -ForegroundColor Red -NoNewline
    Write-Host " Prompt: $Prompt"
    Write-Host "        Expected: $Expected | Actual: $Actual" -ForegroundColor Red
}

# ---------------------------------------------------------------------------
# Dot-source keyword router
# ---------------------------------------------------------------------------
. "$PSScriptRoot\..\scripts\keyword-router.ps1"

# ---------------------------------------------------------------------------
# 9Router configuration
# ---------------------------------------------------------------------------
$NineRouterBaseUrl = "http://localhost:20128"
$NineRouterApiKey   = $env:NINEROUTER_KEY

$global:TestsPassed = 0
$global:TestsFailed = 0

# ---------------------------------------------------------------------------
# Section 1 – Keyword router → model selection
# ---------------------------------------------------------------------------
Write-Section "Keyword Router → Model Selection"

$routerCases = @(
    @{ Prompt = "Design a complex architecture for microservices"; Expected = "auto-berat"    }
    @{ Prompt = "Review and summarize this code"                  ; Expected = "auto-sedang" }
    @{ Prompt = "What is Python?"                                 ; Expected = "auto-ringan" }
)

foreach ($case in $routerCases) {
    $actual = Get-TaskComplexity -Prompt $case.Prompt
    if ($actual -eq $case.Expected) {
        Write-Pass   -Prompt $case.Prompt -Expected $case.Expected -Actual $actual
        $global:TestsPassed++
    }
    else {
        Write-Fail   -Prompt $case.Prompt -Expected $case.Expected -Actual $actual
        $global:TestsFailed++
    }
}

# ---------------------------------------------------------------------------
# Section 2 – 9Router combo availability
# ---------------------------------------------------------------------------
Write-Section "9Router Combo Availability ($NineRouterBaseUrl)"

$combos = @("auto-berat", "auto-sedang", "auto-ringan")

try {
    $headers = @{
        "Authorization" = "Bearer $NineRouterApiKey"
        "Content-Type"  = "application/json"
    }

    $response   = Invoke-RestMethod -Uri "$NineRouterBaseUrl/v1/models" -Headers $headers -Method Get -ErrorAction Stop
    [array]$modelIds = @($response.data.id)

    foreach ($combo in $combos) {
        if ($modelIds -contains $combo) {
            Write-Pass   -Prompt $combo -Expected "available" -Actual "available"
            $global:TestsPassed++
        }
        else {
            Write-Fail   -Prompt $combo -Expected "available" -Actual "not found"
            $global:TestsFailed++
        }
    }
}
catch {
    Write-Host "  [SKIP]" -ForegroundColor Yellow -NoNewline
    Write-Host " 9Router unreachable at $NineRouterBaseUrl – combo checks skipped"
    Write-Host "  Error: $_" -ForegroundColor DarkGray
    $global:TestsFailed += $combos.Count
}

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
Write-Section "Summary"
Write-Host "  Passed: $($global:TestsPassed)" -ForegroundColor Green
Write-Host "  Failed: $($global:TestsFailed)" -ForegroundColor $(if ($global:TestsFailed -gt 0) { "Red" } else { "Green" })

if ($global:TestsFailed -eq 0) {
    Write-Host "`n[Integration tests complete!]" -ForegroundColor Green
}
else {
    Write-Host "`n[Some integration tests failed – review output above]" -ForegroundColor Red
    exit 1
}
