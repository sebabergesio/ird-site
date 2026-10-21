# Publica site/ en el repo público de GitHub Pages (sebabergesio/ird-site)
# mediante git subtree. El repo de trabajo (este) sigue privado.
#
# Uso (desde la raíz del proyecto):
#   powershell -ExecutionPolicy Bypass -File tools/publish_pages.ps1
#   powershell -ExecutionPolicy Bypass -File tools/publish_pages.ps1 -NoBuild
#   powershell -ExecutionPolicy Bypass -File tools/publish_pages.ps1 -Force
#
# Requiere el remote 'site' apuntando al repo público:
#   git remote add site https://github.com/sebabergesio/ird-site.git

param(
    [string]$Python = "python",
    [string]$Git = "git",
    [string]$Remote = "site",
    [string]$Branch = "master",
    [switch]$NoBuild,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$tools = $PSScriptRoot
$root = Split-Path $tools -Parent
$publico = Join-Path $root "site"

if (-not (Test-Path (Join-Path $publico "index.html"))) {
    throw "No se encontro el sitio publico en $publico"
}

Push-Location $root
try {
    if (-not $NoBuild) {
        & $Python "tools\build_site.py"
        if ($LASTEXITCODE -ne 0) { throw "build_site.py fallo con codigo $LASTEXITCODE" }
        & $Python "tools\check_site.py"
        if ($LASTEXITCODE -ne 0) { throw "check_site.py fallo con codigo $LASTEXITCODE" }
    }

    $remotes = & $Git remote
    if ($remotes -notcontains $Remote) {
        throw "No existe el remote '$Remote'. Configuralo con: $Git remote add $Remote https://github.com/sebabergesio/ird-site.git"
    }

    $dirty = & $Git status --porcelain -- site
    if ($dirty) {
        throw "site/ tiene cambios sin commitear. Commitea site/ y src/ juntos antes de publicar."
    }

    if ($Force) {
        $split = (& $Git subtree split --prefix site).Trim()
        if (-not $split) { throw "git subtree split no devolvio un commit" }
        & $Git push $Remote "$($split):$Branch" --force
        if ($LASTEXITCODE -ne 0) { throw "git push fallo con codigo $LASTEXITCODE" }
    }
    else {
        & $Git subtree push --prefix site $Remote $Branch
        if ($LASTEXITCODE -ne 0) {
            throw "git subtree push fallo con codigo $LASTEXITCODE. Si el remoto divergio, repetir con -Force."
        }
    }
}
finally {
    Pop-Location
}

Write-Host "OK: site/ publicado en $Remote/$Branch (GitHub Pages)"
