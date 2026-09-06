# Normal v86f real-N64 intro observation, 2026-09-06 UTC

ROM SHA256 `bf219fa49620be957f366cb2b84ba255d67712bb36faf3e494ddfabfae7fa41e`.
Runtime `87952368964433608af2171e742c4e664e205a67`, no input replay/ROM instrumentation.

The tool-provided terminal ran the bounded worker with `-ResetEd64Usb
-UploadInTerminal -ObservationSeconds 75`. Only exact Plug 1 was targeted.
The transcript reported OFF at23:22:22, exact FTDI reset at23:22:33,
ON at23:22:34, uploader started23:23:10, and
`ROM successfully uploaded in 37.28 seconds!` followed by native exit0.
UNFLoader SHA256 `76d28305fe9ddf209e269d7b5f45927d5069deacad5c5166b628e7f7d5a5ea88`.
No full-image readback is claimed. The prior redirected v86f attempt timed out
at65 seconds, with no capture; it is retained separately, not discarded as a pass.

Owned capture PID4376 started23:23:48. The live window screenshot was black;
activation returned `GetCursorPos failed: Access is denied. (0x80070005)`.
Files appeared zero-byte while the app was running, but flushed on shutdown.
This is not evidence that the ROM was black. The completed recording is the
evidence used below. No further UI input was attempted after the failed activation.

82.839333-second MPEG-TS,154321868 bytes,
SHA256 `1036443a37317000e75affcb2c409fa26db25ea4d052654f3e35a35a20d584fb`.
Encoded capture is640x480/29.97 progressive (Elgato output, not a measurement
of the N64 VI field timing). The segment descriptor is preserved.

Five extracted stills were visually inspected:

- +5s: black transition.
- +25s: moving ship/city intro scene.
- +45s: another city flyover view.
- +65s: Joanna and the ship on the rooftop.
- +80s: Nintendo logo.

This proves the normal ROM reached real-N64 rendered3D past boot, not interactive
gameplay, a complete mission, or the cause of the subsequent logo return.
No exception screen was seen in these samples. No user/Analogue pass is claimed.

Worker finished23:25:49 and confirmed Plug1 OFF23:25:51/statusRelay0 23:25:52.
The inspected TS,40960-byte sidecar and460-byte segment descriptor were
permanently deleted after copying the descriptor. Stills/logs remain.
