import json
import numpy as np
import elasticsearch as es
import spacy_universal_sentence_encoder
from typing import List
from iterator_utils import take

# Model for paragraph embeddings
#embed = spacy_universal_sentence_encoder.load_model("en_use_md")
embed = None
def get_embedding_func ():
    global embed
    if not embed:
        embed = spacy_universal_sentence_encoder.load_model("en_use_md")
    return embed

# Connection settings
#host = "186.29.148.129"
#port = 9400
host = "localhost"
port = 9200
es_connection = es.Elasticsearch([{
    "host": host,
    "port": port
}])

# Index definition
index_name = "cord-19"
index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "id": {
                "type": "text"
            },
            "paragraph": {
                "type": "text"
            },
            "vector": {
                "type": "dense_vector",
                "dims": 512
            }
        }
    }
}

# Index creation
def create_index ():
    try:
        if not es_connection.indices.exists(index=index_name):
            es_connection.indices.create(
                index=index_name,
                body=index_settings
            )
            print(f"Index {index_name} created")
        else:
            print(f"Index {index_name} already exists")
    except Exception as e:
        print(str(e))

# Insert paper in index
def insert_paper (
        id: str,
        paragraph: str,
        vector: List[float]
):
    if not es_connection.indices.exists(index=index_name):
        create_index()
    es_connection.index(
        index=index_name,
        body={
            "id": id,
            "paragraph": paragraph,
            "vector": vector
        }
    )


# Query script for similarity
def sim_query_script (query_vector: np.ndarray):
    return {
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {
                        "query_vector": query_vector
                    }
                }
            }
        }
    }

# Query for documents
def search_similar_docs (
        query_text: str,
        thresh=1.1,
        topn=10
):
    embed = get_embedding_func()
    query_vector = embed(query_text).vector
    matches = es_connection.search(
        index=index_name,
        body=sim_query_script(query_vector),
        request_timeout=30
    )["hits"]["hits"]
    return take(topn, (
        (match["_source"], match["_score"])
        for match in matches
        if match["_score"] > thresh
    ))

data_path = "../data/QA/2021-05-24"
paragraphs_path = f"{data_path}/paragraphs.jsonl"

if __name__ == '__main__':

    
    q = "covid-19 microbiology bioinformatics"
    print(f"Most similar papers to '{q}'")
    for res, score in search_similar_docs(q):
         print(res['paragraph'], score)
    
    '''
    q = {
    "query":{
        "match_all": {}
            }
        }
    
    results = es_connection.search(index=index_name,body=q)
    for result in results['hits']['hits']:
        print(result)
        
    
    create_index()
    embed = get_embedding_func()
    with open(paragraphs_path) as prg_file:
        for line in prg_file:
            data = json.loads(line)
            id = data["id"]
            paragraph = data["paragraph"]
            vector = embed(paragraph).vector.tolist()
            print("Processing: ", id)
            insert_paper(
                id,
                paragraph,
                vector
            )
    '''
