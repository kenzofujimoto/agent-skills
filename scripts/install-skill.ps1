[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z0-9]+(?:-[a-z0-9]+)*$')]
    [string]$Name,

    [string[]]$Targets = @('agents'),

    [string]$HomePath = $HOME
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $repoRoot "skills/$Name"

if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md') -PathType Leaf)) {
    throw "Skill '$Name' is missing SKILL.md at $source"
}

$targetNames = @($Targets | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim().ToLowerInvariant() } | Where-Object { $_ })
$allowed = @('agents', 'codex', 'claude')
$invalid = @($targetNames | Where-Object { $_ -notin $allowed })
if ($invalid.Count -gt 0) {
    throw "Unknown target(s): $($invalid -join ', '). Valid targets: $($allowed -join ', ')."
}

$excludedDirectories = @('__pycache__', 'node_modules', 'dist', 'build', 'downloads', 'private-assets', 'generated-assets', '.scroll-world', '.scroll-world-chrome')
$excludedExtensions = @('.pyc', '.log', '.zip', '.crdownload', '.mp4', '.mov', '.webm')

function Copy-FilteredTree {
    param([string]$From, [string]$To)
    New-Item -ItemType Directory -Force -Path $To | Out-Null
    Get-ChildItem -LiteralPath $From -Recurse -File -Force | ForEach-Object {
        $relative = [System.IO.Path]::GetRelativePath($From, $_.FullName)
        $parts = $relative -split '[\\/]'
        if (($parts | Where-Object { $_ -in $excludedDirectories }).Count -gt 0) { return }
        if ($_.Extension.ToLowerInvariant() -in $excludedExtensions) { return }
        if ($_.Name -eq '.env' -or ($_.Name -like '.env.*' -and $_.Name -ne '.env.example')) { return }
        $targetFile = Join-Path $To $relative
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $targetFile) | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $targetFile -Force
    }
}

foreach ($targetName in $targetNames) {
    $base = Join-Path $HomePath ".$targetName/skills"
    $destination = Join-Path $base $Name
    $staging = Join-Path $base ".$Name.installing-$([guid]::NewGuid().ToString('N'))"
    New-Item -ItemType Directory -Force -Path $base | Out-Null
    try {
        Copy-FilteredTree -From $source -To $staging
        if (-not (Test-Path -LiteralPath (Join-Path $staging 'SKILL.md') -PathType Leaf)) {
            throw "Staged installation is missing SKILL.md"
        }
        if (Test-Path -LiteralPath $destination) {
            Remove-Item -LiteralPath $destination -Recurse -Force
        }
        Move-Item -LiteralPath $staging -Destination $destination
        Write-Output "Installed $Name -> $destination"
    }
    finally {
        if (Test-Path -LiteralPath $staging) {
            Remove-Item -LiteralPath $staging -Recurse -Force
        }
    }
}
