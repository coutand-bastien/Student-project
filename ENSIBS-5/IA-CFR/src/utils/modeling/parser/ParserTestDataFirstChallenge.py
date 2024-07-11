import os
import time
from lxml import etree

from utils.classifier.vectorization_functions import vectorized

class ParserTestDataFirstChallenge:
    """
    The `ParserTestDataFirstChallenge` class contains methods that parse XML files and insert the parsed data into
    a list of dictionaries, for the test data coming from the first challenge.
    """
    def __init__(self):
        self.xml_path_test_first_challenge  = os.getenv('XML_PATH_TEST')
        self.test_data_list = {}

    def get_xml_files(self, xml_path: str):
        """
        The function `get_xml_files` returns a list of XML file paths.
        :param xml_path: the path to the XML files
        :return: a list of XML file paths.
        :rtype: list[str]
        """
        xml_files = []
        for root, dirs, files in os.walk(xml_path):
            for file in files:
                if file.endswith(".xml"):
                    xml_files.append(os.path.join(root, file))

        if len(xml_files) == 0:
            print("No XML files found")

        return xml_files

    def parse(self):
        """
        The function `parse` parses XML files.
        :return: a list of dictionaries containing the parsed data
        :rtype: list[dict]
        """
        start_time = time.time()
        self.parse_from_xml_test_data(self.get_xml_files(xml_path=self.xml_path_test_first_challenge))
        end_time = time.time()

        print(f"[i] Time to do all parsing and indexing : {end_time - start_time} s")

        return self.test_data_list

    def parse_from_xml_test_data(self, xml_files):
        """
        The `parse_from_xml_test_data` function parses XML files for test data coming from the first challenge. The
        function do the vectorization of the data and then store it in a dictionary.
        :param xml_files: The `xml_files` parameter is a list of XML file paths. The `parseFromXML` method
        takes this list as input and processes each XML file
        """
        for xml_file in xml_files:
            print(f"[i] Parsing {xml_file}...")
            filename = xml_file.split("/")[-1]
            app_name = filename.split("_")[1].lower()
            self.test_data_list[app_name] = []

            with (open(xml_file, encoding="utf8") as file):
                tree = etree.parse(file)
                root = tree.getroot()

                # Parse the XML file and create a dictionary for each element
                for element in root.xpath('/test/*'):
                    data_dict = {}

                    for attribute in element.iterchildren():
                        data_dict[attribute.tag] = attribute.text

                    # vectorize the data for each flow for gain in performance
                    self.test_data_list[app_name].append(vectorized(flow=data_dict))