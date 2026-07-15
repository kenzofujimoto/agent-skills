param([int]$Port = 9222)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-Cdp {
    try {
        $result = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/json/version" -TimeoutSec 2
        return [bool]$result.webSocketDebuggerUrl
    }
    catch { return $false }
}

if (-not (Test-Cdp)) {
    $profile = Join-Path $HOME '.scroll-world-chrome'
    $candidates = @(
        "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
        "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
    )
    $chrome = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
    if (-not $chrome) { throw 'Google Chrome regular não encontrado.' }

    New-Item -ItemType Directory -Path $profile -Force | Out-Null
    Start-Process -FilePath $chrome -ArgumentList @(
        "--user-data-dir=`"$profile`"",
        "--remote-debugging-port=$Port",
        '--no-first-run',
        '--no-default-browser-check',
        '--new-window',
        'https://sketchfab.com/features/free-3d-models'
    )

    $ready = $false
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 1
        if (Test-Cdp) { $ready = $true; break }
    }
    if (-not $ready) { throw "Chrome abriu, mas CDP $Port não respondeu." }
}

Write-Host "[OK] Browser dedicado disponível em CDP $Port"
agent-browser --cdp $Port tab
if ($LASTEXITCODE -ne 0) { throw 'agent-browser não conseguiu conectar ao Chrome dedicado.' }
