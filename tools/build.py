#!/usr/bin/env python3
"""Content build: content/raw/*.json + content/lexicon/* -> docs/data/*.

Every story file is self-contained: sentences, translations, per-token lemma/morph,
and a per-story glossary. Fails (exit 1) on any missing lemma/gloss or schema problem.
Offline only: no spaCy/Wiktionary needed for M1 (lemmas come from the curated lexicon).
"""
import gzip
import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "content" / "raw"
LEX = ROOT / "content" / "lexicon"
DOCS = ROOT / "docs"
OUT = DOCS / "data"

LEVELS = ["A1", "A2", "B1", "B2", "C1"]
WORD_RANGE = {"A1": (150, 250), "A2": (250, 400), "B1": (400, 700), "B2": (700, 1100), "C1": (1000, 1600)}
SKIP_EX_POS = {"DET", "PREP", "CONJ", "PRON", "NUM", "PROPN"}
VOWEL = set("aeiouyhâàäéèêëîïôöûüœ")

TOKEN_RE = re.compile(
    r"aujourd['’]hui|(?:qu|jusqu|lorsqu|puisqu|[cdjlmnst])['’]|[^\W\d_]+(?:-[^\W\d_]+)*",
    re.I,
)


def norm(s):
    return s.lower().replace("’", "'")


def tokenize(text):
    """Return [(start, end, normalised_text)] for word tokens (punctuation is skipped)."""
    return [(m.start(), m.end(), norm(m.group())) for m in TOKEN_RE.finditer(text)]


def count_words(text):
    return sum(1 for w in text.split() if re.search(r"[^\W\d_]", w))


# ---------------------------------------------------------------- lexicon

def _rows(path):
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if line and not line.startswith("#"):
            yield n, [p.strip() for p in line.split("|")]


def load_lexicon(lex_dir=LEX):
    forms, phrases, lemmas = {}, {}, {}
    for n, p in _rows(lex_dir / "lemmas.txt"):
        if len(p) < 3:
            raise SystemExit(f"lemmas.txt:{n}: need lemma|POS|gloss")
        lemma, pos, gloss = p[0], p[1], p[2]
        gender = p[3] if len(p) > 3 and p[3] else None
        art = p[4] if len(p) > 4 and p[4] else None
        lemmas[lemma] = {"p": pos, "g": gloss, "gender": gender, "art": art}
    for n, p in _rows(lex_dir / "forms.txt"):
        if len(p) < 3:
            raise SystemExit(f"forms.txt:{n}: need form|lemma|POS|note")
        entry = {"l": p[1], "p": p[2], "m": p[3] if len(p) > 3 else ""}
        if p[0] in forms and forms[p[0]] != entry:
            raise SystemExit(f"forms.txt:{n}: conflicting entry for '{p[0]}' (use a per-occurrence override)")
        forms[p[0]] = entry
    for n, p in _rows(lex_dir / "phrases.txt"):
        key = tuple(p[0].split())
        phrases[key] = {"l": p[1], "p": p[2], "m": p[3] if len(p) > 3 else ""}
    return forms, phrases, lemmas


def noun_article(lemma, info):
    """Definite article for display: le/la/l' (derived from gender + first letter)."""
    if info.get("p") != "NOUN" or not info.get("gender"):
        return None
    if info.get("art"):
        return info["art"]
    if lemma[0].lower() in VOWEL:
        return "l'"
    return "le" if info["gender"] == "m" else "la"


# ---------------------------------------------------------------- enrichment

def merge_phrases(toks, phrases):
    """Greedy longest-match merge of multi-word expressions. Returns list of dicts."""
    out, i = [], 0
    maxlen = max((len(k) for k in phrases), default=1)
    while i < len(toks):
        hit = None
        for n in range(min(maxlen, len(toks) - i), 1, -1):
            key = tuple(t[2] for t in toks[i:i + n])
            if key in phrases:
                hit = (n, phrases[key])
                break
        if hit:
            n, entry = hit
            out.append({"s": toks[i][0], "e": toks[i + n - 1][1], "key": " ".join(t[2] for t in toks[i:i + n]), "entry": entry})
            i += n
        else:
            out.append({"s": toks[i][0], "e": toks[i][1], "key": toks[i][2], "entry": None})
            i += 1
    return out


