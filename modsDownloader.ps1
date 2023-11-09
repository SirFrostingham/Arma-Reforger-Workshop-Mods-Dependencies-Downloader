param (
    [string]$url
)

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
    $idNamePairs += $idNamePair
    
    # Search for the "dependencies" information
    $dependencies = $jsonData.props.pageProps.assetVersionDetail.dependencies

    # Dependencies: Build a collection of "id" and "name" pairs
    foreach ($dep in $dependencies) {
        $asset = $dep.asset
        $idNamePair = @{
            "modId" = $asset.id
            "name" = $asset.name
        }
        $idNamePairs += $idNamePair
    }

    # Output the collection of "id" and "name" pairs
    $idNamePairs | ConvertTo-Json
} else {
    Write-Host "JSON data not found on the page."
}
