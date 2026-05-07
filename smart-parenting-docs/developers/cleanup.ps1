# cleanup.ps1
# Run this in your project root to clean the repository for first-run
# WARNING: This deletes files permanently. Review before running.

Write-Host "Cleaning repository for first-run setup..." -ForegroundColor Cyan
Write-Host ""

# === GENERATED DIRECTORIES ===
$dirs = @("node_modules", ".expo", ".expo-shared", "android", "ios", "dist", "web-build", "coverage")
foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Remove-Item -Recurse -Force $dir
        Write-Host "  Deleted directory: $dir" -ForegroundColor Green
    }
}

# === LOG FILES ===
Get-ChildItem -Filter "*.log" -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item -Force $_.FullName
    Write-Host "  Deleted log: $($_.Name)" -ForegroundColor Green
}
Remove-Item -Force "npm-debug.log*" -ErrorAction SilentlyContinue
Remove-Item -Force "yarn-error.log*" -ErrorAction SilentlyContinue
Remove-Item -Force "yarn-debug.log*" -ErrorAction SilentlyContinue

# === SECRETS ===
if (Test-Path ".env") {
    Remove-Item -Force ".env"
    Write-Host "  Deleted secrets file: .env" -ForegroundColor Green
}

# === OS JUNK ===
Remove-Item -Force ".DS_Store" -ErrorAction SilentlyContinue
Remove-Item -Force "Thumbs.db" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Cleanup complete. Run 'git status' to review changes." -ForegroundColor Cyan
Write-Host "Remember to commit .gitignore and .env.example if not already present." -ForegroundColor Yellow
