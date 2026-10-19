# Read-only model catalog probe. Never print credentials or provider error bodies.
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath 'E:/Winter/Morph'
$morphKeyPath = Join-Path (Get-Location) 'data/nebius-key.dpapi'
if (-not (Test-Path -LiteralPath $morphKeyPath)) { throw 'No encrypted Morph key configured.' }
[System.Reflection.Assembly]::Load('System.Security.Cryptography.ProtectedData') | Out-Null
$morphEncryptedText = [System.IO.File]::ReadAllText($morphKeyPath)
if ($morphEncryptedText.StartsWith('morph-dpapi-v1:')) {
    $morphCipherBytes = [Convert]::FromBase64String($morphEncryptedText.Substring(15))
    $morphEncoding = [System.Text.Encoding]::UTF8
} elseif ($morphEncryptedText -match '^[0-9a-fA-F]+$') {
    # ConvertFrom-SecureString's default Windows format is DPAPI-protected UTF-16, encoded as hex.
    $morphCipherBytes = [Convert]::FromHexString($morphEncryptedText)
    $morphEncoding = [System.Text.Encoding]::Unicode
} else { throw 'Unrecognized encrypted key format.' }
$morphKeyBytes = [System.Security.Cryptography.ProtectedData]::Unprotect($morphCipherBytes, $null, [System.Security.Cryptography.DataProtectionScope]::CurrentUser)
try {
    $morphPlainKey = $morphEncoding.GetString($morphKeyBytes).Trim()
    $morphHeaders = @{ Authorization = ('Bearer ' + $morphPlainKey) }
    try {
        $morphResponse = Invoke-RestMethod -Uri 'https://api.tokenfactory.nebius.com/v1/models' -Headers $morphHeaders -Method Get -MaximumRedirection 0 -TimeoutSec 30
        $morphModels = @($morphResponse.data | Where-Object { $_.id -match '^nvidia/.*nemotron' } | ForEach-Object { $_.id })
        $morphRecord = @{ checked_at = [DateTime]::UtcNow.ToString('o'); kind = 'authenticated_model_catalog'; models = $morphModels; inference_performed = $false; credit_verified = $false }
        $morphRecord | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath 'docs/verification/nebius-model-catalog.json'
        $morphRecord | ConvertTo-Json -Depth 4
    } catch {
        Write-Output 'Nebius catalog check failed. No credential or response body has been printed.'
        exit 2
    }
} finally {
    [Array]::Clear($morphKeyBytes, 0, $morphKeyBytes.Length)
    Remove-Variable morphPlainKey,morphHeaders -ErrorAction SilentlyContinue
}
