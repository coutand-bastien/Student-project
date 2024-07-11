import os
import sys
from dotenv import load_dotenv

from elasticsearch import Elasticsearch

load_dotenv()  # Load environment variables from .env file

class ElasticConfig:
    """
    The `Elastic_config` class is used to configure the connection to Elasticsearch.
    """
    def __init__(self):
        self.host     = f"{os.getenv('HOST')}:{os.getenv('PORT')}"
        self.username = os.getenv('ELASTIC_USERNAME')
        self.password = os.getenv('ELASTIC_PASSWORD')
        self.certs    = os.getenv('CRT_PATH')

        self._es = Elasticsearch(
            self.host,
            basic_auth=(self.username, self.password),
            ca_certs=self.certs,
            request_timeout=60
        )

    def get_es(self):
        """
        The function `get_es` returns the Elasticsearch instance.
        :return: the Elasticsearch instance
        :rtype: Elasticsearch
        """
        return self._es

    def test_es_connection(self, index_name: str) -> bool:
        """
        The function `test_es_connection` tests the connection to Elasticsearch and checks if the index exists.
        :param index_name: the name of the index to check
        :return: True if the connection is OK and the index exists, False otherwise
        :rtype: bool
        """
        try:
            self._es.ping()
            print("[+] Connexion to ElasticSearch OK")

            if not self._es.indices.exists(index=index_name):
                print(f"[i] Index {index_name} not found")
                return False
            else:
                print(f"[i] Index {index_name} found")
                return True

        except ConnectionError:
            print("Connexion to ElasticSearch failed")
            sys.exit(1)