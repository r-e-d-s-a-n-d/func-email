$uri = "http://localhost:7071/api/sendmail"

$body = @{
    name = "User Name Here"
}

Invoke-RestMethod -Method 'Post' -Uri $uri  -ContentType 'application/json' -Body ($body | ConvertTo-Json)