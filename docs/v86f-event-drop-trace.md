# Diagnostic only: interrupt-queue drops

This branch is not a candidate release. It adds an 80-byte trace and a 76-byte
assembly stub to v86f. Only `send_mesg`'s existing full-queue discard branch
enters the stub. It counts the event and stores the last event, queue,
interrupted thread and CP0 Count before returning through the original discard
path. It never retries, clears flags, synthesizes completion or skips gameplay.
The normal enqueue instruction count is unchanged. Layout/timing can still
differ because this is a different ROM, so absence of a reproduced failure is
not proof of a normal-ROM fix. No physical hardware result is asserted here.

The accompanying read-only inspector verifies the trace ABI and resident
enqueue/stub instructions against the exact diagnostic ELF before reading it.
The stock-size scheduler queue is unchanged. Full 8 MiB, 640x480 colour/depth,
the L graph and normal controller input are retained; there is no replay harness.

The investigation follows a normal-v86f Extraction stall at gameframe3 during
a continuous four-controller cold boot. A previous one-controller cold path
passes, so state restoration is not required for the failure.
