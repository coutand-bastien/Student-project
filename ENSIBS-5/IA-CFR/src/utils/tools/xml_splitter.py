import xml.etree.ElementTree as ET
import os


def divide_xml(input_file, output_folder, chunk_size):
    """
    The `divide_xml` function divides a large XML file into smaller parts.
    :param input_file: the input XML file
    :param output_folder: the output folder
    :param chunk_size: the size of each part
    """
    # Charger le fichier XML principal
    tree = ET.parse(input_file)
    root = tree.getroot()

    total_flows = len(root.findall('.//FFlow'))
    chunks = range(0, total_flows, chunk_size)

    # Diviser en parties et sauvegarder chaque partie
    for i, start_idx in enumerate(chunks):
        end_idx = min(start_idx + chunk_size, total_flows)

        # Créer un nouvel arbre XML pour chaque partie
        chunk_root = ET.Element("dataroot", attrib=root.attrib)
        chunk_tree = ET.ElementTree(chunk_root)

        # Ajouter les FFlows à la partie actuelle
        for flow in root.findall('.//FFlow')[start_idx:end_idx]:
            chunk_root.append(flow)

        # Sauvegarder la partie dans un fichier séparé
        output_file = os.path.join(output_folder, f"traffic_os_TRAIN_part_{i}.xml")
        chunk_tree.write(output_file, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    input_file = "../../data/test_second_defi_data/train/traffic_os_TRAIN.xml"
    output_folder = "../../data/test_second_defi_data/train_split/"
    chunk_size = 500000

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Diviser le fichier XML en parties
    divide_xml(input_file, output_folder, chunk_size)