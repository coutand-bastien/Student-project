import matplotlib.pyplot as plt

from utils.config import ElasticConfig


class Accessing:
    """
    The `Accessing` class contains methods that perform various operations on an Elasticsearch index.

    :param es: An instance of the `ElasticConfig` class
    :param index_name: The name of the Elasticsearch index
    """
    def __init__(self, es: ElasticConfig, index_name: str):
        self._es = es
        self.index_name = index_name

        self.size = 10000
        self.scroll = '10m'

    #################################################################
    #       Useful functions
    #################################################################
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

    def get_payload_size(self, w_field: str) -> dict:
        """
        The function `get_payload_size` returns a dictionary containing the total source and destination
        :param w_field: application or protocol
        :return: a dictionary where the keys are the names of the applications or protocols and the values
        :rtype: dict
        """
        results = {}
        wanted_field = self.get_protocols() if w_field == 'protocol' else self.get_applications()
        field_names = ["sourcePayloadAsBase64", "destinationPayloadAsBase64"]

        for field in wanted_field:
            query = {
                "query": {
                    "term": {("protocolName" if w_field == "protocol" else "appName"): field}
                },
                "_source": ["sourcePayloadAsBase64", "destinationPayloadAsBase64"],
                "size": self.size,
                "scroll": self.scroll
            }

            hits = self.search_function(query=query, fields=field_names)

            sums = 0
            for elt in hits:
                source_payload_as_base64 = elt.get("sourcePayloadAsBase64", "")
                destination_payload_as_base64 = elt.get("destinationPayloadAsBase64", "")
                sums += len(source_payload_as_base64) if source_payload_as_base64 is not None else 0 + len(destination_payload_as_base64) if destination_payload_as_base64 is not None else 0

            results[field] = sums

        return results

    def get_attack_and_normal_flows_by_application(self, app_name: str) -> dict:
        """
        The function `get_attack_flows` retrieves attack flows from Elasticsearch based on the specified
        application name.
        :param app_name: The "app_name" parameter is a string that represents the name of the application
        you want to search for in the "flows" index
        :return: The function `get_attack_flows` returns a dictionary containing the results of a search;
        :rtype: dict
        """
        query_attack = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"appName": app_name}},
                        {"term": {"Tag": "attack"}}
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
                        {"term": {"appName": app_name}},
                        {"term": {"Tag": "normal"}}
                    ]
                }
            },
            "size": self.size,
            "scroll": self.scroll
        }

        hits_attack = self.search_function(query=query_attack)
        hits_normal = self.search_function(query=query_normal)

        return {"attack": hits_attack, "normal": hits_normal}

    def get_all_flows_by_applications(self, filenames: list[str]) -> dict:
        """
        The function `get_flows_by_filename_by_applications` retrieves flows from Elasticsearch based on the
        specified filename and all the applications.
        :param filenames: The "filenames" parameter is a list of strings that represents the name of the
        :return: The function `get_flows_by_filename_by_applications` returns a dictionary containing the
        results of a search
        :rtype: dict
        """
        results = {}
        applications = self.get_applications()

        for elt_filename in filenames:
            for app in applications:
                results[elt_filename][app] = self.get_attack_and_normal_flows_by_application(app_name=app)

        return results

    #################################################################
    #       Stats functions
    #################################################################
    def get_stats_protocols(self) -> str:
        """
        The function `get_stats_protocols` displays the total number of flows and the total payload size
        :return: a string
        :rtype: str
        """
        print("[i] Stats payload size and total flows")
        dict_protocols    = self.get_protocols_flow_card()
        dict_payload_size = self.get_protocols_payload_size()

        res = ""
        for key in dict_protocols:
            res += f"{key} -> {dict_protocols[key]} flows | {dict_payload_size[key]} bytes | {dict_payload_size[key] / dict_protocols[key]} bytes/flow"

        return res

    def get_stats_applications(self) -> str:
        """
        The function `get_stats_applications` displays the total number of flows and the total payload size
        :return: a string
        :rtype: str
        """
        print("[i] Stats payload size and total flows")
        dict_protocols = self.get_applications_flow_card()
        dict_payload_size = self.get_application_payload_size()

        res = ""
        for key in dict_protocols:
            res += f"{key} -> {dict_protocols[key]} flows | {dict_payload_size[key]} bytes | {dict_payload_size[key] / dict_protocols[key]} bytes/flow"

        return res

    #################################################################
    #       PROTOCOLS FUNCTIONS
    #################################################################
    def get_protocols(self):
        """
        The function `get_protocols` returns a set of unique protocol names obtained from an aggregation
        query.
        :return: a set of protocol names.
        :rtype: list[str]
        """
        query = {
            "query": {
                "match_all": {}
            },
            "_source": ["protocolName"],  # Specify the field you want to retrieve
            "size": self.size,
            "scroll": self.scroll
        }
        return list(set(self.search_function(query=query, fields=["protocolName"])))

    def get_protocol_flows(self, protocol: str) -> list[dict]:
        """
        The function `get_protocol_flows` retrieves protocol flows from Elasticsearch based on the specified
        protocol name.
        :param protocol: The "protocol" parameter is a string that represents the name of the protocol you
        want to search for in the "flows" index
        :return: The function `get_ProtocolFlows` returns a dictionary containing the results of a search
        query.
        :rtype: list[dict]
        """
        query = {
            "query": {
                "term": {"protocolName": protocol}
            },
            "size": self.size,
            "scroll": self.scroll
        }
        return self.search_function(query=query)

    def get_protocols_flow_card(self) -> dict:
        """
        The function `get_protocols_number_flows` returns a dictionary containing the number of flows for each
        protocol name.
        :return: a dictionary where the keys are the protocol names and the values are the number of flows
        associated with each protocol.
        :rtype: dict
        """
        query = {
            "query": {
                "match_all": {}
            },
            "_source": ["protocolName"],  # Specify the field you want to retrieve
            "size": self.size,
            "scroll": self.scroll
        }
        hits = self.search_function(query=query, fields=["protocolName"])

        results = {}
        for hit in hits:
            results[hit] = results.get(hit, 0) + 1

        return results

    def get_protocol_datas(self, field_names: list[str]):
        """
        The `get_protocol_datas` function retrieves data from the "flows" index based on specified field names
        and protocol names, and returns the sum of the values for each protocol.
        :param field_names: The `field_names` parameter is a list of field names that you want to retrieve
        from the search results. These field names should correspond to the fields in the documents stored
        in the 'flows' index
        :return: a dictionary where the keys are protocol names and the values are the sum of the specified
        field names for each protocol.
        :rtype: dict
        """
        protocols = self.get_protocols()
        results = {}

        for protocol in protocols:
            query = {
                "query": {
                    "term": {"protocolName": protocol}
                },
                "_source": field_names,  # Specify the field you want to retrieve
                "size": self.size,
                "scroll": self.scroll
            }
            hits = self.search_function(query=query)
            results[protocol] = sum(int(hit[field_names[0]])+int(hit[field_names[1]]) for hit in hits)

        return results

    def get_protocols_payload_size(self) -> dict:
        """
        The above code defines three functions that retrieve different types of data related to protocols.
        :return: The functions `get_ProtocolsPayloadSize`, `get_ProtocolsTotalBytes`, and
        `get_ProtocolsTotalPackets` are returning a dictionary.
        :rtype: dict
        """
        return self.get_payload_size(w_field='protocol')

    def get_protocols_total_bytes(self) -> dict:
        """
        The function "get_protocols_total_bytes" returns a dictionary containing the total source bytes and
        :return: A dictionary containing the total source bytes and total destination bytes for each
        :rtype: dict
        """
        return self.get_protocol_datas(field_names=["totalSourceBytes", "totalDestinationBytes"])

    def get_protocols_total_packets(self) -> dict:
        """
        The function "get_protocols_total_packets" returns a dictionary containing the total number of
        source and destination packets for each protocol.
        :return: A dictionary containing the total number of source packets and total number of
        destination packets for each protocol.
        :rtype: dict
        """
        return self.get_protocol_datas(field_names=["totalSourcePackets", "totalDestinationPackets"])

    #################################################################
    #       APPLICATIONS FUNCTIONS
    #################################################################

    def get_applications(self) -> list[str]:
        """
        The function `get_applications` returns a set of unique application names obtained from an
        aggregation query.
        :return: a set of application names.
        :rtype: list[str]
        """
        query = {
            "query": {
                "match_all": {}
            },
            "_source": ["appName"],  # Specify the field you want to retrieve
            "size": self.size,
            "scroll": self.scroll
        }

        return list(set(element.lower() for element in self.search_function(query=query, fields=["appName"])))

    def get_application_flows(self, application: str) -> list[dict]:
        """
        The function `get_application_flows` retrieves application flows from Elasticsearch based on the
        provided application name.
        :param application: The "application" parameter is a string that represents the name of the
        application for which you want to retrieve the application flows
        :return: The function `get_ApplicationFlows` returns a dictionary containing the results of a search
        query performed on an Elasticsearch index.
        :rtype: list[dict]
        """
        query = {
            "query": {
                "term": {"appName": application}
            },
            "size": self.size,
            "scroll": self.scroll
        }
        return self.search_function(query=query)

    def get_applications_flow_card(self) -> dict:
        """
        The function `get_ApplicationNumberOfFlows` returns a dictionary with the count of flows for each
        application name.
        :return: a dictionary where the keys are the names of applications and the values are the number of
        flows associated with each application.
        :rtype: dict
        """
        query = {
            "query": {
                "match_all": {}
            },
            "_source": ["appName"],  # Specify the field you want to retrieve
            "size": self.size,
            "scroll": self.scroll
        }
        hits = self.search_function(query=query, fields=["appName"])

        results = {}
        for hit in hits:
            hit = hit.lower()
            results[hit] = results.get(hit, 0) + 1

        return results

    def get_application_data(self, field_names: list[str]):
        """
        The `get_ApplicationData` function retrieves data from Elasticsearch for a list of applications and
        calculates the sum of specified fields for each application.
        :param field_names: The `field_names` parameter is a list of field names that you want to retrieve
        from the Elasticsearch index. These field names represent the specific data you are interested in
        retrieving for each application
        :return: a dictionary called "results" which contains the sum of the values of the specified field
        names for each application. The keys of the dictionary are the application names and the values are
        the sums.
        :rtype: dict
        """
        apps = self.get_applications()
        results = {}

        for app in apps:
            query = {
                "query": {
                    "term": {"appName": app}
                },
                "_source": field_names,  # Specify the field you want to retrieve
                "size": self.size,
                "scroll": self.scroll
            }
            hits = self.search_function(query=query)
            results[app] = sum(int(hit[field_names[0]]) + int(hit[field_names[1]]) for hit in hits)

        return results

    def get_application_payload_size(self) -> dict:
        """
        The above code defines three functions in a Python class that retrieve different types of data
        related to applications.
        :return: dictionary
        :rtype: dict
        """
        return self.get_payload_size(w_field='appName')

    def get_application_total_bytes(self) -> dict:
        """
        The function "get_application_total_bytes" returns a dictionary containing the total source bytes
        and total destination bytes of an application.
        :return: A dictionary containing the values of "totalSourceBytes" and "totalDestinationBytes"
        from the application data.
        :rtype: dict
        """
        return self.get_application_data(field_names=["totalSourceBytes", "totalDestinationBytes"])

    def get_application_total_packets(self) -> dict:
        """
        The function "get_application_total_packets" returns a dictionary containing the total number of
        source packets and destination packets.
        :return: A dictionary containing the values of "totalSourcePackets" and
        "totalDestinationPackets" from the application data.
        :rtype: dict
        """
        return self.get_application_data(field_names=["totalSourcePackets", "totalDestinationPackets"])

    #################################################################
    #       Diagram functions
    #################################################################
    def get_nb_flows_for_each_nb_packets(self):
        """
        The function `get_nb_flows_for_each_nb_packets` retrieves the number of flows for each number of
        packets.
        :return: a list of dictionaries.
        :rtype: list[dict]
        """
        print("Get number of flows for each number of packets")
        body = {
            "size": 0,
            "aggs": {
                "nb_flows_for_each_nb_packets": {
                    "terms": {
                        "field": "totalSourcePackets.keyword",
                        "size": 100
                    }
                }
            }
        }

        try:
            res = self._es.get_es().search(index=self.index_name, body=body)
            res = res["aggregations"]["nb_flows_for_each_nb_packets"]["buckets"]
        except Exception as e:
            print(f"Error: {e}")
            res = []

        return res

    def display_diagram(self):
        """
        The function `get_Diagram` retrieves the number of flows for each number of packets and draws a
        diagram with a logarithmic scale for the y-axis.
        """
        nb_flows_for_each_nb_packets = self.get_nb_flows_for_each_nb_packets()

        if not nb_flows_for_each_nb_packets:
            print("No data to display")
            return

        # Sort the list by number of packets (be careful, the key is a string)
        nb_flows_for_each_nb_packets = sorted(nb_flows_for_each_nb_packets, key=lambda k: int(k['key']))

        # Get the number of packets (x-axis)
        x = [pair['key'] for pair in nb_flows_for_each_nb_packets]

        # Get the number of flows (y-axis)
        y = [pair['doc_count'] for pair in nb_flows_for_each_nb_packets]

        # Draw the graph with a logarithmic scale for the y-axis
        plt.bar(x, y)
        plt.yscale('log')
        plt.xlabel("Number of packets")
        plt.ylabel("Number of flows")
        plt.title(f"Number of flows for each number of packets in {self.index_name}")
        plt.show()