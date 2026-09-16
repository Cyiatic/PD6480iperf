# PD6480iPerf README logo

README banner: [pd6480iperf-banner.svg](pd6480iperf-banner.svg).
Original artwork: [pd6480iperf-logo.png](pd6480iperf-logo.png).

Generated with the **built-in image generation tool** from a user-supplied
Perfect Dark logo reference. This is custom project lettering, not an official
game logo or a font-file distribution. The requested lettering is
`PD6480iPerf`; the reference supplied the angular lettering and metallic-blue
finish. No font file was used.

The original PNG is 2,172 × 724 pixels with an alpha channel. A self-contained
SVG embeds those exact PNG bytes and displays a 2,172 × 254 viewport, removing
the excess vertical padding without changing the artwork. The README retains
the 483-pixel display width used in
[TND6480i](https://github.com/Cyiatic/TND6480i), with a banner height of about
56 pixels instead of 161. The SVG contains no scripts or external resources.

Rebuild the viewport with `python tools/publication/build_readme_banner.py`.
The viewBox starts at y=229, leaving roughly 12 pixels above and below the
visible lettering. The generated SVG is committed so no build is needed to
view the README.

A built-in image-generation edit was also tried for the tighter framing, but
it retained the oversized canvas and was not selected. The shipped banner
uses the original artwork, not that regenerated variant. Its edit prompt was:

```text
Use case: background-extraction.
Asset type: existing transparent PNG wordmark for a GitHub README.
Input image 1: EDIT TARGET, the existing finished PD6480iPerf logo. Do not redesign.
Primary request: trim away the large empty transparent margins ABOVE and BELOW the existing lettering. Change ONLY the canvas framing to a tight shallow horizontal strip, approximately 2172 by 260 pixels, with just 8-12 pixels clear padding around the outermost lettering/shadow.
Text, verbatim, unchanged: "PD6480iPerf".
Constraints: preserve the exact existing letter shapes, proportions, spacing, navy metallic texture, crisp white outline and purple shadow. Keep the original single-line arrangement. Do not stretch the lettering vertically or horizontally. Do not add letters, decorations, borders or backgrounds. Preserve genuine transparent alpha around the wordmark and in counters. Return the tightly cropped image, NOT another wide banner with blank top/bottom padding. The wordmark must fill almost the entire image height.
```

## Generation prompt

```text
Use case: logo-brand.
Asset type: finished GitHub README header wordmark for an unofficial N64 graphics/performance patch.
Input image 1 is the typography and finish reference: the supplied classic Perfect Dark logo. Create the new project lettering in that same distinctive angular, forward-slanted, cutout science-fiction logo-lettering style. This is a custom project wordmark, not the official game title.
Text, verbatim, exactly once: "PD6480iPerf". Spell the characters P D 6 4 8 0 i P e r f. Retain that spelling and capitalization; distinguish the zero from the lowercase i. No spaces, no extra words, no original "Perfect Dark" text.
Composition: one continuous horizontal wordmark, centered in a wide landscape banner approximately 3:1; tight useful framing with enough clean padding that every stroke fits. All lettering is readable at a GitHub README display width of 483 pixels.
Style: faithfully match the reference's sharp geometric slanted strokes and distinctive broken/angular counters; dark midnight-navy and steel-blue brushed-metal interiors, crisp white outer edging and a very restrained deep-purple offset shadow. Similar disciplined flat/front-facing treatment, not exaggerated 3D.
Background: genuinely transparent alpha outside and through the letter counters, not a black rectangle and not a baked checkerboard.
Constraints: logo only; no characters, symbols, badge, subtitle, registered mark, trademark symbol, watermark, scenery or extra decoration. Preserve precise legibility of "PD6480iPerf".
```

The source reference is not included here. The generated asset is stored in the
repository, not linked to a workstation-only image-generation directory.
