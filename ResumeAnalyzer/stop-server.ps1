$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Push-Location $scriptDir

$pidFile = Join-Path $scriptDir 'server.pid'
if (Test-Path $pidFile) {
    try {
        $pid = Get-Content $pidFile -ErrorAction Stop
        if ($pid) {
            Write-Host "Stopping process id $pid..."
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 1
        }
    } catch {
        Write-Warning "Could not read or stop process from PID file: $_"
    }
    Remove-Item $pidFile -ErrorAction SilentlyContinue
    Write-Host "Stopped server and removed PID file."
} else {
    Write-Host "No PID file found. Attempting to stop any java process running jetty-runner..."
    $procs = Get-Process -Name java -ErrorAction SilentlyContinue
    if ($procs) {
        foreach ($p in $procs) {
            try {
                # Best-effort: stop java processes (be careful on developer machines)
                Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
                Write-Host "Stopped java process id $($p.Id)"
            } catch {
            }
        }
    } else {
        Write-Host "No java processes found."
    }
}

Pop-Location
