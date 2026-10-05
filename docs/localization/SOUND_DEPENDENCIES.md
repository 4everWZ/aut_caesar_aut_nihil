# Three unresolved sound dependencies at the pinned source

This trace uses Git objects from **3ed34f35c94c974f9d2a9102750dbb4866e38f6d**, not moving upstream branches. The three missing files cannot safely be classified as harmless optional audio or proven launch blockers. Their sound definitions are exported globally; their visible consumers are gameplay events and character voices. Engine preload, fallback and missing-file error handling are not implemented in this repository and were not exercised.

## Exact tree and available history

`git ls-tree -r --name-only 3ed34f35c94c974f9d2a9102750dbb4866e38f6d` has no path ending in `woman_death_12.wav`, `disease_sound.wav` or `riot_sound.wav`, including case-insensitive comparisons across the whole tree. Neighboring female clips 3–11 and 13–15 are present. This establishes an upstream-tree omission, independent of ZIP creation or checkout transfer.

The local repository is not shallow. At inspection it exposed 1,015 reachable commits through `localization/zh-cn` and `work`, with no other refs. `git log --all --` on each exact Sound path returned no commits; `git rev-list --objects --all` contained no recorded path with any of the three basenames. This is evidence about available reachable history, not all deleted/unfetched upstream branches or renamed unknown audio blobs.

