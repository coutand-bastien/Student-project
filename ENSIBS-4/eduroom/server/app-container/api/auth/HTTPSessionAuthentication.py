''' 
The goal of this file is to check whether the request is authorized or not [ verification of the proteced route ]
'''
__name__      = "session_authentication.py"
__author__    = "COUTAND Bastien"
__date__      = "15.11.22"


from typing import List
from fastapi import Request, HTTPException
from uuid import uuid4
from decouple import config

from api.constants.rights import Rights
from api.crud.crud_user import update_user_is_authentified, update_user_csrf_token
from api.crud.crud_authorization import get_authorization
from api.models.UserModel import UserModel
from api.database.database import SessionLocal
from .auth_handler import decode_jwt, decode_session


class HTTPSessionAuthentication():
    '''
    Class that allows the verification of a user request to an endpoint. It checks the integrity 
    and veracity of the JWT and that the user has the necessary rights to access this page
    '''

    def __init__(self, scopes: List[Rights]):
        '''
        Initilaisation

        :params scopes : Lists of authorised rights for a request.
        '''
        self.scopes = scopes
        self.db     = SessionLocal()
        self.csrf_protection = config('CSRF_PROTECTION') # just for pentest for leo :-)


    def __call__(self, request: Request):
        '''
        Check if the user exist and has the right to do the request.

        :param request: the request.
            
        :raise: HTTPException(401) if the user is not authorized to access this endpoint
        ''' 
        user          = decode_session(self.db, request=request)
        is_logout_url = request.url.path.endswith("/logout")

        if not is_logout_url and not self.has_required_scope(get_authorization(self.db, authorization_id=user.authorization_id).authorization_name):
            raise HTTPException(status_code=401, detail=f"[ERROR]\t{user.user_id_connect} is not authorized to access this endpoint !")
      
        if self.csrf_protection == "True":
            self.verify_token_csrf(user=user, request=request, is_logout_url=is_logout_url)


    def verify_jwt(self, jwt_token: str) -> bool:
        '''
        Check that the jwt is correct

        :params jwt_token : the jwt token.

        :raise HTTPException(501): if there is a problem with the jwt decode, return false
        
        :return true if correct, othersize false
        '''
        try:
            return True if decode_jwt(token=jwt_token) else False

        except Exception as exception:
            print(f"[ERROR]\tInternal error on verify_jwt function --> {exception}")
            raise HTTPException(status_code=501, detail=f"[ERROR]\tInternal error on verify_jwt function !")


    def has_required_scope(self, user_scope: Rights) -> bool:
        '''
        Verify the user has the desired auth scope for this request

        :params user_scope : the user right.

        :return true if the user right exist, othersize false
        '''
        return True if user_scope in self.scopes else False


    def csrf_token_generation(self, user_id: int) -> str:
        '''
        Function that generates a cssrf token, updates it in the database and returns it

        :param db: the database session
        :param user_id: the user who want to connect

        :return the token cssrf
        '''
        token_csrf = uuid4().hex

        # Add in database the unique token_cssrf by user by session
        update_user_csrf_token(self.db, user_id=user_id, csrf_token=token_csrf)

        return token_csrf


    def verify_token_csrf(self, user: UserModel, request: Request, is_logout_url: bool) -> None:
        '''
        Function that check if the user is authentified: 
            * True -> Checks that the csrf token, contained in the header of the request, 
                      is equal to that of the user in the database. And set is_authentified to True

            * False -> Create a csrf token for the user, put it in the database for the user.  
                       And set is_authenticated to False

        :param request : the request.
        :param user: the user associated to the csrf token
        :param is_logout_url: tell if the url for the request is the logout url

        :except : HTTPException(401) if the user is not authorized to access this endpoint

        :return true if correct, othersize false
        '''
        if user.is_authentified:
            # Get the csrf token in the header
            token_csrf = request.headers.get(key="x-csrf-token")

            # if logout, set is_authentified to False in the db for the user
            if is_logout_url:
                update_user_is_authentified(self.db, user_id=user.id, value=False)

            else:
                # verify the token csrf
                if user.user_token_csrf != token_csrf:
                    raise HTTPException(status_code=401, detail=f"[ERROR]\t{user.user_id_connect} is not authorized to access this endpoint !")

        else:
            csrf_token = self.csrf_token_generation(user_id=user.id)

            update_user_csrf_token(self.db, user_id=user.id, csrf_token=csrf_token) # set th token into the db for the user
            update_user_is_authentified(self.db, user_id=user.id, value=True) # set is_authentified to True un the db for the user