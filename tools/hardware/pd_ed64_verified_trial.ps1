#requires -Version 7.0
# Single test with independent cleanup; only Plug 1 and owned processes.
param([Parameter(Mandatory)][string]$Rom,[Parameter(Mandatory)][string]$RunDirectory,
 [ValidateSet('probe','upload-start')][string]$Mode='probe',
 [ValidateRange(12,45)][int]$BootDelaySeconds=12)
$ErrorActionPreference='Stop'
$pdRoot='C:\Users\codex\Documents\N64 2'
$pdKasa='C:\Program Files\WindowsApps\23769rewster.uk.TPLinkKasaControl_1.4.81.0_neutral__a2smztagkyka6\Kasa Smart Control\TPLinkCmd.exe'
$pdTool=Join-Path $pdRoot '.codex-work\ed64-verified-v3.exe'
$pdRom=(Resolve-Path -LiteralPath $Rom).ProviderPath
$pdOut=[IO.Path]::GetFullPath($RunDirectory)
if (-not $pdRom.StartsWith($pdRoot+'\') -or -not $pdOut.StartsWith($pdRoot+'\')) { throw 'Outside workspace' }
if ((Get-Item -LiteralPath $pdRom).Length -ne 33554432) { throw 'Wrong ROM size' }
if (Get-Process -Name UNFLoader,GameCapture,usb64-reconnect2m,ed64-verified-v1,ed64-verified-v2,ed64-verified-v3 -ErrorAction SilentlyContinue | Where-Object { -not $_.HasExited }) { throw 'Other live hardware process' }
if (Test-Path -LiteralPath $pdOut) { throw 'Existing evidence output' }
New-Item -ItemType Directory -Path $pdOut | Out-Null
$pdUploader=$null; $pdCapture=$null; $pdSequence=0; $pdPowerNeeded=$false
function Trace([string]$Text) { Write-Output ('{0:o} {1}' -f [datetime]::UtcNow,$Text) }
function StopOwned($Process) {
 if (-not $Process) { return }
 $pdLive=Get-Process -Id $Process.Id -ErrorAction SilentlyContinue
 if ($pdLive -and -not $pdLive.HasExited -and $pdLive.StartTime -eq $Process.StartTime) { Stop-Process -Id $Process.Id -ErrorAction Stop }
}
function Power([ValidateSet('on','off','status')][string]$Action) {
 $script:pdSequence++
 $pdLog=Join-Path $pdOut ('power-'+$script:pdSequence+'-'+$Action+'.log')
 $pdProcess=Start-Process -FilePath $pdKasa -ArgumentList @('-device','"Plug 1"',('-'+$Action)) -WindowStyle Hidden -RedirectStandardOutput $pdLog -RedirectStandardError ($pdLog+'.stderr') -PassThru
 if (-not $pdProcess.WaitForExit(20000)) { StopOwned $pdProcess; throw 'Kasa timeout' }
 $pdProcess.WaitForExit()
 $pdText=Get-Content -LiteralPath $pdLog -Raw
 Trace ('Plug 1 '+$Action+': '+$pdText.Trim())
 if ($pdProcess.ExitCode -ne 0 -or $pdText -notmatch ('Relay:\s*'+$(if ($Action -eq 'on') {'1'} else {'0'}))) { throw 'Power state not confirmed' }
}
try {
 Trace ('ROM '+$pdRom+' SHA256 '+(Get-FileHash -LiteralPath $pdRom).Hash)
 Trace ('Transport SHA256 '+(Get-FileHash -LiteralPath $pdTool).Hash+' mode '+$Mode)
 $pdPowerNeeded=$true
 Power on
 Start-Sleep -Seconds $BootDelaySeconds
 $pdUploader=Start-Process -FilePath $pdTool -ArgumentList @($Mode,'COM3',('"'+$pdRom+'"'),(Get-FileHash -LiteralPath $pdRom).Hash) -WindowStyle Hidden -RedirectStandardOutput (Join-Path $pdOut 'transport.log') -RedirectStandardError (Join-Path $pdOut 'transport.stderr.log') -PassThru
 Trace ('Owned transport PID '+$pdUploader.Id+' start '+$pdUploader.StartTime.ToString('o'))
 $pdLimit=[datetime]::UtcNow.AddSeconds($(if ($Mode -eq 'probe') {40} else {310}))
 while (-not $pdUploader.WaitForExit(1000)) { if ([datetime]::UtcNow -ge $pdLimit) { StopOwned $pdUploader; throw 'External transport timeout' } }
 $pdUploader.WaitForExit()
 if ($pdUploader.ExitCode -ne 0) { throw ('Transport exit '+$pdUploader.ExitCode) }
 $pdText=Get-Content -LiteralPath (Join-Path $pdOut 'transport.log') -Raw
 if ($Mode -eq 'probe') {
  if ($pdText -notmatch 'PROBE_ALL_MATCHED' -or $pdText -notmatch 'CLOSE returned') { throw 'Incomplete probe' }
  Trace 'Probe returned normally with readback; this is not a game test'
 } else {
  if ($pdText -notmatch 'ALL_33554432_BYTES_READBACK_MATCHED' -or $pdText -notmatch 'START_COMMAND_SENT' -or $pdText -notmatch 'CLOSE returned') { throw 'Incomplete upload/start/close' }
  Trace 'Readback and start complete; capture still required'
  $pdCapture=Start-Process -FilePath 'C:\Program Files\Elgato\GameCapture\GameCapture.exe' -WindowStyle Hidden -PassThru
  Trace ('Owned capture PID '+$pdCapture.Id)
  for ($pdSecond=0;$pdSecond -lt 150;$pdSecond++) { Start-Sleep -Seconds 1 }
  Trace 'Capture window ended; inspect recording before any ROM-pass claim'
 }
} finally {
 try { StopOwned $pdUploader } finally {
  try { StopOwned $pdCapture } finally {
   if ($pdPowerNeeded) {
    try { Power off } catch { Trace $_.Exception.Message; Power off }
    try { Power status } catch { Trace $_.Exception.Message; Power off; Power status }
   }
   Trace 'Cleanup complete'
  }
 }
}
