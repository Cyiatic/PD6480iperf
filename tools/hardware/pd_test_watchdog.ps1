# Bounded safety companion for ONE active PD hardware test, not a recurring job.
# Never accepts a switch name or a process name from the caller.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][ValidateRange(1,2147483647)][int]$CaptureProcessId,
    [Parameter(Mandatory=$true)][datetime]$CaptureStartedAtUtc,
    [ValidateRange(30,300)][int]$TimeoutSeconds = 300
)
$ErrorActionPreference = 'Stop'
$pdKasaExe = 'C:/Program Files/WindowsApps/23769rewster.uk.TPLinkKasaControl_1.4.81.0_neutral__a2smztagkyka6/Kasa Smart Control/TPLinkCmd.exe'
if (-not (Test-Path -LiteralPath $pdKasaExe -PathType Leaf)) { throw 'Known Kasa executable is missing' }
$pdExpectedStart = $CaptureStartedAtUtc.ToUniversalTime()
$pdDeadline = $pdExpectedStart.AddSeconds($TimeoutSeconds)
Write-Output ('Watchdog armed for Plug 1; capture PID {0}; deadline {1:o}' -f $CaptureProcessId, $pdDeadline)
while ($true) {
    $pdCapture = Get-Process -Id $CaptureProcessId -ErrorAction SilentlyContinue
    if (-not $pdCapture) { Write-Output 'Owned capture already stopped; watchdog exits without affecting another test'; exit 0 }
    if ($pdCapture.ProcessName -ne 'GameCapture' -or
            [math]::Abs(($pdCapture.StartTime.ToUniversalTime() - $pdExpectedStart).TotalSeconds) -gt 1) {
        throw 'PID identity changed; refusing to stop a different process or affect another test'
    }
    if ([datetime]::UtcNow -ge $pdDeadline) { break }
    Start-Sleep -Seconds 2
}
try {
    Stop-Process -Id $CaptureProcessId -ErrorAction Stop
    Write-Output 'Deadline: stopped owned GameCapture process'
} finally {
    # Power cleanup must be attempted even if stopping capture failed/raced.
    & $pdKasaExe -device 'Plug 1' -off
    $pdOffExit = $LASTEXITCODE
    & $pdKasaExe -device 'Plug 1' -status
    Write-Output ('Deadline power-off exit {0}; completed {1:o}' -f $pdOffExit, [datetime]::UtcNow)
    if ($pdOffExit -ne 0) { throw 'Kasa power-off command failed; inspect Plug 1 status' }
}
# Recordings deliberately remain for inspection; no unrelated file deletion.
