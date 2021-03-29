# coding=utf-8
import unittest

from src.utils_suggester import (
    suggest_phrase_query_full_example,
    FR_ANALYZER,
    STD_ANALYZER,
    TRI_GRAM_ANALYZER,
)


class UTests(unittest.TestCase):
    def test_suggest_phrase_query_one_word(self):
        expected = {
            "text": {
                "Bactér": [],
                "Bactéri": ["bactéries"],
                "Bactérie": ["bactéries"],
                "bactérie": ["bactéries"],  # case insensitive
                "bacterie": ["bactéries"],  # accent insensitive
                # => does what we want : lowercase suggestions with accents
            },
            "keyword": {
                "Bactér": [],
                "Bactéri": ["Bactéries"],
                "Bactérie": ["Bactéries"],
                "bactérie": [],  # case sensitive
                "bacterie": [],
                "Bacterie": ["Bactéries"],  # accent insensitive
                # does not what we want (unless we lowercase tags before insertion in ES)
            },
            "completion": {
                "Bactér": [],
                "Bactéri": ["bactéries"],  # case insensitive
                "Bactérie": ["bactéries"],
                "bactérie": ["bactéries"],
                "bacterie": ["bactéries"],  # accent insensitive
                "Bacterie": ["bactéries"],
                # does what we want
            },
        }

        doc = {"tags": ["Bactéries"]}
        for type_ in expected:
            mapping = {"tags": {"type": type_}}
            for text_ in expected[type_]:
                suggestions = suggest_phrase_query_full_example(mapping, doc, text_)
                self.assertEqual(suggestions, expected[type_][text_])

    def test_suggest_phrase_query_multiple_words(self):
        expected = {
            "text": {
                "Appare": ["appareil"],
                "Appareil g": [],
                "Appareil géni": [],
            },
            "keyword": {
                "Appare": [],
                "Appareil g": [],
                "Appareil géni": [],
            },
            "completion": {
                "Appare": [],
                "Appareil g": [],
                "Appareil géni": [],
            },
        }

        doc = {"tags": ["Appareil génital féminin"]}
        for type_ in expected:
            mapping = {"tags": {"type": type_}}
            for text_ in expected[type_]:
                suggestions = suggest_phrase_query_full_example(mapping, doc, text_)
                self.assertEqual(suggestions, expected[type_][text_])

    def test_suggest_phrase_query_multiple_words_trigram_analyzer(self):
        expected = {
            "text": {
                "noble prize": ["nobel prize"],
                "nobel priz": ["nobel prize"],
                "nobel pri": [],
                # "Appare": ["appareil"],
                # "Appareil g": [],
                #     "Appareil géni": [],
                # },
                # "keyword": {
                #     "Appare": [],
                #     "Appareil g": [],
                #     "Appareil géni": [],
                # },
                # "completion": {
                #     "Appare": [],
                #     "Appareil g": [],
                #     "Appareil géni": [],
            },
        }

        # doc = {"tags": ["Appareil génital féminin"]}
        doc = {"tags": ["nobel prize"]}
        for type_ in expected:
            mapping = {"tags": {"type": type_}}
            for text_ in expected[type_]:
                suggestions = suggest_phrase_query_full_example(
                    mapping, doc, text_, analyzer=TRI_GRAM_ANALYZER
                )
                self.assertEqual(suggestions, expected[type_][text_])


if __name__ == "__main__":
    pass
