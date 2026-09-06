# v86b external-terminal upload attempt — failed transfer

Normal ROM SHA256 c33ec1459b3092d89f5a3b00f82f6b4dd8e59c294b479aa7d039dc7471455df7.
Prerelease UNFLoader SHA256 76d28305fe9ddf209e269d7b5f45927d5069deacad5c5166b628e7f7d5a5ea88.
`UNFLoader -b -f 3 -r <normal ROM>` in terminal session 50896 printed
EverDrive forced, USB connection opened, Uploading ROM, but never completion.
`cancel` did not terminate it. Ctrl-C terminated it with exit 1. No ROM handoff
or game boot was established. The independent capture worker is only a power
lease and must not be counted as uploader success.

Capture stills at segment +10, +65 and +140 seconds were visually inspected:
all show the same live EverDrive menu, not Perfect Dark. Power/capture worked.
Worker logs confirm Plug 1 OFF at 19:03:07 UTC and status Relay: 0 at 19:03:08.
An independent status check also returned Relay: 0. No N64-named outlet used.
GameCapture and UNFLoader are both stopped.

The inspected recording files are deleted after retaining these three stills,
`.desc` and `.info`. Exact source identities (total 273467475 bytes):

| Original name | Bytes | SHA256 |
| --- | ---: | --- |
| Recording_####YYYY-MM-DD_hh-mm-ss####_0001.ts | 273388660 | e15500fa0c75557f6d445e2d347ca2d66b5a2c1725be134239bbfa111831e423 |
| Recording_####YYYY-MM-DD_hh-mm-ss####_0001.meta | 77824 | ad43577a8958e2eb1449b52a5ce570f61402ab5d18c5f4ec8df2c87e8194c66a |
| Recording_####YYYY-MM-DD_hh-mm-ss####.desc | 461 | ad84e25f110c74f46b0a161c7b59b937dcda4fad9722f9095fd8af41496ef92f |
| Recording_####YYYY-MM-DD_hh-mm-ss####.info | 530 | 43c069ef0ec288e383f07dc20486262a65a75d105cddab6e1246424e65530406 |

OverlayTimeline.json is retained. This is not hardware validation of v86b.
