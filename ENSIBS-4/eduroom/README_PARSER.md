# ProjetS7
  

## Description


This README file presents the Parser part of the project. The Parser is a program that takes a file as input and returns an excel file as output.

The input is the link of the calendar of the school. The output is a file that contains the information of the calendar in a more readable way.


## Visuals


![](https://i.imgur.com/Y7R6SWa.png)


  
  
  
  

## Installation

  

In order to use this project, you must have Python 3.7 installed on your computer. You can download it \[here\](https://www.python.org/downloads/).

  

\`requirements.txt\` is provided to install the required packages. You can install them with the following command:

  

```bash
pip install -r requirements.txt
```

  

If needed folder \`excels\` and \`ics\` are not created automatically, you can create them manually.

  

If the program is run locally, libreoffice must be installed on the computer in order to open excel files.

  
  

## Usage

  

After all the installations, you can run the program with the following command:

  

```bash
python3 main.py
```

  

We can change the default parameters in the end of the file \`main.py\`:

  

```python
create\_excel\_file(dt.date(2022, 9, 5), dt.date(2022, 10, 5), 50)
```

  

## Roadmap

  

For the future, we would like to download the excel files directly from the website of the university.

![](https://i.imgur.com/jPa491d.png)


But, the most important thing is to print the excel file directly in the box of the printer.

![](https://i.imgur.com/2280zzY.png)

We are close to the goal, but we need to find a way to print the excel file directly in the box of the printer.

We have defined all routes needed by the parseur in order to perform those actions.

  

We are able to send json datas corresponding to user's input on the main page :

![](https://i.imgur.com/w7zBAob.png)
  

## Authors and acknowledgment

  

COUTAND Bastien (coutand.e2100676@etud.univ-ubs.fr)

DAOUDI Elyes (daoudi.e21????@etud.univ-ubs.fr)

DENOUE Enzo (denoue.e21????@etud.univ-ubs.fr)

MARCHAND Robin (marchand.e2101234@etud.univ-ubs.fr)
