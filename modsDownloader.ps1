param (
    [string]$url,
    [switch]$version
)

function IsDuplicateModId($id) {
    foreach ($entry in $idNamePairs) {
        if ($entry["modId"] -eq $id) {
            return $true
        }
    }
    return $false
}

if ([string]::IsNullOrEmpty($url)) {
    Write-Host "Please provide a URL as a parameter."
    exit
}

# Send an HTTP GET request and store the response in a variable
$response = Invoke-WebRequest -Uri $url

# Extract the JSON data from the response content
$regexPattern = '<script id="__NEXT_DATA__" type="application/json">([^<]*)<\/script>'
$match = [regex]::Match($response.Content, $regexPattern)

if ($match.Success) {
    $jsonString = $match.Groups[1].Value
    $jsonData = ConvertFrom-Json $jsonString

    # Search for the "asset" information and store "id" and "name"
    $asset = $jsonData.props.pageProps.asset
    
    # Build a collection of "id" and "name" pairs
    $idNamePairs = @()

    # Add parent mod to the collection
    $idNamePair = @{
        "modId" = $asset.id
        "name" = $asset.name
    }

    if ($version -and $asset.currentVersionNumber) {
        $idNamePair["version"] = $asset.currentVersionNumber
    }
    
    $idNamePairs += $idNamePair
    
    # Search for the "dependencies" information
    $dependencies = $jsonData.props.pageProps.assetVersionDetail.dependencies

    # Dependencies: Build a collection of "id" and "name" pairs
    foreach ($dep in $dependencies) {
        $depAsset = $dep.asset
        $depIdNamePair = @{
            "modId" = $depAsset.id
            "name" = $depAsset.name
        }

        if ($version -and $dep.version) {
            $depIdNamePair["version"] = $dep.version
        }

        if (-not (IsDuplicateModId $depAsset.id)) {
            $idNamePairs += $depIdNamePair
        }

        $subDependencies = $dep.dependencies
        if ($subDependencies) {
            foreach ($subDep in $subDependencies) {
                $subDepAsset = $subDep.asset
                $subDepIdNamePair = @{
                    "modId" = $subDepAsset.id
                    "name" = $subDepAsset.name
                }

                if ($version -and $subDep.version) {
                    $subDepIdNamePair["version"] = $subDep.version
                }

                if (-not (IsDuplicateModId $subDepAsset.id)) {
                    $idNamePairs += $subDepIdNamePair
                }
            }
        }
    }

    # Output the collection of "id" and "name" pairs
    Write-Host "Mods list:"
    $idNamePairs | ConvertTo-Json

    # Output scenario details
    $scenarioId = $jsonData.props.pageProps.assetVersionDetail.scenarios.gameId
    Write-Host "Scenario ID: $scenarioId"
    $gameMode = $jsonData.props.pageProps.assetVersionDetail.scenarios.gameMode
    Write-Host "Game mode: $gameMode"
    $playerCount = $jsonData.props.pageProps.assetVersionDetail.scenarios.playerCount
    Write-Host "Player count: $playerCount"

    # Output version if provided
    if ($version -and $jsonData.props.pageProps.assetVersionDetail.version) {
        $version = $jsonData.props.pageProps.assetVersionDetail.version
        Write-Host "Version: $version"
    }
} else {
    Write-Host "JSON data not found on the page."
}
