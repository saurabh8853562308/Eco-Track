"Installing Maven wrapper JAR into .mvn\wrapper if missing..."
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$wrapperDir = Join-Path $scriptDir '.mvn\wrapper'
if (-not (Test-Path $wrapperDir)) { New-Item -ItemType Directory -Path $wrapperDir -Force | Out-Null }
$jar = Join-Path $wrapperDir 'maven-wrapper.jar'
$url = 'https://repo1.maven.org/maven2/io/takari/maven-wrapper/0.5.6/maven-wrapper-0.5.6.jar'
if (Test-Path $jar) {
    Write-Host "maven-wrapper.jar already present"
    exit 0
}
Write-Host "Downloading maven-wrapper.jar from $url..."
try {
    $wc = New-Object System.Net.WebClient
    $wc.DownloadFile($url, $jar)
    Write-Host "Downloaded to $jar"
} catch {
    Write-Error "Failed to download wrapper JAR: $_"
    exit 1
}
