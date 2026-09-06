# v82h diagnostic: preserve logo buffer submission order

Parent v82g physically caught the title FIFO deadlock: current/next VI both
8076a000, task 1 FB 8076a000, task 2 FB 8036a000, no active RSP/RDP, no
scheduled/queued swap, main on GFX queue and scheduler on IRQ queue.

titleExitCheckControllers calls viConfigureForLogos mid-frame. It previously
reset indices to 0/1 regardless of previous submission parity. This can queue
the displayed image first and leave the free image behind it in a two-buffer
FIFO, which cannot progress. Initialize front/back 0/1 once in .data and
preserve them on logo reconfiguration. Pointer refresh and other logo resets
remain. Watcher/input/save isolation retained; labels updated to V82H.

Compiled actual logo function passes 400 transitions across both initial
parities, including K0/K1 display aliases and initial boot order. The old
index-reset implementation is a negative control and fails the test. This
does not substitute for running the resulting ROM on hardware.

ROM SHA256 50ee8e8961375075c12e34728efa3cbbe693d294b9632e3b9cd2ef1564a71213.
ELF SHA256 214fb5b644b0e373085ecbefd759f19985f05ed2561eb255f57be54cb1154531.
CRC1/2 169f7d2e / c401bb29.

Not a normal candidate: scripted inputs, RAM save and watchdog remain linked.
Normal v82b source/ROM not modified yet; separate hardware/software results
must be recorded before porting this change into that branch.
