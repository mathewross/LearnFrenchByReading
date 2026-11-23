# Lecture: a French graded reader (static PWA)

Read short French stories at your level. Tap a word for its meaning in context, long-press for the sentence translation, save words, track progress. No backend, no accounts, no runtime API calls. Everything is precomputed at build time.

**Status: M1 + a working slice of M2–M4.** 27 stories (A1 ×11, A2 ×7, B1 ×4, B2 ×3, C1 ×2), most illustrated, library, paginated reader, word sheet, sentence sheet, read-aloud, settings, backup, offline service worker. Spaced-repetition review, the content validator/scorer with real frequency bands, and the remaining stories are still to do (see Roadmap). Stories were written by AI agents and reviewed by a second pass (notes in `content/review/`); expect the odd unnatural phrase.

## Run locally
```bash
python3 tools/build.py            # content -> docs/data (fails on any missing lemma/gloss)
python3 -m unittest discover -s tools/tests
python3 tools/check_budgets.py    # size budgets
cd docs && python3 -m http.server 8765   # open http://localhost:8765
```
To test on your phone on the same Wi-Fi, open `http://<your-computer-ip>:8765`. The service worker (and so offline/install) only works on `https` or `localhost`, so use the deployed URL for that.

## Deploy (GitHub Pages)
1. Push this repo to GitHub (branch `main`).
2. Repo → Settings → Pages → Source: **GitHub Actions**.
3. The workflow in `.github/workflows/pages.yml` builds, tests, checks budgets and publishes `docs/`. All paths are relative, so it works under `https://<user>.github.io/<repo>/`.

Install on Android: open the URL in Chrome → ⋮ → *Install app* / *Add to Home screen*. Open each story once (or Settings → *Download all stories*) so it works offline.

## How it works
- `content/raw/*.json`: stories as written (French + English per sentence). No lemmas by hand.
- `content/lexicon/`: `lemmas.txt` (gloss, POS, gender), `forms.txt` (surface form → lemma + form note), `phrases.txt` (multi-word expressions merged into one tappable token).
- `tools/build.py` tokenises each sentence, resolves every token through the lexicon, and **fails the build** on any unknown form, missing gloss, missing translation, key-vocab word that isn't in the story, or bad override. It writes self-contained story files, `library.json` (with per-story lemma ids for "you know X%") and `examples.json`.
- Ambiguous words get a per-occurrence override in the story (`"ov": {"<token index>": {"g": "...", "m": "..."}}`).
- Reader: CSS columns for pages, token spans, own tap/long-press/swipe handling. Position is saved as a token index, so it survives font/margin changes and rotation.
- "Known" words: finishing a story marks every word you did not look up as known; looking up or saving a word moves it back to learning. Library "recommended" aims for ~96% known words once you have 20+ known.

## Pictures
Each paragraph can carry a scene: `{"pic": {"id": "lea-1-train", "alt": "English caption"}, "sentences": [...]}`. The image lives at `content/images/<id>.svg`; the build checks it exists and is valid, copies it to `docs/img/`, and the reader shows it above that paragraph with the caption. Add `"cover": "<pic id>"` to a story to choose its library cover. The current scenes are flat vector art drawn in code by `tools/make_images.py` (re-run it after editing). Readers can switch pictures off in the display settings. To use your own artwork instead, drop SVG (or later WebP) files into `content/images/` with the same ids and skip the generator.

## Adding a story (current manual flow)
1. Write `content/raw/<id>.json` (copy an existing one).
2. Run `python3 tools/build.py`. For each "no lexicon form for …" error, add the word to `lemmas.txt` / `forms.txt`.
3. Check the printed ladder, then commit.

## Known limits (honest list)
- Each new story has a per-story lexicon sidecar `content/lexicon/stories/<id>.lex` (formats in `content/STORY_BRIEF.md`); check one with `python3 -I tools/build.py --check content/raw/<id>.json`. Scene modules for pictures live in `tools/scenes/`.
- **Lexicon is hand-curated for 3 stories.** That does not scale to 60. The M6 plan is to generate lemma/POS/morphology with spaCy (`fr_core_news_*`) or simplemma at build time and have an LLM write glosses, with the build checking them. That needs a network-enabled environment to install.
- The difficulty score is **provisional** (sentence length, word length, tense share), not frequency-band based yet. The sample stories are also shorter than the A1/A2 word targets, so the build prints warnings.
- Speech uses your phone's own voices. Quality varies; if none is French, Settings explains how to install one. Word highlighting during read-aloud is not implemented (sentence-level only).
- Tested in headless Chrome at phone size, not on a physical Android device yet.

## Roadmap
M5 examples polish + saved-word SRS review · M6 validator/scorer with frequency bands, first 12 stories · M7 remaining stories, stats polish · M8 Lighthouse pass, chapter list.
