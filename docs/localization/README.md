# 简体中文本地化 / Simplified Chinese localization

**Status: broad draft localization with explicit holds; not complete and not yet
verified playable in Warband.** Work began with interface text, menus and basic
troops/factions, then expanded across the compiled text inventory. Remaining
entries and their reasons are recorded individually in the hold ledger. Missing
entries retain the game's source/fallback text.

Source baseline: `3ed34f35c94c974f9d2a9102750dbb4866e38f6d` in
`4everWZ/aut_caesar_aut_nihil`, from `buttersnew/aut_caesar_aut_nihil`.
The original MIT license (Butters, 2025), English data, compiled gameplay files,
shaders and assets are unchanged. No game recompilation is needed.

A separate [full-tree packaging candidate](PACKAGING.md) now includes an OFL
Chinese font candidate. It is explicitly incomplete because three referenced
sounds are absent. The instructions below describe the translation-only overlay.

## 安装 / Installation

1. Install the matching ACAN build in Warband's `Modules/Aut_Caesar_Aut_Nihil`.
   Back up an existing Chinese language folder before replacing it.
2. Copy this checkout's `Aut_Caesar_Aut_Nihil/languages/cns` directory into that
   module's `languages` directory. The final path must be
   `Modules/Aut_Caesar_Aut_Nihil/languages/cns/ui.csv`, for example.
   `zh_CN` is the language name used in documentation; **`cns` is the engine code**.
3. Select Simplified Chinese in Warband's launcher and select the ACAN module.
   The base game's Chinese language resources must already be installed.
4. **Resolve the font override before judging the translation.** Both the mod's
   bundled font and its “Original Font” option lack Chinese glyphs. On a test
   copy, back up `Data/font_data.xml` and `Textures/font.dds`, then move those two
   files outside the module to test the game's Chinese font fallback. Do not
   overwrite global game fonts or copy another mod's shader. See
   [format and font evidence](FORMAT.md) for the known limitations.
5. Start a new test campaign and verify characters, menus, troop names, item
   names, quest log, long-line wrapping and percent/register substitutions.
   Test the intended Warband/WSE2 version and UI scale. Save compatibility and
   old dynamically assigned names are not tested; existing saves can retain
   previously stored names. If font fallback fails, restore the two backups:
   a mod-specific font/shader fix is required before this is playable.

Uninstall by removing the added `cns` folder (or restoring its backup), restoring
any moved font files, and selecting your previous language. These instructions
make no changes to the user's computer automatically.

## Delivered scope

There are **37,979 runtime CSV rows**, with **37,968 changed text-candidate IDs**
out of **39,017** across 17 categories (**97.31%**). The remaining
**1,049 candidate IDs** are individually accounted for in
[continuation-holds.json](continuation-holds.json), including intentionally
unchanged values and non-prose tokens. No unclassified backlog remains.

This is conservative inventory coverage, not word, story or playthrough coverage.
The candidate set includes singular/plural pairs, unused/reserved labels and
resource identifiers. ID conventions are supported by reference/source evidence;
they have not been compared with an engine export from this exact ACAN build.

| Category | Translated candidates | Remaining candidates |
| --- | ---: | ---: |
| Dialogue | 12,375 / 12,395 | 20 |
| Factions | 74 / 74 | 0 |
| Menus | 1,834 / 1,976 | 142 |
| Named/game strings | 8,565 / 8,951 | 386 |
| Hints | 30 / 30 | 0 |
| Info pages | 56 / 58 | 2 |
| Items | 3,778 / 3,794 | 16 |
| Item modifiers | 43 / 43 | 0 |
| Map parties | 496 / 503 | 7 |
| Party templates | 300 / 303 | 3 |
| Quests | 171 / 171 | 0 |
| Script/quick strings | 5,537 / 5,574 | 37 |
| Skills | 50 / 84 | 34 |
| Appearance | 35 / 35 | 0 |
| troops.csv | 3,775 / 4,173 | 398 |
| UI | 743 / 745 | 2 |
| Launcher | 106 / 108 | 2 |

Rows deliberately omit incompatible shared menu IDs, ambiguous native unit terms,
source-meaning decisions and code/resource tokens. Three age-sensitive sexual
passages are withheld; nonsexual surrounding narrative is translated. Active
skills are covered; reserved skills remain unchanged. Many source `{!}` and
format-only values are excluded from the candidate denominator. See
[decisions](DECISIONS.md), [narrative review](STORY_PASS.md), and the per-ID ledger.

The authoritative machine-readable breakdown, source collisions and source
formatting issues are in [coverage.json](coverage.json). Recreate a full
English/location backlog with the command below; it is not committed as an
extra copy of all source prose.

## Translation decisions and blockers

- Follow [terminology.md](terminology.md). Translate displayed text, not the ID:
  several troop and item IDs suggest a different name from the actual source.
