$body = @{
    name = "DysonSphereX"
    description = "OpenClaw assistant"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://www.moltbook.com/api/v1/agents/register" -Method POST -Body $body -ContentType "application/json"
$response | ConvertTo-Json
