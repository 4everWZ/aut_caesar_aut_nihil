# Experimental Chinese bitmap-font candidate

## Generated full-module integration

The texture remains a generated build output, not a large tracked source blob.
`prepare_full_font.sh` downloads pinned OFL font packages, checks package and outline
hashes, and regenerates the complete descriptor/atlas/report outside the checkout.
The full-module packager integrates that verified pair with its full OFL notice.
Both external outlines retain the provenance and copyright notices below.

This is an **optional, untested rendering candidate**, not a verified Warband font fix. It is generated entirely from separately licensed Noto outlines. It does not copy the module's existing glyph imagery, change shaders, or replace the base module's font automatically. Keep the existing-game Chinese fallback procedure in [FONT_OPTIONS.md](FONT_OPTIONS.md) available as an alternative.

## Assets and coverage

The generated pair is `Data/font_data.xml` and `Textures/font.dds`; distribute them together with `OFL.txt` and `font_report.json`. The candidate uses one 4096 × 4096, uncompressed 32-bit RGBA legacy DDS texture: 64 MiB of decoded pixels, plus its header on disk. Compression by ZIP reduces download size, not GPU memory. Older machines may not support this texture size or memory cost well; this requires testing.

The audited build contains **7,560 unique glyphs**, covering all 3,620 distinct printable codepoints in the delivered Chinese CSV values, all 108 printable codepoints in the compiled English text inventory, and all 7,444 printable GB2312 characters. This includes the 3,507 Han characters currently used by the translation. It supports common Chinese player-entered names, but **not arbitrary Unicode or every Han character**. These counts are a snapshot; the build script recalculates coverage and refuses missing glyphs when translations change. Only U+1E25 (`ḥ`) needs the secondary Latin face.

This replaces the Latin appearance as well as supplying Chinese. It does not preserve the original font's 1,750-glyph repertoire wholesale: many unused foreign-script and extended-Latin entries are absent. That tradeoff is explicit because the candidate is scoped to this Chinese localization, its English fallback corpus, and GB2312 input. Other installed languages need separate repertoire review.

## Provenance and license

The assets are derivatives licensed under **SIL OFL 1.1**, separate from the project's MIT code license. Keep `OFL.txt`, the font copyright notices, this provenance and the report with the candidate. The derivative is named **ACAN Chinese Bitmap Candidate**, without implying endorsement by Noto, Adobe or Google. No proprietary Warband fonts are redistributed as part of the candidate.

| Input | Version / face | SHA-256 |
| --- | --- | --- |
| `NotoSansCJK-Regular.ttc` | Noto Sans CJK SC, collection index 2; 2.004 | `b76b0433203017ca80401b2ee0dd69350349871c4b19d504c34dbdd80541690a` |
| `NotoSans-Regular.ttf` | Noto Sans; 2.004 | `89c3c497f618fdaa0b2d1e98fef93582f28c71debd2c4a8cdf41f190ced2909d` |

