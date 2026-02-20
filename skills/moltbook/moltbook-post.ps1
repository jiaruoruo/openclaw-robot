# Moltbook Auto-Post with Auto-Verify
# Usage: .\moltbook-post.ps1 -Title "Your post title" -Submolt "general"

param(
    [Parameter(Mandatory=$true)]
    [string]$Title,
    
    [Parameter(Mandatory=$false)]
    [string]$Submolt = "general"
)

$API_KEY = "moltbook_sk_mBZlubCuTFQcbh1M-XQH3NI8Fy23i_u5"
$PROXY = "--proxy http://127.0.0.1:7897"
$BASE_URL = "https://www.moltbook.com/api/v1"

$headers = @{
    "Authorization" = "Bearer $API_KEY"
    "Content-Type" = "application/json"
}

# Step 1: Create post
$body = @{
    title = $Title
    submolt_name = $Submolt
} | ConvertTo-Json

Write-Host "📝 Posting..."
$postResp = Invoke-RestMethod -Uri "$BASE_URL/posts" -Method Post -Headers $headers -Body $body

if ($postResp.success) {
    Write-Host "✅ Post created! Post ID: $($postResp.post.id)"
    
    # Step 2: Check for verification challenge
    if ($postResp.post.verification) {
        $code = $postResp.post.verification.verification_code
        $challenge = $postResp.post.verification.challenge_text
        
        Write-Host "🔐 Verification required: $challenge"
        
        # Parse math problem - extract numbers
        # Format: "X Newtons + Y Newtons" or similar
        $numbers = [regex]::Matches($challenge, '\d+') | ForEach-Object { [double]$_.Value }
        
        if ($numbers.Count -ge 2) {
            # Calculate sum (assuming addition)
            $answer = ($numbers | Measure-Object -Sum).Sum
            $answerFormatted = "{0:N2}" -f $answer
            
            Write-Host "🧮 Calculated answer: $answerFormatted"
            
            # Step 3: Submit verification
            $verifyBody = @{
                verification_code = $code
                answer = $answerFormatted
            } | ConvertTo-Json
            
            $verifyResp = Invoke-RestMethod -Uri "$BASE_URL/verify" -Method Post -Headers $headers -Body $verifyBody
            
            if ($verifyResp.success) {
                Write-Host "🎉 Verification complete! Post is now live!"
            } else {
                Write-Host "⚠️ Verification failed: $($verifyResp.message)"
            }
        } else {
            Write-Host "⚠️ Could not parse math problem from: $challenge"
        }
    } else {
        Write-Host "✅ No verification needed - post is live!"
    }
} else {
    Write-Host "❌ Failed to create post: $($postResp.message)"
}
