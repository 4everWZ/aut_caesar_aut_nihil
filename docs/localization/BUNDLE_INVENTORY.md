# Existing bundle source and license inventory

This inventory describes the **existing** incomplete review ZIP built from
`0868b7db971a5dcb222844300cdbbdcfbc61862a`. It does not rebuild, edit or publish that ZIP.

- Archive: `/workspace/acan-zh-cn-INCOMPLETE-module-review.zip`
- Archive bytes: 1,263,610,441
- Archive SHA-256: `29c9a6a0b2b1b66aa1a1f15e05665c397e45f1b0eb7bc9dc8f42b5782b449dca`
- Pinned upstream: `3ed34f35c94c974f9d2a9102750dbb4866e38f6d`
- Complete machine-readable inventory: `/workspace/acan-bundle-source-license-inventory.json`
- Inventory SHA-256: `9efb4c95574c968585907687dbd07bda104309594681a5b0e1d34ef0a313debf`

The JSON is a separate review artifact outside Git. Preserve it alongside the ZIP
when transferring the review; this document alone is not the per-file inventory.

## Exact accounting

All **4,225 ZIP members** have a path, uncompressed size, SHA-256, source mapping
and declared-license evidence category. All **4,224 entries in the packaged
SHA256SUMS** match decompressed member bytes. SHA256SUMS excludes itself; its own
hash is independently recorded in this inventory. Duplicate ZIP member paths and
unmapped members: **zero**.

For **4,222 committed members**, the Git blob identity computed from the member
bytes matches the exact path in the build commit's tree. The same identity was
checked against the pinned upstream tree. This uses Git's blob-header SHA-1 for
source identity and independently computed SHA-256 for every payload. The three
packaging-generated members map to the exact build-commit packager rather than a
fictional upstream file.

| Origin | Members |
| --- | ---: |
| Byte-identical file at pinned upstream path | 4,178 |
| Fork-added/modified localization files, documentation and README | 39 |
| Committed generated font artifacts, including preview/report | 4 |
| Committed font license notice | 1 |
| Packaging-generated START_HERE.txt, Review/build.json, SHA256SUMS | 3 |
| **Total** | **4,225** |

`source_git` identifies the exact fork path, commit and blob for each committed
member, including remapped Documentation/ and Review/ paths. `upstream_git` is
present only when bytes match that upstream path; null explicitly means no such
byte-identical upstream mapping was established. The bundled UPSTREAM_README.md
is the **fork README preserving upstream credits**, not byte-identical upstream
README. It includes a separate upstream derivation reference. Generated metadata
records its generator and commit. No generated document is represented as an
original upstream asset.

## Font substitutions and developer exclusions

Exactly two runtime members replace the existing module fonts during packaging:

| ZIP-relative module path | Actual committed input |
| --- | --- |
| Data/font_data.xml | tools/localization/font_candidate/font_data.xml |
| Textures/font.dds | tools/localization/font_candidate/font.dds |

The JSON records both original upstream paths/blob IDs/SHA-256 hashes and replacement
paths/blob IDs/SHA-256 hashes. These are packaging-only substitutions: the source
module's original files were not replaced. FONT_OFL.txt comes from the committed
font candidate OFL notice. The atlas, descriptor and rendered preview are labeled
**OFL font derivatives**, separate from MIT documentation/code. The font report
retains the Noto Sans CJK SC and Noto Sans input versions, copyright notices and
source-font SHA-256 hashes; those external font inputs are not falsely assigned
an upstream ACAN Git path. Original optional module fonts retain their separate
unresolved provenance category.

Exactly two tracked developer files are excluded: `fxc.exe` and
`compile_fx.bat`. Their upstream path, commit, blob ID, size and SHA-256 are recorded
under `developer_exclusions`. The Microsoft compiler has no bundled redistribution
terms; the batch file is its development launcher. No runtime asset is labeled an
exclusion merely because its original author is not individually mapped.

## License evidence is not an ownership claim

Each member points to precise evidence records: root MIT declaration, upstream
credits, the redistribution audit, applicable shader notices, bundled OFL notice,
or the package generator. The **4,007 ordinary upstream asset records** use
`upstream_asset_repository_mit_declaration`; this means the repository declares
MIT, **not** that Butters personally authored every texture, model or recording.
Every such row retains its third-party provenance uncertainty.

The **118 shader-family records** preserve a distinct third-party category.
TaleWorlds/LA_GRANDMASTER source notices are concrete evidence for that family;
this inventory does not claim every generated OpenGL or compiled shader was
individually matched to its author. Four optional font records likewise retain
uncertain per-file provenance. See [REDISTRIBUTION.md](REDISTRIBUTION.md) for the
specific notices and model-resource conditional-use evidence. Directory membership
is used to classify review evidence, never to manufacture an asset owner.

This accounting does not recover the three missing sounds, prove CJK engine
compatibility, resolve third-party agreements or turn an incomplete review
candidate into a verified playable release. The existing ZIP and gameplay files
remain unchanged.
