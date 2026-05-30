# agentmemory-manual-save.ps1
# Usage: .\agentmemory-manual-save.ps1 -Content "Your insight here" [-Type fact|pattern|bug|workflow|architecture|preference] [-Project "MyProject"]

param(
  [Parameter(Mandatory=$true)]
  [string]$Content,

  [ValidateSet("fact", "pattern", "bug", "workflow", "architecture", "preference")]
  [string]$Type = "fact",

  [string]$Project = "Mencari_Jurnal_Ilmiah",

  [string[]]$Concepts,

  [string[]]$Files
)

$baseUrl = "http://localhost:3111"
$body = @{
  content = $Content
  project = $Project
  type = $Type
}
if ($Concepts) { $body.concepts = $Concepts }
if ($Files) { $body.files = $Files }
$json = $body | ConvertTo-Json -Depth 3

try {
  $result = Invoke-RestMethod -Uri "$baseUrl/agentmemory/remember" -Method Post -ContentType "application/json" -Body $json
  Write-Host "Memory saved: $($result.memory.id)" -ForegroundColor Green
  Write-Host "Type: $($result.memory.type)" -ForegroundColor Cyan
  Write-Host "Project: $($result.memory.project)" -ForegroundColor Cyan
} catch {
  Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
  if ($_.ErrorDetails.Message) { $_.ErrorDetails.Message | ConvertFrom-Json | ForEach-Object { $_.error } }
  exit 1
}
