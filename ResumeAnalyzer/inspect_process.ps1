$targetPid = 10036
$p = Get-CimInstance Win32_Process -Filter "ProcessId=$targetPid" -ErrorAction SilentlyContinue
if ($p) { $p | Select-Object ProcessId, CommandLine | Format-List } else { Write-Host "Process $targetPid not found" }