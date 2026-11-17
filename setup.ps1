
$ErrorActionPreference = "Stop"

Write-Host "=== Setting up Loghmeh ===" -ForegroundColor Cyan

# Create Python virtual environment if missing
if (!(Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"

# Install Python dependencies
Write-Host "Installing Python packages..."
python -m pip install -r requirements.txt

# Install Node.js dependencies
Write-Host "Installing Node.js packages..."
npm install

# Build Tailwind CSS
Write-Host "Building Tailwind CSS..."
npm run build

Write-Host "Setup completed successfully!" -ForegroundColor Green
