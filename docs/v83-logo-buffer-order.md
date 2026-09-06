# Normal v83: preserve the two-buffer order through logo setup

Based on normal v82b 24995c1c66eaa0e4ac5568f5711f7af7678b5561. The only
runtime source change is vi.c: initialize front/back indices 0/1 once in
.data; do not reset them in viConfigureForLogos. Pointer refresh and other
logo configuration remain. No RAM save, synthetic input or watchdog code is
linked; no pdHw, g_PdHw or g_PdAlloc symbols in this ELF.

Why: original N64 diagnostic v82g showed a stable title framebuffer FIFO
deadlock (displayed/next 8076a000, first queued task 8076a000, second 8036a000,
RSP/RDP idle, no pending swap). titleExitCheckControllers calls logo setup
mid-frame; resetting the indices can duplicate the previous submission and
block the free image behind the displayed one. Separate v82h applies this fix
under the synthetic test: original N64 reached CI, closed menu, L graph on,
changed views through movement, then Video Options. Extended toggle run and
normal-binary tests are separate; do not infer their results here.

Compiled actual logo routine passes 400 transitions for both starting parities
and physical alias guards; the old reset is a failing negative control. v82h
software replay reaches phase 8/three Hi-Res checks, but is not this binary.

Retains newer upstream bf324507 performance core, full 640x480i fixed render,
two full buffers, room/weapon preloading, per-player shared menu scratch and
stock UI/save semantics from v82b. Hi-Res preference remains save-compatible;
rendering stays full resolution regardless of that checkbox.

ROM SHA256 fdb31ec4f4616fedf63b07d3812d5d51bb85e3843b282f8eefe1631acd4357b5.
ELF SHA256 d6bcb69889226a13c67660296e8a9aa6d0946ca1d084d1a126b95ab3fa4a5d18.
CRC1/2 bb7f2f35 / 5c015373.

Normal cold Dark-save emulator test and physical/Analogue testing remain
pending when this source note is created. Physical input automation on a
separate diagnostic is not an unchanged-ROM interactive console pass. No
claim of overall completion or performance benchmark follows from this fix.
