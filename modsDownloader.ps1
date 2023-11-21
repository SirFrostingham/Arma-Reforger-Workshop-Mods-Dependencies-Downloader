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

                $subSubDependencies = $subDep.dependencies
                if ($subSubDependencies) {
                    foreach ($subSubDep in $subSubDependencies) {
                        $subSubDepAsset = $subSubDep.asset
                        $subSubDepIdNamePair = @{
                            "modId" = $subSubDepAsset.id
                            "name" = $subSubDepAsset.name
                        }
        
                        if ($version -and $subSubDep.version) {
                            $subSubDepIdNamePair["version"] = $subSubDep.version
                        }
        
                        if (-not (IsDuplicateModId $subSubDepAsset.id)) {
                            $idNamePairs += $subSubDepIdNamePair
                        }
                    }
                }
            }
        }
    }

    # Create an ordered hashtable for the JSON template
    $jsonTemplate = [ordered]@{
        bindAddress = ""
        bindPort = 2001
        publicAddress = ""
        publicPort = 2001
        a2s = [ordered]@{
            address = "0.0.0.0"
            port = 17777
        }
        game = [ordered]@{
            passwordAdmin = "CHANGEME"
            name = "[SERVER] TITLE"
            password = ""
            scenarioId = $jsonData.props.pageProps.assetVersionDetail.scenarios.gameId
            maxPlayers = $jsonData.props.pageProps.assetVersionDetail.scenarios.playerCount
            visible = $true
            crossPlatform = $true
            supportedPlatforms = @("PLATFORM_PC", "PLATFORM_XBL")
            gameProperties = [ordered]@{
                serverMaxViewDistance = 2500
                serverMinGrassDistance = 50
                networkViewDistance = 1000
                disableThirdPerson = $false
                fastValidation = $true
                battlEye = $true
                VONDisableUI = $false
                VONDisableDirectSpeechUI = $false
            }
            mods = @(foreach ($mod in $idNamePairs) {
                $modEntry = [ordered]@{
                    modId = $mod.modId
                    name = $mod.name
                }
            
                if ($version -and $mod.version) {
                    $modEntry["version"] = $mod.version
                }
            
                $modEntry
            })
        }
    }

    # Convert the ordered hashtable to JSON and output
    $jsonTemplate | ConvertTo-Json -Depth 10
} else {
    Write-Host "JSON data not found on the page."
}
