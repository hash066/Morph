param([ValidateSet('check', 'recovery')][string]$Mode = 'check')
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath 'E:/Winter/Morph'
$morphKeyPath = 'E:/Winter/Morph/data/nebius-key.dpapi'
if (-not (Test-Path -LiteralPath $morphKeyPath)) { throw 'No encrypted Morph key configured.' }
[System.Reflection.Assembly]::Load('System.Security.Cryptography.ProtectedData') | Out-Null
$morphEncryptedText = [System.IO.File]::ReadAllText($morphKeyPath)
if ($morphEncryptedText.StartsWith('morph-dpapi-v1:')) {
    $morphCipherBytes = [Convert]::FromBase64String($morphEncryptedText.Substring(15))
    $morphEncoding = [System.Text.Encoding]::UTF8
} elseif ($morphEncryptedText -match '^[0-9a-fA-F]+$') {
    $morphCipherBytes = [Convert]::FromHexString($morphEncryptedText)
    $morphEncoding = [System.Text.Encoding]::Unicode
} else { throw 'Unrecognized encrypted key format.' }
$morphKeyBytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
    $morphCipherBytes, $null, [System.Security.Cryptography.DataProtectionScope]::CurrentUser
)
try {
    $env:NEBIUS_API_KEY = $morphEncoding.GetString($morphKeyBytes).Trim()
    $morphScript = if ($Mode -eq 'recovery') {
        'E:/Winter/Morph/scripts/live_recovery_selection.py'
    } else {
        'E:/Winter/Morph/scripts/live_planner_check.py'
    }
    & 'E:/Winter/Morph/.venv/Scripts/python.exe' $morphScript
    if ($LASTEXITCODE -ne 0) { throw 'Live planner check failed.' }
} finally {
    Remove-Item Env:NEBIUS_API_KEY -ErrorAction SilentlyContinue
    [Array]::Clear($morphKeyBytes, 0, $morphKeyBytes.Length)
    Remove-Variable morphEncryptedText,morphCipherBytes,morphKeyBytes,morphEncoding -ErrorAction SilentlyContinue
}
