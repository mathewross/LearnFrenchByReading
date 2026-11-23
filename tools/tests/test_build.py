"""Unit tests for the content build: tokenising, phrase merging, tap-to-lemma data, validation.
Run: python3 -m unittest discover -s tools/tests   (from the repo root)"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build  # noqa: E402


def story(sentences, level="A1", key_vocab=None):
    return {
        "id": "t", "title": "T", "title_en": "T", "level": level, "summary_en": "s", "tags": [],
        "key_vocab": key_vocab or [], "source": "original", "license": "CC0",
        "chapters": [{"title": "", "paragraphs": [{"sentences": sentences}]}],
    }


class TokenizeTests(unittest.TestCase):
    def test_elision_splits_off_the_clitic(self):
        toks = build.tokenize("Le train s'arrête.")
        self.assertEqual([t[2] for t in toks], ["le", "train", "s'", "arrête"])

    def test_spans_index_the_original_text(self):
        text = "Un homme dit : « Bonjour ! »"
        for s, e, norm in build.tokenize(text):
            self.assertEqual(build.norm(text[s:e]), norm)

    def test_hyphenated_inversion_is_one_token(self):
        self.assertIn("dit-elle", [t[2] for t in build.tokenize("« Là-bas ! » dit-elle.")])

    def test_curly_apostrophe_is_normalised(self):
        self.assertEqual([t[2] for t in build.tokenize("l’arrêt")], ["l'", "arrêt"])


class PhraseTests(unittest.TestCase):
    def setUp(self):
        self.forms, self.phrases, self.lemmas = build.load_lexicon()

    def test_longest_phrase_wins_and_spans_all_words(self):
        text = "Il y a beaucoup de monde."
        merged = build.merge_phrases(build.tokenize(text), self.phrases)
        keys = [m["key"] for m in merged]
        self.assertEqual(keys, ["il y a", "beaucoup de", "monde"])
        self.assertEqual(text[merged[0]["s"]:merged[0]["e"]], "Il y a")

    def test_tap_on_any_word_of_a_phrase_resolves_to_one_lemma(self):
        errors = []
        res = build.enrich_story(story([{"fr": "Léa a faim.", "en": "Léa is hungry."}]), self.forms, self.phrases, self.lemmas, errors)
        self.assertEqual(errors, [])
        tokens = res[0]["chapters"][0]["paragraphs"][0][0]["tk"]
        self.assertEqual([t["l"] for t in tokens], ["Léa", "avoir faim"])


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.forms, self.phrases, self.lemmas = build.load_lexicon()

    def run_story(self, raw):
        errors = []
        res = build.enrich_story(raw, self.forms, self.phrases, self.lemmas, errors)
        return res, errors

    def test_unknown_word_fails_the_build(self):
        _, errors = self.run_story(story([{"fr": "Le train zorglubé.", "en": "x"}]))
        self.assertTrue(any("zorglubé" in e for e in errors))

    def test_lemma_without_gloss_fails(self):
        forms = dict(self.forms, zzz={"l": "zzzlemma", "p": "NOUN", "m": ""})
        errors = []
        build.enrich_story(story([{"fr": "Le zzz.", "en": "x"}]), forms, self.phrases, self.lemmas, errors)
        self.assertTrue(any("no gloss" in e for e in errors))

    def test_key_vocab_must_occur_in_story(self):
        _, errors = self.run_story(story([{"fr": "Le train.", "en": "The train."}], key_vocab=["gare"]))
        self.assertTrue(any("key_vocab" in e for e in errors))

    def test_missing_translation_fails(self):
        _, errors = self.run_story(story([{"fr": "Le train.", "en": ""}]))
        self.assertTrue(any("fr and en" in e for e in errors))

    def test_override_replaces_the_gloss_for_one_occurrence_only(self):
        raw = story([{"fr": "Il y a beaucoup de monde.", "en": "x", "ov": {"2": {"g": "a crowd"}}}])
        res, errors = self.run_story(raw)
        self.assertEqual(errors, [])
        tk = res[0]["chapters"][0]["paragraphs"][0][0]["tk"]
        self.assertEqual(tk[2]["g"], "a crowd")
        self.assertNotIn("g", tk[0])

    def test_bad_override_index_fails(self):
        _, errors = self.run_story(story([{"fr": "Le train.", "en": "x", "ov": {"9": {"g": "y"}}}]))
        self.assertTrue(any("out of range" in e for e in errors))


class ArticleTests(unittest.TestCase):
    def test_gender_article_and_elision(self):
        self.assertEqual(build.noun_article("gare", {"p": "NOUN", "gender": "f"}), "la")
        self.assertEqual(build.noun_article("train", {"p": "NOUN", "gender": "m"}), "le")
        self.assertEqual(build.noun_article("arbre", {"p": "NOUN", "gender": "m"}), "l'")
        self.assertIsNone(build.noun_article("petit", {"p": "ADJ", "gender": None}))


class LibraryTests(unittest.TestCase):
    def test_every_shipped_story_is_consistent(self):
        import json
        out = Path(__file__).resolve().parent.parent.parent / "docs" / "data"
        lib = json.loads((out / "library.json").read_text(encoding="utf-8"))
        self.assertTrue(lib["stories"])
        for e in lib["stories"]:
            st = json.loads((out / "stories" / f"{e['id']}.json").read_text(encoding="utf-8"))
            for ch in st["chapters"]:
                for para in ch["paragraphs"]:
                    for s in para:
                        for t in s["tk"]:
                            self.assertIn(t["l"], st["lemmas"])
                            self.assertTrue(0 <= t["s"] < t["e"] <= len(s["fr"]))
            for i in e["lx"]:
                self.assertIn(lib["lemmas"][i], st["lemmas"])


if __name__ == "__main__":
    unittest.main()