`git log -S` traces disease and riot filename references to [initial commit 3f246f00d43ee178ab701660203fb2d4c931decc](https://github.com/buttersnew/aut_caesar_aut_nihil/commit/3f246f00d43ee178ab701660203fb2d4c931decc). The female filename reference was introduced in [3924e480362605d8570f41a118c123294ab0306b](https://github.com/buttersnew/aut_caesar_aut_nihil/commit/3924e480362605d8570f41a118c123294ab0306b), titled “new fembot dead sounds”; the missing file is absent from that commit's tree too. No recoverable exact-path file was found. Local archives found under `/workspace` are this task's localization/candidate packages, not an independent upstream installation or recovery source; their existence does not supply missing originals.

## Definitions, flags and compiled references

[Source definitions](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/module_sounds.py#L122) declare `woman_die` with priority 10 and volume 9, containing thirteen clips including missing `woman_death_12.wav`. Disease and riot are each single-file groups, declared at [lines 242–243](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/module_sounds.py#L242) with priority 9, volume 5 and `sf_stream_from_hd`.

The [flag definitions](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/header_sounds.py#L10) yield combined numeric flags 2464 (`0x9a0`) for female death and 1432 (`0x598`) for disease/riot. Female death does **not** set the streaming flag. Streaming does not prove that file existence is checked only when played.

The pinned compiled `sounds.txt` contains the missing filenames at lines 208, 589 and 590, with zero-based file indices 205, 586 and 587 respectively. Sound-group rows at lines 764, 880 and 881 reference those indices. Thus these are genuine compiled dependencies, not stale source-only names. See [compiled sound table](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/Aut_Caesar_Aut_Nihil/sounds.txt#L764).

The [WRECK sound aggregator](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/compiler.py#L1273) enumerates filenames and writes flags/indices; it does not open or validate WAV contents. Successful module compilation therefore cannot establish audio availability.

## All literal sound-ID consumers in pinned Python source

A pinned `git grep` for `snd_(woman_die|disease_sound|riot_sound)` finds the following active consumers, plus generated ID assignments. This is a literal-reference inventory, not proof against indirect numeric/dynamic use.

| Sound | Consumer | Pinned file and line |
|---|---|---|
| riot | Siege notification | `module_game_menus.py:22709`, `notification_center_under_siege` |
| riot | Completed village raid notification | `module_game_menus.py:22731`, `notification_village_raided` |
| riot | Village raid starting | `module_game_menus.py:22753`, `notification_village_raid_started` |
| riot | Rebel village raid starting | `module_game_menus.py:22774`, `notification_village_raid_started_rebells` |
| riot | Kingdom restoration | `module_game_menus.py:22814`, `notification_kingdom_restored` |
| riot | Kingdom liberation | `module_game_menus.py:22835`, `notification_kingdom_liberated` |
| disease | Siege sickness casualties/recovery | `module_game_menus.py:28176`, `enfermedad2_siege` |
| disease | Village sickness court petition | `module_game_menus.py:43331`, `event_11_juicio` |
| disease | Frontier famine following livestock disease | `module_game_menus.py:54419`, `minor_faction_event_5` |
| disease | Epidemic notification | `module_game_menus.py:60815`, `epidemic_outbreak` |
| woman_die | Antonia death dialogue consequence | `module_dialogs.py:17384`, `final_side_poppaea_13` |
| woman_die | `woman` skin death-voice mapping | `module_skins.py:328` |
| woman_die | `girl` skin death-voice mapping | `module_skins.py:391` |

Pinned source links: [riot menu block](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/module_game_menus.py#L22709), [siege sickness](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/module_game_menus.py#L28176), [court petition](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/module_game_menus.py#L43331), [frontier event](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/module_game_menus.py#L54419), [epidemic](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/module_game_menus.py#L60815), [dialogue](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/module_dialogs.py#L17384), [skin voice mappings](https://github.com/buttersnew/aut_caesar_aut_nihil/blob/3ed34f35c94c974f9d2a9102750dbb4866e38f6d/module_system/module_skins.py#L328).

## Packaging conclusion

Disease and riot are played from event menus; female death also has engine-triggered skin voice mappings. None of that proves launch is unaffected: all three filenames are registered in the global compiled sound table. Neither “optional warning only” nor “will prevent launch” is supported by this source inspection. Keep the full-module package explicitly **incomplete and unverified**, with these exact dependencies disclosed. Establishing severity requires a compatible lawful Warband installation and observed startup/event/voice tests, or authentic compatible files plus provenance. Do not omit sound definitions, rename neighboring clips, synthesize placeholders or treat unrelated commercial-mod files as verified Native fallbacks.

## Official release archive inspected by byte ranges

The publisher's [v1.0.1.13 asset listing](https://github.com/buttersnew/aut_caesar_aut_nihil/releases/expanded_assets/v1.0.1.13) identifies
`ACAN-v1.0.1.13.zip`. Its entire ZIP central directory was read from the official
download using HTTPS byte ranges on 2026-10-05: **4,196 members**, archive length
**1,255,687,732 bytes**. Searching every member basename case-insensitively finds
none of the three missing WAVs. Thus a differently cased filename or nested path
in this official archive does not supply them. No other local recovery archive
was discovered.

Only the directory and `module.ini` / `sounds.txt` members were fetched (519,604
range bytes total); those two members passed ZIP CRC verification. The full
archive was not downloaded or locally SHA-256-verified. The publisher's declared
SHA-256 and retrieved member hashes are recorded in
[official-release-audio-check.json](official-release-audio-check.json).

The release commit is `aa1279d73d39c066ac34e361bfb458bf270d17ac`, an ancestor of
the pinned July 25 revision; it is **not** an exact-revision replacement. Its
compiled sound table still references all three files with the same flags and
indices. The absence therefore predates this localization and is not caused by
the candidate packager. No assets from a different mod were substituted.

## Native evidence and runtime severity

The publisher's official Native module-system SDK endpoints could not be retrieved
from this environment (HTTP 403); no authenticated Native file inventory was
available. None of the three exact names is established here as game-provided.
The [WSE2 developer changelog](https://github.com/Ruslan-700/WSE2-Releases/blob/master/CHANGELOG.MD#1016)
documents changes to streaming-sound support; it provides no missing-file failure
contract. Therefore version-specific runtime behavior remains unknown.

There is no optional-missing-file flag in these definitions. Event-scoped play
calls alone do not prove the engine delays loading all sound files until an event
runs, especially for the non-streamed female voice group. The strongest supported
classification is **active audio dependencies absent from the mod distribution,
with unverified Native fallback and unverified failure severity**.

## Actionable installed-game check

On the user's own lawful, matching Warband installation, check for the exact
filenames in the game's `Sounds` directory, `Modules/Native/Sounds`, and the
installed ACAN module's `Sounds`. Record full path, game/WSE2 version, size and
SHA-256 if found. Presence in another commercial module does not authorize copying
or redistribution. These files need not be uploaded: a file-presence/hash report
or maintainer confirmation of supported fallback locations is useful first.

Test a separate copy: capture startup/loading messages, then test the siege/raid
and epidemic notifications and the female voice group. Because the female group
selects among thirteen variants, one successful voice playback does not cover
the missing variant. Record warnings, silence, crashes or successful fallback as
observations, not assumptions. Do not change sound IDs or replace neighboring
clips merely to make the check pass.
