# Remaining troop-name pass

Manifest: `troops_remaining.json`, obtained from `check.inventory()` text-candidate
records, excluding the then-current runtime troops CSV and companion_names.csv.
3,439 candidate IDs; 2,996 newly translated; 443 explicit holds. All output IDs
are unique, exact source IDs and all 2,996 placeholder/format signatures match.
Output is UTF-8 BOM. This is candidate-name coverage, not proof of reachability.

## Method

- Exact display-name glossary, not English-looking ID replacement. Latin civilian
  grammatical forms are individually enumerated (ethnonym + role); number-neutral
  Chinese is used for genuine singular/plural equivalents.
- Greek/Latin military plurals are paired only within the known early regular-unit
  block, ending before `trp_looter`. `(exp)`, `(vet)`, `(custom)` are preserved as
  distinct readable 熟练 / 老练 / 自定义 suffixes.
- Proper names use an explicit reviewed component glossary, with Roman name
  abbreviations retained (`Q.`, `P.`, etc.) rather than inventing expansions.
  Nobility titles and cultural role names remain distinct. In particular, lord
  singulars often display a title while plurals store individual given names;
  these two fields were translated independently, never copied blindly.
- Misleading IDs still use actual source: Dacian `heavy_inf` is Toxotes (archer),
  Dacian `archers` is Akontistes (javelin infantry). Germanic Stainawerpandz and
  Skuttilaz have explicit Stone-Thrower/Shooter glosses in `.github/agents/linguist.md`.
- Minor source typos `GermanicLady`, `Dacian Ladyl`, `Supplicantw`, `Muscullus`
  are rendered according to their obvious full-name/role context; English is unchanged.
- `Lin Lee Shen Shen` and `Lei Li Xiao Qiu` have uncertain intended Chinese spelling.
  Provisional phonetic labels retain the full Latin spelling in parentheses.
  This is not a claim to have recovered original Chinese names.
- `trp_diggus` displays `Biggus Dickus`, rendered 比古斯·迪库斯. Earlier dialogue
  says `Diggus Biggus`; keep that differing source form (迪古斯·比古斯) rather
  than silently rewriting the story. `Claudia Urgulanallia` is normalized to the
  established 乌尔古拉尼拉 spelling used for Urgulanilla in story dialogue.

## 398 linguistic holds

`continuation-holds.json` gives every exact ID and source. These cover
reconstructed/non-Latin unit labels, two traveller titles, and native religious
roles whose precise intended meaning was not established. For example,
`Alanno Badaro`, `Gaizafulkan Frijatoz`, `Duno Asyo`, `W'b n Jmn`.
The equipment/ID establishes broad gameplay function, not a reliable translation
of the actual native title. Do not mark these nontranslatable or silently invent
rank/weapon meaning. An author-approved semantic glossary, or approval to use
functional Chinese labels with retained endonyms, would resolve this boundary.

## 45 internal/storage/debug holds (not assumed player-facing)

Every affected ID remains in the hold JSON; no source classification is changed.

- `trp_tournament_participants`, `trp_random_town_sequence`, `trp_global_variables`
  are storage holders. See module_scripts.py:32971 (participant storage contract),
  :22994 (town sequence slots). Multiplayer profile/temp/cheat helpers retain their
  internal source names; no ordinary NPC reachability claim is made.
- Range sentinels include mercenaries_end, town_walker_1, tournament_master
  (`Spywalkers END`), tutorial_trainer (`Tournament Champions END`),
  kingdom_heroes_including_player_begin, merchants_end, custom_troops_end,
  household_end and troops_end. Definitions in module_troops.py:1295,3471,3819,
  3846,3972,7020,7694,7701; range constants in module_constants.py:2424,2554,3841.
  `troops_end` also initializes the fallback hero variable in
  module_game_menus.py:44801, so this is a marker audit, not proof it can never leak.
- `trp_knight_1_1_wife` explicitly displays `Error - FUCKER should not appear in game`;
  it is a range endpoint/start marker (module_constants.py:2320,2329), not a wife
  name that should be creatively translated.
- Player camp chests 1–3 are storage holders renamed dynamically at
  module_scripts.py:61073; the range end is additionally party storage as documented
  in module_constants.py:4195. Static translation would not localize those assigned names.
- `trp_inventory_backup` is `tf_inactive` (module_troops.py:7022), referenced in
  commented inventory-copy calls. `pseudo_troop_end_pl` literally says
  `pseudo troop end`, so its plural remains held even though singular is translated.

## Marker-like names that ARE translated after tracing usage

- `trp_bard_end` / plural display `New Month`: its name is interpolated into the
  Edictum mensum report (module_scripts.py:51026). Translated 新月份.
- `trp_pseudo_troop_end` singular displays `Second Outfit`: player-copy actor is
  spawned into the senate (module_game_menus.py:30935). Translated 第二套服装;
  the plural's internal marker remains held.
- `trp_follower_party_mules` / plural: actual loot screen target
  (module_game_menus.py:1171). Translated 随军队伍的骡子.
- `trp_bannerlord` / plural `HOLY SOON` is an actual joke NPC, not debug text:
  spawned at a party (module_game_menus.py:45992), with dedicated dialogue
  (module_dialogs.py:18331 onward). Rendered 霍利·苏恩（HOLY SOON） to preserve the name.

No runtime CSV or game source edits were made in this pass. No in-game QA.

## Final debug-inspector review (supersedes internal-label holds above)

# Bounded review of 45 troop internal/debug holds

All 45 are given supplemental translations solely because the actual debug troop inspector renders both singular and plural names. This does not reclassify storage or sentinel troops as ordinary narrative characters. The 398 uncertain native-language troop labels remain held and untouched.

Evidence in module_system/module_game_menus.py:
- 27353 display_troop_slots helper; 27359–27360 str_store_troop_name and str_store_troop_name_plural render current selected troop into the menu.
- 27440–27454 next/previous selectors step from trp_player through trp_troops_end and render the next/previous troop name. Thus all 45 reviewed names are visible/selectable through this debug interface.
- 26858 and 49177 jump into that inspector.
- 2211/2217 directly expose trp_find_item_cheat through loot/trade screens.
- 3419 and many other ordinary loot paths expose trp_temp_troop through change_screen_loot.
- 44801 sets trp_troops_end as the default myth-hero fallback; this is additional evidence against describing it as universally unreachable, but no normal successful path is claimed.

Delivered troops_debug_supplement.csv: 45 UTF-8 BOM pipe rows, exact IDs, every signature matches. Paired original inventory records in troops_debug_supplement.json. No runtime edits. This supersedes only the 45 internal_storage_marker_or_debug holds, not 398 unresolved_ancient_language_role holds.

The final continuation ledger contains only still-held entries. All 45 labels
previously held as internal storage/range/debug names are now translated because
the troop inspector can display both singular and plural names across this range.
The 398 uncertain native unit-name forms remain held.
