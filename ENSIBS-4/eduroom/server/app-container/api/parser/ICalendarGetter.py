__name__      = "iCalendarGetter.py"
__author__    = "MARCHAND Robin"
__date__      = "05.10.22"


from requests import get
from time import time
from os import path


class ICalendarGetter:
    """_summary_ : Fonction qui permet de récupérer le fichier iCalendar

    Returns:
        _type_: iCalendar
    """
    TIME_BEFORE_REFRESH = 60 * 10000000  # in seconds, 10 minutes by default
    def __init__(self, url, filename): # Fonction qui permet de récupérer le fichier iCalendar
        """_summary_ : Fonction qui permet de récupérer le fichier iCalendar

        Args:
            url ([type]): [description]
            filename ([type]): [description]
        """
        self.url = url # url of the iCalendar file
        self.filename = filename # the file where the calendar will be saved
        self.calendar = None # the calendar is not loaded


    # Fonction qui permet de récupérer le fichier iCalendar
    def get_calendar(self):
        """_summary_ : Fonction qui permet de récupérer le fichier iCalendar

        Returns:
            _type_: iCalendar
        """
        try:
            last_update = path.getmtime(self.filename) # unit in seconds
        except FileNotFoundError: # if the file doesn't exist
            last_update = 0 # we force the update

        if self.calendar is None and time() - last_update < self.TIME_BEFORE_REFRESH: # if the file is not loaded or if it's too old
            with open(self.filename, 'r') as f: # we open the file
                self.calendar = f.read() # and we read it

        elif self.calendar is None:     # if the file is not loaded
            self.calendar = get(self.url).text # we download it
            with open(self.filename, 'w') as f: # and we save it
                f.write(self.calendar) # in the file

        return self.calendar # we return the calendar