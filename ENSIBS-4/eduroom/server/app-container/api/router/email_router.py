''' Routes for the email stuff '''
__name__      = "email_router.py"
__author__    = "DAOUDI Elyes"
__date__      = "20.11.22"


from fastapi import Depends, APIRouter, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from decouple import config

from api.crud.crud_alert import get_alert_by_name
from api.crud.crud_alert_user import get_user_email_by_alert_id
from api.router.dependencies import get_db
from api.auth.HTTPSessionAuthentication import HTTPSessionAuthentication
from api.constants.rights import Rights


router = APIRouter(
    prefix="/email",
    tags=["email"],
    dependencies=[Depends(HTTPSessionAuthentication([Rights.ADMIN, Rights.SUPERVISOR]))],
    responses={404: {"description": "Not found"}},
)

conf = ConnectionConfig(
    MAIL_USERNAME = "onemail@gmail.fr",
    MAIL_PASSWORD = str(config("PWD_MAIL")),
    MAIL_FROM = "onemail@gmail.fr",
    MAIL_PORT = 587,
    MAIL_SERVER = "gmail.fr",
    MAIL_FROM_NAME="Admin",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


@router.get("/alert/{alert_name}")
async def send_email(alert_name: str, db: Session = Depends(get_db)):
    '''
    Route that sends an email to alert a list of users

    @param db: the database session 
    @param email: a email who follows the schema 
    @param alert_name: name of the alert that will be mentioned in the email 

    @raise HTTPException(422) if the alert is not in the database or if the email list is empty

    @return an JSON response
    '''
    try:
        id_alert = get_alert_by_name(db, alert_name=alert_name).id

    except Exception:
        raise HTTPException(status_code=422, detail=f"[ERROR]\tThe alert doesn't exist !")
        
    list_user_email = []
    [list_user_email.append(elt[0]) for elt in get_user_email_by_alert_id(db, id_alert=id_alert)] # because the db return List[Tuple[res]]
    
    if not list_user_email:
        raise HTTPException(status_code=422, detail=f"[ERROR]\tThere is no one on the email list linked to this alert !")
    
    html = """<p>This email is automatic, please do not reply</p>"""

    message = MessageSchema(
        subject    = alert_name,
        recipients = list_user_email, 
        body       = html,
        subtype    = MessageType.html
    )

    await FastMail(conf).send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
