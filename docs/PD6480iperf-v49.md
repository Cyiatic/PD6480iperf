# PD6480iperf v49

v49 is the current 640x480i/performance merge candidate. It retains the
performance branch's L-trigger FPS graph and requires an Expansion Pak.

## Artifacts

- ROM: `artifacts/PD6480iperf-v49-vi-slot-2-480i-performance.z64`
- xdelta: `artifacts/PD6480iperf-v49-vi-slot-2-480i-performance.xdelta`
- round-trip reference: `artifacts/PD6480iperf-v49-vi-slot-2-480i-performance-roundtrip.z64`
- Base: `Perfect Dark (U) (V1.1) [!]`
- Base SHA-256: `4E51142ACAC686D96861CECC58CF7CB7C3B06B21733B7F8ED609A709DC039A21`
- ROM SHA-256: `38D1BEABF0672F9E34DBE553D99473769AFD17F2BA17A2B845316A5B57F10B4A`
- xdelta SHA-256: `B76673CF35E9AA90371B26FAE942BC597D52B90B044DA56AF942C9CEC4FE7DFD`
- Size: 32 MiB
- N64 game code/version: `NPDE` / `01`
- Header CRC1/CRC2: `352AF7C5` / `2AF297E1`

## Fix

The 480i merge uses three colour framebuffers, but the scheduler's VI mode
configuration remains a two-entry ring (`OSViMode var8008dcc0[2]`). The prior
candidate advanced `g_ViSlot` modulo 3, so the third mode update wrote past the
two-entry mode table. v49 changes only that ring back to modulo 2; framebuffer
rotation remains triple-buffered.

## Hardware pass — 2026-08-20

Only Kasa `Plug 1` was used for N64 power. The separately named `N64` switch
was not touched.

- `UNFLoader.exe -b -f 3 -r <v49-rom>` uploaded the full 32 MiB image in 36.33
  seconds.
- At approximately 18 seconds and 56 seconds after handoff, Game Capture HD
  reported `640x480p30` and active N64 audio at level 71.
- The desktop preview is black even for the known stock/menu control because
  the available window capture path does not expose the GPU video surface. No
  visual gameplay or L-trigger graph claim is made from this pass.
- No recording was created. `Plug 1` was powered off after the observation
  window.
