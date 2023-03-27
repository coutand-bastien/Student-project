''' CRUD operation on alert in the database '''
__name__      = "crud_alert.py"
__author__    = "DAOUDI Elyes"
__date__      = "05.11.22"


from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.models.AlertModel import AlertModel


def get_alerts(db: Session, skip: int = 0, limit: int = 100):
    '''
    Function that retrieves the list of alerts from the database

    @param db: the database session
    @param skip: [default=0] number of skiped line
    @parm limit: [default=100] maximum line in the result

    @raise HTTPException(501) if the request failed in bdd

    @return an list of AlertModel
    '''
    try:
        res = db.query(AlertModel).offset(skip).limit(limit).all()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_alerts function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_alerts function !")

    return res


def get_alert_by_name(db: Session, alert_name: str):
    '''
    Function that retrieves an alert with it's name 

    @param db: the database session
    @param alert_name: the name of the alert

    @raise HTTPException(501) if the request failed in bdd

    @return an alertModel
    '''
    try:
        res = db.query(AlertModel).filter(AlertModel.alert_name == alert_name).first()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_alert_by_name function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_alert_by_name function !")

    return res