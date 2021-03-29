# coding=utf-8

from src.utils_es import (
    pp,
    create_index,
    delete_index,
    insert_single_doc,
    query_index_mapping,
    update_index_mapping,
)
from src.utils_analyzer import (
    query_analyzer,
    get_analyzer_name,
    STD_ANALYZER,
    FR_ANALYZER,
    TRI_GRAM_ANALYZER,
    REVERSE_ANALYZER,
    ACCENT_ANALYZER,
)


################################################################################
def suggest_query(index_name, client, body):
    res = client.search(body={"suggest": body}, index=index_name, params=None)
    return res["suggest"]


def suggest_query_full_example(mapping, input_doc, query_text, analyzer=None):
    """
    no mapping provided
    """
    INDEX = "pytest"
    es = create_index(INDEX, mapping=mapping, analyzer=analyzer)
    # update_index_mapping(INDEX, es, mapping)
    insert_single_doc(INDEX, es, input_doc)
    query_index_mapping(INDEX, es)

    if analyzer is None:
        body = {"text": query_text, "suggest-1": {"term": {"field": "tags"}}}
    else:
        analyzer_name = get_analyzer_name(analyzer)
        query_analyzer(INDEX, es, analyzer_name, query_text)
        body = {
            "text": query_text,
            "suggest-1": {"term": {"field": "tags", "analyzer": analyzer_name}},
        }

    res = suggest_query(INDEX, es, body=body)
    res = res["suggest-1"]
    for r in res:
        inp = r["text"]
        opt = [o["text"] for o in r["options"]]
        print(f"input text : {inp}\noptions :")
        pp.pprint(opt)
        print()

    delete_index(INDEX, es)
    return opt


################################################################################


def suggest_phrase_query_full_example(mapping, input_doc, query_text, analyzer=None):
    INDEX = "pytest"
    es = create_index(INDEX, mapping=mapping, analyzer=analyzer)
    insert_single_doc(INDEX, es, input_doc)
    query_index_mapping(INDEX, es)

    if analyzer is None:
        body = {
            "text": query_text,
            "suggest-1": {
                "phrase": {
                    "field": "tags",
                    "size": 5,
                    "gram_size": 3,
                    "direct_generator": [{"field": "tags", "suggest_mode": "always"}],
                    "highlight": {"pre_tag": "<em>", "post_tag": "</em>"},
                }
            },
        }
    else:
        analyzer_name = get_analyzer_name(analyzer)
        query_analyzer(INDEX, es, analyzer_name, query_text)
        body = {
            "text": query_text,
            "suggest-1": {
                "phrase": {
                    "field": "tags",
                    "analyzer": analyzer_name,
                    "size": 5,
                    "gram_size": 3,
                    "direct_generator": [{"field": "tags", "suggest_mode": "always"}],
                    "highlight": {"pre_tag": "<em>", "post_tag": "</em>"},
                }
            },
        }

    res = suggest_query(INDEX, es, body=body)
    res = res["suggest-1"]
    for r in res:
        inp = r["text"]
        opt = [o["text"] for o in r["options"]]
        print(f"input text : {inp}\noptions :")
        pp.pprint(opt)
        print()

    delete_index(INDEX, es)
    return opt


################################################################################
if __name__ == "__main__":
    if False:
        suggest_query_full_example(
            {"tags": {"type": "keyword"}}, {"tags": ["Bactéries"]}, "Bactéri"
        )

    if False:
        print(get_analyzer_name(FR_ANALYZER))

    if False:  # test analyzer
        INDEX = "pytest"
        mapping = {"tags": {"type": "keyword"}}
        input_doc = {"tags": ["Bactéries", "bact", "Appareil génital féminin"]}
        delete_index(INDEX)
        for analyzer in [
            STD_ANALYZER,
            FR_ANALYZER,
            TRI_GRAM_ANALYZER,
            REVERSE_ANALYZER,
            ACCENT_ANALYZER,
        ]:
            for query_text in input_doc["tags"]:
                es = create_index(INDEX, mapping=mapping, analyzer=analyzer)
                insert_single_doc(INDEX, es, input_doc)
                query_analyzer(INDEX, es, get_analyzer_name(analyzer), query_text)
                delete_index(INDEX, es)
