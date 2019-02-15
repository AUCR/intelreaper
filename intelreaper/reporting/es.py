from click import echo
from intelreaper.config import Config
from elasticsearch import Elasticsearch


def index_data_to_es(index, payload):
    config_data = Config.CONFIG_DATA
    if "ELASTICSEARCH_URL" in config_data:
        es = Elasticsearch(Config.CONFIG_DATA["ELASTICSEARCH_URL"])
        es.index(index=index, doc_type="ar", id=None, body=payload, request_timeout=300)
    else:
        echo("ELASTICSEARCH_URL IS NOT SET! No Data was added to Elasticsearch! Make sure to set it in Vault.")
