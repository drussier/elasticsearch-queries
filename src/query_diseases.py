# coding=utf-8

from src.utils_es import (
    pp,
    create_index,
    delete_index,
    insert_single_doc,
    query_index_mapping,
    update_index_mapping,
    query_index,
)

################################################################################


def query_disease_example(
    input_doc, query_text, body=None, mapping=None, analyzer=None, fuzziness=None
):
    INDEX = "pytest"
    if mapping is None:
        mapping = {"diseases": {"type": "text"}}

    es = create_index(INDEX, mapping=mapping, analyzer=analyzer)
    insert_single_doc(INDEX, es, input_doc)
    query_index_mapping(INDEX, es)

    if body is None:
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "diseases": {
                                    "query": query_text,
                                    "fuzziness": 0 if fuzziness is None else 1,
                                }
                            }
                        }
                    ]
                }
            }
        }

    res = query_index(INDEX, es, body)

    delete_index(INDEX, es)
    try:
        return res[0]["_source"]["diseases"]
    except IndexError:
        return []


################################################################################
if __name__ == "__main__":
    tmp = {
        "script": {
            "lang": "mustache",
            "source": {
                "_source": ["{{query_field}}"],
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "{{query_field}}": {
                                        "query": "{{query_string}}",
                                        "fuzziness": "{{query_fuzziness}}",
                                        "boost": 1,
                                    }
                                }
                            },
                            {
                                "match": {
                                    "{{query_field}}": {
                                        "query": "{{query_string}}",
                                        "operator": "and",
                                        "fuzziness": "{{query_fuzziness}}",
                                        "boost": 2,
                                    }
                                }
                            },
                            {
                                "match_phrase": {
                                    "{{query_field}}": {
                                        "query": "{{query_string}}",
                                        "boost": 4,
                                    }
                                }
                            },
                        ]
                    }
                },
            },
        }
    }

    input_doc = {"diseases": ["névralgie post-zostérienne"]}
    query_text = "névralgie post-zostérienne"

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

    body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"diseases": {"query": query_text, "fuzziness": 0}}}
                ]
            }
        }
    }

    res = query_disease_example(
        input_doc, query_text, analyzer=analyzer, mapping=mapping, body=body
    )
    pp.pprint(res)
