# scripts/start-searxng.ps1
# Auto-start SearXNG Docker container with fixed name and port

$ErrorActionPreference = "Stop"
$prevEAP = $global:ErrorActionPreference
try {
    $global:ErrorActionPreference = "Stop"

    Write-Host "`n🔍 Checking SearXNG..." -ForegroundColor Cyan

    # Check if container exists and running
    $running = docker ps --filter "name=searxng-fixed" --format "{{.Names}}" 2>$null
    if ($running -eq "searxng-fixed") {
        Write-Host "   ✅ SearXNG running on port 8080" -ForegroundColor Green
        exit 0
    }

    # Check if container exists but stopped
    $exists = docker ps -a --filter "name=searxng-fixed" --format "{{.Names}}" 2>$null
    if ($exists -eq "searxng-fixed") {
        Write-Host "   ⏳ Starting existing container..." -ForegroundColor Yellow
        docker start searxng-fixed
        Start-Sleep -Seconds 3
    } else {
        Write-Host "   📦 Creating new container..." -ForegroundColor Yellow
        $composePath = Join-Path $PSScriptRoot "..\searxng\docker-compose.yml"
        if (Test-Path $composePath) {
            docker compose -f $composePath up -d
        } else {
            docker run -d --name searxng-fixed -p 8080:8080 `
                -e SEARXNG_BASE_URL=http://localhost:8080/ `
                searxng/searxng:latest
        }
        Start-Sleep -Seconds 5
    }

    # Verify it's running
    $running = docker ps --filter "name=searxng-fixed" --format "{{.Names}}" 2>$null
    if ($running -eq "searxng-fixed") {
        Write-Host "   ✅ SearXNG started on http://localhost:8080" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Failed to start SearXNG" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    $global:ErrorActionPreference = $prevEAP
}
