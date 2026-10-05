# Simplified Chinese font options

**The original translation overlay ships no font. A new OFL Chinese font candidate is included only in the separate full-tree review package; it is not declared working in Warband.** See [FONT_CANDIDATE.md](FONT_CANDIDATE.md). The translation text can be validated in the cloud; actual glyph rendering, wrapping and shader compatibility require Warband. See [FORMAT.md](FORMAT.md) for locale installation and the reversible stock-font test.

## What this checkout proves

`Aut_Caesar_Aut_Nihil/Data/font_data.xml` declares a 4096 × 2048 atlas, padding 10, font size 105, font scale 80 and line spacing 110. All 1,750 glyph records use page 0. None covers U+4E00–U+9FFF. The optional “Original Font” descriptor also has no CJK glyphs. The module overrides `Textures/font.dds`; copying the optional font cannot establish Chinese support.

The delivered CSVs contain 3,507 distinct Han characters, all missing from that descriptor. This is the delivered repertoire, not a complete future font requirement: further translations, fallback English, names generated at runtime and player-entered text must also be considered.

`mb_src.fx` contains `ps_font_uniform_color`, `ps_font_background` and `ps_font_outline` around lines 986–1009. Uniform rendering samples alpha; the outline calculation combines red and alpha (`(1.0h - sample.r) + sample.a`). Consequently, a generic atlas with arbitrary channel packing is not automatically compatible. The checked-in compiled `mb.fx` has not been reproduced from that source. OpenGL shader files also exist and need separate platform testing. Do not replace the whole shader with one from another mod.

## Option A: use the player's installed Warband Chinese resources

The [TLD developer's published guide](https://steamcommunity.com/workshop/filedetails/discussion/299974223/1470840994976508635/) documents how module font overrides can prevent Chinese and identifies the game's `Data/languages/cns` font resources. Its shader replacement is specific to TLD; it is evidence for the fallback approach, not an ACAN compatibility guarantee.

Prerequisites are a working Warband installation with Simplified Chinese selected and its Chinese font resources installed. Test Native in Chinese first. On a copy of the ACAN module, back up and move `Data/font_data.xml` and `Textures/font.dds` outside the module, then start the mod and inspect Chinese text. Restore both backups to reverse the test. Do not alter global game files or redistribute their fonts. If Native works but ACAN does not, retain the test result and investigate the mod's shader/font interaction.

This is the first option to test because it uses game resources the player already has. It is **not yet a verified installation fix for ACAN**.

## Option B: build a separately licensed Chinese bitmap font

Two primary-source candidates supply Simplified Chinese outlines suitable for investigating a reproducible bitmap build:

| Font source | Verified availability | License evidence |
| --- | --- | --- |
| [Noto Sans CJK](https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/README.md) | Simplified Chinese language-specific and China subset packages, including static OTF and variable TTF configurations | [Noto Sans OFL 1.1](https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/LICENSE) |
| [Adobe Source Han Sans / 思源黑体](https://github.com/adobe-fonts/source-han-sans) | Pan-CJK OpenType project with CN configurations and published build sources | [Adobe's OFL 1.1 notice](https://raw.githubusercontent.com/adobe-fonts/source-han-sans/master/LICENSE.txt), which reserves the font name “Source” |

These are outline-font sources, **not ready-to-install Warband fonts**. An OTF/TTF cannot simply replace `font.dds`. Choose the Simplified Chinese face so shared Han codepoints use the intended regional glyph forms.

The licenses permit bundling and modification subject to their conditions. Preserve the downloaded font's copyright notice and full OFL with any redistributed derivative, honor reserved names and avoid presenting a modified font as an endorsed original. Keep font licensing separate from the repository's MIT code license. Record the exact font release, source hash, rasterization settings and changes. No font has been downloaded into this repository or redistributed by this task.

[AngelCode BMFont](https://www.angelcode.com/products/bmfont/) is an available rasterization tool: its author documents Unicode input, character selection from UTF-8 text, DDS output, configurable padding and command-line generation. Its descriptor format is not Warband's `FontData` format, so conversion and validation are still required. Its optional multi-channel packing needs special shaders and should not be enabled without a matching verified shader. If the chosen font format is unsupported by the rasterizer, first create a supported static face through a documented font-build workflow rather than renaming its extension.

A reproducible prototype would:

1. Derive a codepoint inventory from translated **values**, source fallback text and required UI symbols; decide whether player-input support requires a broader repertoire.
2. Rasterize a selected licensed face and retain readable metrics at small game UI sizes. Avoid assuming unlimited texture dimensions or multi-page support: this module proves only a single-page example.
3. Convert glyph rectangles and advances to Warband's XML fields (`code`, `page`, `u/v/w/h`, `preshift`, `yadjust`, `postshift`), then independently validate rectangle bounds, duplicate codepoints and repertoire coverage. Metric semantics require engine calibration; do not substitute BMFont numbers blindly.
4. Match atlas channels to the active shader and verify Windows and OpenGL paths where supported. Rebuild shaders only after establishing the source/toolchain and binary correspondence.
5. Test menu labels, long dialogue, quest logs, troop names, combat messages and input fields at multiple UI sizes. Compare spaced and unspaced Chinese for line wrapping. Font padding alone is not proof that wrapping works.

Until one option passes those in-game checks, describe this work as a translated-text milestone with an unresolved font prerequisite, not a fully playable Chinese release.
