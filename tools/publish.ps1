param(
    [string]$Python = "python",
    [switch]$NoBuild,
    [switch]$Zip
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$tools = $PSScriptRoot
$root = Split-Path $tools -Parent
$publico = Join-Path $root "site"
$out = Join-Path $root "var"
$dist = Join-Path $out "dist"
$zipPath = Join-Path $out "ird-site.zip"

if (-not (Test-Path (Join-Path $publico "index.html"))) {
    throw "No se encontro el sitio publico en $publico"
}
if (-not (Test-Path (Join-Path $tools "build_site.py"))) {
    throw "No se encontro build_site.py en $tools"
}

New-Item -ItemType Directory -Force $out | Out-Null

if (-not $NoBuild) {
    Push-Location $root
    try {
        & $Python "tools\build_site.py"
        if ($LASTEXITCODE -ne 0) { throw "build_site.py fallo con codigo $LASTEXITCODE" }
    }
    finally {
        Pop-Location
    }
}

if (Test-Path $dist) {
    Remove-Item -LiteralPath $dist -Recurse -Force
}
New-Item -ItemType Directory -Path $dist | Out-Null

# Copia solo la carpeta publica. El .git del sitio no se publica.
& robocopy $publico $dist /E /XD "$publico\.git" /NFL /NDL /NJH /NJS /NP
if ($LASTEXITCODE -ge 8) {
    throw "robocopy fallo con codigo $LASTEXITCODE"
}

$required = @(
    "index.html",
    "documento.html",
    "laboratorio.html",
    "sobre-mi.html",
    "contacto.html",
    "terminos.html",
    "404.html",
    "en\index.html",
    "en\document.html",
    "en\lab.html",
    "en\about.html",
    "en\contact.html",
    "en\terms.html",
    "robots.txt",
    "sitemap.xml",
    "assets\css\style.css",
    "assets\js\site.js",
    "assets\js\rates.js",
    "assets\docs\muestra-SOL-001.pdf",
    "assets\docs\muestra-SOL-001-en.pdf",
    "assets\img\og-ird-es.png",
    "assets\img\og-ird-en.png"
)
foreach ($rel in $required) {
    if (-not (Test-Path (Join-Path $dist $rel))) {
        throw "Falta un archivo obligatorio en dist: $rel"
    }
}

# Material interno y fuentes que nunca deben llegar a produccion.
# assets\docs es publico: contiene las muestras PDF.
$forbiddenRootDirs = @(
    ".git", ".superpowers", "_legacy", "admin", "archive", "content",
    "documentos", "Recursos", "herramientas", "docs", "src", "tools", "var", "qa"
)
$forbiddenFileNames = @("qa-mobile.html", "qa-view.html")
$forbiddenExtensions = @(".tex", ".py", ".ps1", ".md", ".log", ".aux", ".out")
$bad = Get-ChildItem -LiteralPath $dist -Recurse -Force | Where-Object {
    $rel = $_.FullName.Substring($dist.Length).TrimStart('\')
    $first = $rel.Split('\')[0]
    ($first -in $forbiddenRootDirs) -or
    ($_.Name -in $forbiddenFileNames) -or
    ($_.PSIsContainer -eq $false -and $_.Extension -in $forbiddenExtensions)
}
if ($bad) {
    $detalle = ($bad | ForEach-Object { $_.FullName.Substring($dist.Length + 1) }) -join ", "
    throw "Archivos internos o prohibidos dentro de dist: $detalle"
}

$textos = Get-ChildItem -LiteralPath $dist -Recurse -File -Include *.html, *.txt, *.xml, *.css, *.js
$prohibida = $textos | Select-String -SimpleMatch "ird.com.ar"
if ($prohibida) {
    throw "Se encontro ird.com.ar en dist (ver check_site.py)"
}

Push-Location $root
try {
    & $Python "tools\check_site.py" --root $dist
    if ($LASTEXITCODE -ne 0) { throw "check_site.py fallo con codigo $LASTEXITCODE" }
}
finally {
    Pop-Location
}

if ($Zip) {
    if (Test-Path $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
    Compress-Archive -Path (Join-Path $dist "*") -DestinationPath $zipPath -CompressionLevel Optimal
    Write-Host "ZIP: $zipPath"
}

$fileCount = (Get-ChildItem -LiteralPath $dist -Recurse -File -Force).Count
$size = [math]::Round(((Get-ChildItem -LiteralPath $dist -Recurse -File -Force | Measure-Object Length -Sum).Sum / 1MB), 2)
Write-Host "OK: sitio publico listo en $dist ($fileCount archivos, $size MB)"
