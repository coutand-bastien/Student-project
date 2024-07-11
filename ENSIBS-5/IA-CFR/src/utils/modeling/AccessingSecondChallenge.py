from utils.config.ElasticConfig import ElasticConfig

class AccessingSecondChallenge:
    """
    The `AccessingSecondChallenge` class contains methods that perform various operations on an Elasticsearch index, 
    on the second challenge data.

    :param es: The "es" parameter is an instance of the `ElasticConfig` class.
    :param index_name: The "index_name" parameter is a string that represents the name of the index you want to access.
    """
    def __init__(self, es: ElasticConfig, index_name: str):
        self._es = es
        self.index_name = index_name

        self.size = 10000
        self.scroll = '10m'

    def search_function(self, query: dict, fields: [str] = None) -> list[dict]:
        """
        The function `search_function` retrieves all the hits from a given Elasticsearch query by using the
        scroll API. If there is only one field, we can return a list of values instead of a list of dictionaries
        :param query: The "query" parameter is a dictionary that represents the Elasticsearch query you want to execute.
        :param fields: The "fields" parameter is a list of field names that you want to retrieve from the search results.
        default: None
        :return: The function `search_function` returns a list of dictionaries containing the results of a search query.
        :rtype: list[dict]
        """
        res = []

        # Send the initial search request without the scroll
        response = self._es.get_es().search(index=self.index_name, **query)

        # Process initial results
        for hit in response['hits']['hits']:
            if fields is None:     res.append(hit['_source'])
            elif len(fields) == 1: res.append(hit['_source'].get(fields[0]))
            else:                  res.append({field: hit['_source'].get(field) for field in fields})

        # Use scroll to retrieve next results
        while True:
            scroll_id = response.get('_scroll_id')

            if not scroll_id:
                break

            response = self._es.get_es().scroll(scroll_id=scroll_id, scroll='5m')

            if not response['hits']['hits']:
                break

            for hit in response['hits']['hits']:
                if fields is None:     res.append(hit['_source'])
                elif len(fields) == 1: res.append(hit['_source'].get(fields[0]))
                else:                  res.append({field: hit['_source'].get(field) for field in fields})

        # Clear scroll resources
        if scroll_id:
            self._es.get_es().clear_scroll(scroll_id=scroll_id)

        return res

    def get_attack_normal_victim_unknown_flows_part(self, index_part: int) -> dict:
        """
        The function `get_attack_normal_victim_unknown_flows` returns a dictionary containing the results of a search
        :param index_part: The "index_part" parameter is an integer that represents the index part you want to search.
        :return: The function `get_attack_flows` returns a dictionary containing the results of a search
        :rtype: dict
        """
        query_attack = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"Tag": "attacker"}},
                        {"term": {"index_part": index_part}}
                    ]
                }
            },
            "size": self.size,
            "scroll": self.scroll
        }
        query_normal = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"Tag": "normal"}},
                        {"term": {"index_part": index_part}}
                    ]
                }
            },
            "size": self.size,
            "scroll": self.scroll
        }
        query_victim = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"Tag": "victim"}},
                        {"term": {"index_part": index_part}}
                    ]
                }
            },
            "size": self.size,
            "scroll": self.scroll
        }

        hits_attack = self.search_function(query=query_attack)
        hits_normal = self.search_function(query=query_normal)[:50000]  # for have 800 000 normal flows (17*50000)
        hits_victim = self.search_function(query=query_victim)

        return {"attack": hits_attack, "normal": hits_normal, "victim": hits_victim}