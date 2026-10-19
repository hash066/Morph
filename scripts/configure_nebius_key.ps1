$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath 'E:/Winter/Morph'
[System.Reflection.Assembly]::Load('System.Security.Cryptography.ProtectedData') | Out-Null
$morphSecretDirectory = Join-Path (Get-Location) 'data'
New-Item -ItemType Directory -Force -Path $morphSecretDirectory | Out-Null
Write-Host 'Morph: paste your Nebius API key below, then press Enter.'
Write-Host 'Input is hidden. The key will be encrypted using Windows DPAPI, not saved as plaintext.'
$morphSecureKey = Read-Host 'Nebius API key' -AsSecureString
if ($morphSecureKey.Length -eq 0) { throw 'No key entered; nothing saved.' }
try {
    $morphKeyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($morphSecureKey)
    try {
        $morphKeyBytes = [System.Text.Encoding]::UTF8.GetBytes([Runtime.InteropServices.Marshal]::PtrToStringBSTR($morphKeyPointer))
        $morphCipherBytes = [System.Security.Cryptography.ProtectedData]::Protect($morphKeyBytes, $null, [System.Security.Cryptography.DataProtectionScope]::CurrentUser)
        [System.IO.File]::WriteAllText((Join-Path $morphSecretDirectory 'nebius-key.dpapi'), ('morph-dpapi-v1:' + [Convert]::ToBase64String($morphCipherBytes)))
    } finally {
        if ($null -ne $morphKeyBytes) { [Array]::Clear($morphKeyBytes, 0, $morphKeyBytes.Length) }
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($morphKeyPointer)
    }
    Write-Host 'Saved encrypted key for this Windows account. No inference or compute was started.'
} finally {
    $morphSecureKey.Dispose()
    Remove-Variable morphKeyBytes,morphCipherBytes -ErrorAction SilentlyContinue
}
