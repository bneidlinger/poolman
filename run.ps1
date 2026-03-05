$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# Start the Flask app
Start-Process "$PSScriptRoot\venv\Scripts\python.exe" -ArgumentList "app.py"

# Wait for server to spin up
Start-Sleep -Seconds 3

# Launch Chrome in fullscreen kiosk mode
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" `
    -ArgumentList "--kiosk http://127.0.0.1:5000/lab"