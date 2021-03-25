# coding=utf-8

from src.utils_es import (
    pp,
    create_index,
    delete_index,
    insert_single_doc,
    query_index_mapping,
    update_index_mapping,
)


def suggest_query(index_name, client, body, text):
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
        body = {
            "text": query_text,
            "suggest-1": {"term": {"field": "tags", "analyzer": "default"}},
        }

    res = suggest_query(INDEX, es, body=body, text="Bactéri")
    res = res["suggest-1"]
    for r in res:
        inp = r["text"]
        opt = [o["text"] for o in r["options"]]
        print(f"input text : {inp}\noptions :")
        pp.pprint(opt)
        print()

    delete_index(INDEX, es)
    return opt


if __name__ == "__main__":
    suggest_query_full_example(
        {"tags": {"type": "keyword"}}, {"tags": ["Bactéries"]}, "Bactéri"
    )
