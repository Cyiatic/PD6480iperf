# Publication payload audit

See [the public-release audit](../../docs/PUBLIC_RELEASE.md) for scope, exclusions,
credential-scan instructions and old-clone migration. The script reads Git
objects and writes only its requested JSON report; it does not rewrite history.

Run with Python 3 and Git. Create the output directory before running.
