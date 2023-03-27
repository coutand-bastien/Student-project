''' Constants for user rights '''
__name__      = "rights.py"
__author__    = "COUTAND Bastien"
__date__      = "05.11.22"


from enum import Enum


class Rights(str, Enum):
    '''
    Constants for the various roles scoped in the application ecosystem
    '''
    
    '''
    @name: NEW_USER,
    @description: A NEW_USER Account.
    '''
    NEW_USER = "NEW_USER",
    '''
    @name: READER,
    @description: Display of room statistics with selection of a set and slots.
    '''
    READER = "READER",
    '''
    @name: SUPERVISOR,
    @description: Display of room statistics with selection of a set and slots, configuration of email alerts, extraction of Excel files..
    '''
    SUPERVISOR = "SUPERVISOR",
    '''
    @name: ADMIN,
    @description: Configuration, management of user rights and CAS server to be used. Feeding of the room database (feedable by import of .ics file) and creation of room groups (e.g.: TD rooms, entity A rooms, entity B reserved rooms)..
    '''
    ADMIN = "ADMIN"
   