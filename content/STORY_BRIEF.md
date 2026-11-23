# Story authoring brief (graded reader)

You write ORIGINAL French stories for a native English speaker learning French through extensive reading (Krashen's i+1: ~95-98% of the words should be understandable; the rest inferable from context). Each story you write is one JSON file plus one lexicon sidecar file. A validator tells you exactly what is missing, so you iterate until it says `-> clean`.

## 1. What to write

Authentic, natural French (not translated English), correct accents and typography (« », œ, ç, é...). Strong hook, real characters, a small conflict, a satisfying ending, vivid concrete detail. Vary settings and tone. Nothing offensive, political, sexual, violent in a disturbing way, or sensitive. Dialogue where it suits. Plain straight apostrophes (') only, no digits (write numbers in words), no emoji.

| Level | Words | Grammar | Sentences |
|---|---|---|---|
| A1 | 170-250 | present tense only (plus imperative of simple requests), ~500 highest-frequency words, simple connectors (et, mais, alors, puis, parce que) | 4-9 words, never more than 10 |
| A2 | 280-400 | adds passé composé, imparfait, futur proche, reflexives, comparatives, object pronouns; up to ~12 words per sentence (max 14) | up to 14 |
| B1 | 450-700 | adds futur simple, conditionnel, plus-que-parfait, basic subjonctif, relative pronouns (qui, que, où, dont), clear idioms | up to 24 |
| B2 | 750-1000 | full tense range, passive, nuanced connectors, abstract topics, reported speech | up to 34 |
| C1 | 1000-1300 | idiomatic and literary register, complex syntax, passé simple allowed in narration, cultural references | up to 60 |

Pedagogy: repeat the key vocabulary 3-5 times naturally (the validator warns under 3); only a few new words per paragraph, inferable from context; a paragraph is 3-6 sentences (A1) up to ~8 (C1). B2/C1 may use 2-3 chapters with short titles; lower levels use one chapter with an empty title.

## 2. The story file: `content/raw/<id>.json`

Copy the shape of `content/raw/parapluie-jaune.json` (and `lea-1.json`). Fields: `id` (kebab-case, equals file name), `series_id` (null or a series id), `episode` (null or a number), `title`, `title_en`, `level`, `summary_en` (1-2 sentences, no spoilers of the ending), `tags` (2-4 lowercase words), `key_vocab` (10-15 LEMMAS that really occur 3+ times), `source` ("original"), `license` ("CC0"), `chapters` -> `[{"title": "", "paragraphs": [{"sentences": [{"fr": "...", "en": "..."}]}]}]`.

- One sentence object per sentence (a quoted line with its « » and a following « dit-elle » tag stays ONE sentence). `en` is a natural but close English translation (readers study from it).
- Do not add `pic`/`cover` fields; pictures are added later by someone else.
- Per-occurrence overrides: when a form is used in an unusual sense or is a different word than your F line says, add `"ov": {"<token index>": {...}}` to that sentence. Token index = 0-based position among the sentence's word tokens (punctuation is not a token; expressions listed as P lines count as ONE token). Keys: `"g"` gloss for this occurrence, `"m"` form note, `"p"` POS, `"l"` a different lemma (that lemma needs an L line). The validator prints the token index in its error messages.

## 3. The lexicon sidecar: `content/lexicon/stories/<id>.lex`

Every word token must resolve to a lemma with a gloss. The shared lexicon (`content/lexicon/lemmas.txt`, `forms.txt`, `phrases.txt`) already covers some words; your sidecar covers everything else and wins over the shared files for this story. Read the shared files once to copy their conventions. Lines starting with `#` are comments. Fields separated by `|`.

```
L|lemma|POS|English gloss|gender|article-override
F|surface form|lemma|POS|form note
P|word word word|lemma|POS|form note
```

- **L (lemma)**: dictionary form (verbs = infinitive, reflexives as `se laver`; nouns = singular; adjectives = masculine singular). POS is one of NOUN VERB ADJ ADV PRON DET PREP CONJ NUM INTJ EXPR PROPN. Gloss = short, concrete English for the sense used in your story (verbs start with "to "). Nouns REQUIRE gender `m` or `f` (the app shows le/la/l' itself; only set the article column for an aspirated h, e.g. `la`). Names of people and places are PROPN (no gloss translation needed beyond e.g. "Léa (a girl's name)").
- **F (form)**: one line per surface form as it appears, lowercase, normalised. `form` is the lowercase token. Elisions are split off as their own token with the apostrophe attached: `l'`, `d'`, `j'`, `s'`, `n'`, `qu'`, `c'`, `m'`, `t'`, `jusqu'` (so `l'arbre` = tokens `l'` + `arbre`; map `l'` to `le` DET, `d'` to `de` PREP, `j'` to `je` PRON, `s'` to `se` PRON, `n'` to `ne` ADV, `qu'` to `que` CONJ, `c'` to `ce` PRON). `aujourd'hui` is one token. Hyphenated words are ONE token (`dit-elle`, `peut-être`, `est-ce`, `là-bas`, `grand-mère`, `c'est-à-dire` splits as `c'` + `est-à-dire`). Contractions: `du` -> `de` PREP note `de + le`; `au` -> `à` PREP note `à + le`; `des`/`aux` similarly.
- **P (phrase)**: a multi-word expression merged into one tappable token (`il y a`, `tout de suite`, `à côté de`, `avoir faim` forms like `a faim`). Use for idioms and fixed expressions whose meaning is not the sum of the words.
- **Form notes** (4th/5th field) use this vocabulary so the difficulty scorer can read tenses: `present (je)`, `present (il/elle)`, `present (nous)`..., `imparfait (il/elle)`, `past participle`, `futur simple (il/elle)`, `conditionnel (je)`, `subjonctif present (qu'il)`, `passé simple (il/elle)`, `imperative (tu)`, `infinitive`, `present participle`, `feminine`, `plural`, `feminine plural`, `before a vowel`, `de + le`. Auxiliary forms in compound tenses: note them like `present (il/elle), auxiliary`. Leave the note empty for invariable words.
- One surface form maps to ONE reading in F. If another reading occurs in the same story (e.g. `porte` as a verb and as a noun), pick the commoner reading in F and use an `ov` with `"l"` for the other.

## 4. Check loop (do this until clean)

From the repo root `/home/claude/french-reader`:

```
python3 -I tools/build.py --check content/raw/<id>.json
```

It prints MISSING lines (forms or lemmas not yet defined, each with the first sentence where it occurs), errors, warnings and stats (word count, sentence lengths, tense share, provisional score). Add the missing lines to your `.lex` and re-run. Treat warnings seriously: word count outside the level range, sentences over the level's limit, key vocab met fewer than 3 times. The provisional score "reads_as" is only a rough guide; ignore it unless it is two levels off. Do NOT run `python3 tools/build.py` without `--check` (it rewrites `docs/`), and do not edit any file other than your own story files.

## 5. Finish

Your final message: for each story one line with `id`, level, word count, and anything you could not resolve. Be honest about doubts (e.g. an uncertain gloss or an unnatural phrase you were unsure of).
