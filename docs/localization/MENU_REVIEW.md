# Additional menu review

Six test/debug controls were restored after tracing player-visible menu paths.
Nineteen routing stubs/sentinels and one ambiguous guardianship option remain
held, in addition to the 126 shared-ID conflicts in `menu-id-review.json`.

The cost label `mno_choice_28_1nor` says `50,00` in compiled English, but its
condition and `troop_remove_gold` both use 50000. Chinese therefore says 50,000
denarii. Save-recovery instructions restore the actual filename
`last_savegame_backup.sav`; automatic underscore decoding otherwise produces an
unusable filename. English source and operations were not changed.

