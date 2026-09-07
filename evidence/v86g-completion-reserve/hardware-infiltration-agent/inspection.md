# First labelled v86g hardware attempt: upload timeout

ROM `cb3568848785e143d2c9adb1e7e0ce1bbdd72a3d11e08efce0df01f43e2157a3`.
September7UTC: Plug1OFF01:56:27, exact FTDI restart01:56:33,
ON01:56:35. Uploader PID21380 opened USB and began at01:57:11,
but timed out at the bounded65-second deadline without completion text.
Owned uploader stopped; OFF/statusRelay0 confirmed01:58:19/20. Worker exit1.
No GameCapture started and no recording was created. No ROM test/pass claim.

Before the separate retry, its process was confirmed absent, the interface
present/OK and Plug1OFF. The terminal failure is preserved, not silently replaced
by the retry's success. No unrelated switch or unowned process was targeted.
