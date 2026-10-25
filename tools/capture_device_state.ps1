[CmdletBinding()]
param(
    [string]$DeviceUrl = 'http://192.168.1.101',
    [string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    $stamp = Get-Date -Format 'yyyy-MM-dd-HHmmss'
    $OutputDirectory = Join-Path $projectRoot "evidence\logs\$stamp"
}

$outputPath = [System.IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $outputPath) {
    throw "Ausgabeordner existiert bereits; vorhandene Belege werden nicht ueberschrieben: $outputPath"
}
New-Item -ItemType Directory -Path $outputPath | Out-Null

$hostUri = "$DeviceUrl/cgi-bin/index.cgi?id=host"
$logUri = "$DeviceUrl/cgi-bin/index.cgi?id=logcat"
$hostData = Invoke-RestMethod -Uri $hostUri -TimeoutSec 15
$hostData | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $outputPath 'host.json') -Encoding utf8NoBOM

$encryptedPath = Join-Path $outputPath 'logcat.encrypted'
$plainPath = Join-Path $outputPath 'logcat.txt'
$metadataPath = Join-Path $outputPath 'logcat-metadata.json'
Invoke-WebRequest -Uri $logUri -OutFile $encryptedPath -TimeoutSec 30

$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw "Projekt-Python fehlt: $python"
}

& $python (Join-Path $PSScriptRoot 'decrypt_logcat.py') $encryptedPath $plainPath --metadata $metadataPath
if ($LASTEXITCODE -ne 0) {
    throw "Log-Entschluesselung fehlgeschlagen (Exitcode $LASTEXITCODE)"
}

$currentHash = (Get-FileHash -LiteralPath $encryptedPath -Algorithm SHA256).Hash
$previousExports = Get-ChildItem -LiteralPath (Join-Path $projectRoot 'evidence\logs') -Filter 'logcat.encrypted' -Recurse -File |
    Where-Object { $_.FullName -ne $encryptedPath } | Sort-Object LastWriteTime -Descending
foreach ($previous in $previousExports) {
    if ((Get-FileHash -LiteralPath $previous.FullName -Algorithm SHA256).Hash -eq $currentHash) {
        Write-Warning "Identischer Export wie $($previous.Directory.Name). Der Adapter cached /tmp/log.gz. Fuer einen neuen Versuch den Adapter vorher neu starten und erst NACH der Musikwiedergabe das Log abrufen."
        break
    }
}

$hashLines = Get-ChildItem -LiteralPath $outputPath -File | Sort-Object Name | ForEach-Object {
    $hash = Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256
    '{0}  {1}' -f $hash.Hash, $_.Name
}
$hashLines | Set-Content -LiteralPath (Join-Path $outputPath 'SHA256SUMS.txt') -Encoding ascii

Write-Host "Diagnose gesichert: $outputPath"
