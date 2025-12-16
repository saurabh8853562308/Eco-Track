# Build script for ResumeAnalyzer (PowerShell)
# Usage: Open PowerShell in repo root and run: .\build.ps1

$srcDir = "src"
$libSrc = Join-Path $srcDir "lib"
$webDir = "Webcontent"
$outDir = "build"

Write-Host "Cleaning output directory..."
if (Test-Path $outDir) { Remove-Item -Recurse -Force $outDir }
New-Item -ItemType Directory -Path $outDir | Out-Null

# Ensure PDFBox jar exists
$pdfbox = Join-Path $libSrc "pdfbox.jar"
if (-not (Test-Path $pdfbox)) {
    Write-Error "Missing pdfbox.jar in $libSrc. Place pdfbox.jar there and re-run the script."
    exit 1
}

Write-Host "Compiling Java sources..."
$classesDir = Join-Path $outDir "classes"
New-Item -ItemType Directory -Path $classesDir | Out-Null

# Locate servlet API JAR (search src/lib first, then common Tomcat env vars)
Write-Host "Locating servlet API JAR..."
$servletJar = $null
try {
    $servletJar = Get-ChildItem -Path $libSrc -Filter "*servlet*.jar" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1 | ForEach-Object { $_.FullName }
} catch {}

if (-not $servletJar) {
    if ($env:CATALINA_HOME) {
        $candidate = Join-Path $env:CATALINA_HOME "lib\servlet-api.jar"
        if (Test-Path $candidate) { $servletJar = $candidate }
    }
}
if (-not $servletJar -and $env:TOMCAT_HOME) {
    $candidate = Join-Path $env:TOMCAT_HOME "lib\servlet-api.jar"
    if (Test-Path $candidate) { $servletJar = $candidate }
}

if (-not $servletJar) {
    Write-Error "Could not find a servlet API JAR. Please copy Tomcat's servlet-api.jar (or a compatible 'javax.servlet' JAR) into '$libSrc' or set the 'CATALINA_HOME' or 'TOMCAT_HOME' environment variable to your Tomcat installation. Compilation cannot proceed."
    exit 1
}

Write-Host "Using servlet API: $servletJar"

$cp = "$pdfbox;$servletJar;.";
Write-Host "Compiling with --release 17 for wider container compatibility..."
Get-ChildItem -Path $srcDir -Filter "*.java" -Recurse | ForEach-Object {
    & javac --release 17 -cp $cp -d $classesDir $_.FullName
}

Write-Host "Assembling WAR structure..."
$warDir = Join-Path $outDir "war"
New-Item -ItemType Directory -Path $warDir | Out-Null

Copy-Item -Path (Join-Path $webDir "*") -Destination $warDir -Recurse

# Create WEB-INF and place classes + libs
$webInf = Join-Path $warDir "WEB-INF"
if (-not (Test-Path $webInf)) { New-Item -ItemType Directory -Path $webInf | Out-Null }

$libDir = Join-Path $webInf "lib"
New-Item -ItemType Directory -Path $libDir | Out-Null
# Copy all library jars except servlet API jars to avoid classloader conflicts in containers
Get-ChildItem -Path $libSrc -Filter "*.jar" -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch 'servlet' -and $_.Name -notmatch 'javax.servlet' } | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $libDir -Force
}

$classesDest = Join-Path $webInf "classes"
New-Item -ItemType Directory -Path $classesDest | Out-Null
Copy-Item -Path (Join-Path $classesDir "*") -Destination $classesDest -Recurse

Write-Host "Packaging WAR..."
$warName = "ResumeAnalyzer.war"
if (Test-Path $warName) { Remove-Item $warName -Force }
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($warDir, $warName)

Write-Host "Build complete. Created $warName in the repo root. Deploy it to Tomcat's webapps folder."