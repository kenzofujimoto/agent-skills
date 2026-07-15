[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z0-9]+(?:-[a-z0-9]+)*$')]
    [string]$Name
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
& python (Join-Path $PSScriptRoot 'validate_repo.py')
if ($LASTEXITCODE -ne 0) { throw 'Repository validation failed; package was not created.' }

$manifest = Get-Content -Raw -LiteralPath (Join-Path $repoRoot 'skills.json') | ConvertFrom-Json
$entry = @($manifest.skills | Where-Object name -eq $Name)
if ($entry.Count -ne 1) { throw "Expected exactly one manifest entry for '$Name'." }
$source = Join-Path $repoRoot $entry[0].path
if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))) { throw "Skill '$Name' is missing SKILL.md." }

$dist = Join-Path $repoRoot 'dist'
$archive = Join-Path $dist "$Name-v$($entry[0].version).zip"
$checksum = "$archive.sha256"
$staging = Join-Path ([System.IO.Path]::GetTempPath()) "$Name-package-$([guid]::NewGuid().ToString('N'))"
try {
    New-Item -ItemType Directory -Force -Path $dist, $staging | Out-Null
    Get-ChildItem -LiteralPath $source -Recurse -File -Force | Where-Object {
        $_.Extension -notin @('.pyc','.log','.zip','.crdownload','.mp4','.mov','.webm') -and
        $_.Name -ne '.env' -and -not ($_.Name -like '.env.*' -and $_.Name -ne '.env.example') -and
        ([System.IO.Path]::GetRelativePath($source, $_.FullName) -split '[\\/]' | Where-Object { $_ -in @('__pycache__','node_modules','dist','build','downloads','private-assets','generated-assets','.scroll-world','.scroll-world-chrome') }).Count -eq 0
    } | ForEach-Object {
        $relative = [System.IO.Path]::GetRelativePath($source, $_.FullName)
        $target = Join-Path $staging $relative
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $target
    }
    Remove-Item -LiteralPath $archive, $checksum -Force -ErrorAction SilentlyContinue
    Compress-Archive -Path (Join-Path $staging '*') -DestinationPath $archive -CompressionLevel Optimal
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $archive).Hash.ToLowerInvariant()
    Set-Content -LiteralPath $checksum -Value "$hash  $([System.IO.Path]::GetFileName($archive))" -Encoding ascii
    Write-Output "Created $archive"
    Write-Output "SHA256 $hash"
}
finally {
    if (Test-Path -LiteralPath $staging) { Remove-Item -LiteralPath $staging -Recurse -Force }
}
