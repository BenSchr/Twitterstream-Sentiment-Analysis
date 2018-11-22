from elasticsearch import helpers
from elasticsearch import Elasticsearch


elasticurl = "YourElasticHost"


def getElastic():
    return Elasticsearch([elasticurl + ':9200'], timeout=30)

def deleteIndex(index):
    try:
        esclient = getElastic()
        esclient.indices.delete(index=index)
    except:
        pass


def readCSV(filename):
    import pandas as pd
    df = pd.read_csv(filename, encoding='utf-8', sep=',', engine="python")

    doc = df.to_dict(orient='records')
    return doc

def readLinedJSON(filename):
    import json
    doc=[]
    with open(filename) as f:

        for line in f:
            obj = json.loads(line)
            try:
                del obj["_id"]
            except:
                pass

            doc.append(obj)

    return doc
def createIndex(index):
    try:
        esclient = getElastic()
        esclient.indices.create(index=index)
    except:
        pass


def sth2elastic(doc, index, type):
    esclient = getElastic()
    statcnt = 0
    actions = []
    for row in doc:
        actions.append({
            "_op_type": "index",
            "_index": index,
            "_type": type,
            "_source": row
        })

    for ok, response in helpers.streaming_bulk(esclient, actions, index=index, doc_type=type,
                                               max_retries=5,
                                               raise_on_error=False, raise_on_exception=False):
        if not ok:
            statcnt+=0
            print(response)
        else:
            statcnt += 1
    return statcnt


