# Full-module packaging outcome

This pass packages the tracked runtime tree, not just the translation overlay.
It is an **incomplete full-tree review candidate**, not a complete playable release.
A lawful Warband installation remains required. No game executable or Native
CommonRes resources are redistributed.

## Exact blocking inputs

The compiled sound table references three files absent from this checkout:

- `Sounds/woman_death_12.wav`
- `Sounds/disease_sound.wav`
- `Sounds/riot_sound.wav`

Obtain the authentic compatible files with redistribution provenance, or maintainer
confirmation of exact installed-game fallback locations and versions. No silent
substitutes, synthesized sounds, removed play calls or invented engine behavior
were used. Public upstream checks did not recover these files. See
[ASSET_AUDIT.md](ASSET_AUDIT.md) and [asset_audit.json](asset_audit.json).

The 21 texture casing discrepancies, engine-resource dependencies, source stray
INI line and platform skeleton behavior remain documented runtime/portability
questions. They do not justify changing game logic during localization.

## Package layout and deliberate differences

The ZIP root contains `Modules/Aut_Caesar_Aut_Nihil/module.ini` and the module's
Resource, Textures, SceneObj, Sounds, Music, Data, shader and compiled text files.
The `cns` translations are under that module's `languages` directory.

The build omits only `fxc.exe` and its compiler launcher `compile_fx.bat`, which
are build tools, not game runtime dependencies. Microsoft compiler redistribution
terms were not supplied in this repository. Full upstream README/credits and
MIT LICENSE are included inside the module. Third-party evidence and qualifications
are preserved in [REDISTRIBUTION.md](REDISTRIBUTION.md).

The package substitutes two font files with a generated OFL Chinese font candidate.
The repository's original module font and all compiled gameplay files remain
unchanged. The font's OFL notice is bundled; see FONT_CANDIDATE.md for generation,
coverage, static preview and untested engine behavior. This is a packaging-only
font substitution, not a proven font compatibility fix.

## Controlled installation test

Do not overwrite a working installation. Back up the existing module, extract
this ZIP's `Modules/Aut_Caesar_Aut_Nihil` into Warband's Modules folder, and select
Simplified Chinese and ACAN in the launcher. Read START_HERE before testing.
Missing audio may cause load or runtime problems; resolve it before claiming the
module is complete. Test fonts, wrapping, substitutions, scene loads, audio events,
quests and saves on the intended Warband/WSE2 platform. In-game QA is unavailable
in this cloud environment. Uninstall by restoring the backed-up module.

## Reproduction and publication handoff

From a clean reviewed commit:

```sh
python3 tools/localization/audit_module.py
# If the refreshed report changes, review and commit it first.
python3 tools/localization/package_module.py --output /tmp/acan-zh-cn-module.zip
```

The default build rejects known missing dependencies. For an explicitly incomplete
review artifact only, add `--allow-incomplete-review`. Its metadata and opening
notice state the unresolved files. Every ZIP member is hash-verified after creation,
and module.ini layout and compiler exclusion are checked. No symlinks or untracked
font inputs are accepted. The focused follow-up patch is against `e27651b`.

No GitHub authentication retries or credential changes are part of this work.
A publisher with authorized tools can inspect these artifacts; do not describe
this candidate as complete, and use a prerelease if publishing an untested build.

## Library delivery packs

For reliable transfer, the large candidate may be delivered as multiple ordinary
ZIP packs, each containing a different subset of the same module tree. Download
**every** numbered pack and extract them all into the same empty folder. Do not
concatenate ZIPs. PACKSET.json records each pack's SHA-256 and the full local ZIP's
SHA-256; READ_ALL_PACKS.txt repeats the required pack list. The split operation
verifies every member against the already verified full ZIP. A pack by itself is
not an installable module. The missing sounds remain missing after all packs are
combined; splitting does not resolve that known source dependency gap.

## Follow-up evidence (existing archive preserved)

[SOUND_DEPENDENCIES.md](SOUND_DEPENDENCIES.md) now traces exact pinned Git objects,
reachable history and the official release ZIP directory. The three sounds are
absent from upstream distribution; warning-only versus launch-fatal behavior is
not established. [BUNDLE_INVENTORY.md](BUNDLE_INVENTORY.md) describes the separate
per-member JSON source/license inventory covering every member of the existing
1.26 GB ZIP. These follow-up reports do not silently rebuild that archive.
