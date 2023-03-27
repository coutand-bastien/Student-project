__name__      = "ICalendarParseur.py"
__author__    = "MARCHAND Robin"
__date__      = "05.10.22"


import datetime as dt
import re


class ICalendarParser:    # Fonction qui permet de parser le fichier iCalendar
    def __init__(self, calendar):   # Fonction qui permet de parser le fichier iCalendar
        """_summary_ : Fonction qui permet de parser le fichier iCalendar"""
        self.calendar = calendar # on récupère le fichier iCalendar

    def __parse_event(self, event): # on parse un événement
        """_summary_ : Fonction qui permet de parser un événement

        Args:
            event (str): événement à parser

        Returns:
            _type_: dict
        """
        hiver_inf = dt.date(2022, 10, 29) # date de fin de l'hiver
        hiver_sup = dt.date(2023, 3, 25) # date de début de l'hiver
        event_dict = {} # dictionnaire qui contiendra les informations de l'événement
        for line in event.splitlines(): # splitlines() permet de découper une chaine de caractère en plusieurs lignes
            if ":" in line: # if the line is not empty
                key, value = line.split(":", 1) # split on the first ":"
                if key == "DTSTART" or key == "DTEND": # on récupère les dates
                    event_date = dt.datetime(int(value[0:4]), int(value[4:6]), int(value[6:8]), int(value[9:11]) + 2, int(value[11:-3])) # +2h pour passer de UTC à heure locale
                    if hiver_inf < event_date.date() < hiver_sup: # si l'événement est en hiver
                        event_date = event_date - dt.timedelta(hours=1) # -1h pour passer de l'heure d'hiver à l'heure d'été
                    event_dict[key] = event_date # on ajoute la date à l'event
                elif key == "LOCATION": # on ne garde que le nom de la salle
                    event_dict[key] = re.sub(r"\\,", ",", value) # remplace les \, par des ,

        return event_dict


    def parse(self):
        """_summary_ : Fonction qui permet de parser le fichier iCalendar

        Returns:
            _type_: list
        """
        events = self.calendar.split("END:VEVENT\nBEGIN:VEVENT") # on découpe le fichier iCalendar en plusieurs événements
        return [self.__parse_event(event) for event in events] # on retourne la liste des événements
