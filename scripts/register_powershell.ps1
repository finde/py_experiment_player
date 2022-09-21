function Set-PathVariable (
        [string]$AddPath,
        [string]$RemovePath
    ) {
    $regexPaths = @()
    if ($PSBoundParameters.Keys -contains 'AddPath'){
        $regexPaths += [regex]::Escape($AddPath)
    }

    if ($PSBoundParameters.Keys -contains 'RemovePath'){
        $regexPaths += [regex]::Escape($RemovePath)
    }
    
    $arrPath = $env:Path -split ';'
    foreach ($path in $regexPaths) {
        $arrPath = $arrPath | Where-Object {$_ -notMatch "^$path\\?"}
    }

    $env:Path = ($arrPath + $addPath) -join ';'

    $env:Path = $env:Path.Replace(";;",";")
    [System.Environment]::SetEnvironmentVariable("PATH", $env:Path)
}

# 
Set-PathVariable -AddPath (python -m site --user-site).Replace("site-packages", "Scripts")
Set-PathVariable -AddPath (yarn global bin)

# pipenv shell