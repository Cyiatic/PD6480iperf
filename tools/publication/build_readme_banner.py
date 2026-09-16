#!/usr/bin/env python3
"""Wrap the unchanged logo PNG in a compact, self-contained README viewport.

No raster editing: the embedded PNG bytes are identical to the source file.
Embedding avoids external image references, which SVG-as-image viewers block.
"""

import base64
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[2]
    source = root / "images/pd6480iperf-logo.png"
    target = root / "images/pd6480iperf-banner.svg"
    payload = base64.b64encode(source.read_bytes()).decode("ascii")
    target.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'width="2172" height="254" viewBox="0 229 2172 254" '
        'role="img" aria-labelledby="title">\n'
        '  <title id="title">PD6480iPerf</title>\n'
        '  <!-- Original PNG, unchanged; viewport removes excess vertical padding. -->\n'
        f'  <image x="0" y="0" width="2172" height="724" '
        f'xlink:href="data:image/png;base64,{payload}"/>\n'
        '</svg>\n',
        encoding="utf-8",
    )
    print(f"Built {target.name}: 2172 x 254 viewport; PNG bytes unchanged")


if __name__ == "__main__":
    main()
