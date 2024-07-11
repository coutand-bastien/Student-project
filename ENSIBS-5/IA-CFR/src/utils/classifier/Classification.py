import pickle
import random
import sys
import time
import json
import os

import matplotlib.pyplot as plt
import numpy as np
from numpy import interp
from sklearn.metrics import roc_curve, auc, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

from utils.classifier.vectorization_functions import run_vectorization
from utils.config import ElasticConfig
from utils.modeling.parser.ParserTestSecondChallenge import ParserTestSecondChallenge


class Classification:
    """
    The class `Classification` creates the initial subset for each application, train the KNN and NB models, and
    evaluates the performance of the models on the test_data set. It can also display the ROC curve and display the
    confusion matrix and the performance metrics.

    :param es: the Elasticsearch configuration
    :param accessing: the accessing class
    """

    def __init__(self, es: ElasticConfig, accessing):
        self.es = es
        self.accessing = accessing

        self.is_test_first_challenge = False
        self.is_second_challenge = False
        self.is_draw_roc_curve = False

        self.is_knn = False
        self.is_nb = False

        self.output_file = os.getenv('RESULT_PATH')

    def is_knn_model(self, is_knn: bool):
        """
        The function `is_knn_model` sets the flag 'is_knn' to True if the test_data must be run with the KNN classifier.
        :param is_knn: True if the test_data must be run with the KNN classifier, False otherwise
        """
        self.is_knn = is_knn

    def is_nb_model(self, is_nb: bool):
        """
        The function `is_nb_model` sets the flag 'is_nb' to True if the test_data must be run with the NB classifier.
        :param is_nb: True if the test_data must be run with the NB classifier, False otherwise
        """
        self.is_nb = is_nb

    def set_is_second_challenge(self, is_second_challenge: bool):
        """
        The function `set_is_second_challenge` sets the flag 'is_second_challenge' to True if the test_data must be run with the
        second definition of the attack.
        :param is_second_challenge: True if the test_data must be run with the second definition of the attack, False otherwise
        """
        self.is_second_challenge = is_second_challenge

    def set_test_first_challenge(self, is_test_first_challenge: bool):
        """
        The function `set_test_first_challenge` sets the flag 'is_first_challenge' to True if the test_data
        must be run with the test_data coming from first challenge data.
        :param is_test_first_challenge: True if the test_data must be run with the test_data coming from first challenge data,
        """
        self.is_test_first_challenge = is_test_first_challenge  # set test with another file

    def set_draw_roc_curve(self, draw_roc_curve: bool):
        """
        The function `set_draw_roc_curve` sets the flag 'is_draw_roc_curve' to True if the ROC curve must be displayed.
        :param draw_roc_curve: True if the ROC curve must be displayed, False otherwise
        """
        self.is_draw_roc_curve = draw_roc_curve

    def shuffle_list(self, list1, list2):
        """
        The function `shuffle_list` shuffles two lists in the same order. It returns the two shuffled lists.
        :param list1: the first list
        :param list2: the second list
        :return: the two shuffled lists
        :rtype: tuple of lists
        """
        paired_list = list(zip(list1, list2))  # Combine the two lists into a list of pairs
        random.shuffle(paired_list)  # Shuffle the paired list
        return zip(*paired_list)

    def create_subset(self, flows: dict, rate_for_attacks: float = 0.2):
        """
        The function `create_subset` creates a subset for one application. The subset contains the same number of attacks
        and the same number of normal flows. The subset is created randomly. The subset is created by combining the
        training and test_data sets.
        :param flows: a dictionary of flows for one application
        :param rate_for_attacks: the rate of attacks in the test_data sets. Default is 0.2
        :return: a dictionary of 'nb_subsets' test_data sets for each application
        :rtype: dict of lists
        """
        normal_flows_size = len(flows['normal'])
        attack_flows_size = len(flows['attack'])

        print("Nb flows : " + str(normal_flows_size + attack_flows_size) + " flows")

        vectorized_attacks = run_vectorization(flows=flows['attack'])
        vectorized_normals = run_vectorization(flows=flows['normal'])

        y = [1] * attack_flows_size  # because only attacks so 1
        X_train_attack, X_test_attack, y_train_attack, y_test_attack = train_test_split(vectorized_attacks, y, test_size=rate_for_attacks, random_state=random.randint(0, 100), shuffle=True)

        y = [0] * normal_flows_size  # because only normal so 0
        X_train_normal, X_test_normal, y_train_normal, y_test_normal = train_test_split(vectorized_normals, y, test_size=rate_for_attacks, random_state=random.randint(0, 100), shuffle=True)

        # Create the training and test_data sets by combining the attack and normal flows and shuffling them
        X_train, y_train = self.shuffle_list(list1=np.array(X_train_attack + X_train_normal, dtype=object), list2=np.array(y_train_attack + y_train_normal, dtype=object))
        X_test, y_test   = self.shuffle_list(list1=np.array(X_test_attack + X_test_normal, dtype=object), list2=np.array(y_test_attack + y_test_normal, dtype=object))

        return {
            "X_train" : np.array(X_train),
            "X_test"  : np.array(X_test),
            "y_train" : np.array(y_train),
            "y_test"  : np.array(y_test)
        }

    def create_subset_second_challenge(self, flows: dict, rate_for_attacks: float = 0.2):
        """
        The function `create_subset_second_challenge` creates a subset for one application. The subset contains the same number of attacks
        and the same number of normal flows. The subset is created randomly. The subset is created by combining the
        training and test_data sets.
        :param flows: a dictionary of flows for one application
        :param rate_for_attacks: the rate of attacks in the test_data sets. Default is 0.2
        :return: a dictionary of 'nb_subsets' test_data sets for each application
        :rtype: dict of lists
        """
        X_train_attack, X_train_normal, X_train_victim = [], [], []
        X_test_attack, X_test_normal, X_test_victim    = [], [], []
        y_train_attack, y_train_normal, y_train_victim = [], [], []
        y_test_attack, y_test_normal, y_test_victim    = [], [], []

        normal_flows_size, attack_flows_size, victim_flows_size = len(flows['normal']), len(flows['attack']), len(flows['victim'])

        if flows['attack']:
            vectorized_attacks = run_vectorization(flows=flows['attack'], is_second_challenge=True)
            y = [1] * attack_flows_size  # because only attacks so 1
            X_train_attack, X_test_attack, y_train_attack, y_test_attack = train_test_split(vectorized_attacks, y,
                                                                                            test_size=rate_for_attacks,
                                                                                            random_state=random.randint(
                                                                                                0, 100), shuffle=True)

        if flows['normal']:
            vectorized_normals = run_vectorization(flows=flows['normal'], is_second_challenge=True)
            y = [0] * normal_flows_size  # because only normal so 0
            X_train_normal, X_test_normal, y_train_normal, y_test_normal = train_test_split(vectorized_normals, y,
                                                                                            test_size=rate_for_attacks,
                                                                                            random_state=random.randint(
                                                                                                0, 100), shuffle=True)

        if flows['victim']:
            vectorized_victims = run_vectorization(flows=flows['victim'], is_second_challenge=True)
            y = [2] * victim_flows_size  # because only victims so 2
            X_train_victim, X_test_victim, y_train_victim, y_test_victim = train_test_split(vectorized_victims, y, test_size=rate_for_attacks, random_state=random.randint(0, 100), shuffle=True)


        # Create the training and test_data sets by combining the attack and normal flows and shuffling them
        X_train, y_train = self.shuffle_list(
            list1=np.array(X_train_attack + X_train_normal + X_train_victim + X_test_attack + X_test_normal + X_test_victim, dtype=object),
            list2=np.array(y_train_attack + y_train_normal + y_train_victim + y_test_attack + y_test_normal + y_test_victim, dtype=object))

        return {
            "X_train" : np.array(X_train),
            "y_train" : np.array(y_train)
        }

    def create_initial_subset(self, application_names: list[str]):
        """
        The function `create_initial_subset` creates the initial subset for each application. The initial subset
        contains the same number of attacks and the same number of normal flows. The initial subset is created
        randomly.
        :param application_names: the list of application names
        :return: a dictionary of initial subsets for each application
        :rtype: dict of lists
        """
        flows_by_app = {}

        for app_name in application_names:
            flows_by_app[app_name] = self.accessing.get_attack_and_normal_flows_by_application(app_name=app_name)

        subsets_by_app = {}

        # Create the initial subset for each application by filename, with X_train, X_test, y_train, y_test
        for app_name in application_names:
            subsets_by_app[app_name] = self.create_subset(flows=flows_by_app[app_name])

        return subsets_by_app

    def cross_validation(self, X_train, y_train, classifier):
        """
        The function `cross_validation` performs a cross validation on the training set. It returns the ROC curve
        and the area under the curve.
        :param X_train: the training set
        :param y_train: the training set labels
        :param classifier: the classifier function
        :return: the base false positive rate, the mean true positive rate, the area under the curve, and the optimal
        threshold
        :rtype: NDArray, Float, Float, Float 
        """
        base_fpr = np.linspace(0, 1, 101)
        tprs, thresholds_list = [], []
        cv = StratifiedKFold(n_splits=5, shuffle=True)

        for train, test in cv.split(X_train, y_train):
            classifier = classifier
            probas_ = classifier.fit(X_train[train], y_train[train]).predict_proba(X_train[test])
            # Compute ROC curve and area under the curve

            fpr, tpr, thresholds = roc_curve(y_train[test], probas_[:, 1])

            # Find the optimal threshold from the ROC curve
            optimal_idx = np.argmax(tpr - fpr)
            optimal_threshold = thresholds[optimal_idx]
            thresholds_list.append(optimal_threshold)

            # use interpolation to get the same length for each ROC curve
            # because the number of thresholds can be different for each fold
            # and can create issues when computing the mean ROC curve
            tpr = interp(base_fpr, fpr, tpr)
            tpr[0] = 0.0
            tprs.append(tpr)

        mean_tprs = np.mean(tprs, axis=0)
        mean_auc = auc(base_fpr, mean_tprs)
        mean_threshold = np.mean(thresholds_list)

        return base_fpr, mean_tprs, mean_auc, mean_threshold

    def display_roc_curve(self, curve_dict: list, app_name):
        """
        The function `display_roc_curve` displays the ROC curve for the classifier.
        :param curve_dict: a list containing the ROC curve and the area under the curve for each 
        classifier. It contains the following keys: 'base_fpr', 'mean_tprs', 'mean_auc', 'classifier_name'.
        :param app_name: the application name
        """
        colors = [
            'darkorange', 'darkgreen', 'darkred', 'darkblue', 'darkcyan', 'darkmagenta', 'darkgoldenrod',
            'darkslategray', 'darkolivegreen', 'darkkhaki', 'orange', 'green', 'red', 'blue', 'cyan',
            'magenta', 'goldenrod', 'slategray', 'olivegreen', 'khaki'
        ]

        plt.figure()

        for i, curve in enumerate(curve_dict):
            plt.plot(curve['base_fpr'], curve['mean_tprs'], color=colors[i % len(colors)], lw=2, label=f'{curve["classifier_name"]} mean ROC (AUC = {curve["mean_auc"]:.2f})', alpha=.8)

        plt.title(f'Receiver Operating Characteristic (ROC) Curve for {app_name}')
        plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Chance', alpha=.8)
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.legend(loc='lower right')
        plt.savefig(f'{self.output_file}/{app_name}_roc_curve.png')  # Save the ROC curve
        plt.show()

    def performance_evaluation_on_test_set(self, y_test, y_pred_test):
        """
        The function `performance_evaluation_on_test_set` evaluates the performance of the classifier on the test_data set.
        It displays the confusion matrix and the performance metrics.
        :param y_test: the test_data set labels
        :param y_pred_test: the test_data set predictions
        """
        accuracy = accuracy_score(y_test, y_pred_test)
        precision = precision_score(y_test, y_pred_test, zero_division=1)
        recall = recall_score(y_test, y_pred_test, zero_division=1)
        f1 = f1_score(y_test, y_pred_test, zero_division=1)
        conf_matrix = confusion_matrix(y_test, y_pred_test)

        # Create a DataFrame from the confusion matrix
        conf_matrix_df = pd.DataFrame(conf_matrix, index=['Actual Negative', 'Actual Positive'], columns=['Predicted Negative', 'Predicted Positive'])

        # Add totals to the DataFrame
        conf_matrix_df['Total']     = conf_matrix_df.sum(axis=1)
        conf_matrix_df.loc['Total'] = conf_matrix_df.sum()

        print("Confusion Matrix:")
        print(conf_matrix_df)
        print("----------------------------------------")
        print(f"Accuracy: {accuracy:.4f}. This is the proportion of correct predictions among the total number of input samples.")
        print(f"Precision: {precision:.4f}. This is the ability of the classifier not to label as positive a sample that is negative.")
        print(f"Recall: {recall:.4f}. This is the ability of the classifier to find all the positive samples.")
        print(f"F1 Score: {f1:.4f}. This is a weighted average of the precision and recall, where an F1 score reaches its best value at 1 and worst score at 0.")

    def performance_evaluation_on_test_set_first_defi(self, y_pred_test_proba, probs, classifer_name: str = None, app_name: str = None, version_number: int = None):
        """
        The function `performance_evaluation_on_test_set_first_defi` writes the predictions and the probabilities
        to a JSON file.
        :param y_pred_test_proba: the test_data set predictions
        :param preds: the test_data set predictions with the optimal threshold
        :param classifer_name: the classifier name
        :param app_name: the application name
        :param version_number: the version number
        """
        label_mapping = {1: "Attack", 0: "Normal"}
        y_pred_test_labels = [label_mapping[i] for i in y_pred_test_proba]  # Map the labels to their corresponding names

        result_dict = {
            "preds": y_pred_test_labels,
            "probs": probs,
            "names": ["COUTAND", "MARCHAND"],
            "method": classifer_name,
            "appName": app_name,
            "version": version_number
        }

        result_json = json.dumps(result_dict, indent=2)

        # Write the JSON string to the specified output file
        with open(f'{self.output_file}/COUTAND_MARCHAND_{app_name}_{version_number}.json', 'w') as file:
            file.write(result_json)

    def knn_model(self, X_train, X_test, y_train, y_test = None, app_name: str = None, version_number: int = None):
        """
        The function `knn_model` runs the test_data with the KNN classifier. It performs a cross validation
        on the training set, applies the optimal threshold to the test_data set, and evaluates the performance
        of the classifier on the test_data set. It also displays the ROC curve.
        - The optimal threshold is the threshold that maximizes the difference between the true positive rate and the
        false positive rate.
        :param X_train: the training set
        :param X_test: the test_data set
        :param y_train: the training set labels
        :param y_test: the test_data set labels
        :param app_name: the application name
        :param version_number: the version number
        :return: various metrics used to draw the ROC curve
        :rtype: NDArray, Float, Float, Float, String
        """
        # 1. Train the model KNN
        knn = KNeighborsClassifier()
        knn.fit(X_train, y_train)
        print("[i] Training done")

        # 2. Cross validation on the training set to find the optimal threshold
        base_fpr, mean_fpr, mean_auc, optimal_threshold = self.cross_validation(X_train=X_train, y_train=y_train, classifier=KNeighborsClassifier())
        print("[i] Cross validation done")

        # 3. Applying the optimal threshold to the test_data set
        probs = knn.predict_proba(X_test)  # [prb_normal, prb_attack]
        preds = (probs[:, 1] > optimal_threshold)
        print("[i] Prediction done")

        # 4. Evaluate the performance of the classifier on the test_data set
        if not self.is_test_first_challenge:  # because no metrics for test with first challenge data, we don't now the attack flows
            self.performance_evaluation_on_test_set(y_test=y_test, y_pred_test=preds)
        else:
            inverse_probs = [elt[::-1] for elt in probs.tolist()]  # revert the order of seconds tabs [prb_normal, prb_attack] -> [prb_attack, prb_normal]
            self.performance_evaluation_on_test_set_first_defi(y_pred_test_proba=preds, probs=inverse_probs, classifer_name="KNN", app_name=app_name, version_number=version_number)

        return base_fpr, mean_fpr, mean_auc, optimal_threshold, 'KNN'


    def NB_model(self, X_train, X_test, y_train, y_test = None, app_name: str = None, version_number: int = None):
        """
        The function `NB_model` runs the test_data with the NB classifier. It performs a cross validation
        on the training set, applies the optimal threshold to the test_data set, and evaluates the performance
        of the classifier on the test_data set. It also displays the ROC curve.
        - The optimal threshold is the threshold that maximizes the difference between the true positive rate and the
        false positive rate.
        :param X_train: the training set
        :param X_test: the test_data set
        :param y_train: the training set labels
        :param y_test: the test_data set labels
        :param app_name: the application name
        :param version_number: the version number
        :return: various metrics used to draw the ROC curve
        :rtype: NDArray, Float, Float, Float, String
        """
        # 1. Train the model NB
        nb = MultinomialNB()
        nb.fit(X_train, y_train)
        print("[i] Training done")

        # 2. Cross validation on the training set to find the optimal threshold
        base_fpr, mean_fpr, mean_auc, optimal_threshold = self.cross_validation(X_train=X_train, y_train=y_train, classifier=MultinomialNB())
        print("[i] Cross validation done")

        # 3. Applying the optimal threshold to the test_data set
        probs = nb.predict_proba(X_test)  # [prb_normal, prb_attack]
        preds = (probs[:, 1] > optimal_threshold).astype(int)
        print("[i] Prediction done")

        # 4. Evaluate the performance of the classifier on the test_data set
        if not self.is_test_first_challenge:  # because no metrics for test with first challenge data, we don't now the attack flows
            self.performance_evaluation_on_test_set(y_test=y_test, y_pred_test=preds)
        else:
            inverse_probs = [elt[::-1] for elt in probs.tolist()]  # revert the order of seconds tabs [prb_normal, prb_attack] -> [prb_attack, prb_normal]
            self.performance_evaluation_on_test_set_first_defi(y_pred_test_proba=preds, probs=inverse_probs,
                                                               classifer_name="NB", app_name=app_name,
                                                               version_number=version_number)

        return base_fpr, mean_fpr, mean_auc, optimal_threshold, 'NB'

    def run(self, app_names: list[str], test_subsets = None):
        """
        The function `run` runs the general process for the first challenge data nad classical_data. It creates the
        initial subset for each application, trains the KNN and NB models, and evaluates the performance of the models
        on the test_data set. It also displays the ROC curve.
        :param app_names: the list of application names
        :param test_subsets: the test_subsets already created and vectorized
        """
        X_test, y_test, X_train, y_train = [], [], [], []

        # Create the initial subset for each application
        start_time = time.time()
        classic_subsets = self.create_initial_subset(application_names=app_names if 'all' not in app_names else self.accessing.get_applications())
        end_time = time.time()
        print(f"[i] Time to create initial subset : {end_time - start_time} s")

        # Run the test_data for each application in the list
        for app_name in app_names:
            if self.is_test_first_challenge:
                # Train with classic data and test with test data coming from first challenge data
                X_train = np.vstack([classic_subsets[app_name]['X_train'], classic_subsets[app_name]['X_test']])
                y_train = np.concatenate((classic_subsets[app_name]['y_train'], classic_subsets[app_name]['y_test']))
                X_test  = test_subsets[app_name]
            else:
                X_train = classic_subsets[app_name]['X_train']
                y_train = classic_subsets[app_name]['y_train']
                X_test  = classic_subsets[app_name]['X_test']
                y_test  = classic_subsets[app_name]['y_test']

            if self.is_knn:
                start_time = time.time()
                if self.is_test_first_challenge:
                    knn_base_fpr, knn_mean_fpr, knn_mean_auc, knn_optimal_threshold, knn_classifier_name = self.knn_model(X_train=X_train, X_test=X_test, y_train=y_train, app_name=app_name, version_number=2)
                else:
                    knn_base_fpr, knn_mean_fpr, knn_mean_auc, knn_optimal_threshold, knn_classifier_name = self.knn_model(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
                end_time = time.time()
                print(f"[i] Time to run knn : {end_time - start_time} s")

            if self.is_nb:
                start_time = time.time()
                if self.is_test_first_challenge:
                    nb_base_fpr, nb_mean_fpr, nb_mean_auc, nb_optimal_threshold, nb_classifier_name = self.NB_model(X_train=X_train, X_test=X_test, y_train=y_train, app_name=app_name, version_number=2)
                else:
                    nb_base_fpr, nb_mean_fpr, nb_mean_auc, nb_optimal_threshold, nb_classifier_name = self.NB_model(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
                end_time = time.time()
                print(f"[i] Time to run NB : {end_time - start_time} s")

            # Display the ROC curve
            if not self.is_test_first_challenge and self.is_draw_roc_curve:
                self.display_roc_curve(curve_dict=[
                    {'base_fpr': knn_base_fpr, 'mean_tprs': knn_mean_fpr, 'mean_auc': knn_mean_auc, 'classifier_name': knn_classifier_name},
                    {'base_fpr': nb_base_fpr, 'mean_tprs': nb_mean_fpr, 'mean_auc': nb_mean_auc, 'classifier_name': nb_classifier_name}
                ], app_name=app_name)


    ###############################################################################
    # Second challenge
    ###############################################################################
    def performance_evaluation_on_second_challenge(self, y_pred_test_proba, probs, part_number, classifier_name: str = None, version_number: int = None):
        """
        The function `performance_evaluation_on_second_challenge` writes the predictions and the probabilities to
        a JSON file.
        :param y_pred_test_proba: the test_data set predictions
        :param preds: the test_data set predictions with the optimal threshold
        :param classifier_name: the classifier name
        :param app_name: the application name
        :param version_number: the version number
        :param part_number: the part number
        """
        label_mapping = {2: "Victim", 1: "Attack", 0: "Normal"}
        y_pred_test_labels = [label_mapping[i] for i in y_pred_test_proba]  # Map the labels to their corresponding names

        result_dict = {
            "preds": y_pred_test_labels,
            "probs": probs,
            "names": ["COUTAND", "MARCHAND"],
            "method": classifier_name,
            "version": version_number
        }

        result_json = json.dumps(result_dict, indent=2)

        # Write the JSON string to the specified output file
        with open(f'{self.output_file}/splitted/COUTAND_MARCHAND_second_challenge_{version_number}_part_{part_number}.json', 'w') as file:
            file.write(result_json)

    def knn_model_train_second_challenge(self, X_train, y_train, classifier_knn, save_path):
        """
        The function `knn_model_train_second_challenge` trains the KNN model if it doesn't exist with the second challenge data.
        It saves the model to a file with pickle. If the model already exists, it loads the model from the file.
        :param X_train: the training set
        :param y_train: the training set labels
        :param classifier_knn: the KNN model
        :return: the KNN model and the optimal threshold
        :rtype: KNeighborsClassifier
        """
        print(f"[i] KNN model train...")
        classifier_knn.fit(X_train, y_train)
        print("[i] Training done")

        print(f'{sys.getsizeof(classifier_knn)/1024} ko')

        # Save the model to a file
        with open(f"{save_path}.pkl", 'wb') as model_file:
            pickle.dump(classifier_knn, model_file)

        print("[i] KNN model saved")

        return classifier_knn

    def knn_model_test_second_challenge(self, classifier, test_subsets, version_number, part_number):
        """
        The function `knn_model_test_second_challenge` tests the KNN model with the test data coming from second
        challenge data.
        :param classifier: the KNN model
        :param test_subsets: the test data coming from second challenge data
        :param version_number: the version number
        :param part_number: the part number of the file
        :return: the predictions and the probabilities
        :rtype: list, list
        """
        # 3. Applying the optimal threshold to the test_data set
        probs = classifier.predict_proba(test_subsets)  # [prb_normal, prb_attack, prb_victim]
        preds = [np.argmax(proba) for proba in probs]
        print("[i] Prediction done")

        # Transformation proba en [prb_normal, prb_attack, prb_victim] -> [prb_attack, prb_normal, prb_victim]
        new_probs = []
        for proba in probs:
            new_probs.append([proba[1], proba[0], proba[2]])

        # 4. Evaluate the performance of the classifier on the test_data set
        self.performance_evaluation_on_second_challenge(y_pred_test_proba=preds, probs=new_probs, classifier_name="KNN", version_number=version_number, part_number=part_number)

    def run_second_challenge(self):
        """
        The function `run_second_challenge` runs the general process for the second challenge. It creates the initial
        subset for all the data and trains the KNN model. It then tests the KNN model with the test data.
        """
        classifier_nb = KNeighborsClassifier()
        X_train, y_train = [], []
        save_path = os.getenv('KNN_MODEL_SAVE_PATH')

        # if the classifier doesn't exist create it and save it
        if not os.path.exists(f"{save_path}.pkl"):
            # Create the initial subset
            for i in range(16):
                start_time = time.time()
                classic_subsets_tmp = self.create_subset_second_challenge(flows=self.accessing.get_attack_normal_victim_unknown_flows_part(index_part=i))
                print(f"[i] Create initial subset with file part {i} with {len(classic_subsets_tmp['X_train'])} flows")
                X_train = np.vstack([X_train, classic_subsets_tmp['X_train']]) if len(X_train) > 0 else classic_subsets_tmp['X_train']
                y_train = np.concatenate((y_train, classic_subsets_tmp['y_train'])) if len(y_train) > 0 else classic_subsets_tmp['y_train']
                end_time = time.time()
                print(f"[i] Time to create initial subset with file part {i}: {end_time - start_time} s")

            # Train the model
            print(len(X_train))
            start_time = time.time()
            classifier_nb = self.knn_model_train_second_challenge(X_train=X_train, y_train=y_train, classifier_knn=classifier_nb, save_path=save_path)
            end_time = time.time()
            print(f"[i] Time to train the nb: {end_time - start_time} s")
        else:
            # Load the model from the file
            with open(f"{save_path}.pkl", 'rb') as model_file:
                classifier_nb = pickle.load(model_file)

        oParserTestDataSecondChallenge = ParserTestSecondChallenge()
        xml_files = oParserTestDataSecondChallenge.get_xml_files(xml_path=os.getenv('XML_PATH_TEST_SECOND_CHALLENGE_SPLIT'))

        for _, (i, xml_file) in enumerate(xml_files.items()):
            test_subsets = oParserTestDataSecondChallenge.parse_from_xml_test_data(xml_file)
            print(f"[i] Test with file part {i} with {len(test_subsets)} flows")
            start_time = time.time()
            self.knn_model_test_second_challenge(classifier=classifier_nb, test_subsets=test_subsets, version_number=1, part_number=i)
            end_time = time.time()
            print(f"[i] Time to test the knn for the part {i} : {end_time - start_time} s")
