''' Initialzation of the database '''
__name__      = "init_db.py"
__author__    = "COUTAND Bastien"
__date__      = "12.11.22"


from sqlalchemy.orm import Session

from api.models.UserModel import UserModel
from api.models.AuthorizationModel import AuthorizationModel
from api.models.AlertModel import AlertModel
from api.models.AlertUserModel import AlertUserModel
from api.models.CASModel import CASModel
from api.crud.crud_user import get_user_by_user_id_connect
from api.crud.crud_authorization import get_authorization_by_name
from api.crud.crud_alert import get_alert_by_name
from api.crud.crud_alert_user import get_alert_user
from .database import SessionLocal


USERS = ['e2100676', 'e2485631', 'e2141548', 'e2134567', 'e2109763', 'e2112348', 'e2146852', 'e2153897', 'e2175423', 'e2198657', 'e2134689', 'e1452658', 'e2145863', 'e2147856']


def init_db(db: Session = SessionLocal()) -> None:
    '''
    Initialization of the database with some examples
    :param db: the session of the database
    '''  
    init_alert(db)
    init_authorization(db)
    init_user(db)
    init_alert_user(db)
    init_cas(db)
        

def init_user(db: Session) -> None:
    '''
    Initialization of the table user with some examples
    :param db: the session of the database
    '''
    base_users_info = [ # {id_connect, authorization_id, user_email}
        (USERS[0], 1, 'coutand.e2100676@etud.univ-ubs.fr'), 
        (USERS[1], 2, 'e.e2105487@etud.univ-ubs.fr'), 
        (USERS[2], 3, 'z.2141548@etud.univ-ubs.fr'), 
        (USERS[3], 4, 'r.e2134567@etud.univ-ubs.fr'),
        (USERS[4], 1, 'j.smith@gmail.com'),
        (USERS[5], 2, 'm.johnson@yahoo.com'),
        (USERS[6], 3, 't.brown@outlook.com'),
        (USERS[7], 4, 'r.taylor@aol.com'),
        (USERS[8], 1, 'j.azerty@gmail.com'),
        (USERS[9], 2, 'm.pierre@yahoo.com'),
        (USERS[10], 3, 't.lenon@outlook.com'),
        (USERS[11], 4, 'r.pokemon@aol.com'),
        (USERS[12], 3, 't.des@outlook.com'),
        (USERS[13], 4, 'r.julian@aol.com')
    ]
    add_list = []

    for user in base_users_info:
        if not get_user_by_user_id_connect(db, user_id_connect=user[0]): 
            add_list.append(UserModel(user_id_connect=user[0], authorization_id=user[1], user_email=user[2]))
        
    db.add_all(add_list)
    db.commit()


def init_authorization(db: Session) -> None:
    '''
    Initialization of the table authorization with some examples
    :param db: the session of the database
    '''
    base_authorization_info = [  # {right_name, description}
        ('ADMIN', 'Configuration, management of user rights and CAS server to be used. Feeding of the room database and creation of room groups e.g.: TD rooms, entity A rooms, entity B reserved rooms'), 
        ('SUPERVISOR', 'Display of room statistics with selection of a set and slots, configuration of email alerts, extraction of Excel files'), 
        ('READER', 'Display of room statistics with selection of a set and slots'), 
        ('NEW_USER', 'a new user account')
    ]
    add_list = []

    for authorization in base_authorization_info:
        if not get_authorization_by_name(db, authorization_name=authorization[0]): 
            add_list.append(AuthorizationModel(authorization_name=authorization[0], authorization_description=authorization[1]))
    
    db.add_all(add_list)
    db.commit()


def init_alert(db: Session) -> None:
    '''
    Initialization of the table alert with some examples
    :param db: the session of the database
    '''
    base_alert_info = [ # {alert_name, alert_description}
       ('UPDATE_RIGHT_ALERT', 'Alert for the update of a right'), 
       ('THRESHOLD_EXCEEDED_ALERT', 'Alert for the threshold exceeded of a day')
    ]
    add_list = []

    for alert in base_alert_info:
        if not get_alert_by_name(db, alert_name=alert[0]): 
            add_list.append(AlertModel(alert_name=alert[0], alert_description=alert[1]))
    
    db.add_all(add_list)
    db.commit()


def init_alert_user(db: Session) -> None:
    '''
    Initialization of the table alert_user with some examples
    :param db: the session of the database
    '''
    base_alert_user_info = [ # {id_user, id_alert}
        (get_user_by_user_id_connect(db, user_id_connect=USERS[0]).id, 1), 
        (get_user_by_user_id_connect(db, user_id_connect=USERS[1]).id, 2),
        (get_user_by_user_id_connect(db, user_id_connect=USERS[2]).id, 2)
    ]
    add_list = []

    for au in base_alert_user_info:
        if not get_alert_user(db, id_user=au[0], id_alert=au[1]): 
            add_list.append(AlertUserModel(id_user=au[0], id_alert=au[1]))
    
    db.add_all(add_list)
    db.commit()


def init_cas(db: Session) -> None:
    '''
    Initialization of the table cas with some examples
    :param db: the session of the database
    '''
    db.add(CASModel(cas_ip="127.0.0.1", cas_port=8444))
    db.commit()