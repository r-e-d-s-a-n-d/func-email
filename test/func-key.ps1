function RotateFunctionAppKey()
{
    param([string] $resourceName, [string] $resouceGroup, [string] $keyVaultName, [string] $secretName, [string] $subscription)


    $keyExpirationDate = (Get-Date).AddMonths(6)
    $access = Get-AzAccessToken -ResourceUrl "https://management.core.windows.net/"
    $resourceId = "subscriptions/$subscription/resourceGroups/$resouceGroup/providers/Microsoft.Web/sites/$resourceName"    

    $keys = Get-AzFunctionAppKey -FunctionAppId $resourceId -Token $access.token

    $keys += @{
        name = "_master"
        value = ""
    }

    $keys | ForEach-Object {

        $keyKind = $_.name

        $keyToRotate = New-AzFunctionAppKey -FunctionAppId $resourceId -KeyKind $keyKind -Token $access.token
        $secureKey = ConvertTo-SecureString -String $keyToRotate -AsPlainText -Force
        $keyName = $keyKind.replace("_", "")
        $secret = "$secretName-$keyName"

        Set-AzKeyVaultSecret -Name $secret -VaultName $keyVaultName -SecretValue $secureKey -Expires $keyExpirationDate

        Write-Output "---------------------------------"    
    }
    
    Write-Output "Complete Key Rotation for FunctionApp: $resourceName - $keyKind"
}

function Get-AzFunctionAppKey()
{
    param([string] $functionAppId, [string] $token)
    
    $headers = @{Authorization = "Bearer $token"}
    $url = "https://management.azure.com/$($functionAppId)/host/default/listkeys?api-version=2022-03-01"
    $keys = @()

    $response = Invoke-WebRequest `
        -Method POST `
        -Headers $headers `
        -ContentType "application/json" `
        -Uri $url `
        -UseBasicParsing
    
    $content = $response.content | ConvertFrom-Json
    $content.functionKeys.PSObject.Properties | ForEach-Object {
        $keys += @{
            name = $_.name
            value = $_.value
        }
    }

    return $keys
}

function New-AzFunctionAppKey()
{
    param([string] $functionAppId, [string] $keyKind, [string] $token)

    $key = @{ 
        Name = $keyKind
        Value = '' 
    }

    $headers = @{Authorization = "Bearer $token"}
    $body = @{Properties = $key} | ConvertTo-Json
    $url = "https://management.azure.com/$($functionAppId)/host/default/functionKeys/$($keyKind)?api-version=2022-03-01"

    $response = Invoke-WebRequest `
        -Method PUT `
        -Headers $headers `
        -Body $body `
        -ContentType "application/json" `
        -Uri $url `
        -UseBasicParsing

    $content = $response.content | ConvertFrom-Json
    return $content.properties.value
}


$resourceName = "resourceName01"
$resouceGroup = "resouceGroup01"
$keyVaultName = "keyVaultName01"
$secretName = "functionApp"
$subscription = "0000"

$context = $(Get-AzContext)

if ($context.Subscription.Id -ne $subscription)
{
    $context = $(Connect-AzAccount)
}

RotateFunctionAppKey -ResourceName $resourceName -ResouceGroup $resouceGroup -KeyVaultName $keyVaultName -SecretName $secretName -Subscription $subscription