$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath 'E:/Winter/Morph'
$morphPreviousTemp = $env:TEMP
$morphPreviousTmp = $env:TMP
$morphPreviousCache = $env:UV_CACHE_DIR
$morphPreviousLinkMode = $env:UV_LINK_MODE
try {
    New-Item -ItemType Directory -Force -Path 'data/build-temp' | Out-Null
    $env:TEMP = 'E:/Winter/Morph/data/build-temp'
    $env:TMP = $env:TEMP
    $env:UV_CACHE_DIR = 'E:/Winter/Morph/data/uv-cache'
    $env:UV_LINK_MODE = 'copy'
    $morphCommit = git -C vendor/IsaacLabTutorial rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $morphCommit -ne '9a4286b4bc8a5720ac97f87e5e0140f7542c22d9') {
        throw 'Fetch the pinned tutorial checkout before running setup.'
    }
    uv sync --project vendor/IsaacLabTutorial --locked --python 3.12 --no-python-downloads
    if ($LASTEXITCODE -ne 0) { throw 'Pinned simulator setup failed; inspect output, do not mark runtime verified.' }
} finally {
    $env:TEMP = $morphPreviousTemp
    $env:TMP = $morphPreviousTmp
    $env:UV_CACHE_DIR = $morphPreviousCache
    $env:UV_LINK_MODE = $morphPreviousLinkMode
}
