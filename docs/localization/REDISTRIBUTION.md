# Redistribution evidence and package scope

Audited 2026-10-05 against checkout `e27651ba0f659762ccdfc5217e80c74f970d1c37` and its working tree. This is an evidence inventory for the localized ACAN module, not a new license for third-party material. No assets, notices or tools were changed by this audit.

## What the repository grants

The root [LICENSE](../../LICENSE) explicitly grants MIT rights to copy, modify and distribute the software and associated documentation, with copyright `2025 Butters`. Retain the **entire** license, including its disclaimer, in every module package. A missing repeated MIT header on an individual asset is not by itself a restriction or a reason to demand fresh permission.

The root [README](../../README.md#credits) explicitly credits contributors, other mods and community resources. This fork changes localization, not the asset collection; it does not newly assemble an overhaul from those resources. Preserve the complete upstream README and credits with the distribution. The root MIT declaration is the affirmative repository-level grant; the specific third-party notices below must also remain visible. Do not describe all bundled third-party works as authored by Butters or newly relicensed under MIT.

The existing `create-release.yml` and `create-pre-release.yml` workflows each run `zip -r ... Aut_Caesar_Aut_Nihil` at line 25. That command does not include the root LICENSE or README. A localized package must explicitly add those documents; copying that command unchanged would omit them.

## Concrete third-party evidence

| Component | Evidence | Distribution treatment |
| --- | --- | --- |
| ACAN data, scenes, models, textures, sound and music | Root MIT plus full upstream credits. The module includes 108 files under `Resource`, 2,205 under `Textures`, 925 under `SceneObj`, 648 under `Sounds`, and 119 under `Music` at audit time. | Preserve the existing runtime collection and credits for this localization-only fork. The counts describe the scope inspected, not a per-file authorship certificate. No contrary asset-wide prohibition was found in repository notices. |
| TaleWorlds-derived shader sources | `mb_src.fx:36–44`, `mb_src_stochastic.fx:14–22` and `mb_src_backup.fx:14–22` identify Mount&Blade Warband shaders and TaleWorlds, retain “All rights reserved”, expressly allow editing main shaders/lighting, and say not to change `fx_configuration.h`. Their opening headers also credit LA_GRANDMASTER and Viking Conquest. | Preserve sources and headers unchanged. This is evidence of a separate rights notice and limited editing statement, not an MIT grant from TaleWorlds. No independently worded shader redistribution grant is present in those headers. The localized fork does not modify these shaders. Keep the existing compiled shader and platform shader assets needed by the mod; do not claim the headers independently clear them for unrestricted reuse outside this module. |
| `Aut_Caesar_Aut_Nihil/fxc.exe` | Executable version metadata identifies Microsoft Corporation, DirectX for Windows, version `9.27.952.3012`, copyright 1994–2007. `compile_fx.bat` invokes it to compile `mb_src.fx` into `mb.fx`. No Microsoft license or redistributable-file list accompanies it. | **Exclude from the player/runtime package.** It is a build tool, not a required game asset. The root MIT notice is not evidence of Microsoft's redistribution grant. Developers can obtain a suitable compiler separately under its own terms. This audit did not execute it. |
| Existing module bitmap fonts | Active `Data/font_data.xml` / `Textures/font.dds`; optional pairs under `Optional/Original Font` and `Optional/Lanjane's Font`. The directory name credits Lanjane; the active atlas is not byte-identical to the optional Lanjane atlas. No separate font grant or reliable per-file origin manifest is present. | Preserve existing upstream files and attribution when retaining the module collection; do not infer that “Original Font” proves a particular game's ownership or that the active atlas is Lanjane's. These files do not establish Chinese glyph support. See [FONT_OPTIONS.md](FONT_OPTIONS.md). |
| Fonts or binaries from the player's Warband installation | These are external to this repository and not covered by its MIT declaration. | **Do not add game executables, game font atlases/descriptors or other files copied from an installed game to this package.** A local installed-game font fallback is a user-side operation, not a redistribution grant. A separately licensed generated font would need its own license and provenance; none is approved by this audit. |
| W.R.E.C.K. compiler | `module_system/compile.py:11–31` contains MIT terms, copyright 2015 Alexander Lomski. | Source archives must retain this full notice in addition to Butters' MIT license. `module_system` is unnecessary for a runtime-only package. |
| Colorama 0.3.1 | `module_system/colorama/__init__.py` identifies version 0.3.1; six Python headers identify Jonathan Hartley 2013 and BSD 3-Clause, referring to a LICENSE file. That referenced license file is absent from this checkout. | Omit `module_system` from the runtime package. For a separately redistributed source/tool archive, restore the matching upstream BSD notice rather than treating these files as MIT-only. No extra code permission is inferred from the missing notice. |
| Bundled web visualization libraries | `lib/vis-9.1.2/vis-network.min.js:1–25` identifies Almende B.V./visjs contributors and offers Apache-2.0 **or** MIT. `lib/tom-select/tom-select.complete.min.js:1–4` identifies Tom Select v2.0.0-rc.4 under Apache-2.0. No additional standalone license files were found. | Omit `lib/` from the runtime package. Any separate distribution of these libraries must preserve their headers and supply the chosen/applicable full license texts and applicable upstream notices; Butters' notice alone does not replace them. |

No game executable was found in the runtime tree apart from the Microsoft build tool identified above. Base-game `load_resource` entries in `module.ini` are references to the player's installation, not files that need to be copied into the archive.

## Specific asset permission source: Roman Models Extravaganza

ACAN's README links [Roman Models Extravaganza 1.0.9](https://steamcommunity.com/sharedfiles/filedetails/?id=1506238217). Its creator-authored Permissions section, checked 2026-10-05, grants individuals free use with resource/contributor credit. It requires discussion for large mixed-resource teams and overhaul-related submods, and requires a use-with-credit policy for one's own assets. Credited creators: Noniac, Celticus, Benjin, Hloeric, Kaziel and Zaskar70; retain these names with the resource credit.

Assessment: a localization-only fork is not automatically a new large-team overhaul. Individual use with credit is affirmative permission evidence, and MIT permits reuse of this fork's own licensed work. Unresolved: the publisher's applicable category, any existing ACAN agreement, and which actual meshes/textures originate from this pack. Do not infer a denied or nonexistent agreement from its absence in the checkout. This page also does not establish a per-file cross-game provenance chain. No filename-to-author mapping was invented.

The README also identifies Polished Landscapes and other OSP resources. The linked Polished Landscapes forum page could not be retrieved during this audit; no additional restriction is asserted from that retrieval failure. The remaining credits were not independently resolved into asset-by-asset licenses. This limits the completeness of provenance verification; it does not negate the explicit root MIT grant or justify classifying every credited file as blocked.

## Package disposition

For a **private review package**, include the localized `Aut_Caesar_Aut_Nihil` runtime tree with its existing assets, omit `fxc.exe`, and add root LICENSE, complete README, localization documentation and this evidence record. Preserve pre-existing shader source headers unchanged. Do not add `module_system`, `lib`, `.git`, caches, credentials or externally copied game resources to the player package. These are package rules; this audit does not delete anything from the source checkout.

A full module package can be prepared under that scope without pretending that every third-party provenance question has been independently resolved. Before describing a public package as universally cleared, the remaining **specific** evidence gaps are: the shader header's lack of an independent redistribution clause, the model pack's applicable conditional-use category/any upstream agreement, and exact provenance of existing font/other credited assets. No new permission flow is imposed merely because files lack duplicate headers. Public release/publication remains a separate parent-task decision; this document neither publishes nor authorizes publication.

For any future source/tool distribution, additionally resolve the missing Colorama full license notice and web-library license texts. Those omissions do not affect a runtime package that excludes those development directories.

## Full upstream credits (preserved)

The following is copied from the repository README's Credits section so a review package can retain the complete list even if only this document is opened. Preserve the README itself as well.


### Contributors
A huge thank you to everyone who has contributed to the development of *Aut Caesar Aut Nihil*:

*   **@lilibyiumb:** 2D art and textures
*   **@migdeu19:** Models, Research, Historical Advice
*   **@wlodoviecus:** Scenes, Research, Historical Advice
*   **@oliver:** Models, Scenes, Support
*   **@ali04681:** Writing
*   **@odysseus** Faces, Writing
*   **@Northwind:** Writing
*   **@swissgoblin:** Sounds and Writting
*   **@minuucios:** Models, Textures
*   **@possiblyyourgrandpa:** Sounds (Voice Orders)
*   **@rafa666:** Scenes, Models
*   **@Arzelle:** Models
*   **@Dmitry1945:** Scenes
*   **@mamonexus:** Textures
*   **@tocan:** Coding
*   **@frankbourne:** Testing
*   **@BanDHMO:** Writing (Quests, Events)
*   **@adriankowaty:** Writing, Support
*   **@federicomancinelli:** Quest Writing, Support
*   And to **everybody** who ever wrote a meaningful bug report!

### Inspiration & Acknowledgements
We stand on the shoulders of giants. Special thanks to the creators of these mods for their inspiration and resources:

*   [457AD Last year of the Western Empire](https://www.moddb.com/mods/457ad)
*   [ANCESTORS 2112BC](https://www.moddb.com/mods/time-of-new-chances-ancestors-2112-bc-bronze-age-mod)
*   [Bellum Imperii](https://www.moddb.com/mods/bellum-imperii)
*   [Imperial Rome](https://forums.taleworlds.com/index.php/topic,333982.0.html)
*   [Mount and Gladius](https://www.moddb.com/mods/mount-and-gladius)
*   [Romae Bellum](https://forums.taleworlds.com/index.php/board,318.0.html)
*   [Rome at War](https://forums.taleworlds.com/index.php/board,307.0.html)
*   [Brytenwalda](https://forums.taleworlds.com/index.php/board,189.0.html)
*   [Diplomacy](https://forums.taleworlds.com/index.php/board,176.0.html)

### Open Source Projects (OSP) & Assets
This mod utilizes various Open Source Projects and assets from the community:

*   **Polished Landscapes** ([Link](https://forums.taleworlds.com/index.php?topic=122423.0))
*   **Gold and Iron Mines** ([Link](https://forums.taleworlds.com/index.php/topic,322815.0.html))
*   **rubik's worldmap** ([Link](https://forums.taleworlds.com/index.php/topic,251355.0.html))
*   **Native Scene Replacement** ([Link](https://forums.taleworlds.com/index.php/topic,320580.0.html))
*   **9 Timurid Yurts** ([Link](https://forums.taleworlds.com/index.php/topic,379895.0.html))
*   **Crusaders Way to Expiation** ([Link](https://forums.taleworlds.com/index.php/topic,337081.0.html))
*   **AlphaDelta's Ancient warriors pack**
*   **Ambient Soundtrack Warband**
*   **Map Icons Pack**
*   **I want to eat food**
*   **ULTIMATE COMBAT OSP**
*   **Grandmasters Shaders** (Basic Seasons & Wind effects)
*   **Spec life 0.8**
*   **Stylize HUD mini-interface** by FALX
*   **box prop** by Red_Serf
*   **Roman Models Extravaganza 1.0.9** ([Link](https://steamcommunity.com/sharedfiles/filedetails/?id=1506238217&searchtext=models))

