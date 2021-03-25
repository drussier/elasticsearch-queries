# coding=utf-8
import unittest

from src.utils_suggester import suggest_query_full_example


class UTests(unittest.TestCase):
    def test_suggest_query_one_word(self):
        expected = {
            "text": {
                #  max_edits
                # The maximum edit distance candidate suggestions can have in order to be considered as a suggestion.
                # Can only be a value between 1 and 2. Any other value results in a bad request error being thrown. Defaults to 2.
                "Bactér": [],
                "Bactéri": ["bactéries"],
                "Bactérie": ["bactéries"],
                "bactérie": ["bactéries"],  # case insensitive
                "bacterie": ["bactéries"],  # accent insensitive
            },
            "keyword": {
                "Bactér": [],
                "Bactéri": ["Bactéries"],
                "Bactérie": ["Bactéries"],
                "bactérie": [],  # case sensitive
                "bacterie": [],
                "Bacterie": ["Bactéries"],  # accent insensitive
            },
        }

        doc = {"tags": ["Bactéries"]}
        for type_ in expected:  # ["text", "keyword"]:
            mapping = {"tags": {"type": type_}}
            for text_ in expected[type_]:  # ["Bactéri"]:
                suggestions = suggest_query_full_example(mapping, doc, text_)
                # print(suggestions)
                self.assertEqual(suggestions, expected[type_][text_])

    def test_suggest_query_one_word_analyzer(self):
        analyzer = {
            "filter": {
                "french_elision": {
                    "type": "elision",
                    "articles_case": "true",
                    "articles": [
                        "l",
                        "m",
                        "t",
                        "qu",
                        "n",
                        "s",
                        "j",
                        "d",
                        "c",
                        "jusqu",
                        "quoiqu",
                        "lorsqu",
                        "puisqu",
                    ],
                },
                "french_stop": {"type": "stop", "stopwords": "_french_"},
                "french_stemmer": {"type": "stemmer", "language": "french"},
            },
            "analyzer": {
                "default": {
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"],
                    "filter": [
                        "french_elision",
                        "lowercase",
                        "french_stop",
                        "french_stemmer",
                    ],
                }
            },
        }

        expected = {
            "text": {
                "bacter": ["bacter"],
                "Bacter": ["bacter"],
                "Bactér": [],
                "Bactéri": [],
                "Bactérie": [],
            },
            "keyword": {
                "bacter": [],
                "Bacter": [],
                "Bactér": [],
                "Bactéri": [],
                "Bactérie": [],
                "Bactéries": [],
            },
        }

        doc = {"tags": ["Bactéries"]}

        for type_ in expected:
            mapping = {"tags": {"type": type_}}
            for text_ in expected[type_]:
                suggestions = suggest_query_full_example(
                    mapping, doc, text_, analyzer=analyzer
                )
                # print(suggestions)
                self.assertEqual(suggestions, expected[type_][text_])


if __name__ == "__main__":
    pass
