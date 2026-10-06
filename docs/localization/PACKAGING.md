# Full-module localized installer

The full-module installer preserves upstream runtime commit
`3ed34f35c94c974f9d2a9102750dbb4866e38f6d`. Only the `languages/cns` overlay and
the packaged `Data/font_data.xml` / `Textures/font.dds` pair differ. This is a
full runtime tree with partial Chinese translations, **not in-game tested**.
Untranslated technical IDs and documented English fallback do not block packaging.
No gameplay recompilation, model substitution or sound replacement is performed.

## Build and validation

From a clean committed checkout, install the pinned font dependencies, generate
licensed font assets outside the checkout, then package:

```sh
python3 -m pip install -r tools/localization/font_candidate/requirements.txt
bash tools/localization/prepare_full_font.sh /tmp/acan-full-font
python3 -B tools/localization/package_module.py --font-dir /tmp/acan-full-font \
  --output /tmp/ACAN-zh-cn-full-module.zip
```

Pinned Debian package and outline SHA-256 checks precede font generation. The
builder checks glyph coverage, atlas bounds/overlap and DDS roundtrip. Packaging
checks upstream runtime immutability, current translation/font correspondence,
complete OFL notice, ZIP CRC and every member hash. Tracked input bytes come from
HEAD, not unreviewed working files. Missing BRF/compiled tables and LFS pointer
assets are structural errors. The ZIP contains its own SHA256SUMS and build report.

## Runtime layout and notices

Extract `Modules/Aut_Caesar_Aut_Nihil` into a lawful Warband installation's Modules
directory after backing up the existing module. Select ACAN and Simplified Chinese.
The archive retains module.ini, resources, textures, scenes, sounds, music, data,
compiled gameplay tables and shaders. It excludes `fxc.exe` and `compile_fx.bat`,
and never adds module_system, web libraries, credentials or base-game assets.
Root MIT LICENSE, full upstream README/credits, third-party notice inventory,
full OFL text/copyrights and all localization docs are included. The generated
font is named ACAN Chinese Bitmap Candidate, with no implied author endorsement.

## Preserved upstream limitations

The three sounds `woman_death_12.wav`, `disease_sound.wav`, `riot_sound.wav` are
absent from the pinned upstream tree and the audited official upstream ZIP.
They remain unchanged; packaging proceeds with warnings. Their actual loading
or runtime impact is **unverified**, not asserted harmless or fatal. The existing
texture casing, INI and platform skeleton observations are retained in ASSET_AUDIT.

The 4096-square OFL atlas covers translated text, English fallback and printable
GB2312, but needs game testing for Chinese layout, outline rendering, save loading,
scene/audio events and GPU compatibility. No Windows/WSE2/OpenGL gameplay test
has been performed. Restore the backed-up module to uninstall.

## Independent full-module Actions/tag

`localization-full-module.yml` runs on `zh-cn-full-module-*` tags or manual dispatch.
It tests tooling, validates translations, regenerates pinned licensed fonts, builds
and verifies the full ZIP, and uploads only non-resource verification evidence.
The installer is built locally and in Actions; public full-module resource upload
is held solely for the specific Roman Models conditional-permission answer in
ROMAN_MODELS_PERMISSION.md. No author message has been sent. Existing patch tags
and patch prereleases remain separate and unchanged.
