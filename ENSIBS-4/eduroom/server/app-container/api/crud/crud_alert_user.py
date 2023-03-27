''' CRUD operation on alert_user in the database '''
__name__      = "crud_alert_user.py"
__author__    = "COUTAND Bastien, DAOUDI Elyes"
__date__      = "12.12.22"


from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.models.AlertUserModel import AlertUserModel
from api.models.UserModel import UserModel
from api.models.AlertModel import AlertModel
from api.schemas.AlertUserSchema import AlertUserCreate


def get_alert_user(db: Session, id_alert: int, id_user: int):
    '''
    Function that retrieves a tuple id_alert and id_user from the database

    :param db: the database session
    :param id_alert: the id of an alert
    :param id_user: the id of an user

    :raise HTTPException(501) if the request failed in bdd

    :return an AlertUserModel
    '''
    try:
        res = db.query(AlertUserModel).filter(AlertUserModel.id_alert == id_alert, AlertUserModel.id_user == id_user).first()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_alert_by_name function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_alert_by_name function !")

    return res


def get_user_email_by_alert_id(db: Session, id_alert: int, skip: int = 0, limit: int = 100):
    '''
    Function that retrieves user email from alert id

    :param db: the database session
    :param id_alert: the id of an alert
    :param skip: [default=0] number of skiped line
    :parm limit: [default=100] maximum line in the result
   
    :raise HTTPException(501) if the request failed in bdd

    :return an list of User emails
    '''
    try:  
        res = db.query(UserModel.user_email).join(AlertUserModel, AlertUserModel.id_user == UserModel.id).filter(AlertUserModel.id_alert == id_alert).offset(skip).limit(limit).all()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_user_email_by_alert_id function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_user_email_by_alert_id function !")

    return res


def get_users_alert_join(db: Session, skip: int = 0, limit: int = 100):
    '''
    Function that retrieves all the user associated with all alerts.

    :param db: the database session
    :param skip: [default=0] number of skiped line
    :parm limit: [default=100] maximum line in the result
   
    :raise HTTPException(501) if the request failed in bdd

    :return an list of user with their alerts
    '''
    try:  
        res = db.query(UserModel.user_id_connect, AlertUserModel.created_at, AlertModel.alert_name)\
                .join(AlertUserModel, AlertUserModel.id_user == UserModel.id)\
                .join(AlertModel, AlertModel.id == AlertUserModel.id_alert)\
                .offset(skip)\
                .limit(limit)\
                .all()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_user_email_by_alert_id function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_user_email_by_alert_id function !")

    return res


def create_alert_user(db: Session, alert_user: AlertUserCreate):
    '''
    Function that associates in a given database a user and an alert

    :param db: the database session
    :param user: the alert user to create
    
    :raise HTTPException(501) if the request failed in bdd
    '''
    try:
        db_alert_user = AlertUserModel(id_user=alert_user.id_user,id_alert=alert_user.id_alert)
        db.add(db_alert_user)
        db.commit()
     
    except Exception as exception:
        print(f"[ERROR]\tInternal error on create_alert_user function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on create_alert_user function !")


def delete_alert_user(db: Session, alert_user: AlertUserCreate):
    '''
    Function that delete an line in the database for the user assign to the alert

    :param db: the database session
    :param user: the user assign to the alert
    :param alert: the alert assign to user
    
    :raise HTTPException(501) if the request failed in bdd
    '''
    try:
        db_alert_user = get_alert_user(db, id_user=alert_user.id_user, id_alert=alert_user.id_alert)
        db.delete(db_alert_user)
        db.commit()
     
    except Exception as exception:
        print(f"[ERROR]\tInternal error on delete_alert_user function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on delete_alert_user function !")