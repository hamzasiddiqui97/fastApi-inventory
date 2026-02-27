# Start the React dev server (bypasses PowerShell execution policy for npm)
Set-Location $PSScriptRoot
if (-not (Test-Path "node_modules")) {
    & "C:\Program Files\nodejs\npm.cmd" install
}
& "C:\Program Files\nodejs\npm.cmd" start
