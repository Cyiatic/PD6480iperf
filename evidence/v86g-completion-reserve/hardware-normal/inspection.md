# Normal v86g real-N64 intro, 2026-09-07 UTC

ROM SHA256 `79a8f9698190aa76c8600b22f2f35de49abe62b8be2b5ce8dcd84bb834815e40`.
This is the normal ROM, without input replay or observer instrumentation.

The existing bounded worker used exact Plug 1, the exact ED64 FTDI restart
while OFF, 35-second cold boot dwell, and terminal-mode UNFLoader upload.
Observed terminal events:

- 01:33:39: Plug 1 OFF, Relay 0.
- 01:33:47: exact ED64 FTDI interface restarted.
- 01:33:49: Plug 1 ON, Relay 1.
- 01:34:25: upload began, owned uploader PID 15348.
- 01:35:01: `ROM successfully uploaded in 35.81 seconds!`; native exit 0.
- 01:35:01: owned GameCapture PID 16912 started.
- 01:35:46: startup allowance ended; 75-second observation began.
- 01:37:02: observation ended and owned capture stopped.
- 01:37:04/05: Plug 1 OFF and independent status Relay 0 confirmed.

Uploader SHA256
`76d28305fe9ddf209e269d7b5f45927d5069deacad5c5166b628e7f7d5a5ea88`.
No full-image cartridge readback is claimed. Power logs and exact device-restart
output are preserved. No command targeted the unrelated switch named N64.

The flushed Timeshift TS was 157,304,300 bytes, SHA256
`a7da58e88be40b33efc60fc9a54556d00788c48e8b4127a7205eed284324d314`,
created 01:35:38, closed 01:37:02 UTC. The preserved segment descriptor reports
84.084 seconds. Files were zero-byte while GameCapture was recording; only the
completed file was used as evidence. FFmpeg emitted a decoder POC warning on
two seeks, returned 0 and produced all requested stills.

All five extracted stills were visually inspected:

- +5 s: black transition.
- +25 s: ship flying through the rendered city.
- +45 s: another moving city/ship view.
- +65 s: ship above the rooftop/platform scene.
- +80 s: Nintendo logo.

This proves normal-ROM real-N64 rendered 3D intro past boot, not interactive
gameplay, Extraction on hardware, a full mission, or the cause of the subsequent
logo return. No exception screen appeared in these samples. No Analogue pass
is inferred. The source fix's Extraction check is separately software evidence.

After inspection, the exact TS, 45,056-byte metadata sidecar and 460-byte
descriptor were permanently deleted (157,349,816 bytes total). Stills, copied
descriptor and logs remain. Timeshift now contains only its 176-byte timeline;
no owned GameCapture or UNFLoader process remains. Plug 1 remains OFF.
