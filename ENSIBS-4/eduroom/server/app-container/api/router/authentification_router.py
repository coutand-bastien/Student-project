''' Routes for the authentification stuff '''
__name__      = "authentification_router.py"
__author__    = "COUTAND Bastien"
__date__      = "12.11.22"


from fastapi import Depends, Request, APIRouter, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from cas import CASClient
from decouple import config

from api.auth.auth_handler import sign_jwt
from api.schemas.UserSchema import UserCreate
from api.crud.crud_user import get_user_by_user_id_connect, create_user, get_authorization_by_user
from api.crud.crud_cas import get_cas
from api.router.dependencies import get_db


cas_client     = None
APP_IP         = config('APP_IP')
APP_PORT       = config('APP_PORT')
APP_LOCAL_IP   = config('APP_LOCAL_IP')
APP_LOCAL_PORT = config('APP_LOCAL_PORT')


router = APIRouter (
    prefix="/authentification",
    tags=["authentification"],
    responses={404: {"description": "Not found"}},
)

cas_client = CASClient (
    version=3,
    service_url=f'http://{APP_LOCAL_IP}:{APP_LOCAL_PORT}/authentification/login',
    server_url='',
    verify_ssl_certificate=False
)


@router.get('/login')
async def login(request: Request, ticket: Optional[str] = None, db: Session = Depends(get_db)):
    '''
    The function allows the interfacing with the CAS server and the retrieval of the user, thanks 
    to the tiket_TGT after it.
    It then redirects the user to the right panel according to his role if it exists, otherwise 
    he will have the default role of new user

    Creating the session cookie with a JWT, and sending the cssrf token.

    :param request: the initial request
    :param ticket: [default=None] the TGT ticket from the CAS server
    :param db: the database session
    
    :raise HTTPException(501) if the user is not implemented in the TGT ticket
    :raise HTTPException(400) if the ticket is not correct

    :return an redirection to the GET the goods panel
    '''
    # get the cas addresse in the database
    cas_add = get_cas(db)
    cas_client.server_url = f'https://{cas_add.cas_ip}:{cas_add.cas_port}/cas/login'
 
    # No ticket, the request come from end user, send to CAS login
    if not ticket:
        return RedirectResponse(status_code=307, url=cas_client.get_login_url())

    user, info_cas, _ = cas_client.verify_ticket(ticket=ticket)
    request_header    = request.headers.getlist

    # checks that the user-agents are the same
    if info_cas.get('userAgent') != request_header('user-agent')[0]:
        raise HTTPException(status_code=400, detail='[ERROR]\tNon-authorised, different identities !')

    if not user:
        raise HTTPException(status_code=400, detail='[ERROR]\tFailed to verify ticket !')

    # Login successfully, now redirect according the authorization of the user, new_user if not exist in db.
    try:
        user_in_db = get_user_by_user_id_connect(db, user_id_connect=user)
    except Exception:
        raise HTTPException(status_code=501, detail='[ERROR]\tServer CAS error !')

    if not user_in_db:
        create_user(db, user=UserCreate(user_email=user))

    user_authorization = get_authorization_by_user(db, user_id_connect=user).authorization_name
    redirect_url       = request.url_for(name="new_user_panel")    

    if user_authorization == 'ADMIN'     : redirect_url = request.url_for(name="admin_panel")
    if user_authorization == 'SUPERVISOR': redirect_url = request.url_for(name="supervisor_panel")
    if user_authorization == 'READER'    : redirect_url = request.url_for(name="reader_panel")
    if user_authorization == 'NEW_USER'  : redirect_url = request.url_for(name="new_user_panel")

    request.session['user'] = sign_jwt(user=get_user_by_user_id_connect(db, user_id_connect=user))['access_token']
    return RedirectResponse(status_code=307, url=redirect_url)


@router.get('/logout')
async def logout(request: Request):
    '''
    Route to logout a user, delete the session
    :param request: the initial request
    :return an redirection to the GET /logout_callback
    '''
    request.session.pop('user', None) # clear the session
    cas_logout_url = cas_client.get_logout_url(redirect_url=request.url_for(name='login'))
    return RedirectResponse(status_code=307, url=cas_logout_url)