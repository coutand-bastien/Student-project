''' CRUD operation on user to the database '''
__name__      = "crud_user.py"
__author__    = "COUTAND Bastien"
__date__      = "07.11.22"


from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.models.UserModel  import UserModel
from api.models.AuthorizationModel import AuthorizationModel
from api.schemas.UserSchema import UserCreate
from .crud_authorization import get_authorization_by_name


def get_users(db: Session, skip: int = 0, limit: int = 100):
    '''
    Function that retrieves the list of users from the database

    @param db: the database session
    @param skip: [default=0] number of skiped line
    @parm limit: [default=100] maximum line in the result

    @raise HTTPException(501) if the request failed in bdd

    @return an list of UserModel
    '''
    try:
        res = db.query(UserModel).offset(skip).limit(limit).all()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_users function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_users function !")

    return res


def get_users_with_authorizations(db: Session, skip: int = 0, limit: int = 100):
    '''
    Function that retrieves the list of users with their authorization from the database

    @param db: the database session
    @param skip: [default=0] number of skiped line
    @parm limit: [default=3] maximum line in the result

    @raise HTTPException(501) if the request failed in bdd

    @return an list of UserModel
    '''
    try:
        res = db.query(UserModel.user_id_connect, UserModel.created_at, UserModel.updated_at, AuthorizationModel.authorization_name).join(AuthorizationModel, UserModel.authorization_id == AuthorizationModel.id).order_by(UserModel.user_id_connect.asc()).offset(skip).limit(limit).all()
    
    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_users_with_authorizations function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_users_with_authorizations function !")

    return res


def get_user(db: Session, user_id: int):
    '''
    Function that retrieves a user from the database based on its id

    @param db: the database session
    @param user_id: the id of the user who want to show

    @raise HTTPException(501) if the request failed in bdd

    @return an UserModel
    '''
    try:
        res = db.query(UserModel).filter(UserModel.id == user_id).first()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_user_by_user_id_connect function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_user_by_user_id_connect function !")

    return res


def get_user_by_user_id_connect(db: Session, user_id_connect: str):
    '''
    Function that retrieves a user from the database based on its user id conect (ex: e2100676)
    
    @param db: the database session
    @param user_id_connect: the user id connect of the user who want to show
    
    @raise HTTPException(501) if the request failed in bdd

    @return an UserModel
    '''
    try:
        res = db.query(UserModel).filter(UserModel.user_id_connect == user_id_connect).first()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_user_by_user_id_connect function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_user_by_user_id_connect function !")

    return res


def get_authorization_by_user(db: Session, user_id_connect: str):
    '''
    Function that retrieves an authorization from the database based on an user and its user id conect (ex: e2100676)
    
    @param db: the database session
    @param user_id_connect: the user id connect of the user who want to get his authorization
    
    @raise HTTPException(501) if the request failed in bdd

    @return an UserModel
    '''
    try:
        res = db.query(UserModel.user_id_connect, AuthorizationModel.authorization_name).join(AuthorizationModel, UserModel.authorization_id == AuthorizationModel.id).filter(UserModel.user_id_connect == user_id_connect).first()
    
    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_authorization_by_user function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on get_authorization_by_user function !")

    return res


def update_user_csrf_token(db: Session, user_id: int, csrf_token: str) -> None:
    '''
    Function that update an cssrf_token of one user in the database.

    @param db: the database session
    @param user_id: the user to whom we will change the cssrf_token
    @param cssrf_token: the cssrf_token to be applie

    @raise HTTPException(501) if the request failed in bdd
    '''
    try:
        db.query(UserModel).filter(UserModel.id == user_id).update({"user_token_csrf": csrf_token}, synchronize_session='fetch')
        db.commit()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on update_user_csrf_token function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on update_user_csrf_token function !")


def update_user_is_authentified(db: Session, user_id: int, value: bool) -> None:
    '''
    Function that update the is_authentified of one user in the database.

    @param db: the database session
    @param user_id: the user to whom we will change the cssrf_token
    @apram value: True or False

    @raise HTTPException(501) if the request failed in bdd
    '''
    try:
        db.query(UserModel).filter(UserModel.id == user_id).update({"is_authentified": value}, synchronize_session='fetch')
        db.commit()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on update_user_is_authentified function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on update_user_is_authentified function !")


def update_user_authorization(db: Session, user_id: int, authorization_id: int = 4) -> None:
    '''
    Function that update an authorization of one user in the database.

    @param db: the database session
    @param user_id: [default=4] the user to whom we will change the authorization
    @param authorization_id: the authorization to be applie

    @raise HTTPException(501) if the request failed in bdd
    '''
    try:
        db.query(UserModel).filter(UserModel.id == user_id).update({"authorization_id": authorization_id}, synchronize_session='fetch')
        db.commit()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on update_user_authorization function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on update_user_authorization function !")


def create_user(db: Session, user: UserCreate):
    '''
    Function that create an user in the database, with the default authorization : NEW_USER.

    @param db: the database session
    @param user: the user to create

    @raise HTTPException(501) if the request failed in bdd

    @return the new UserModel in the database
    '''
    try:
        authorization = get_authorization_by_name(db, "NEW_USER") # get the database objet from the new_user authorization
        db_user = UserModel(user_id_connect=user.user_id_connect, authorization_id=authorization)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    except Exception as exception:
        print(f"[ERROR]\tInternal error on create_user function --> {exception}")
        raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on create_user function !")

    return db_user
