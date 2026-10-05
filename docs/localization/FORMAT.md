# Warband localization format and verification notes

This project targets Simplified Chinese (`zh_CN` as a human-facing language identifier). **Warband's runtime directory is `Aut_Caesar_Aut_Nihil/languages/cns/`, not `languages/zh_CN/`.** Select Simplified Chinese in the Warband launcher. Do not replace the English module-system text or rebuild game logic merely to install translations.

## Evidence and conventions

- The [Red Wars development team's Simplified Chinese patch instructions](https://www.moddb.com/mods/the-red-war-12/downloads) explicitly install CSV files into `Modules/<mod>/languages/cns`.
- [Brytenwalda Studios' developer instructions](https://steamcommunity.com/app/48700/discussions/0/530649887208111946/) describe the authoritative export: start a campaign in windowed mode, enter the world map, then choose **View → Create Language Template → Default**. The game writes `new_language` in the Warband directory. Enable edit mode if that menu is unavailable. A fresh export from this exact mod build is the final check on the extracted inventory.
- Despite the `.csv` extension, rows are `stable_id|translated text`, one physical line per record. Commas are ordinary prose. Do not use spreadsheet CSV quoting or change the ID. The [Economy Mod's original cns files](https://github.com/mbw-economy/Economy-Mod-for-Mount-and-Blade--Warband/tree/master/languages/cns) provide directly inspectable runtime examples. Their bytes decode as UTF-8 and begin with `EF BB BF` (UTF-8 BOM); this repository's existing en/de files decode as UTF-8 without BOM. UTF-8 is verified; the engine's absolute requirement or indifference to BOM has not been independently tested here.
- Preserve register references, printf conversions, escaped percent signs, formatting controls and branch structure. Examples include `{s13}`, `{reg1}`, `{playername}`, `%d`, `%%`, `^` and `{reg1?plural:singular}`. Translate branch prose while retaining its register and delimiters. Chinese may use identical text in both plural branches.
- Underscores in compiled `.txt` text encode spaces; underscores in IDs must remain unchanged. Read the committed compiled output to retain the compiler's actual IDs, especially for quick strings.

| Runtime file | Verified ID convention |
| --- | --- |
| `game_menus.csv` | `menu_<menu id>` and `mno_<option id>` |
| `troops.csv` | `trp_<id>` and `trp_<id>_pl` |
| `item_kinds.csv` | `itm_<id>` and `itm_<id>_pl` |
| `factions.csv` | `fac_<id>` |
| `parties.csv` | `p_<id>` |
| `info_pages.csv` | `ip_<id>` and `ip_<id>_text` |
| `item_modifiers.csv` | `imod_<id>` (compiled source in `Data/item_modifiers.txt`) |
| `skills.csv` | `skl_<id>` and `skl_<id>_desc` |
| `quests.csv` | `qst_<id>` and nonempty description `qst_<id>_text` |
| `dialogs.csv` | Actual compiled `dlga_...` IDs |
| `quick_strings.csv` | Actual committed `qstr_...` IDs |

Info-page title/body IDs are directly verified in the [reference mod’s info_pages.csv](https://raw.githubusercontent.com/mbw-economy/Economy-Mod-for-Mount-and-Blade--Warband/master/languages/cns/info_pages.csv). The modifier IDs and `%s` format are verified in the [reference mod’s item_modifiers.csv](https://raw.githubusercontent.com/mbw-economy/Economy-Mod-for-Mount-and-Blade--Warband/master/languages/cns/item_modifiers.csv). The quest description suffix is evidenced by the [Japanese translation project's published translation](https://w.atwiki.jp/warband/pages/386.html) and its [English export](https://w.atwiki.jp/warband/pages/361.html). The active WRECK compiler (`module_system/compiler.py:process_quests`) writes the description field unconditionally; do not silently exclude nonempty descriptions based on quest flags. Engine-export comparison remains part of in-game QA.

## IDs and collisions

The active `module_system/compiler.py:process_dialogs` constructs dialogue IDs from input and output state names, adding `.1`, `.2`, etc. when differing texts collide. The legacy `Process/process_dialogs.py:create_auto_id2` agrees; its older text-based `create_auto_id` is not the active convention.

`module_system/compiler.py:parse_string_operand` initially takes 20 normalized English characters for a `qstr_` ID and extends the prefix when it collides. Existing quick strings are loaded before compilation. Recreating quick-string IDs from a fresh source traversal can change them, so use the committed `quick_strings.txt` and compare against a future in-game export.

`module_system/compiler.py:process_game_menus` writes `menu_` and `mno_` IDs directly. Repeated option IDs are real: the external cns example contains `mno_continue` 110 times and `mno_go_back` 9 times, including different text. **Do not invent `.1` suffixes for menu options.** Keep collisions visible in the inventory. One ID cannot reliably provide two context-dependent translations; select a shared translation only where its meaning fits every occurrence, otherwise defer the conflicting ID and report it. The engine's duplicate-row precedence has not been tested. Translation output should have unique IDs even if the source inventory has repeated occurrences.

## Chinese fonts and installation QA

The checked-in `Data/font_data.xml` and `Optional/Original Font/font_data.xml` each contain 1,750 character records and **zero CJK Unified Ideograph glyphs**. The module also supplies `Textures/font.dds`. Merely copying Chinese CSV files therefore does not establish that Chinese text will render correctly. The optional “Original Font” does not solve this.

The [Last Days developer's font guide](https://steamcommunity.com/workshop/filedetails/discussion/299974223/1470840994976508635/) confirms that module font overrides can prevent Chinese rendering, and describes falling back to Warband's language font resources. On a test installation, back up the module's `Data/font_data.xml` and `Textures/font.dds`, then move those two overrides outside the module and test with the game's installed Simplified Chinese resources (`Data/languages/cns/font_data.xml` and corresponding Chinese font texture). Restore the backups to undo this test. Do not delete or replace the game's global files.

That guide also changes TLD's shader: **do not copy TLD's shader into this mod.** ACAN’s `mb.fx` is a compiled binary. Shader source `mb_src.fx` is also present, but its correspondence to that binary and compatibility with the stock Chinese font have not been verified. If restoring the stock font still produces blank or broken characters, a mod-specific font/shader compatibility fix is needed before calling the localization playable. No proprietary game fonts are redistributed here.

Older Chinese translations insert spaces between Han characters. This can affect Warband's word wrapping. Their presence is verified in reference files, but whether this exact mod/game build requires them is not established. Test dialogue wrapping, quest logs, long menu options, combat notifications and troop names at multiple UI sizes before release; retain this as an explicit layout QA question rather than assuming a particular font padding value fixes it.

No in-game QA is claimed from this cloud workspace. Engine export comparison, Chinese glyph display, wrapping, menu collisions and saved-game behavior require a real Warband installation.

## Gender alternatives

Warband permits arbitrary translated text in `{male text/female text}` alternatives. The branch follows the dialogue listener’s gender; it does not necessarily describe the speaker. Preserve braces, slash, branch order and nested register controls while translating branch prose. See the [module-system gender reference](https://mbmodwiki.github.io/Gender_string) and [Chinese reference translation](https://github.com/mbw-economy/Economy-Mod-for-Mount-and-Blade--Warband/blob/master/languages/cns/dialogs.csv). Runtime selection still needs in-game QA.

## Inventory certainty

Coverage uses conservative text candidates extracted from compiled files. It
includes unused labels and some code/resource tokens, which are documented in
`continuation-holds.json`. `runtime_id_convention_verified` records supporting
evidence for ID conventions; it does not mean an exact-build engine export was
compared. `exact_build_engine_export_compared` and `player_visibility_verified`
remain false. No candidate count is a claim of reachable gameplay coverage.

Source `str_emperor_request_text_42` contains prose ASCII colons inside a gender
conditional. Its existing separators are preserved, but the source defect can
affect runtime branch display. This requires in-game/source review rather than
an unapproved localization-side control rewrite.
