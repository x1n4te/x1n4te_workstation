# verify-clean.ps1
# Run this to check if your repo is clean for first-run

$errors = 0

$forbiddenPaths = @(
    "node_modules",
    ".expo",
    ".expo-shared",
    "android",
    "ios",
    "dist",
    "web-build",
    "coverage",
    ".env"
)

Write-Host "Checking for forbidden files/directories..." -ForegroundColor Cyan

foreach ($path in $forbiddenPaths) {
    $matches = Get-ChildItem -Path $path -ErrorAction SilentlyContinue
    if ($matches) {
        Write-Host "  FOUND: $path" -ForegroundColor Red
        $errors++
    }
}

# Check log files
$logFiles = Get-ChildItem -Filter "*.log" -ErrorAction SilentlyContinue
if ($logFiles) {
    foreach ($f in $logFiles) {
        Write-Host "  FOUND: $($f.Name)" -ForegroundColor Red
        $errors++
    }
}

# Check .gitignore
if (-not (Test-Path .gitignore)) {
    Write-Host "  MISSING: .gitignore" -ForegroundColor Red
    $errors++
} else {
    $gitignore = Get-Content .gitignore -Raw
    $required = @("node_modules/", ".env", ".expo/", "android/", "ios/")
    foreach ($entry in $required) {
        if ($gitignore -notmatch [regex]::Escape($entry)) {
            Write-Host "  .gitignore missing: $entry" -ForegroundColor Yellow
            $errors++
        }
    }
}

# Check .env.example
if (-not (Test-Path .env.example)) {
    Write-Host "  MISSING: .env.example (template for secrets)" -ForegroundColor Red
    $errors++
}

# Check package.json
if (-not (Test-Path package.json)) {
    Write-Host "  MISSING: package.json" -ForegroundColor Red
    $errors++
}

Write-Host ""
if ($errors -eq 0) {
    Write-Host "Repository is clean and ready for first run!" -ForegroundColor Green
} else {
    Write-Host "Found $errors issue(s). Fix before sharing the repository." -ForegroundColor Red
    exit 1
}
