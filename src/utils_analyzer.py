# coding=utf-8

from src.utils_es import (
    IndicesClient,
    pp,
    create_index,
    delete_index,
    insert_single_doc,
    query_index_mapping,
    update_index_mapping,
)

# https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-analyzer.html
STD_ANALYZER = {
    "analyzer": {
        "std_analyzer": {
            "type": "standard",
            "max_token_length": 5,
            "stopwords": "_french_",
        }
    }
}

# https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lang-analyzer.html#french-analyzer
FR_ANALYZER = {
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
        "fr_analyzer": {
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

# https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html
TRI_GRAM_ANALYZER = {
    "analyzer": {
        "trigram": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["lowercase", "shingle"],
        },
    },
    "filter": {
        "shingle": {"type": "shingle", "min_shingle_size": 2, "max_shingle_size": 3}
    },
}

REVERSE_ANALYZER = {
    "analyzer": {
        "reverse": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["lowercase", "reverse"],
        }
    }
}


# https://www.elastic.co/guide/en/elasticsearch/guide/current/asciifolding-token-filter.html
# https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-htmlstrip-charfilter.html
ACCENT_ANALYZER = {
    "analyzer": {
        "folding": {
            "tokenizer": "standard",
            "char_filter": ["html_strip"],
            "filter": ["lowercase", "asciifolding"],
        }
    }
}


################################################################################


def get_analyzer_name(analyzer):
    return list(analyzer["analyzer"].keys())[0]


def query_analyzer(index_name, client, analyzer_name, text):
    body = {"analyzer": analyzer_name, "text": text}
    res = IndicesClient(client).analyze(index=index_name, body=body)
    print(f"query analyzer '{analyzer_name}'")
    pp.pprint(res)
    return res


def analyze_text(txt, analyzer):
    INDEX = "pytest"
    input_doc = {"tags": [txt]}
    delete_index(INDEX)
    es = create_index(INDEX, analyzer=analyzer)
    insert_single_doc(INDEX, es, input_doc)
    res = query_analyzer(INDEX, es, get_analyzer_name(analyzer), txt)
    delete_index(INDEX, es)

    tokens = [e["token"] for e in res["tokens"]]
    return tokens


if __name__ == "__main__":
    if False:
        print(get_analyzer_name(ACCENT_ANALYZER))

    if True:
        tokens = analyze_text("panne de réveil ce matin !", ACCENT_ANALYZER)
        print(tokens)

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
