import os
import time
from elasticsearch.helpers import bulk
from lxml import etree
from dotenv import load_dotenv

from utils.config.ElasticConfig import ElasticConfig

load_dotenv()  # Load environment variables from .env file

class Indexing:
    """
    The `Indexing` class contains methods that parse XML files and insert the parsed data into. It also contains
    methods that create an Elasticsearch index and bulk insert the parsed data into Elasticsearch.

    :param es: The "es" parameter is an instance of the `ElasticConfig` class.
    :param index_name: The "index_name" parameter is a string that represents the name of the index you want to create.
    :param is_second_challenge: The "is_second_challenge" parameter is a boolean that indicates whether the data. Default: False
    """
    def __init__(self, es: ElasticConfig, index_name, is_second_challenge: bool = False):
        self._es = es
        self.index_name = index_name
        self.is_second_challenge = is_second_challenge

        self.xml_path_classic = os.getenv('XML_PATH_CLASSIC')
        self.xml_path_second_challenge = os.getenv('XML_PATH_TRAIN_SECOND_CHALLENGE_SPLIT')

    def create_index(self):
        """
        The function creates an Elasticsearch index called "flows" with specific settings.
        """
        request_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
            }
        }

        self._es.get_es().indices.create(index=self.index_name, body=request_body)
        print(f"[i] Index {self.index_name} created")

    def get_xml_files(self, xml_path: str):
        """
        The function `get_xml_files` returns a list of XML file paths.
        :param xml_path: the path to the XML files
        :return: a list of XML file paths.
        :rtype: list[str]
        """
        xml_files = {}
        for root, dirs, files in os.walk(xml_path):
            for file in files:
                if file.endswith(".xml"):
                    if self.is_second_challenge:
                        index = int(file.split("_")[-1].split(".")[0])
                        xml_files[index] = (os.path.join(root, file))
                    else:
                        xml_files[file] = (os.path.join(root, file))

        if len(xml_files) == 0:
            print("No XML files found")
            exit(1)

        xml_files = dict(sorted(xml_files.items()))
        return xml_files.values()

    def parse(self):
        """
        The function `parse` parses XML files, creates an index if it doesn't exist, and bulk inserts the
        parsed data into Elasticsearch. If the index already exists, it is deleted and recreated. This function
        is used for the first challenge and second challenge.
        """
        if not self._es.test_es_connection(self.index_name):
            self.create_index()
        else:
            self._es.get_es().indices.delete(index=self.index_name)  # delete the index if it already exists
            print(f"[i] Index {self.index_name} deleted")
            self.create_index()

        start_time = time.time()
        self.parse_from_xml_classic_data(self.get_xml_files(xml_path=self.xml_path_classic if not self.is_second_challenge else self.xml_path_second_challenge))
        end_time = time.time()

        print(f"[i] Time to do all parsing and indexing : {end_time - start_time} s")

    def parse_from_xml_classic_data(self, xml_files: list):
        """
        The `parse_from_xml` function parses XML files, creates an index if it doesn't exist, and bulk inserts
        the parsed data into Elasticsearch.
        :param xml_files: The `xml_files` parameter is a list of XML file paths. The `parseFromXML` method
        takes this list as input and processes each XML file
        :type xml_files: list
        """
        nb = 0
        for xml_file in xml_files:
            print(f"[i] Parsing {xml_file}...")
            with (open(xml_file, encoding="utf8") as file):
                tree = etree.parse(file)
                root = tree.getroot()
                bulk_data = []

                # Parse the XML file and create a dictionary for each element
                for element in root.xpath('/dataroot/*'):
                    data_dict = {}
                    nb += 1
                    for attribute in element.iterchildren():
                        data_dict[attribute.tag] = attribute.text

                    data_dict['index_part'] = xml_file.split("_")[-1].split(".")[0]
                    bulk_data.append({"_op_type": "index", "_index": self.index_name, "_source": data_dict})

                # Send the data into es in bulk mode
                batch_size = 10000

                for i in range(0, len(bulk_data), batch_size):
                    batch = bulk_data[i:i + batch_size]
                    _, failed = bulk(self._es.get_es(), batch, index=self.index_name, raise_on_error=False)

                    if failed:
                        print(f"Failed : {failed}")

        print(f"[i] {nb} documents indexed")