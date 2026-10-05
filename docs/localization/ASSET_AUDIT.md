# Static module packaging audit

Audit date: 2026-10-05. This checkout contains a substantial complete-looking module tree, not merely module-system source. It can be archived as a **local, unverified full-module candidate**, but the audit does not establish a complete, licensed-for-every-asset, playable release. Three referenced sound files are absent, platform-specific texture filename mismatches remain, and Chinese font/rendering validation is separate.

Run `python tools/localization/audit_module.py` from any directory to refresh [asset_audit.json](asset_audit.json). The script reads module assets and writes only that report. It does not download, repair or redistribute assets. Counts describe this checkout at audit time, before any optional font candidate is applied.

## Bundled assets and runtime inputs

| Directory | Files | Bytes |
|---|---:|---:|
| Resource | 108 | 402,621,370 |
| Textures | 2,205 | 1,055,336,416 |
| SceneObj | 925 | 160,606,609 |
| Sounds | 648 | 207,768,039 |
| Music | 119 | 216,766,336 |
| Data | 6 | 238,036 |
| GLShaders | 36 | 31,266 |
| GLShadersOptimized | 76 | 203,662 |
| Optional | 4 | 4,421,181 |

All 107 active `load_mod_resource` BRF filenames exist with exact casing. All 31 checked compiled tables exist, alongside `module.ini`, the map, `mb.fx`, `postFX.fx`, OpenGL shader directories and data overrides. No empty files or Git LFS pointer stubs were found in the module tree; `.gitattributes` contains no LFS declarations. The report includes the exact checked table list. Presence does not prove a table or shader is valid or matches its source.

The module has 52 active `load_resource` references, including `test`, `shaders`, `helpers`, `object_bodies` and animation archives. These explicitly designate game resources, as distinct from `load_mod_resource`; they require the user's installed Warband resources and should not be called missing module files or copied into a localization package. Exact names are in the JSON. No installed Warband/CommonRes baseline was available for verification. `operation_set_version = 1170`, `compatible_with_warband = 1` and `supports_directx_7 = 0` are the module's own declared requirements, not a newly tested compatibility matrix.

## Exact unresolved sound dependencies

651 entries in the sound-file table resolve to 648 module files; there are no case-only sound matches. The three absent filenames are:

| File | Source evidence | Interpretation |
|---|---|---|
| `woman_death_12.wav` | `module_system/module_sounds.py:122`, among 13 female death variations | Missing member of the locally bundled numbered set; do not silently substitute a neighboring file. |
| `disease_sound.wav` | `module_system/module_sounds.py:242`; active play calls in `module_game_menus.py`, including line 28176 | Referenced event audio absent from this checkout. |
| `riot_sound.wav` | `module_system/module_sounds.py:243`; active play calls in `module_game_menus.py`, including line 22709 | Referenced event audio absent from this checkout. |

These are **unresolved external files**, not verified Native-provided audio. Their exact provider, redistribution terms and runtime failure behavior cannot be determined here. An upstream full installation or a lawful installed-game comparison is needed to establish whether they are omissions or valid game fallbacks. No binary substitutes were created. All 138 music-table entries resolve exactly to local files (some tracks reuse filenames, hence only 119 files).

## Texture and scene exceptions

The two texture declaration archives, `x_texture_all.brf` and `x_textures_engine.brf`, contain 2,068 unique texture names. Their complete initial texture sections were parsed as length-prefixed names and flags; the following `end` section was verified. There are 21 case-only filename mismatches, individually listed in the JSON, including `PictishDress_blue2.dds` versus `PictishDress_Blue2.dds` and `.dds` versus `.DDS`. These are portability risks on case-sensitive systems, not absent file content. The remaining nonlocal declaration is extensionless `waterbump`, an engine-resource candidate whose resolution is unverified. It is not evidence of a missing `waterbump.dds` file. No filenames were changed.

A raw string scan of BRFs is deliberately not treated as a dependency graph: material identifiers can themselves end in `.tga`. No complete cross-archive mesh/material/shader graph validation or binary decoding test was performed. The unreferenced `Resource/kalasiris.brf` is outside active `module.ini` loads.

