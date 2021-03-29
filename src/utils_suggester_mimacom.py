# coding=utf-8

from src.utils_es import (
    pp,
    create_index,
    delete_index,
    insert_single_doc,
    query_index_mapping,
    update_index_mapping,
)
from src.utils_analyzer import ACCENT_ANALYZER
from src.utils_suggester import suggest_query


################################################################################
def suggest_phrase_query_full_example_mimacom(
    input_doc, query_text, body=None, mapping=None, analyzer=None, fuzziness=None
):
    # https://blog.mimacom.com/autocomplete-elasticsearch-part3/
    INDEX = "pytest"
    if mapping is None:
        mapping = {"tags": {"type": "completion"}}

    es = create_index(INDEX, mapping=mapping, analyzer=analyzer)
    insert_single_doc(INDEX, es, input_doc)
    query_index_mapping(INDEX, es)

    if body is None:
        body = {
            "suggest-1": {
                "prefix": query_text,
                "completion": {"field": "tags"},
            }
        }

    if not (fuzziness is None):
        for k in body.keys():
            d = body[k]["completion"]
            d.update({"fuzzy": {"fuzziness": 1}})
            body[k]["completion"] = d

    res = suggest_query(INDEX, es, body=body)
    # pp.pprint(res)
    opt = {}
    for k, v in res.items():
        for r in v:
            inp = r["text"]
            opt[k] = [o["text"] for o in r["options"]]
            print(f"input text : {inp}\noptions :")
            pp.pprint(opt)
            print()

    delete_index(INDEX, es)
    return opt


################################################################################
if __name__ == "__main__":

    if False:
        INDEX = "pytest"
        delete_index(INDEX)
        input_doc = {"tags": ["Bactéries", "Appareil génital féminin"]}
        query_text = "appar"
        suggest_phrase_query_full_example_mimacom(input_doc, query_text)

    if False:
        INDEX = "pytest"
        delete_index(INDEX)
        input_doc = {"tags": ["Bactéries", "Appareil génital féminin"]}
        query_text = "apareil gén"
        suggest_phrase_query_full_example_mimacom(input_doc, query_text, fuzziness=1)

    if False:  # accent
        # old version of ES !!
        # https://www.elastic.co/guide/en/elasticsearch/guide/current/asciifolding-token-filter.html
        INDEX = "pytest"
        input_doc = {"tags": ["Appareil génital féminin"]}
        query_text = "appareil gen"
        mapping = {
            "tags": {
                "type": "completion",
                "analyzer": "standard",
                "fields": {"no_accent": {"type": "completion", "analyzer": "folding"}},
            }
        }
        body = {
            "suggest-1": {
                # "multi_match": {
                # "type": "most_fields",
                # "query": query_text,
                # "fields": ["tags", "tags.no_accent"]
                # }
                "prefix": query_text,
                # "completion": {"field": "tags"},
                "completion": {"field": ["tags", "tags.no_accent"]},
            }
        }

        body = {
            "query": {
                "bool": {
                    "must": {"match_phrase_prefix": {"suggest": {"query": "doli"}}}
                }
            },
            "size": 50,
        }

        body = {
            "query": {
                "multi_match": {
                    "type": "most_fields",
                    "query": query_text,
                    "fields": ["tags", "tags.no_accent"],
                }
            },
            "size": 50,
        }

        suggest_phrase_query_full_example_mimacom(
            input_doc, query_text, body=body, mapping=mapping, analyzer=ACCENT_ANALYZER
        )

        # {"from":0,"query":{"bool":{"must":{"match_phrase_prefix":{"suggest":{"query":"doli"}}}}},"size":50}0

    if True:  # accent
        INDEX = "pytest"
        input_doc = {"tags": ["Appareil génital féminin"]}
        query_text = "appareil gen"
        mapping = {
            "tags": {
                "type": "completion",
                "analyzer": "standard",
                "fields": {"no_accent": {"type": "completion", "analyzer": "folding"}},
            }
        }
        body = {
            "suggest-1": {
                "prefix": query_text,
                "completion": {"field": "tags"},
            },
            "suggest-2": {
                "prefix": query_text,
                "completion": {"field": "tags.no_accent"},
            },
        }

        suggest_phrase_query_full_example_mimacom(
            input_doc, query_text, body=body, mapping=mapping, analyzer=ACCENT_ANALYZER
        )

        # {"from":0,"query":{"bool":{"must":{"match_phrase_prefix":{"suggest":{"query":"doli"}}}}},"size":50}0
