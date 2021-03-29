# coding=utf-8
import unittest

from src.utils_analyzer import analyze_text, ACCENT_ANALYZER

ANALYZERS = {"accent": ACCENT_ANALYZER}


class UTests(unittest.TestCase):
    def test_analyze_text(self):
        expected = {
            "panne de réveil ce matin !": {
                "accent": ["panne", "de", "reveil", "ce", "matin"]
            },
            "<p>panne de réveil ce matin </b>!</p>": {
                "accent": ["panne", "de", "reveil", "ce", "matin"]
            },
        }
        for text_ in expected:
            for analyzer_ in expected[text_]:
                tokens = analyze_text(text_, ANALYZERS[analyzer_])
                self.assertEqual(tokens, expected[text_][analyzer_])


if __name__ == "__main__":
    pass
