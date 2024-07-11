#!/usr/bin/python3
# @Authors : COUTAND-MARCHAND
# IA et Détection d'Intrusion

import argparse
import os

from utils.config.ElasticConfig import ElasticConfig
from utils.modeling.Indexing import Indexing
from utils.modeling.Accessing import Accessing
from utils.modeling.AccessingSecondChallenge import AccessingSecondChallenge
from utils.modeling.parser.ParserTestDataFirstChallenge import ParserTestDataFirstChallenge
from utils.classifier.Classification import Classification


if __name__ == "__main__":
    oElasticConfig  = ElasticConfig()
    oAccessing      = Accessing(es=oElasticConfig, index_name=os.getenv('INDEX_NAME'))
    oClassification = Classification(es=oElasticConfig, accessing=oAccessing)
    oParserTestData = ParserTestDataFirstChallenge()

    parser = argparse.ArgumentParser(description='Process some integers.')

    # global
    parser.add_argument("--test-data", dest="test", action="store_true", help="Test the connection to XML files and ElasticSearch")
    parser.add_argument("--parse", dest="parse", action="store_true", help="Parse the classical test set")
    parser.add_argument("--parse-second-challenge", dest="parseSecondChallenge", action="store_true", help="Parse the data come from the second challenge")
    parser.add_argument("--diagram", dest="diagram", action="store_true", help="Show diagram")
    parser.add_argument("--draw-curve", dest="drawCurve", action="store_true", help="Draw ROC curve")

    # protocols
    parser.add_argument("--protocols", dest="protocols", action="store_true", help="Get the list of all the (distinct) protocols")
    parser.add_argument("--protocols-stats", dest="protocolsStats", action="store_true", help="Show stats about protocols")
    parser.add_argument("--protocol-flows", dest="protocolFlow", type=str, help="Get the list of flows for a given protocol")
    parser.add_argument("--protocols-flows-card", dest="protocolsFlowCard", action="store_true", help="Get the number of flows for each protocol")
    parser.add_argument("--protocols-payload-size", dest="protocolsPayloadSize", action="store_true", help="Get the source and destination payload size for each protocol")
    parser.add_argument("--protocols-total-bytes", dest="protocolsTotalBytes", action="store_true", help="Get the total source/destination bytes for each protocol")
    parser.add_argument("--protocols-total-packets", dest="protocolsTotalPackets", action="store_true", help="Get the total source/destination packets for each protocol")

    # applications
    parser.add_argument("--applications", dest="applications", action="store_true", help="Get the list of all the (distinct) applications")
    parser.add_argument("--applications-stats", dest="applicationsStats", action="store_true", help="Show stats about applications")
    parser.add_argument("--application-flows", dest="applicationFlow", type=str, help="Get the list of flows for a given application")
    parser.add_argument("--applications-flows-card", dest="applicationsFlowCard", action="store_true", help="Get the number of flows for each application")
    parser.add_argument("--applications-payload-size", dest="applicationsPayloadSize", action="store_true", help="Get the source and destination payload size for each application")
    parser.add_argument("--applications-total-bytes", dest="applicationsTotalBytes", action="store_true", help="Get the total source/destination bytes for each application")
    parser.add_argument("--applications-total-packets", dest="applicationsTotalPackets", action="store_true", help="Get the total source/destination packets for each application")

    # Flow classification params
    parser.add_argument("--classifier", dest="classifier", type=str, help="Classifier (knn/nb/knn,nb,etc...) - default: knn")

    # Flow classification
    parser.add_argument("--flow-classification", dest="flowClassification", action="store_true", help="Classify flows for all applications in the classical test set")
    parser.add_argument("--flow-classification-application", dest="flowClassificationApplication", type=str, help="Classify flows for a given applications (comma separated list) in the classical test set. Exemple: --flow-classification-application 'httpweb,ssh,...")

    # Flow classification test (Défi 1)
    parser.add_argument("--flow-classification-first-challenge", dest="flowClassificationFirstChallenge", action="store_true", help="Classify flows for all applications and test with data coming from test_data")
    parser.add_argument("--flow-classification-application-first-challenge", dest="flowClassificationApplicationFirstChallenge", type=str, help="Classify flows for a given applications (comma separated list) and test with data coming from test_data. Exemple: --flow-classification-application 'httpweb,ssh,...")

    # Flow classification bis (Défi 2)
    parser.add_argument("--flow-classification-bis", dest="flowClassificationBis", action="store_true", help="Classify flows for all applications and test with data coming from second defi data")

    args = parser.parse_args()

    if len(vars(args)) == 0               : parser.print_help()
    if args.test                          : oElasticConfig.test_es_connection(os.getenv('INDEX_NAME'))

    if args.parse                         :
        Indexing = Indexing(es=oElasticConfig, index_name=os.getenv('INDEX_NAME'))
        Indexing.parse()

    if args.parseSecondChallenge               :
        Indexing = Indexing(es=oElasticConfig, index_name=os.getenv('INDEX_NAME_SECOND_CHALLENGE'), is_second_challenge=True)
        Indexing.parse()

    if args.diagram                       : oAccessing.display_diagram()
    if args.protocolsStats                : print(oAccessing.get_stats_protocols())
    if args.protocols                     : print(oAccessing.get_protocols())
    if args.protocolFlow                  : print(oAccessing.get_protocol_flows(protocol=args.protocolFlow))
    if args.protocolsFlowCard             : print(oAccessing.get_protocols_flow_card())
    if args.protocolsPayloadSize          : print(oAccessing.get_protocols_payload_size())
    if args.protocolsTotalBytes           : print(oAccessing.get_protocols_total_bytes())
    if args.protocolsTotalPackets         : print(oAccessing.get_protocols_total_packets())
    if args.applications                  : print(oAccessing.get_applications())
    if args.applicationsStats             : print(oAccessing.get_stats_applications())
    if args.applicationFlow               : print(oAccessing.get_application_flows(application=args.applicationFlow))
    if args.applicationsFlowCard          : print(oAccessing.get_applications_flow_card())
    if args.applicationsPayloadSize       : print(oAccessing.get_application_payload_size())
    if args.applicationsTotalBytes        : print(oAccessing.get_application_total_bytes())
    if args.applicationsTotalPackets      : print(oAccessing.get_application_total_packets())
    if args.drawCurve                     : oClassification.set_draw_roc_curve(True)  # set draw roc curve

    if args.classifier                    :
        lclassifiers = args.classifier.split(',')
        if not lclassifiers:
            oClassification.is_knn_model(True)
        else:
            if 'knn' in lclassifiers : oClassification.is_knn_model(True)
            if 'nb' in lclassifiers  : oClassification.is_nb_model(True)

    if args.flowClassification :
        oClassification.run(app_names=['all'])

    if args.flowClassificationApplication :
        app_names = args.flowClassificationApplication.split(',')
        oClassification.run(app_names=app_names)

    if args.flowClassificationFirstChallenge:
        oClassification.set_test_first_challenge(True)  # set test with diff data
        app_names = args.flowClassificationApplication.split(',')
        dtest_subsets = oParserTestData.parse()
        oClassification.run(app_names=app_names, test_subsets=dtest_subsets)

    if args.flowClassificationApplicationFirstChallenge :
        oClassification.set_test_first_challenge(True)  # set test with diff data
        dtest_subsets = oParserTestData.parse()
        oClassification.run(app_names=[args.flowClassificationApplicationFirstChallenge], test_subsets=dtest_subsets)

    if args.flowClassificationBis:
        oClassification = Classification(es=oElasticConfig, accessing=AccessingSecondChallenge(es=oElasticConfig, index_name=os.getenv('INDEX_NAME_SECOND_CHALLENGE')))
        oClassification.set_is_second_challenge(True)
        oClassification.run_second_challenge()
