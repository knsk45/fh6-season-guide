<#!
Compatibility JSON reader for the FH6 PowerShell scripts.

PowerShell 7.5+ can keep ISO 8601 values as literal strings through
ConvertFrom-Json -DateKind String. Windows PowerShell 5.1 lacks that parameter
and otherwise coerces timestamps before validation can parse them explicitly.
#>

function ConvertFrom-Fh6JsonValue {
    param([object]$Value)

    if ($Value -is [System.Collections.IDictionary]) {
        $properties = [ordered]@{}
        foreach ($key in $Value.Keys) {
            $properties[[string]$key] = ConvertFrom-Fh6JsonValue -Value $Value[$key]
        }
        return [pscustomobject]$properties
    }

    if ($Value -is [System.Collections.IEnumerable] -and -not ($Value -is [string])) {
        return @($Value | ForEach-Object { ConvertFrom-Fh6JsonValue -Value $_ })
    }

    return $Value
}

function ConvertFrom-Fh6Json {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Json)

    $convertFromJson = Get-Command -Name ConvertFrom-Json -ErrorAction Stop
    if ($convertFromJson.Parameters.ContainsKey('DateKind')) {
        return $Json | ConvertFrom-Json -DateKind String
    }

    Add-Type -AssemblyName System.Web.Extensions -ErrorAction Stop
    $serializer = New-Object System.Web.Script.Serialization.JavaScriptSerializer
    $serializer.MaxJsonLength = [int]::MaxValue
    return ConvertFrom-Fh6JsonValue -Value $serializer.DeserializeObject($Json)
}
