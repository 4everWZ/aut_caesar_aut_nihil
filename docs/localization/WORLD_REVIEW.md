# World text review

Staged496 parties,300 party templates,56 info page entries. UTF8 BOM; duplicate IDs and source signature parity checked. Dyrrachium uses 都拉基乌姆.

The primary reference https://github.com/mbw-economy/Economy-Mod-for-Mount-and-Blade--Warband/tree/master/languages/cns establishes category names and p_/pt_/ip_*_text conventions, NOT export or visibility of every ACAN candidate. No engine-generated ACAN language template/in-game test is available. The approximately39k inventory entries remain compiled-source candidates; disabled parties, helper templates and default/dynamic info text mean they are not all demonstrated player-visible strings.

pf_disabled alone cannot justify exclusion: quest locations are enabled later. The seven held parties have legacy/range/helper roles. pt_patrols_end is actually spawned in module_dialogs.py25751 and is translated as 巡逻队 despite its suffix. Active reinforcement template labels may be intermediates, so translation does not prove display.

Info-page legion bodies default to “This legion has been disbanded.”; module_scripts_hardcoded.py7181 onward dynamically builds legion notes from quick strings, and translating defaults alone does not cover those notes. autoloot retains the source stray literal d twice. Companion page preserves Marcus Tullius as 马尔库斯·图利乌斯 though current troop npc23 is Lucius Varus Drusus; source appears stale, not silently corrected. Cohors Prima Legio I Adjuterix is translated from displayed text as 第I援助军团第一大队, despite ID containing xxii_primigenia. Archer cohort templates displaying generic infantry/cohort remain generic in Chinese. Temple_of_rhodogune display Zamb remains 赞布; display text takes precedence over ID guesses.

Held semantic decisions: Furor Teutonics malformed Latin; hotkeys G heading/J instruction; info renown ceiling contradicts code floor. See JSON. No game logic or English source changed.

## Narrative and generated-name continuation

### World game strings: indices 4550–5999

Snapshot inventory: 1,450 assigned indices, 27 already present in runtime or other staged `strings_remaining_*.csv` files, 1,423 eligible. Delivered 1,387 translations: 856 generated-person names in shards 01–03 and 531 prose/labels in shards 04–05. Remaining 36 are explicit internal markers or reserved skill labels, itemized with source and reason in `continuation-holds.json`. All eligible indices accounted exactly once; stage UTF-8 BOM, exact IDs, unique IDs and exact checker signatures checked. This is static validation, not in-game QA.

Name review: 101 exact whole-source name reuses from existing semantic name translations; other names manually transliterated. G. Appius Fundus keeps G. unexpanded; AccoAddedomarus keeps the source combined spelling as one transliterated name. Germanic -burg uses 布尔格, not semantic 堡. No conjectural ranks, roles or etymological meanings added.

Prose review: contains staff assessments, festival/gladiator dialogue, flirtation, spouse/child conversation, regional rumors, holy-site notes, book summaries, and slave skill assessments. Rumor `_end` strings with real dialogue are translated; only literal sentinel ends are held. Adult imperial-feast prose (4714–4722) is faithfully translated from supplied text without added material. Hermes's source century-long career at 4646 is retained literally; source historical claims and inconsistencies are not repaired. Book descriptions retain exact caret run counts. All skill-reference bonuses match existing localized skill names. Gladiator 忒特赖忒斯 and 弗拉马 aligned with runtime troops; other familiar Roman names and sacred places checked against existing localized parties/troops. Proper-name variants received cross-batch terminology review.

No unresolved semantic blocker among the translated rows. Reserved/internal entries remain source fallback and are classified separately from demonstrated playable prose. Candidate IDs come from the existing inventory and are not new proof of engine-export coverage.
