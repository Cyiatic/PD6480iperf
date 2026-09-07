# v86f — held, not a new test release

The locally prepared xdelta reconstructs normal ROM SHA256
`bf219fa49620be957f366cb2b84ba255d67712bb36faf3e494ddfabfae7fa41e` exactly
from the verified USA1.1 base. Patch SHA256
`ac016dbba00ae8faf36d66f01b3b318834fc276cbc33de6d79984f5ca701d795`,1447105bytes.

Do not promote this patch: Extraction stalls at gameframe3 in the current
software test from a saved menu state, even without a later mid-intro restore.
A continuous cold boot does reach Extraction alive/unpaused; preserving four
controllers on the failing restored path does not cure it. The state-dependent
cause remains unexplained. No new ZIP or user-ready ROM is issued by this record.

Positive bounded results: AI-co-op room failures43→12→0 across v86d/e/f;
four-controller CI/four-player Skedar; full640x480 colour/depth and L;
real-N64 normal intro, plus a separate labelled diagnostic's alive Infiltration
pause/menu/L and short resume. The diagnostic later dies normally in combat.
These do not override the failed Extraction test or prove Analogue support.

The generated stock100%Dark EEPROM remains available separately, unchanged.
Only Plug1 was used for hardware; OFF verified and inspected recordings deleted.
