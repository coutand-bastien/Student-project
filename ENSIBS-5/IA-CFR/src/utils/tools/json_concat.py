import os
import json


def assembler_jsons(dossier_entree, fichier_sortie):
    """
    The `assembler_jsons` function assembles JSON files into a single JSON file.
    :param dossier_entree: the input folder containing the JSON files
    :param fichier_sortie: the output file
    """
    json_values = {}

    # Find all JSON files in the input folder
    for filename in os.listdir(dossier_entree):
        if filename.endswith(".json"):
            index = int(filename.split("_")[-1].split(".")[0])  # Extract the index from the filename

            with open(os.path.join(dossier_entree, filename), 'r') as file:
                data = json.load(file)

            # Ajout des valeurs spécifiques au dictionnaire trié
            json_values[index] = {
                "preds": data["preds"],
                "probs": data["probs"],
                "names": data["names"],
                "method": data["method"],
                "version": data["version"]
            }

    # Concaténation des valeurs triées dans le résultat final
    result_dict = {
        "preds": [],
        "probs": [],
        "names": ["COUTAND", "MARCHAND"],
        "method": 'knn',
        "version": 1
    }

    for i in sorted(json_values.keys()):
        result_dict["preds"].extend(json_values[i]["preds"])
        result_dict["probs"].extend(json_values[i]["probs"])

    # Conversion en format JSON
    result_json = json.dumps(result_dict, indent=2)

    # Écriture du résultat dans le fichier de sortie
    with open(fichier_sortie, 'w') as output_file:
        output_file.write(result_json)


if __name__ == "__main__":
    dossier_entree = "../../../results/splitted/knn/"
    fichier_sortie = "../../../results/COUTAND_MARCHAND_second_challenge_1.json"
    assembler_jsons(dossier_entree, fichier_sortie)
