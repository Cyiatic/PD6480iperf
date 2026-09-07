# Diagnostic passes; cause still not isolated

Separate private source branch `diagnostics/v86f-event-drop-trace`, commit
`6460ad0b3`. This is NOT a user candidate, normal-ROM pass or hardware test.
It adds a counter only to the existing kernel full-queue discard path: no
retries, synthesized completion, flag clearing or gameplay bypass. The queue
capacity and successful-enqueue instruction count are unchanged. The added
80-byte BSS trace/76-byte stub nevertheless change layout and startup timing.

Source-header ROM SHA256
`649afe98d8747c8e73904ae07b51ccf3ae7667dab14ef05fcb6a4f8c36b139ef`;
ELF `b410daf78dbb61ccb4925939a71119830958e31672912fb3b5f7de8d7df1cfdf`.
The existing immutable host/core/V6 layout and ordinary continuous9150-tick
cold input are unchanged from the adjacent controls, with Dark EEPROM and
four controllers throughout. No state restore or RAM pokes. Native exit0.

Final Extraction/Solo frame1434, controller mask15, one player, alive health1,
unpaused/cutscene0, 640x480, graph enabled. OOM/cache/allocator/CPU faults0,
valid room partition; idle-rule evictions0. All16 event-drop counters are0.
The inspector authenticates the resident enqueue/stub instructions and the
80-byte trace ABI against this exact ELF. Actual MIPS disassembly is included;
the46 Python tests, including malformed/foreign trace rejection, pass.
Final state `1fd577dfd803b6fecc369b082744e7be374215397b10901d3390a3b59f1a9688`;
RAM `437a84372315cb2d5d8e54037099aa667b9a6f798a46fd8a16e3c23028c0f377`.
The final still was inspected: dark scope/HUD, like the passing controls.

This diagnostic did **not reproduce** the normal cold-four stall. Thus zero
queue drops here do not rule out drops in that failed normal-ROM run. The
instrumented pass cannot replace the normal failure. Further isolation needs
a less perturbing observation or an independently validated timing/RSP control,
not a speculative normal-ROM scheduler change. The candidate remains held.

Build notes: the first MSYS build completed but was slow; a native invocation
with a space-containing shell path failed its file-discovery subprocesses and
misleadingly returned0/"nothing to do". That was not used as build proof. The
corrected invocation compiled/linked the final named stub, but packaging
returned0xc0000135 because its runtime DLL directory was absent from PATH.
Re-running the exact existing mkrom command with that directory present
completed native0; its log and the failed final build log are retained.

Afterward normal source was restored and rebuilt, yielding the exact original
ELF. Rebuilt source-header ROM hash
`1d3fe2fad1cca7ae729f0fa6be3e87fa82001acdbe75c68de004aab663e120b3`;
only header bytes0x3c/0x3f differ from the normal retail candidate. The entire
body after byte63 was hash-compared equal before restoring the known retail
header image in the generated build slot. Its final ROM/ELF hashes are the
normal `bf219fa4...` / `82d6a0e7...`; normal runtime source is unchanged.

No console ON/capture/upload was needed for these computer-side controls.
Final Plug1 OFF and independent status both confirm Relay0. An initial direct
PowerShell invocation incorrectly passed literal quotes in the device name;
its error logs remain and were not treated as confirmation despite native0.
The established hidden-process invocation then confirmed the exact Plug1.
No new recordings were made. The unrelated Kasa N64 device was not queried.
