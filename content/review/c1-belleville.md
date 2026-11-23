# Review: photographe-belleville (C1)

Final check: `python3 -I tools/build.py --check content/raw/photographe-belleville.json` -> clean (1141 words, max sentence 46).

## Fixed
- "Vous avez préparé cette phrase depuis combien de temps ?" -> present "Vous préparez ... depuis combien de temps ?" (depuis + passé composé is wrong for an ongoing action; EN already "have you been preparing"). Lex: préparé -> préparez.
- "s'attablèrent au comptoir" -> "s'installèrent" (s'attabler = sit at a table, odd at a bar counter). Lex updated.
- Lex glosses: confidence (now "a confidence, told in private; not self-confidence"), serré (café serré = short strong espresso), rayon (area of expertise, lit. shop aisle), pouvoir ("to be able to"), Vieux Belleville (restaurant, not "café"), Trenet note softened.
- Removed duplicate line `P|tandis qu'|...` in .lex (only duplicate found).

## Checked, left as is
- "sans qu'il prenne une seule photo": present subjunctive is correct (simultaneous action); "ait pris" would be wrong here. "il" could momentarily read as chacun, but "lui" and the EN make Lucien clear.
- pirouette gloss (dodge/evasive answer) correct. EN translations accurate throughout; no changes needed.
- Piaf: plaque at 72 rue de Belleville claims she was born on the steps; birth record says hôpital Tenon. Text uses "serait née" and "supposedly", so it is safe.
- Trenet: song "Ménilmontant" exists; Lucien "gets the singer, neighbourhood and key wrong" works as a joke (Trenet not Piaf, Ménilmontant not Belleville). Could not verify the exact lyric wording from search snippets, so the lex gloss says "associated with".
- Ronis/Doisneau/Cartier-Bresson, rue Denoyez graffiti, parc de Belleville tai chi and Eiffel view: plausible and accurate.

## Residual doubts
- Vieux Belleville is really on rue des Envierges, but the text puts it on rue de Belleville (minor, fiction).
- "soixante ans de soleil" for a 67-year-old is lyrical hyperbole.
- Lucien switches to "tu" only in chapter 3 (natural as warmth grows).
