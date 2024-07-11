# Run and configure the project

## Summary

- [Configure the project](#Configure the project)
    - [First step : Install the project](#First step Install the project)
    - [Second step : Install elastic search with docker](#Second step Install elastic search with docker)
    - [Third step : Add the data in the project](#Third step Add the data in the project)
- [Run the project](#Run the project)
- [Example of use in the terminal](#Example of use in the terminal)
  - [Classification with the classic data](#Classification with the classic data)
  - [Use the api function](#Use the api function)
  - [Classification with the first challenge data](#Classification with the first challenge data)
  - [Classification with the second challenge data](#Classification with the second challenge data)
  - [run the API using the web server](#run the API using the web server)
- [Verify the json data](#Verify the json data)
- [Code documentation](#Code documentation)

## Configure the project

You have two options to run the project, but first you need to install the dependencies and the data with the following command:

### First step : Install the project
```bash
projet@projet-PC:~$ git clone TODO
projet@projet-PC:~$ cd IA_project
projet@projet-PC:~/IA_project$ python3 -m venv .venv
projet@projet-PC:~/IA_project$ source .venv/bin/activate
projet@projet-PC:~/IA_project$ pip install -r requirements.txt
```

### Second step : Install elastic search with docker

Cf. [ELASTIC_CONFIGURATION.md](ELASTIC_CONFIGURATION.md)

### Third step : Add the data in the project

You need to add the data in the data folder. You can find some [data about the project](https://www.unb.ca/cic/datasets/ids-2017.html) here : [./src/data/classic_data.zip](../src/data/classic_data.zip)

```bash
projet@projet-PC:~/IA_project$ cd data
projet@projet-PC:~/IA_project/data$ unzip classic_data.zip
```

The ISCX files contain detailed flow information in XML format for each day. The flows have been generated (from the packet files (pcap)) using IBM  QRadar appliance. The ”Tag” column indicates whether the flow is normal or part of an attack scenario.

The XML files contain the following: ”appName”, ”totalSourceBytes”, ”totalDestinationBytes”, ”totalDestinationPackets”, ”totalSourcePackets”, ”sourcePayloadAsBase64”, ”destinationPayloadAsBase64”, ”destinationPayloadAsUTF”,”direction”, ”sourceTCPFlagsDescription”, ”destinationTCPFlagsDescription”, ”source” ,”protocolName” ,”sourcePort”, ”destination” ,”destinationPort”, ”startDateTime”, ”stopDateTime”, ”Tag”

The ISCX data is available as a bunch of XML files :
- TestbedSatJun12Flows.xml
- TestbedSunJun13Flows.xml
- TestbedMonJun14Flows.xml
- TestbedTueJun15-1Flows.xml
- TestbedTueJun15-2Flows.xml
- TestbedWedJun16-1Flows.xml
- TestbedThuJun17-1Flows.xml
- TestbedWedJun16-2Flows.xml
- TestbedThuJun17-2Flows.xml

There are various tests available for testing the project: like [first challenge](FIRST_CHALLENGE) test ssh and httpWeb available in the [./src/data/test_data.zip](../src/data/test_data.zip) or [second challenge](SECOND_CHALLENGE) data available in the [./src/data/second_challenge_data.zip](./src/data/second_challenge_data.zip)

## Run the project

### WARNING, first add the data to elastic search
```bash
projet@projet-PC:~/IA_project$ python3 main.py --parse
# or for the second challenge data
projet@projet-PC:~/IA_project$ python3 main.py --parse-second-challenge
```

```bash
projet@projet-PC:~/IA_project$ python3 main.py
```

You have many options with the terminal, you can see them with the following command:
```
usage: main.py [-h] [--test-data] [--parse] [--parse-second-challenge] [--diagram] [--draw-curve] [--protocols] [--protocols-stats] [--protocol-flows PROTOCOLFLOW] [--protocols-flows-card] [--protocols-payload-size]
               [--protocols-total-bytes] [--protocols-total-packets] [--applications] [--applications-stats] [--application-flows APPLICATIONFLOW] [--applications-flows-card] [--applications-payload-size] [--applications-total-bytes]
               [--applications-total-packets] [--classifier CLASSIFIER] [--flow-classification] [--flow-classification-application FLOWCLASSIFICATIONAPPLICATION] [--flow-classification-test]
               [--flow-classification-application-test FLOWCLASSIFICATIONAPPLICATIONTEST] [--flow-classification-bis]

Process some integers.

options:
  -h, --help                            show this help message and exit
  --test-data                           Test the connection to XML files and ElasticSearch
  --parse                               Parse XML files and send data to ElasticSearch
  
  # API functions
  --protocols                           Get the list of all the (distinct) protocols
  --protocols-stats                     Stats about the protocols
  --protocol-flows PROTOCOLFLOW         Get the list of flows for a given protocol
  --protocols-flows-card                Get the number of flows for each protocol
  --protocols-payload-size              Get the source and destination payload size for each protocol
  --protocols-total-bytes               Get the total source/destination bytes for each protocol
  --protocols-total-packets             Get the total source/destination packets for each protocol
  --applications                        Get the list of all the (distinct) applications
  --applications-stats                  Stats about the applications
  --application-flows APPLICATIONFLOW   Get the list of flows for a given application
  --applications-flows-card             Get the number of flows for each application
  --applications-payload-size           Get the source and destination payload size for each application
  --applications-total-bytes            Get the total source/destination bytes for each application
  --applications-total-packets          Get the total source/destination packets for each application
  --diagram                             Show diagram of the ”ranked” distribution #Flows v.s. #Packets, from the largest flow on the left to the smallest to the right.
    
  # Classification with the classic data
  --flow-classification                                              Classify flows for all applications
  --flow-classification-application FLOWCLASSIFICATIONAPPLICATION    Classify flows for a given applications (comma separated list). Exemple: --flow-classification-application 'httpweb,ssh,...
  --classifier CLASSIFIER                                            Classifier (knn/nb/knn,nb,etc...) - default: knn
  --draw-curve                                                       Draw ROC curve
    
  # Test with the first challenge data
  --flow-classification-application-first-challenge FLOWCLASSIFICATIONAPPLICATIONTEST  Classify flows for a given applications (comma separated list) and test with data coming from test_data. Exemple: --flow-classification-application 'httpweb,ssh,...
  --flow-classification-first-challenge                                                Classify flows for all applications and test with data coming from test_data
  
  # Test with the second challenge data
  --parse-second-challenge      Parse second challenge data
  --flow-classification-bis     Classify flows for all applications and test with data coming from second challenge data
```

## Example of use in the terminal
### Classification with the classic data
Classify flows for all applications using knn classifier and draw ROC curve.
```bash
projet@projet-PC:~/IA_project$ python3 main.py --parse
projet@projet-PC:~/IA_project$ python3 main.py --classifier knn --flow-classification-application ssh --draw-curve
```

### Use the api function
Get the list of all the (distinct) protocols
```bash
projet@projet-PC:~/IA_project$ python3 main.py --protocols
```

Get the list of flows for a given protocol
```bash
projet@projet-PC:~/IA_project$ python3 main.py --protocol-flows tcp
```

etc...

### Classification with the first challenge data
Classify flows for all applications and test with data coming from test_data, for httpWeb and ssh applications.
```bash
projet@projet-PC:~/IA_project$ python3 main.py --parse
projet@projet-PC:~/IA_project$ python3 main.py --flow-classification-application-first-challenge httpweb,ssh
```

At the end you can see the results in the [results](../results) folder.

### Classification with the second challenge data
First you need to divide the data for the training and the test. Because the files are too big to be loaded in memory.
```bash
# change the file input in the ./src/utils/tools/xml_splitter.py file
# one for test and one for train
projet@projet-PC:~/IA_project$ python3 ./src/utils/tools/xml_splitter.py 
```

And then classify flows for all applications and test with data coming from test_data.
```bash
projet@projet-PC:~/IA_project$ python3 main.py --parse-second-challenge
projet@projet-PC:~/IA_project$ python3 main.py --flow-classification-bis
```

The result are split also, so you need to concatenate them with the following command:
```bash
projet@projet-PC:~/IA_project$ python3 ./src/utils/tools/json_concat.py
```

At the end you can see the results in the [results](../results) folder.

### run the API using the web server
```bash
projet@projet-PC:~/IA_project$ uvicorn src.web-api.server:app --reload
```
Then you can go to http://localhost:8000/docs to see the documentation and test the API.

## Verify the json data
You can verify the json data with the following command:
```bash
projet@projet-PC:~/IA_projet/src/utils/tools$ python3 json_compatible.py ../../../results/COUTAND_MARCHAND_ssh_1.json 
```
see [check_json_result.py](../src/utils/check_json_result.py) for more information.

# Code documentation
click here to see the [code documentation](...)