def enrich_story(raw, forms, phrases, lemmas, errors):
    sid = raw.get("id", "?")
    for field in ("id", "title", "title_en", "level", "summary_en", "tags", "key_vocab", "source", "license", "chapters"):
        if field not in raw:
            errors.append(f"{sid}: missing field '{field}'")
    if errors and any(e.startswith(f"{sid}: missing") for e in errors):
        return None
    if raw["level"] not in LEVELS:
        errors.append(f"{sid}: bad level {raw['level']}")
        return None

    story_lemmas, chapters_out = {}, []
    sent_lens, word_len_sum, token_total, tense_sents, sent_total = [], 0, 0, 0, 0
    total_words, lemma_tokens = 0, []
    for ci, ch in enumerate(raw["chapters"]):
        paras_out = []
        for pi, para in enumerate(ch["paragraphs"]):
            sents_out = []
            for si, s in enumerate(para["sentences"]):
                where = f"{sid} ch{ci}.p{pi}.s{si}"
                fr, en = s.get("fr", ""), s.get("en", "")
                if not fr or not en:
                    errors.append(f"{where}: sentence needs fr and en")
                    continue
                merged = merge_phrases(tokenize(fr), phrases)
                ov_all = s.get("ov", {})
                toks, has_tense = [], False
                for ti, m in enumerate(merged):
                    entry = m["entry"] or forms.get(m["key"])
                    if not entry:
                        errors.append(f"{where}: no lexicon form for '{m['key']}' in \"{fr}\"")
                        continue
                    lemma = entry["l"]
                    info = lemmas.get(lemma)
                    ov = ov_all.get(str(ti), {})
                    if not info:
                        errors.append(f"{where}: lemma '{lemma}' (form '{m['key']}') has no gloss in lemmas.txt")
                        continue
                    t = {"s": m["s"], "e": m["e"], "l": lemma}
                    morph = ov.get("m", entry["m"])
                    if morph:
                        t["m"] = morph
                    if "g" in ov:
                        t["g"] = ov["g"]
                    if "p" in ov:
                        t["p"] = ov["p"]
                    toks.append(t)
                    if lemma not in story_lemmas:
                        sl = {"g": info["g"], "p": info["p"]}
                        art = noun_article(lemma, info)
                        if art:
                            sl["a"] = art
                            sl["x"] = info["gender"]
                        story_lemmas[lemma] = sl
                    lemma_tokens.append(lemma)
                    if any(k in morph for k in ("imparfait", "past participle", "futur", "conditionnel", "subjonctif")):
                        has_tense = True
                for ov_key in ov_all:
                    if int(ov_key) >= len(merged):
                        errors.append(f"{where}: override index {ov_key} out of range")
                wl = count_words(fr)
                sent_lens.append(wl)
                total_words += wl
                sent_total += 1
                tense_sents += 1 if has_tense else 0
                word_len_sum += sum(t[1] - t[0] for t in tokenize(fr))
                token_total += len(tokenize(fr))
                sents_out.append({"fr": fr, "en": en, "tk": toks})
            paras_out.append(sents_out)
        chapters_out.append({"title": ch.get("title", ""), "paragraphs": paras_out})

    for kv in raw["key_vocab"]:
        if kv not in story_lemmas:
            errors.append(f"{sid}: key_vocab lemma '{kv}' does not occur in the story")

    msl = statistics.mean(sent_lens) if sent_lens else 0
    mwl = word_len_sum / max(token_total, 1)
    tense_share = tense_sents / max(sent_total, 1)
    difficulty = score_difficulty(msl, mwl, tense_share)
    lo, hi = WORD_RANGE[raw["level"]]
    warnings = []
    if not lo <= total_words <= hi:
        warnings.append(f"{sid}: {total_words} words is outside the {raw['level']} target {lo}-{hi}")
    derived = cefr_from_score(difficulty)
    if derived != raw["level"]:
        warnings.append(f"{sid}: declared {raw['level']} but provisional score {difficulty} reads as {derived}")

    story = {
        "id": raw["id"], "title": raw["title"], "title_en": raw["title_en"], "level": raw["level"],
        "series_id": raw.get("series_id"), "episode": raw.get("episode"),
        "summary_en": raw["summary_en"], "tags": raw["tags"], "source": raw["source"], "license": raw["license"],
        "words": total_words, "difficulty": difficulty,
        "lemmas": story_lemmas, "chapters": chapters_out,
    }
    stats = {"msl": round(msl, 1), "max_sl": max(sent_lens) if sent_lens else 0, "mwl": round(mwl, 2), "tense": round(tense_share, 2)}
    return story, stats, warnings


def score_difficulty(msl, mwl, tense_share):
    """PROVISIONAL 1-100 score from sentence length, word length and tense variety.
    M6 replaces this with frequency-band coverage once a frequency list is wired in."""
    clamp = lambda x: max(0.0, min(1.0, x))
    v = 0.55 * clamp((msl - 3) / 20) + 0.25 * clamp((mwl - 3.4) / 2.6) + 0.20 * clamp(tense_share / 0.6)
    return max(1, round(v * 100))


