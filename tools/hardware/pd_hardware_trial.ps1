#requires -Version 7.0
# One bounded upload/capture experiment. Start hidden so cleanup survives a chat interruption.
# Never a recurring job; only the fixed Plug 1 child and processes created here.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Rom,
    [Parameter(Mandatory=$true)][string]$RunDirectory,
    [ValidateRange(15,480)][int]$ObservationSeconds=75,
    [ValidateSet('UNFLoader','Usb64')][string]$LoaderBackend='UNFLoader',
    [switch]$CaptureOnly,
    [switch]$ExternalUpload
)
$ErrorActionPreference='Stop'
$pdWorkspace='C:\Users\codex\Documents\N64 2'
$pdKasa='C:\Program Files\WindowsApps\23769rewster.uk.TPLinkKasaControl_1.4.81.0_neutral__a2smztagkyka6\Kasa Smart Control\TPLinkCmd.exe'
# The saved hardware workflow identifies the prerelease as the working uploader.
# Keep the older July-2024 executable intact; do not silently substitute it.
$pdLoader=Join-Path $pdWorkspace '.codex-work\UNFLoader-x86-pre\UNFLoader.exe'
if ($LoaderBackend -eq 'Usb64') {
    $pdLoader=Join-Path $pdWorkspace '.codex-work\usb64-build-reconnect2m\usb64-reconnect2m.exe'
}
$pdCaptureExe='C:\Program Files\Elgato\GameCapture\GameCapture.exe'
$pdRomPath=(Resolve-Path -LiteralPath $Rom).ProviderPath
if ($CaptureOnly -and $ExternalUpload) { throw 'Choose one no-internal-uploader mode' }
$pdRunPath=[IO.Path]::GetFullPath($RunDirectory)
if (-not $pdRomPath.StartsWith($pdWorkspace+'\', [StringComparison]::OrdinalIgnoreCase) -or
    -not $pdRunPath.StartsWith($pdWorkspace+'\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Targets must remain in the PD workspace' }
if ((Get-Item -LiteralPath $pdRomPath).Length -ne 33554432) { throw 'Expected 32 MiB test ROM' }
if (Test-Path -LiteralPath $pdRunPath) { throw 'Evidence directory already exists; refusing overwrite' }
if (Get-Process -Name GameCapture,UNFLoader,usb64-reconnect2m -ErrorAction SilentlyContinue | Where-Object { -not $_.HasExited }) { throw 'Capture/uploader already running; refusing to affect unowned processes' }
New-Item -ItemType Directory -Path $pdRunPath -ErrorAction Stop | Out-Null
$pdDeadline=[datetime]::UtcNow.AddSeconds(660)
$pdCapture=$null
$pdUpload=$null
$pdPowerOffNeeded=$false
$pdKasaSequence=0

function Trace-Pd([string]$Message) { Write-Output ('{0:o} {1}' -f [datetime]::UtcNow,$Message) }
function Quote-Pd([string]$Value) {
    if ($Value.Contains('"')) { throw 'Unexpected quote in argument' }
    return '"'+$Value+'"'
}
function Stop-PdOwned($Process) {
    if (-not $Process) { return }
    $pdCurrent=Get-Process -Id $Process.Id -ErrorAction SilentlyContinue
    if ($pdCurrent -and -not $pdCurrent.HasExited -and $pdCurrent.StartTime -eq $Process.StartTime -and $pdCurrent.ProcessName -eq $Process.ProcessName) {
        Stop-Process -Id $Process.Id -ErrorAction Stop
    }
}
function Wait-PdProcess($Process,[int]$Seconds) {
    $pdUntil=[datetime]::UtcNow.AddSeconds($Seconds)
    while (-not $Process.WaitForExit(1000)) {
        if ([datetime]::UtcNow -ge $pdUntil -or [datetime]::UtcNow -ge $pdDeadline) {
            Stop-PdOwned $Process
            throw ('Process timeout: '+$Process.ProcessName)
        }
    }
    $Process.WaitForExit()
    if ($Process.ExitCode -ne 0) { throw ('Native process exit '+$Process.ExitCode) }
}
function Wait-PdSeconds([int]$Seconds) {
    $pdUntil=[datetime]::UtcNow.AddSeconds($Seconds)
    while ([datetime]::UtcNow -lt $pdUntil) {
        if ([datetime]::UtcNow -ge $pdDeadline) { throw 'Overall test deadline reached' }
        Start-Sleep -Seconds 1
    }
}
function Invoke-PdKasa([ValidateSet('on','off','status')][string]$Action) {
    $script:pdKasaSequence++
    $pdPowerLog=Join-Path $pdRunPath ('power-'+$script:pdKasaSequence+'-'+$Action+'.log')
    $pdPowerErr=Join-Path $pdRunPath ('power-'+$script:pdKasaSequence+'-'+$Action+'.stderr.log')
    $pdPowerProcess=Start-Process -FilePath $pdKasa -ArgumentList @('-device','"Plug 1"',('-'+$Action)) -WindowStyle Hidden -RedirectStandardOutput $pdPowerLog -RedirectStandardError $pdPowerErr -PassThru
    # Cleanup power commands must still get their bounded attempt after overall deadline.
    if (-not $pdPowerProcess.WaitForExit(20000)) { Stop-PdOwned $pdPowerProcess; throw 'Kasa command timeout' }
    $pdPowerProcess.WaitForExit()
    [string]$pdPowerText=Get-Content -LiteralPath $pdPowerLog -Raw
    Trace-Pd ('Plug 1 '+$Action+': '+$pdPowerText.Trim())
    if ($pdPowerProcess.ExitCode -ne 0) { throw ('Kasa exit '+$pdPowerProcess.ExitCode) }
    if ($Action -in @('off','status') -and $pdPowerText -notmatch 'Relay:\s*0') { throw 'Plug 1 OFF not confirmed' }
    if ($Action -eq 'on' -and $pdPowerText -notmatch 'Relay:\s*1') { throw 'Plug 1 ON not confirmed' }
}

try {
    Trace-Pd ('ROM '+$pdRomPath+' SHA256 '+(Get-FileHash -LiteralPath $pdRomPath).Hash)
    $pdPowerOffNeeded=$true
    Invoke-PdKasa 'on'
    Wait-PdSeconds 12
    if ($CaptureOnly -or $ExternalUpload) {
        if ($ExternalUpload) {
            Trace-Pd 'EXTERNAL UPLOADER: power/capture lease only; separate terminal evidence is required for upload success'
        } else {
            Trace-Pd 'CAPTURE-ONLY PREFLIGHT: no ROM upload; inspect the cold console/menu signal'
        }
    } else {
        Trace-Pd ('Uploader '+$pdLoader+' SHA256 '+(Get-FileHash -LiteralPath $pdLoader).Hash)
        $pdUploadSeconds=65
        $pdUploadArgs=@('-b','-f','3','-r',(Quote-Pd $pdRomPath))
        if ($LoaderBackend -eq 'Usb64') {
            $pdUploadSeconds=120
            $pdUploadArgs=@((Quote-Pd ('-rom='+$pdRomPath)),'-start')
        }
        Trace-Pd ('Uploading with GameCapture closed; timeout '+$pdUploadSeconds+' seconds')
        $pdUpload=Start-Process -FilePath $pdLoader -ArgumentList $pdUploadArgs -WindowStyle Hidden -RedirectStandardOutput (Join-Path $pdRunPath 'upload.log') -RedirectStandardError (Join-Path $pdRunPath 'upload.stderr.log') -PassThru
        Trace-Pd ('Owned upload PID '+$pdUpload.Id)
        $pdNativeUploadComplete=$false
        try {
            Wait-PdProcess $pdUpload $pdUploadSeconds
            $pdNativeUploadComplete=$true
        } catch {
            # The legacy serial utility can print Finished then hang closing
            # its port. Wait-PdProcess has stopped only our owned process.
            # Preserve that failure, but inspect video before cutting power.
            [string]$pdCompletedText=Get-Content -LiteralPath (Join-Path $pdRunPath 'upload.log') -Raw
            if ($LoaderBackend -ne 'Usb64' -or $pdCompletedText -match 'ERROR:' -or
                    $pdCompletedText -notmatch 'Finished in:') { throw }
            Trace-Pd ('SERIAL PROCESS FAILURE after completion text: '+$_.Exception.Message)
            Trace-Pd 'Inspecting capture despite failed process exit; no native-success or ROM-pass claim'
        }
        if ($LoaderBackend -eq 'Usb64') {
            # This existing C# utility catches exceptions without a nonzero exit.
            [string]$pdUploadText=Get-Content -LiteralPath (Join-Path $pdRunPath 'upload.log') -Raw
            if ($pdUploadText -match 'ERROR:' -or $pdUploadText -notmatch 'Finished in:') {
                throw 'Usb64 did not report successful completion'
            }
        }
        if ($pdNativeUploadComplete) { Trace-Pd 'Native upload exit 0; this alone is not a ROM pass' }
        $pdUpload=$null
    }
    $pdCapture=Start-Process -FilePath $pdCaptureExe -WindowStyle Hidden -PassThru
    Trace-Pd ('Owned GameCapture PID '+$pdCapture.Id+' start '+$pdCapture.StartTime.ToString('o'))
    Wait-PdSeconds 45
    Trace-Pd ('Capture startup allowance ended; observing '+$ObservationSeconds+' seconds')
    Wait-PdSeconds $ObservationSeconds
    Trace-Pd 'Observation ended; recording still needs inspection'
} finally {
    try { Stop-PdOwned $pdUpload; Stop-PdOwned $pdCapture } finally {
        if ($pdPowerOffNeeded) {
            try { Invoke-PdKasa 'off' } catch {
                Trace-Pd ('First OFF attempt failed: '+$_.Exception.Message)
                Invoke-PdKasa 'off'
            }
            try { Invoke-PdKasa 'status' } catch {
                Trace-Pd ('First OFF status check failed: '+$_.Exception.Message)
                Invoke-PdKasa 'off'
                Invoke-PdKasa 'status'
            }
        }
        Trace-Pd 'Trial cleanup ended; retain bounded recordings until inspected'
    }
}
