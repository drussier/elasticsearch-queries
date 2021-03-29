# coding=utf-8
import unittest

from src.utils_suggester import ACCENT_ANALYZER
from src.utils_suggester_mimacom import suggest_phrase_query_full_example_mimacom


class UTests(unittest.TestCase):
    def test_suggest_phrase_query_multiple_words_mimacom(self):
        expected = {
            "completion": {
                None: {  # fuzziness
                    "appar": ["Appareil génital féminin"],
                    "appareil gén": ["Appareil génital féminin"],
                    "appareil gen": [],  # => problem when no accent in user query
                    "apareil gén": [],
                },
                1: {  # fuzziness
                    "apareil gén": ["Appareil génital féminin"],
                    "appareil gen": [],
                    "apareil gen": [],  # => ajouter analyzer pour ne pas prendre en compte les accents
                    "pareil gén": [],
                    "appareil génita": ["Appareil génital féminin"],
                    "appareil genita": [],
                },
                2: {  # fuzziness
                    "pareil gén": [],
                },
            },
        }

        doc = {"tags": ["Bactéries", "Appareil génital féminin"]}
        for type_ in expected:
            for fuzziness_ in expected[type_]:
                for text_ in expected[type_][fuzziness_]:
                    suggestions = suggest_phrase_query_full_example_mimacom(
                        doc, text_, fuzziness=fuzziness_
                    )
                    self.assertEqual(
                        suggestions, {"suggest-1": expected[type_][fuzziness_][text_]}
                    )

    def test_suggest_phrase_query_multiple_words_mimacom_accent(self):
        expected = {
            "completion": {
                None: {  # fuzziness
                    "appar": {
                        "suggest-1": ["Appareil génital féminin"],
                        "suggest-2": ["Appareil génital féminin"],
                    },  # ["Appareil génital féminin"],
                    "appareil gén": {
                        "suggest-1": ["Appareil génital féminin"],
                        "suggest-2": ["Appareil génital féminin"],
                    },
                    "appareil gen": {
                        "suggest-1": [],
                        # that's what we want : suggestion when no accent in user's query and accent in possible completions list!!
                        "suggest-2": ["Appareil génital féminin"],
                    },
                },
                1: {  # fuzziness
                    "apareil gén": {
                        "suggest-1": ["Appareil génital féminin"],
                        "suggest-2": ["Appareil génital féminin"],
                    },
                    "apareil gen": {
                        "suggest-1": [],
                        "suggest-2": ["Appareil génital féminin"],
                    },
                },
            },
        }

        doc = {"tags": ["Appareil génital féminin"]}
        mapping = {
            "tags": {
                "type": "completion",
                "analyzer": "standard",
                "fields": {"no_accent": {"type": "completion", "analyzer": "folding"}},
            }
        }

        for type_ in expected:
            for fuzziness_ in expected[type_]:
                for text_ in expected[type_][fuzziness_]:
                    body = {
                        "suggest-1": {
                            "prefix": text_,
                            "completion": {"field": "tags"},
                        },
                        "suggest-2": {
                            "prefix": text_,
                            "completion": {"field": "tags.no_accent"},
                        },
                    }

                    suggestions = suggest_phrase_query_full_example_mimacom(
                        doc,
                        text_,
                        body=body,
                        mapping=mapping,
                        fuzziness=fuzziness_,
                        analyzer=ACCENT_ANALYZER,
                    )

                    print(suggestions)
                    self.assertEqual(suggestions, expected[type_][fuzziness_][text_])


if __name__ == "__main__":
    pass
