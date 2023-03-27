''' Routes for the supervisor '''
__name__      = "supervisor_router.py"
__author__    = "COUTAND Bastien"
__date__      = "20.11.22"


from fastapi import Depends, APIRouter, Request, HTTPException, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from api.auth.HTTPSessionAuthentication import HTTPSessionAuthentication
from api.router.dependencies import templates, get_db, get_user_authorization_by_request
from api.constants.rights import Rights

from api.schemas.UserSchema import UserBase
from api.schemas.AlertSchema import AlertBase
from api.schemas.AlertUserSchema import AlertUserInDB

from api.crud.crud_alert import get_alert_by_name, get_alerts
from api.crud.crud_alert_user import create_alert_user, get_users_alert_join, delete_alert_user
from api.crud.crud_user import get_user_by_user_id_connect

from api.parser.parser import parser


router = APIRouter(
    prefix="/supervisor_panel",
    tags=["supervisor_panel"],
    dependencies=[Depends(HTTPSessionAuthentication([Rights.ADMIN, Rights.SUPERVISOR]))],
    responses={404: {"description": "Not found"}},
)


def get_alert_rate():
    '''
    Function that read the alert rate in the file configExcel.
    Then launch the parser

    :return the alert rate value
    '''
    config_file = open('api/parser/config/configExcel.txt', 'r')
    value = config_file.readlines()[2]
    config_file.close()

    return value


@router.get("/", response_class=HTMLResponse)
async def supervisor_panel(request: Request, db: Session = Depends(get_db)):
    '''
    The panel supervisor route. Use for the mails alertes, read statistiques and extract excel.

    :param request: the initial request
    :param db: the database session

    :authorisation ADMIN, SUPERVISOR

    :return an HTMLResponse for the front
    '''
    return templates.TemplateResponse("supervisor/supervisor_panel.html", {"request": request, "right": get_user_authorization_by_request(db, request=request)})


@router.post("/assign_alert/alert_rate")
async def alert_rate(alert_rate: int = Body(...)):
    '''
    Modify the alert rate in the file and then launch the parser

    :param alert_rate: the new value of alert rate

    :raise HTTPException(422) The alert rate is not in [1, 100] !

    :authorisation ADMIN, SUPERVISOR
    '''
    if (alert_rate < 1 or alert_rate > 100):
        raise HTTPException(status_code=422, detail="The alert rate is not in [1, 100] !")

    config_file = open('api/parser/config/configExcel.txt', 'r')
    lines = config_file.readlines()
    config_file.close()

    lines[2] = str(alert_rate)

    config_file = open('api/parser/config/configExcel.txt', 'w')
    
    for elt in lines:
        config_file.write(elt)

    config_file.close()

    parser()


@router.get("/assign_alert")
async def assign_alert(request: Request, db: Session = Depends(get_db)):
    '''
    The panel supervisor route. Use for assign an alert to a user.

    :param request: the initial request
    :param db: the database session

    :authorisation ADMIN, SUPERVISOR

    :return an HTMLResponse for the front
    '''
    return templates.TemplateResponse("supervisor/assign_alert.html", {
        "request": request, 
        "user_alert_list": get_users_alert_join(db), 
        "alerts": get_alerts(db),
        "alert_rate": get_alert_rate(),
        "right": get_user_authorization_by_request(db, request=request)
    })

@router.post("/assign_alert")
def assign_email_alerte(user: UserBase, alert: AlertBase, db: Session = Depends(get_db)):
    '''
    Route to assign an email to an alert session

    :param db: the database session
    :param user: a user who follows the schema
    :param alert: an alert who follows the schema

    :raise HTTPException(422) if the user or the alert are not in the database

    :return an JSON response
    '''
    try:
        user_id  = get_user_by_user_id_connect(db, user_id_connect=user.user_id_connect).id
    except Exception:
        raise HTTPException(status_code=422, detail=f"[ERROR]\tThe user doesn't exist !")

    try:
        id_alert = get_alert_by_name(db, alert_name=alert.alert_name).id
    except Exception:
        raise HTTPException(status_code=422, detail=f"[ERROR]\tThe alert doesn't exist !")

    alert_user_schema = AlertUserInDB(id_user=user_id, id_alert=id_alert)
    create_alert_user(db, alert_user=alert_user_schema)

    return JSONResponse(content=jsonable_encoder({"message": f"{user_id} Updated !"}))


@router.delete("/assign_alert")
def assign_email_alerte(user: UserBase, alert: AlertBase, db: Session = Depends(get_db)):
    '''
    Route to delete an alert assign to an user

    :param db: the database session
    :param user: a user who follows the schema
    :param alert: an alert who follows the schema

    :raise HTTPException(422) if the user or the alert are not in the database

    :return an JSON response
    '''
    try:
        user_id  = get_user_by_user_id_connect(db, user_id_connect=user.user_id_connect).id
    except Exception:
        raise HTTPException(status_code=422, detail=f"[ERROR]\tThe user doesn't exist !")

    try:
        id_alert = get_alert_by_name(db, alert_name=alert.alert_name).id
    except Exception:
        raise HTTPException(status_code=422, detail=f"[ERROR]\tThe alert doesn't exist !")

    alert_user_schema = AlertUserInDB(id_user=user_id, id_alert=id_alert)
    delete_alert_user(db, alert_user=alert_user_schema)

    return JSONResponse(content=jsonable_encoder({"message": f"{user_id} Delete !"}))
