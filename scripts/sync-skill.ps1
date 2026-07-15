[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z0-9]+(?:-[a-z0-9]+)*$')]
    [string]$Name,

    [string]$Source = 'auto'
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$destination = Join-Path $repoRoot "skills/$Name"
$candidates = @()
if ($Source -eq 'auto') {
    $candidates = @('.agents', '.codex', '.claude') | ForEach-Object { Join-Path $HOME "$_/skills/$Name" } | Where-Object { Test-Path -LiteralPath (Join-Path $_ 'SKILL.md') }
} elseif ($Source -in @('agents', 'codex', 'claude')) {
    $candidates = @(Join-Path $HOME ".$Source/skills/$Name")
} else {
    $candidates = @((Resolve-Path -LiteralPath $Source).Path)
}
if ($candidates.Count -eq 0) { throw "No installed copy of '$Name' was found." }

$selected = $candidates | Sort-Object -Descending -Property @{ Expression = { (Get-ChildItem -LiteralPath $_ -Recurse -File -Force).Count } }, @{ Expression = { (Get-ChildItem -LiteralPath $_ -Recurse -File -Force | Measure-Object Length -Sum).Sum } } | Select-Object -First 1
if (-not (Test-Path -LiteralPath (Join-Path $selected 'SKILL.md'))) { throw "Selected source is missing SKILL.md: $selected" }

$before = if (Test-Path -LiteralPath $destination) { @(Get-ChildItem -LiteralPath $destination -Recurse -File | ForEach-Object { [System.IO.Path]::GetRelativePath($destination, $_.FullName) }) } else { @() }
$backup = Join-Path ([System.IO.Path]::GetTempPath()) "$Name-backup-$([guid]::NewGuid().ToString('N'))"
try {
    if (Test-Path -LiteralPath $destination) { Copy-Item -LiteralPath $destination -Destination $backup -Recurse }
    $preserved = @{}
    foreach ($file in @('README.md', 'CHANGELOG.md')) {
        $path = Join-Path $destination $file
        if (Test-Path -LiteralPath $path) { $preserved[$file] = Get-Content -Raw -LiteralPath $path }
    }
    if (Test-Path -LiteralPath $destination) { Remove-Item -LiteralPath $destination -Recurse -Force }
    Copy-Item -LiteralPath $selected -Destination $destination -Recurse
    Get-ChildItem -LiteralPath $destination -Recurse -Directory -Force | Where-Object { $_.Name -in @('__pycache__','node_modules','dist','build','downloads','private-assets','generated-assets','.scroll-world','.scroll-world-chrome') } | Sort-Object FullName -Descending | Remove-Item -Recurse -Force
    Get-ChildItem -LiteralPath $destination -Recurse -File -Force | Where-Object { $_.Extension -in @('.pyc','.log','.zip','.crdownload','.mp4','.mov','.webm') -or $_.Name -eq '.env' -or ($_.Name -like '.env.*' -and $_.Name -ne '.env.example') } | Remove-Item -Force
    foreach ($file in $preserved.Keys) { Set-Content -LiteralPath (Join-Path $destination $file) -Value $preserved[$file] -Encoding utf8NoBOM -NoNewline }
    & python (Join-Path $repoRoot 'scripts/validate_repo.py')
    if ($LASTEXITCODE -ne 0) { throw "Repository validation failed after synchronization." }
    $after = @(Get-ChildItem -LiteralPath $destination -Recurse -File | ForEach-Object { [System.IO.Path]::GetRelativePath($destination, $_.FullName) })
    $diff = Compare-Object $before $after
    Write-Output "Selected source: $selected"
    Write-Output "Synchronized ${Name}: $(@($diff | Where-Object SideIndicator -eq '=>').Count) added, $(@($diff | Where-Object SideIndicator -eq '<=').Count) removed path(s)."
}
catch {
    if (Test-Path -LiteralPath $backup) {
        if (Test-Path -LiteralPath $destination) { Remove-Item -LiteralPath $destination -Recurse -Force }
        Copy-Item -LiteralPath $backup -Destination $destination -Recurse
    }
    throw
}
finally {
    if (Test-Path -LiteralPath $backup) { Remove-Item -LiteralPath $backup -Recurse -Force }
}
