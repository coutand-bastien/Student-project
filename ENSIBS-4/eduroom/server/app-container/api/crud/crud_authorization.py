''' CRUD operation on authorization in the database '''
__name__      = "crud_authorization.py"
__author__    = "COUTAND Bastien"
__date__      = "05.11.22"


from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.models.AuthorizationModel import AuthorizationModel


def get_authorizations(db: Session, skip: int = 0, limit: int = 4):
    '''
    Function that retrieves the list of authorizations from the database

    @param db: the database session
    @param skip: [default=0] number of skiped line
    @parm limit: [default=3] maximum line in the result

    @raise HTTPException(501) if the request failed in bdd

    @return an list of AuthorizationModel
    '''
    try:
        res = db.query(AuthorizationModel).offset(skip).limit(limit).all()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_authorizations function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_authorizations function !")

    return res


def get_authorization(db: Session, authorization_id: int):
    '''
    Function that retrieves a authorization from the database based on its id

    @param db: the database session
    @param authorization_id: the id of the authorization who want to show

    @raise HTTPException(501) if the request failed in bdd

    @return an AuthorizationModel
    '''
    try:
        res = db.query(AuthorizationModel).filter(AuthorizationModel.id == authorization_id).first()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_authorization function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_authorization function !")

    return res


def get_authorization_by_name(db: Session, authorization_name: str):
    '''
    Function that retrieves a authorization from the database based on its name

    @param db: the database session
    @param authorization_name: the name of the authorization who want to show

    @raise HTTPException(501) if the request failed in bdd

    @return an AuthorizationModel
    '''
    try:
        res = db.query(AuthorizationModel).filter(AuthorizationModel.authorization_name == authorization_name).first()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_authorization_by_name function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_authorization_by_name function !")

    return res