def cefr_from_score(score):
    for limit, lvl in ((22, "A1"), (42, "A2"), (56, "B1"), (72, "B2")):
        if score < limit:
            return lvl
    return "C1"


# ---------------------------------------------------------------- outputs

def build_examples(stories, per_lemma=5):
    """lemma -> up to N short example sentences (other stories first, lower level first)."""
    cands = {}
    for st in stories:
        for ch in st["chapters"]:
            for para in ch["paragraphs"]:
                for s in para:
                    for lemma in {t["l"] for t in s["tk"]}:
                        if st["lemmas"][lemma]["p"] in SKIP_EX_POS:
                            continue
                        cands.setdefault(lemma, []).append((LEVELS.index(st["level"]), count_words(s["fr"]), st["id"], s["fr"], s["en"]))
    out = {}
    for lemma, items in cands.items():
        seen, picked = set(), []
        for lvl, n, sid, fr, en in sorted(items):
            if fr not in seen:
                seen.add(fr)
                picked.append({"fr": fr, "en": en, "s": sid})
            if len(picked) >= per_lemma:
                break
        if len(picked) > 1:  # a single sentence is just the one the reader is already looking at
            out[lemma] = picked
    return out


def build_library(stories, series, extra):
    lemma_list, lemma_idx = [], {}
    entries = []
    for st in stories:
        lx = []
        for lemma, info in st["lemmas"].items():
            if info["p"] == "PROPN":
                continue
            if lemma not in lemma_idx:
                lemma_idx[lemma] = len(lemma_list)
                lemma_list.append(lemma)
            lx.append(lemma_idx[lemma])
        entries.append({
            "id": st["id"], "title": st["title"], "title_en": st["title_en"], "level": st["level"],
            "difficulty": st["difficulty"], "words": st["words"], "tags": st["tags"],
            "series": st["series_id"], "episode": st["episode"], "summary": st["summary_en"],
            "source": st["source"], "lx": sorted(lx),
        })
    return {"version": 1, "series": series, "lemmas": lemma_list, "stories": entries}


def stamp_service_worker(docs=DOCS):
    """Version the service-worker cache by a hash of every shipped file except sw.js itself."""
    h = hashlib.sha256()
    for p in sorted(docs.rglob("*")):
        if p.is_file() and p.name != "sw.js" and "stories" not in p.parts:
            h.update(p.relative_to(docs).as_posix().encode())
            h.update(p.read_bytes())
    version = h.hexdigest()[:10]
    sw = docs / "sw.js"
    if sw.exists():
        txt = sw.read_text(encoding="utf-8")
        sw.write_text(re.sub(r"const VERSION = '[^']*';", f"const VERSION = '{version}';", txt), encoding="utf-8")
    return version


def main():
    forms, phrases, lemmas = load_lexicon()
    series = json.loads((ROOT / "content" / "series.json").read_text(encoding="utf-8"))
    errors, warnings, stories, rows = [], [], [], []
    for path in sorted(RAW.glob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        res = enrich_story(raw, forms, phrases, lemmas, errors)
        if res:
            story, stats, warn = res
            stories.append(story)
            warnings += warn
            rows.append((story, stats))
    if errors:
        print(f"BUILD FAILED: {len(errors)} problem(s)")
        for e in errors:
            print("  -", e)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "stories").mkdir(exist_ok=True)
    for old in (OUT / "stories").glob("*.json"):
        old.unlink()
    for st in stories:
        (OUT / "stories" / f"{st['id']}.json").write_text(json.dumps(st, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (OUT / "library.json").write_text(json.dumps(build_library(stories, series, None), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (OUT / "examples.json").write_text(json.dumps(build_examples(stories), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    print("\nLibrary ladder (sorted by provisional difficulty):")
    print(f"  {'id':<18}{'level':<6}{'score':<7}{'words':<7}{'avg sent':<10}{'max':<5}{'lemmas'}")
    for st, s in sorted(rows, key=lambda r: r[0]["difficulty"]):
        print(f"  {st['id']:<18}{st['level']:<6}{st['difficulty']:<7}{st['words']:<7}{s['msl']:<10}{s['max_sl']:<5}{len(st['lemmas'])}")
    if warnings:
        print("\nWarnings (non-fatal in M1):")
        for w in warnings:
            print("  -", w)
    version = stamp_service_worker()
    print(f"\nOK: {len(stories)} stories built. Service-worker cache version {version}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