- 141 menu-option IDs have differing source texts. Context review resolved 15
  with shared wording; 126 remain deferred. See [menu-id-review.json](menu-id-review.json). Examples include
  `mno_continue`, `mno_go_back`, `mno_recruit_volunteers`, `mno_castle_wait` and
  `mno_town_leave`. These common controls can remain English even on translated
  screens. Context-specific localization needs upstream unique IDs or a
  reviewed translation that fits every occurrence.
- UI source collisions were reviewed: `ui_retreated_battle` uses the shared
  “%s 已逃离战场。” for routed/fled; `ui_group_rename` differs only in case.
  Duplicate `ui_midnight` and `ui_chest` rows have identical meanings.
- `Dionysus Rege!` remains verbatim within its translated quest category pending
  author clarification. Unfamiliar reconstructed ancient-language troop names
  are deferred. We do not invent a narrative or silently correct source lore.
- Four malformed brace strings already exist upstream, and twelve source
  strings contain literal pipes requiring engine-escaping review. All are
  listed in the report, left unchanged, and outside the delivered translations.
- Chinese font fallback, long-text wrapping (including whether Han-character
  spacing is required), shader compatibility and save behavior need in-game QA.
  No Warband executable is available on this cloud workspace's PATH.
- The GitHub CLI reports an invalid `GH_TOKEN`. Read-only `git ls-remote`
  succeeds for the public fork; this does not establish push permission. No
  alternate credentials or browser login were used. Nothing was pushed, merged
  or released.
- The initial nine meaning-changing source ambiguities remain in English:
  see [pending-meaning-decisions.json](pending-meaning-decisions.json), with source,
  location and proposed contextual readings. [STORY_PASS.md](STORY_PASS.md) records
  the narrative scope and review limitations. Additional continuation questions
  and technical holds are recorded in DECISIONS.md and continuation-holds.json.

## Maintaining and validating

Use Python 3.10+ and no third-party dependencies, from the repository root:

```sh
python3 tools/localization/check.py --check
python3 -m unittest discover -s tools/localization -p 'test_*.py'
python3 tools/localization/check.py --report /tmp/acan-coverage.json --missing /tmp/acan-backlog.json
python3 tools/localization/check.py --export-dir /tmp/acan-english
```

`--export-dir` emits unique English candidate IDs for translators, omitting
conflicting IDs and literal pipes. It is an aid, not an authoritative in-game
language export, and refuses to write into the runtime module. Do not ship these
English templates as translations. Compare with Warband's **View → Create
Language Template → Default** export from this exact build when available.

The tool parses committed compiled files using WRECK field/operation counts,
checks declared record totals, and retains actual dialogue/quick-string IDs. It
inventories English CSVs, named/quick strings, dialogues, menus, troops, items,
factions, quests, skills, map parties/templates, info pages, skin controls and
`Data/item_modifiers.txt`. It also tokenizes 50 module-system source files and
hashes them, including script/presentation/trigger sources, systems and character
names. String-literal counts include identifiers: they are a source audit, not
additional player-facing coverage. 209 compiled hexadecimal face-key values are classified as data and excluded
from text candidates. Numeric face-key source resources, meshes, scenes,
sounds, textures, shaders, compiler headers, handbook and website are outside the
runtime translation inventory; game text in their operations is represented by
compiled quick/named strings. Reachability is not inferred.

Validation rejects duplicate/unknown output IDs, empty translations of nonempty
source, wrong UTF-8/BOM, changed register counts, nested/gender branch structure,
non-positional printf order, percent/escape/newline controls and translated `{!}`
markers. Deliberate trailing spaces in UI fragments are preserved for concatenation;
`.gitattributes` exempts only these runtime CSVs from end-of-line whitespace lint.
Semantic accuracy still needs human review.

[baseline.json](baseline.json) pins source hashes and every delivered milestone
ID, so `--check` fails on source drift or removed milestone rows. Following an
upstream update, review the new engine export and source changes, update affected
translations, then explicitly refresh the baseline/report:

```sh
python3 tools/localization/check.py --pin --report docs/localization/coverage.json
python3 tools/localization/check.py --check
```

Do not use `--pin` merely to silence missing translations. Reports deliberately
keep partial coverage visible; an untranslated backlog is not a passing claim of
complete localization. The regression suite covers parser layouts and negative
cases for IDs, encoding, source drift and formatting corruption.

## Building an installation archive

After validation and a clean local commit, run:

```sh
python3 tools/localization/package.py --output /tmp/acan-zh-cn-localization.zip
```

The reproducible archive includes the runtime `cns` directory, installation and
font notes, coverage, glossary, pending decisions, license, SHA-256 manifest and
a review patch against the pinned source. It excludes fonts and gameplay assets.
The builder rejects dirty checkouts, untracked inputs and non-localization changes.
