# v87 original-N64 retry after ED64 reconnect

**September 14, 2026 UTC — normal-ROM transfer and animated intro pass.**

Exact unchanged v87 ROM SHA-256:

```text
04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b
```

The bounded worker used Kasa **Plug 1**, restarted only the saved ED64 interface while power was off, powered on, waited 35 seconds and uploaded the normal candidate. The unrelated **N64** switch was not used.

The prerelease uploader explicitly reported a successful upload in **36.48 seconds** and closed the connection. Elgato then captured a progressing 3D intro:

| Capture time | Observed view |
| --- | --- |
| 1 second | [Black transition](capture-1s.png) |
| 15 seconds | [City](capture-15s.png) |
| 30 seconds | [Different city angle](capture-30s.png) |
| 45 seconds | [Aircraft and city](capture-45s.png) |

This is evidence of animated in-engine intro progress, not merely an exit-code or upload-message pass. Product/Rare-logo timing was not captured. No interactive CamSpy gameplay, full mission, or physical EEPROM import was tested.

## Shutdown and retained provenance

Plug 1 OFF was confirmed at **06:09:12 UTC**; the final status reported Relay 0 at **06:09:13 UTC**. See [OFF log](power-3-off.log) and [status log](power-4-status.log). These are historical trial results, not a claim about current live power state.

The original recording was 51.349333 seconds, 95,579,012 bytes, SHA-256 `bd3390063085553c158ee9f60db4b8d5f9dcfd166a14e2b43a57f5d9bb735ad0`. Its 640×480 / 30000÷1001 capture metadata does not independently establish internal framebuffer resolution.

Only the small stills and shutdown logs are included here. The original trial record is local at `.codex-work/v87-ed64-reconnect-20260913-trial/`. Despite that directory's start-date label, this retry occurred on September 14 UTC.

Recording cleanup was rejected by execution policy before process creation. About 91.2 MiB remained in the isolated local capture directory; no alternate deletion route was attempted. The recording is not included in Git. The capture output setting was restored and owned processes were closed.

[Back to v87 evidence](../README.md)