890 of 907 scene IDs have exact local `.sco` files. The 17 exceptions are itemized with flags, mesh and terrain in the JSON. They comprise nine `reserved4`–`reserved12` records, three range-end markers, `water`, generated `camp_scene_horse_track`, generated `random_scene_mountain`, generated `sea_barbarian`, and mesh-based `presentation_scene`. `header_scenes.py:16` explicitly defines `sf_generate` as terrain generation. Thus absence of `.sco` alone is not evidence of 17 broken scenes. `presentation_scene` is actively entered by menu code and uses `ch_meet_plain_a`/`bo_encounter_spot`; its runtime placement remains untested. The audit does not claim all generated scenes need no objects or all reserved records are unreachable.

The existing `module.ini:227` also contains a standalone `W`. It is not a valid key/value directive; engine tolerance is untested. It was preserved, not silently repaired.

## Packaging and asset provenance

The upstream release workflow `.github/workflows/create-release.yml` archives `Aut_Caesar_Aut_Nihil` directly after checkout, with no separate asset-fetch or LFS step. That supports using this tree as the intended packaging input; it does not resolve the missing files or prove runtime completeness.

The repository [LICENSE](../../LICENSE) is MIT, copyright Butters 2025. The [README credits](../../README.md#credits) separately name contributors, other mods, soundtrack/community resources and shader/model packs. No per-asset license manifest mapping those binary files to permissions was found. The repository's MIT notice alone is insufficient evidence that every credited third-party binary or bundled build executable was authored by that copyright holder. This audit makes no new blanket redistribution assertion. Keep the upstream license and credits with any candidate; obtain provenance clarification before claiming all assets are independently redistributable. Native/CommonRes game assets are dependencies, not redistributable inputs to this task.

`fxc.exe`, `compile_fx.bat`, shader source/backup files and module-system tooling are build inputs, not required localization runtime files. A packaging tool can omit build tools without recompiling or altering game data; it should retain the compiled shaders and relevant runtime data. The existing Mac/Linux custom-skeleton caveat in the README also remains applicable and is not solved by ZIP packaging.

Chinese font prerequisites and font licensing are documented separately in [FONT_OPTIONS.md](FONT_OPTIONS.md). A generated optional font candidate must be labeled unverified until Warband rendering tests pass. No Warband launch, scene walk-through, sound playback, savegame compatibility check or Chinese glyph inspection was possible in this environment.

## Bounded public recovery check

On 2026-10-05, direct public raw-file URLs for all three missing WAVs returned 404 under both upstream `main` and release tag `v1.0.1.13`. For example: [main disease sound](https://raw.githubusercontent.com/buttersnew/aut_caesar_aut_nihil/main/Aut_Caesar_Aut_Nihil/Sounds/disease_sound.wav), [tagged riot sound](https://raw.githubusercontent.com/buttersnew/aut_caesar_aut_nihil/v1.0.1.13/Aut_Caesar_Aut_Nihil/Sounds/riot_sound.wav), and [tagged female death sound](https://raw.githubusercontent.com/buttersnew/aut_caesar_aut_nihil/v1.0.1.13/Aut_Caesar_Aut_Nihil/Sounds/woman_death_12.wav). Attempts against `develop` were inconclusive fetch errors, not evidence of absence.

The [official release asset listing](https://github.com/buttersnew/aut_caesar_aut_nihil/releases/expanded_assets/v1.0.1.13) lists a 1.17 GB full-module ZIP, handbook and source archives, with no individual sound repair bundle. The full archive was not downloaded or claimed to have been inspected. Shell access to the public GitHub API was blocked by the environment proxy (403 tunnel failure), so historical path recovery could not be established. No credentials or alternate login were sought. Public browser reads of upstream pages remained available.

No primary evidence found in this bounded check establishes these exact three files as Native-provided resources. Upstream module source references them but does not identify their provider. Recovery therefore needs either the three authentic files from a compatible upstream installation with provenance/permission, or maintainer confirmation of the exact installed-game location and compatible version supplying each file. A matching filename in another mod or commercial DLC would not establish either compatibility or redistribution rights. All three remain unresolved; no audio was synthesized, renamed from neighboring clips or removed from gameplay definitions.

## Follow-up archive and severity investigation

The earlier bounded check above has now been extended: the **entire central
directory** of the official v1.0.1.13 ZIP was inspected with HTTP byte ranges.
All three filenames are absent, including case/path variants, while its extracted
sound table references them. See [SOUND_DEPENDENCIES.md](SOUND_DEPENDENCIES.md) for
exact revision/history evidence, complete literal consumers, flags, Native
evidence limits and an actionable installed-game check. No launch failure or
warning-only behavior has been established. The existing review ZIP is preserved.
