# Read-only register probe for the exact ParaLLEl core used by these tests.
# Offsets derived from libretro/parallel-n64 revision2f3bf60:
# mupen64plus-core/src/main/savestates.c, savestates_load_m64p v1.6.
param([Parameter(Mandatory=$true)][string[]]$StatePaths)
$ErrorActionPreference='Stop'
$pdResults=@(foreach($pdPath in $StatePaths) {
    $pdResolved=(Resolve-Path -LiteralPath $pdPath).ProviderPath
    $pdBytes=[IO.File]::ReadAllBytes($pdResolved)
    if($pdBytes.Length -ne 16790604 -or
       [Text.Encoding]::ASCII.GetString($pdBytes,0,8) -ne 'M64+SAVE' -or
       [Convert]::ToHexString($pdBytes,8,4) -ne '00010006') {
        throw 'Unexpected state format/length; offsets must be re-derived'
    }
    $pdRamStream=[IO.MemoryStream]::new($pdBytes,448,8388608,$false)
    $pdHasher=[Security.Cryptography.SHA256]::Create()
    try { $pdRamHash=[Convert]::ToHexString($pdHasher.ComputeHash($pdRamStream)).ToLowerInvariant() }
    finally { $pdHasher.Dispose(); $pdRamStream.Dispose() }
    $pdRamPath=Join-Path ([IO.Path]::GetDirectoryName($pdResolved)) 'rdram-last.bin'
    [pscustomobject]@{
        state=$pdResolved
        state_sha256=(Get-FileHash -LiteralPath $pdResolved).Hash.ToLowerInvariant()
        format='M64+SAVE v1.6, 16790604bytes'
        rdram_sha256=$pdRamHash
        agrees_with_last_ram=($pdRamHash -eq (Get-FileHash -LiteralPath $pdRamPath).Hash.ToLowerInvariant())
        sp_mem_addr=('0x{0:x8}' -f [BitConverter]::ToUInt32($pdBytes,172))
        sp_dram_addr=('0x{0:x8}' -f [BitConverter]::ToUInt32($pdBytes,176))
        sp_status=('0x{0:x8}' -f [BitConverter]::ToUInt32($pdBytes,192))
        sp_dma_full=[BitConverter]::ToUInt32($pdBytes,212)
        sp_dma_busy=[BitConverter]::ToUInt32($pdBytes,216)
        sp_pc=('0x{0:x8}' -f [BitConverter]::ToUInt32($pdBytes,224))
        dpc_status=('0x{0:x8}' -f [BitConverter]::ToUInt32($pdBytes,400))
        dp_do_on_unfreeze=[int]$pdBytes[415]
        rsp_task_locked=[BitConverter]::ToUInt32($pdBytes,8397312)
        source='https://raw.githubusercontent.com/libretro/parallel-n64/2f3bf60/mupen64plus-core/src/main/savestates.c'
        hardware_verified=$false
    }
})
$pdResults | ConvertTo-Json -Depth 3