These inputs were already installed in the cloud environment under `/usr/share/fonts/opentype/noto/` and `/usr/share/fonts/truetype/noto/`. Their embedded copyright notices identify Adobe (2014–2021) and Google LLC (2015), respectively. Embedded name-table licensing and the installed Debian font-package notices identify OFL 1.1. See the [Noto CJK project's license](https://github.com/notofonts/noto-cjk/blob/main/Sans/LICENSE) and [official release sources](https://github.com/notofonts/noto-cjk). The hashes above pin the actual build inputs; a different download with the same family name is not necessarily byte-identical. The source outline files are not included in this candidate.

## Rebuild

Use `tools/localization/build_font_candidate.py` with explicit paths to the licensed inputs, repository checkout, full license notice and output directory. Example for the audited Linux font installation:

```sh
python3 tools/localization/build_font_candidate.py \
  --root "$PWD" \
  --cjk-font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc \
  --latin-font /usr/share/fonts/truetype/noto/NotoSans-Regular.ttf \
  --face-index 2 \
  --license-file tools/localization/font_candidate/OFL.txt \
  --out /tmp/acan-font-build
```

The generator requires Python 3, Pillow and fontTools. Exact Pillow, FreeType and fontTools versions are recorded in `font_report.json`; no SciPy, external rasterizer, remote service or model is used. It rasterizes at 40 pixels, with a common baseline, 3 pixels of padding and a 1-pixel outline. Deterministic shelf packing stays within one page and fails on overflow rather than silently increasing texture size. Source hashes, translation-input hashes and output hashes are recorded. Reproduction requires matching those inputs and tool versions; the report itself contains environment-specific input paths.

The preview script also takes explicit paths:

```sh
python3 tools/localization/preview_font_candidate.py \
  --root "$PWD" \
  --descriptor /tmp/acan-font-build/Data/font_data.xml \
  --texture /tmp/acan-font-build/Textures/font.dds \
  --label-font /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf \
  --out /tmp/acan-font-preview
```

`comparison.png` is a side-by-side offline decoding of the original and candidate XML/DDS, **not an engine screenshot**. Red boxes mark absent original descriptor entries. The preview uses illustrative baseline/advance arithmetic and a shader calculation; it cannot demonstrate actual wrapping or engine font scaling. `channels.png` shows candidate alpha and inverse-red channels. The comparison includes small samples of the already checked-in original solely for review; distribute the independently generated font assets under their own OFL notice.

## Format and channel evidence

[Swyter's original Mount&Blade BMFont converter](https://github.com/Swyter/swyter.bitbucket.org/blob/master/index.html#L81-L101) establishes these correspondences: `u/v` are rectangle origins; **`w/h` are far-edge coordinates, not dimensions**. `preshift` corresponds to horizontal offset, `postshift` to horizontal advance, and `yadjust` to baseline minus vertical offset minus twice the BMFont spacing. This independent rasterizer uses zero extra BMFont spacing and explicitly baseline-anchored glyphs. These formulas are modding-tool evidence, not an official engine specification; runtime calibration remains necessary.

The active original XML declares 4096 × 2048, but its DDS actually decodes to **2048 × 1024**. The same discrepancy occurs in the optional Original Font. This is observed source behavior, not proof of a defect: normalized texture coordinates may explain it. The candidate deliberately uses equal declared and decoded dimensions. No base XML dimensions were corrected or overwritten.

The checked-in `mb_src.fx` has three relevant UI shader functions around lines 986–1009. Uniform font rendering reads alpha. Outline rendering uses `(1 - red) + alpha` for opacity, and alpha for fill brightness. The map-font function around line 1084 also multiplies RGB. Consequently, the candidate stores glyph fill in alpha and **only the outline ring** in inverse RGB, keeping filled glyph RGB white. Transparent background is white RGB / zero alpha. This is consistent with both source formulas; the checked-in compiled `mb.fx` has not been proven to correspond to that source. OpenGL paths remain untested.

The builder validates unique codepoints, required repertoire coverage, one-page selection, rectangle bounds, absence of overlapping rectangles and byte-exact DDS encode/decode round trip. These are static checks only.

## Installation and required game checks

On a **separate test copy** of ACAN, back up the original `Data/font_data.xml` and `Textures/font.dds` outside the module, then copy the candidate pair into those locations. Select Simplified Chinese in the launcher. Keep both backups so the test is reversible. Do not modify global Warband resources, copy a shader from another mod, or assume this works merely because the preview is readable.

Before calling the candidate playable, test at least:

- Windows Warband and the intended WSE2 version; OpenGL platforms separately where supported.
- Launcher-selected Chinese, English fallback and player-entered Chinese names.
- Main menu, long dialogue, quests, party/troop names, inventory, combat messages and map labels.
- Small and large UI sizes, narrow windows, long unspaced Chinese, punctuation and numerals.
- Filled glyphs, dark outlines, transparent background, baseline alignment, line height and truncation.
- Loading times and GPU memory on target hardware; saved-game loading and re-entry into scenes.

If rendering fails, restore the original pair and test the player's installed Chinese resources using the documented fallback procedure. Do not describe this font candidate, or a package with other unresolved asset issues, as a completed tested Chinese release.
