@echo off
rem Minimal Windows mvnw-wrapper: downloads the wrapper JAR if missing then runs it
setlocal
set BASEDIR=%~dp0
set WRAPPER_DIR=%BASEDIR%.mvn\wrapper
set WRAPPER_JAR=%WRAPPER_DIR%\maven-wrapper.jar
set WRAPPER_URL=https://repo1.maven.org/maven2/io/takari/maven-wrapper/0.5.6/maven-wrapper-0.5.6.jar

if not exist "%WRAPPER_JAR%" (
  echo Maven wrapper JAR not found — downloading...
  if not exist "%WRAPPER_DIR%" mkdir "%WRAPPER_DIR%"
  powershell -Command "Try { (New-Object System.Net.WebClient).DownloadFile('%WRAPPER_URL%','%WRAPPER_JAR%'); exit 0 } Catch { exit 1 }"
  if errorlevel 1 (
    echo Failed to download maven-wrapper.jar. Install PowerShell or download the file manually.
    exit /b 1
  )
)

java -jar "%WRAPPER_JAR%" %*
