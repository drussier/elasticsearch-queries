# coding=utf-8
import unittest

from src.utils_suggester import suggest_query_full_example, FR_ANALYZER, STD_ANALYZER


class UTests(unittest.TestCase):
    def test_suggest_query_one_word(self):
        # type 'text' is analyzed using standard analyzer :
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-analyzer.html
        # standard tokenizer, lower case, stopwords (english by default)
        # case insensitive except for type=keyword
        # accent insensitive
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
        for type_ in expected:  # ["text", "keyword"]:
            mapping = {"tags": {"type": type_}}
            for text_ in expected[type_]:  # ["Bactéri"]:
                suggestions = suggest_query_full_example(mapping, doc, text_)
                # print(suggestions)
                self.assertEqual(suggestions, expected[type_][text_])

    def test_suggest_query_one_word_standard_analyzer(self):

        expected = {
            "text": {
                "bact": [],
                "bacté": [],
                "bacter": [],
                "Bacter": [],
                "Bacteri": [],
                "Bacterie": [],
                "Bactér": [],
                "Bactéri": [],
                "Bactérie": [],
                # does not what we want : we don't want to suggest 'bacter' to the user
            },
            "keyword": {
                "bacter": [],
                "Bacter": [],
                "Bactér": [],
                "Bactéri": [],
                "Bactérie": [],
                "Bactéries": [],
                "Bacteries": [],
                "bacteries": [],
                # does nothing good
            },
            "completion": {
                "bacter": [],
                "Bacter": [],
                "Bactér": [],
                "Bactéri": [],
                "Bactérie": [],
                "Bactéries": [],
                "Bacteries": [],
                "bacteries": [],
                # does nothing good
            },
        }

        doc = {"tags": ["Bactéries"]}

        for type_ in expected:
            mapping = {"tags": {"type": type_}}
            for text_ in expected[type_]:
                suggestions = suggest_query_full_example(
                    mapping, doc, text_, analyzer=STD_ANALYZER
                )
                # print(suggestions)
                self.assertEqual(suggestions, expected[type_][text_])

    def test_suggest_query_one_word_french_analyzer(self):

        expected = {
            "text": {
                "bacter": [],
                "Bacter": [],
                "Bacteri": [],
                "Bacterie": [],
                "Bactér": [],
                "Bactéri": [],
                "Bactérie": [],
                # does not what we want : we don't want to suggest 'bacter' to the user
            },
            "keyword": {
                "bacter": [],
                "Bacter": [],
                "Bactér": [],
                "Bactéri": [],
                "Bactérie": [],
                "Bactéries": [],
                "Bacteries": [],
                "bacteries": [],
                # does nothing good
            },
            "completion": {
                "bacter": [],
                "Bacter": [],
                "Bactér": [],
                "Bactéri": [],
                "Bactérie": [],
                "Bactéries": [],
                "Bacteries": [],
                "bacteries": [],
                # does nothing good
            },
        }

        doc = {"tags": ["Bactéries"]}

        for type_ in expected:
            mapping = {"tags": {"type": type_}}
            for text_ in expected[type_]:
                suggestions = suggest_query_full_example(
                    mapping, doc, text_, analyzer=FR_ANALYZER
                )
                # print(suggestions)
                self.assertEqual(suggestions, expected[type_][text_])


if __name__ == "__main__":
    pass
