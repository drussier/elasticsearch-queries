# coding=utf-8
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, parallel_bulk
from elasticsearch.client import IndicesClient
import pprint

pp = pprint.PrettyPrinter(indent=4)

################################################################################


def create_index(index_name, mapping=None, analyzer=None):
    # https://elasticsearch-py.readthedocs.io/en/7.10.0/api.html#ignore
    es = Elasticsearch()
    # ignore 400 cause by IndexAlreadyExistsException when creating an index

    body = None
    if mapping:
        body = {"mappings": {"properties": mapping}}

    if analyzer:
        d = {"settings": {"analysis": analyzer}}
        if body is None:
            body = d
        else:
            body.update(d)

    res = es.indices.create(index=index_name, body=body, ignore=400)
    print(f"{index_name} creation status :", res)
    return es


def refresh_index(index_name, client):
    client.indices.refresh(index=index_name)


def delete_index(index_name, client=None):
    client = Elasticsearch() if client is None else client
    # ignore 404 and 400
    res = client.indices.delete(index=index_name, ignore=[400, 404])
    print(f"{index_name} deletion status :", res)
    return client


################################################################################
def query_index_mapping(index_name, client):
    mapping = IndicesClient(client).get_mapping(index=index_name)
    mapping = mapping["pytest"]["mappings"]["properties"]
    pp.pprint(mapping)
    return mapping


def update_index_mapping(index_name, client, mapping):
    IndicesClient(client).put_mapping(
        {"mappings": {"properties": mapping}}, index=index_name
    )
    return


################################################################################


def insert_single_doc(index_name, client, doc, id=None):
    res = client.index(index=index_name, id=id, body=doc)
    print("Single doc", res["result"])
    refresh_index(index_name, client)
    return res


def insert_multiple_docs(client, data_generator, para=False):
    if para:
        bulk(client, data_generator)
    else:
        for success, info in parallel_bulk(client, data_generator):
            if not success:
                print("A document failed:", info)


################################################################################


def query_single_doc_by_id(index_name, client, id):
    res = es.get(index=index_name, id=id)
    print(res["_source"])
    return res


def query_index(index_name, client, body):
    res = client.search(index=index_name, body=body)
    print("Query index : got %d hits" % res["hits"]["total"]["value"])
    return res["hits"]["hits"]


def match_all(index_name, client):
    refresh_index(index_name, client)
    return query_index(index_name, client, {"query": {"match_all": {}}})


################################################################################
if __name__ == "__main__":
    INDEX = "pytest"
    es = create_index(INDEX)
    insert_single_doc(
        INDEX,
        es,
        {
            "author": "kimchy",
            "text": "Elasticsearch: cool. bonsai cool.",
            "timestamp": datetime.now(),
        },
    )

    mapping = query_index_mapping(INDEX, es)

    res = match_all(INDEX, es)
    pp.pprint(res)

    # query_single_doc_by_id(INDEX, es, id=1)

    insert_multiple_docs(
        es, ({"_index": INDEX, "word": w} for w in ["bla", "bli", "blo"]), para=True
    )
    res = match_all(INDEX, es)
    pp.pprint(res)

    delete_index(INDEX, es)
