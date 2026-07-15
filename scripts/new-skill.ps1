[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Name
)

$ErrorActionPreference = 'Stop'
if ($Name -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$') {
    throw "Name must be a lowercase hyphenated slug."
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$template = Join-Path $repoRoot 'templates/skill-template'
$destination = Join-Path $repoRoot "skills/$Name"
if (Test-Path -LiteralPath $destination) {
    throw "Skill '$Name' already exists; refusing to overwrite it."
}

$title = (($Name -split '-') | ForEach-Object { (Get-Culture).TextInfo.ToTitleCase($_) }) -join ' '
$date = Get-Date -Format 'yyyy-MM-dd'
Copy-Item -LiteralPath $template -Destination $destination -Recurse
Get-ChildItem -LiteralPath $destination -Recurse -File | ForEach-Object {
    $content = Get-Content -Raw -LiteralPath $_.FullName
    $content = $content.Replace('{{SKILL_NAME}}', $Name).Replace('{{SKILL_TITLE}}', $title).Replace('{{DATE}}', $date)
    Set-Content -LiteralPath $_.FullName -Value $content -Encoding utf8NoBOM -NoNewline
}

$manifestPath = Join-Path $repoRoot 'skills.json'
$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
$entry = [pscustomobject]@{
    name = $Name
    version = '0.1.0'
    status = 'draft'
    path = "skills/$Name"
    description = "TODO: describe $Name."
    categories = @('uncategorized')
    targets = @('agents', 'codex', 'claude')
}
$manifest.skills = @($manifest.skills) + $entry
$manifest | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $manifestPath -Encoding utf8NoBOM
Write-Output "Created skills/$Name at version 0.1.0"
