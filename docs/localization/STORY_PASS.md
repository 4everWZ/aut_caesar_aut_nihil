# Narrative expansion and review

The initial interface/menu/troop milestone was followed by inventory-wide
translation batches for dialogue, script messages, descriptions, world names,
items, troops and generated personal names. Current counts are in README.md and
coverage.json; they measure candidate IDs, not words or proven gameplay reachability.

## Review performed

Independent batches received shared terminology review and selected source/context
checks. Corrections included a reversed insult, an incorrectly negative rendering
of “iron-hearted,” an imperial army officer misidentified as a court official,
“second child” incorrectly narrowed to “second son,” and kinship wording that
assumed the shared spouse's sex without support in the relationship graph. Menu
costs and the recovery filename were checked against operations/source. Numeric
samples and all formatting signatures were checked. This is not an exhaustive
bilingual review of every sentence.

Unusual fictional geography, inconsistent names and relationship descriptions are
preserved where the source itself is inconsistent. Historical correction is
outside this localization. Source mistakes are not repaired in English or gameplay.
Gender alternatives retain their existing order and nesting; Chinese translations
do not create new branch logic.

## Explicit holds

The continuation ledger records untranslated candidate IDs and reasons. It includes
uncertain native unit terms, meaningful source ambiguities, incompatible shared
menu IDs, resource/code tokens and internal sentinels. Old Norse prayer passages
remain unchanged because their incomprehensibility is part of the dialogue.
Three age-sensitive sexual passages are also withheld; the ledger gives IDs and
neutral context without reproducing those passages. Nonsexual surrounding narrative
is translated. This category is not a request to approve explicit translation.

DECISIONS.md and pending-meaning-decisions.json contain proposed readings for
source ambiguities. No unanswered interpretation has been treated as approved.

## Runtime limits

ID conventions are supported by reference localization and source evidence, but
an engine-generated export from this exact ACAN build has not been compared.
The bundled font lacks Chinese glyphs. Warband/WSE2 was unavailable, so font
fallback, wrapping, substitutions, quest progress and saved names still require
in-game QA. No claim of verified playability or complete localization is made.
