Param(
    [switch]$Build
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Push-Location $scriptDir

if ($Build) {
    Write-Host "Building project before start..."
    $mvnwCmd = Join-Path $scriptDir 'mvnw.cmd'
    $mvnwPosix = Join-Path $scriptDir 'mvnw'
    if (Test-Path $mvnwCmd) {
        Write-Host "Found Maven Wrapper (Windows) - running mvnw.cmd"
        & $mvnwCmd -U clean package
        if ($LASTEXITCODE -ne 0) { Write-Error "Maven build failed (mvnw.cmd)"; Pop-Location; exit 1 }
    } elseif (Test-Path $mvnwPosix) {
        Write-Host "Found Maven Wrapper (POSIX) - running ./mvnw"
        & $mvnwPosix -U clean package
        if ($LASTEXITCODE -ne 0) { Write-Error "Maven build failed (./mvnw)"; Pop-Location; exit 1 }
    } else {
        Write-Host "Maven wrapper not found; falling back to legacy build.ps1"
        $legacyBuild = Join-Path $scriptDir 'build.ps1'
        if (Test-Path $legacyBuild) {
            & powershell -NoProfile -ExecutionPolicy Bypass -File $legacyBuild
        } else {
            Write-Error "No build mechanism found (mvnw or build.ps1). Aborting."; Pop-Location; exit 1
        }
    }
}

$pidFile = Join-Path $scriptDir 'server.pid'
if (Test-Path $pidFile) {
    try {
        $old = Get-Content $pidFile -ErrorAction Stop
        if ($old) {
            Write-Host "Found existing PID $old - attempting to stop it first..."
            Stop-Process -Id $old -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 1
        }
    } catch {
        Remove-Item $pidFile -ErrorAction SilentlyContinue
    }
}

$jar = Join-Path $scriptDir 'jetty-runner.jar'
$slf4j = Join-Path $scriptDir 'slf4j-simple-1.7.36.jar'
# prefer a Maven-built WAR in target/ if present
$targetWar = Get-ChildItem -Path (Join-Path $scriptDir 'target') -Filter "*.war" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($targetWar) {
    $war = $targetWar.FullName
} else {
    $war = Join-Path $scriptDir 'ResumeAnalyzer.war'
}

if (-not (Test-Path $jar)) { Write-Error "jetty-runner.jar not found in $scriptDir"; Pop-Location; exit 1 }
if (-not (Test-Path $war)) { Write-Error "WAR not found (searched target/ and repo root)"; Pop-Location; exit 1 }

$log = Join-Path $scriptDir 'jetty.log'

$cp = if (Test-Path $slf4j) { "$jar;$slf4j" } else { "$jar" }

Write-Host "Starting Jetty runner... logs -> $log"
# Build a one-line cmd command so we can redirect both stdout and stderr to the same file
$cmd = 'java -cp "' + $cp + '" org.eclipse.jetty.runner.Runner --port 8080 "' + $war + '" > "' + $log + '" 2>&1'
$proc = Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', $cmd -WindowStyle Hidden -PassThru

if ($proc) {
    $proc.Id | Out-File -FilePath $pidFile -Encoding ascii
    Write-Host "Started Jetty (pid $($proc.Id)). PID saved to $pidFile"
} else {
    Write-Error "Failed to start Jetty runner"
}

Pop-Location
