''' 
    This file is responsible for signing , encoding , decoding and returning JWTS
'''
__name__      = "auth_handler.py"
__author__    = "COUTAND Bastien"
__date__      = "15.10.22"


import time
import jwt

from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Dict
from decouple import config
from cryptography.hazmat.primitives import serialization

from api.schemas.UserSchema import UserBase
from api.crud.crud_user import get_user_by_user_id_connect


# Constants
JWT_ALGORITHM = config('ALGORITHM')
RSA_PWD       = config('RSA_PWD').encode()

RSA_PRIVATE_KEY_FILE = open('.ssh/id_rsa', 'r').read()
RSA_PUBLIC_KEY_FILE  = open('.ssh/id_rsa.pub', 'r').read()

RSA_PRIVATE_KEY = serialization.load_ssh_private_key(RSA_PRIVATE_KEY_FILE.encode(), password=RSA_PWD)
RSA_PUBLIC_KEY  = serialization.load_ssh_public_key(RSA_PUBLIC_KEY_FILE.encode())


def token_response(token: str):
    '''
    Function that return the jwt token of an user in JSON Object..

    :param token : the jwt token of an user
    :return token
    '''
    return { 'access_token': token }


def sign_jwt(user: UserBase) -> Dict[str, str]:  
    '''
    Signature of the jwt. It's construct with an user id connect (ex: e2100676) and
    an expires times.

    :param user : the user who want to sign is JWT
    :return the user jwt token
    '''
    payload = {
        'user_id_connect': user.user_id_connect,
        'expires': time.time() + 6000
    }

    token = jwt.encode(payload, key=RSA_PRIVATE_KEY, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str) -> dict:
    '''
    Decode of the jwt. It's construct with an user id connect (ex: e2100676) and
    an expires times. If the expire_time is expire, return None

    :param token : the jwt token of an user

    :return the decode token or None
    '''
    try:
        decoded_token = jwt.decode(token, key=RSA_PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    
    except jwt.InvalidTokenError as exception:
        print('[ERROR]\tJWT token invalid !')
        raise exception


def decode_session(db: Session, request: Request):
    '''
    Function that decodes the user's session cookie.

    :param db: the database session
    :param request : the request.

    :except : HTTPException(403) if the jwt token is invalid, expired or not authenticated
    :except : HTTPException(401) if the user doesn't have a session cookie
            
    :return the user
    '''
    try:
        credentials_session = request.session['user']

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get session function --> {exception}")
        raise HTTPException(status_code=401, detail="[ERROR]\t No session cookie !")

    if not credentials_session:
        raise HTTPException(status_code=403, detail="[ERROR]\tInvalid authorization code !")

    jwt = decode_jwt(token=credentials_session)

    if not jwt:
        raise HTTPException(status_code=403, detail="[ERROR]\tInvalid or expired token !")

    # Look if the user exist in the database and if he has the necessary authorization
    user = get_user_by_user_id_connect(db, jwt["user_id_connect"])

    if not user:
       raise HTTPException(status_code=403, detail="[ERROR]\tNot authenticated !")
    
    return user