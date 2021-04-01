# coding=utf-8
import unittest

from src.query_diseases import query_disease_example


class UTests(unittest.TestCase):
    def test_query_match_or(self):

        analyzer = {
            "analyzer": {
                "lowercase_unaccent": {
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"],
                    "filter": ["lowercase", "asciifolding"],
                }
            }
        }

        mapping = {
            "diseases": {
                "type": "text",
                "analyzer": "lowercase_unaccent",
                "fields": {
                    "as_completion": {
                        "type": "completion",
                        "analyzer": "lowercase_unaccent",
                    }
                },
            }
        }

        expected = [
            # exact match
            {
                "fuzziness": 0,
                "query": "névralgie post-zoostérienne",
                "result": ["névralgie post-zoostérienne"],
            },
            # no accent
            {
                "fuzziness": 0,
                "query": "nevralgie post-zoosterienne",
                "result": ["névralgie post-zoostérienne"],
            },
            # one word only
            {
                "fuzziness": 0,
                "query": "névralgie",
                "result": ["névralgie post-zoostérienne"],
            },
            # typo error
            {"fuzziness": 0, "query": "nérvalgie", "result": []},
            # typo error but fuzziness
            {
                "fuzziness": 1,
                "query": "néqralgie",
                "result": ["névralgie post-zoostérienne"],
            },
            # typo error but fuzziness 2
            {
                "fuzziness": 2,
                "query": "nérvalgie",
                "result": ["névralgie post-zoostérienne"],
            },
        ]

        for e in expected:
            body = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "diseases": {
                                        "query": e["query"],
                                        "fuzziness": e["fuzziness"],
                                    }
                                }
                            }
                        ]
                    }
                }
            }
            res = query_disease_example(
                {"diseases": ["névralgie post-zoostérienne"]},
                e["query"],
                analyzer=analyzer,
                mapping=mapping,
                body=body,
            )
            self.assertEqual(res, e["result"])

    def test_query_match_and(self):
        analyzer = {
            "analyzer": {
                "lowercase_unaccent": {
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"],
                    "filter": ["lowercase", "asciifolding"],
                }
            }
        }

        mapping = {
            "diseases": {
                "type": "text",
                "analyzer": "lowercase_unaccent",
                "fields": {
                    "as_completion": {
                        "type": "completion",
                        "analyzer": "lowercase_unaccent",
                    }
                },
            }
        }

        expected = [
            # exact match
            {
                "fuzziness": 0,
                "query": "névralgie post-zoostérienne",
                "result": ["névralgie post-zoostérienne"],
            },
            # no accent
            {
                "fuzziness": 0,
                "query": "nevralgie post-zoosterienne",
                "result": ["névralgie post-zoostérienne"],
            },
            # one word only
            {
                "fuzziness": 0,
                "query": "névralgie",
                "result": ["névralgie post-zoostérienne"],
            },
            # 2 words but one word only matches
            {"fuzziness": 0, "query": "névralgie blabla", "result": []},
        ]

        for e in expected:
            body = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "diseases": {
                                        "query": e["query"],
                                        "operator": "and",
                                        "fuzziness": e["fuzziness"],
                                    }
                                }
                            }
                        ]
                    }
                }
            }
            res = query_disease_example(
                {"diseases": ["névralgie post-zoostérienne"]},
                e["query"],
                analyzer=analyzer,
                mapping=mapping,
                body=body,
            )
            self.assertEqual(res, e["result"])

    def test_query_match_phrase(self):
        analyzer = {
            "analyzer": {
                "lowercase_unaccent": {
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"],
                    "filter": ["lowercase", "asciifolding"],
                }
            }
        }

        mapping = {
            "diseases": {
                "type": "text",
                "analyzer": "lowercase_unaccent",
                "fields": {
                    "as_completion": {
                        "type": "completion",
                        "analyzer": "lowercase_unaccent",
                    }
                },
            }
        }

        expected = [
            # exact match
            {
                "query": "névralgie post-zoostérienne",
                "result": ["névralgie post-zoostérienne"],
            },
            # no accent
            {
                "query": "nevralgie post-zoosterienne",
                "result": ["névralgie post-zoostérienne"],
            },
            # one word only
            {"query": "névralgie", "result": ["névralgie post-zoostérienne"]},
            # words in wrong order
            {"query": "post-zoostérienne névralgie", "result": []},
        ]

        for e in expected:
            body = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match_phrase": {
                                    "diseases": {
                                        "query": e["query"],
                                    }
                                }
                            }
                        ]
                    }
                }
            }
            res = query_disease_example(
                {"diseases": ["névralgie post-zoostérienne"]},
                e["query"],
                analyzer=analyzer,
                mapping=mapping,
                body=body,
            )
            self.assertEqual(res, e["result"])


if __name__ == "__main__":
    pass
