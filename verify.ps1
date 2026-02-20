$proxy = "http://127.0.0.1:7897"
$headers = @{
    'Authorization' = 'Bearer moltbook_sk_mBZlubCuTFQcbh1M-XQH3NI8Fy23i_u5'
    'Content-Type' = 'application/json'
}

# Parse the challenge: "28 Newtons + 15 Newtons"
$answer = "43.00"

$verifyBody = @{
    verification_code = "moltbook_verify_aed9657e15565ea4e8634c60a5f16b07"
    answer = $answer
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'https://www.moltbook.com/api/v1/verify' -Method Post -Headers $headers -Body $verifyBody -Proxy $proxy -ErrorAction Stop
    Write-Host "Verification Success!"
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Verification Error: $_"
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.Value__)"
}
