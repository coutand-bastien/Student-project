''' All the dependencies of the app '''
__name__      = "dependencies.py"
__author__    = "COUTAND Bastien"
__date__      = "12.11.22"


from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session

from api.auth.auth_handler import decode_session
from api.crud.crud_authorization import get_authorization
from api.database.database import SessionLocal


templates = Jinja2Templates(directory="api/templates")


async def get_db():
    '''
    Function that return an instance of the database

    :param request: the request

    :return the db.
    '''
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_user_authorization_by_request(db: Session, request: Request):
    '''
    Function that gives the role of the user according to his request

    :param requets : the user request's
    :param db : the session of the database

    :return the authorization of the user wo do the request
    '''
    user = decode_session(db, request=request)
    return get_authorization(db, authorization_id=user.authorization_id).authorization_name