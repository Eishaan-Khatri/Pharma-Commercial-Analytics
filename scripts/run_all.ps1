Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

python -m src.run_pipeline --rows 25000 --force

Write-Host "Pipeline complete. Open reports/final_report.md and dashboards/screenshots/executive_dashboard.svg."

