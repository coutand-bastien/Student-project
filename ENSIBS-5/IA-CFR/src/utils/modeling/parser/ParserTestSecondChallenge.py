import os

import numpy as np
from lxml import etree

from utils.classifier.vectorization_functions import vectorized_second_challenge


class ParserTestSecondChallenge:
    """
    The `Parser_test_data` class contains methods that parse XML files and insert the parsed data into
    a list of dictionaries, for the test data coming from the second challenge.
    """
    def __init__(self):
        self.xml_path_test_with_other_file  = os.getenv('XML_PATH_TEST_SECOND_CHALLENGE_SPLIT')

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
                    index = int(file.split("_")[-1].split(".")[0])
                    xml_files[index] = (os.path.join(root, file))

        if len(xml_files) == 0:
            print("No XML files found")

        xml_files = dict(sorted(xml_files.items()))
        return xml_files

    def parse_from_xml_test_data(self, xml_file):
        """
        The `parse_from_xml_test_data` function parses XML files for test data coming from the second challenge. The
        function do the vectorization of the data and then store it in a dictionary.
        :param xml_file: The `xml_files` parameter is a list of XML file paths. The `parseFromXML` method
        takes this list as input and processes each XML file
        :return: a list of vectors
        :rtype: list[np.array]
        """
        print(f"[i] Parsing {xml_file}...")
        test_data_list = []

        with (open(xml_file, encoding="utf8") as file):
            tree = etree.parse(file)
            root = tree.getroot()
            # Parse the XML file and create a dictionary for each element
            for element in root.xpath('*'):
                data_dict = {}

                for attribute in element.iterchildren():
                    data_dict[attribute.tag] = attribute.text

                # vectorize the data for each flow for gain in performance
                test_data_list.append(vectorized_second_challenge(flow=data_dict))

        return np.array(test_data_list)