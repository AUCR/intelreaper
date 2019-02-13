from intelreaper.config import Config
from elasticsearch import Elasticsearch


def index_data_to_es(index, payload):
    if "ELASTICSEARCH_URL" in Config.CONFIG_DATA:
        es = Elasticsearch(Config.CONFIG_DATA["ELASTICSEARCH_URL"])
        es.index(index=index, doc_type=index, id=None, body=payload,
                 request_timeout=300)
