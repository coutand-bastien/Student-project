''' Routes for the admin '''
__name__      = "admin_router.py"
__author__    = "COUTAND Bastien"
__date__      = "12.11.22"


from fastapi import Body, Depends, HTTPException, APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from socket import inet_pton, inet_aton, AF_INET
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Union

from api.crud.crud_user import get_user_by_user_id_connect, get_users_with_authorizations, update_user_authorization
from api.auth.HTTPSessionAuthentication import HTTPSessionAuthentication
from api.constants.rights import Rights
from api.crud.crud_authorization import get_authorization_by_name, get_authorizations
from api.crud.crud_cas import create_add_cas, remove_old_cas_add
from api.schemas.CASSchema import CASCreate
from api.router.dependencies import get_db, templates, get_user_authorization_by_request
from api.parser.parser import parser

import api.router.authentification_router as auth_r


router = APIRouter(
    prefix="/admin_panel",
    tags=["admin_panel"],
    dependencies=[Depends(HTTPSessionAuthentication([Rights.ADMIN]))],
    responses={404: {"description": "Not found"}}
)


def verif_id_connect(id_connect: str):
    '''
    Function that do an verification of the id connect construction. 
    True if okey, othersize false

    :param id_connect: an id connect (ex: e2100676)

    :return Boolean
    '''
    return id_connect.startswith("e")


def is_valid_ipv4_address(address: str):
    '''
    Function that do an verification of the ip.

    :param address: the ip addresse

    ;return true if is an valid address, othersize false.
    '''
    try:
        inet_pton(AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            inet_aton(address)
        except Exception:
            return False
    except Exception:
        return False

    return True


@router.get("/", response_class=HTMLResponse)
async def admin_panel(request: Request, db: Session = Depends(get_db)):
    '''
    The panel admin route. Use for the authorization management, cas management, create groups in the database.

    :param request: the initial request
    :param db: the database session

    :authorisation ADMIN

    :return an template for the front
    '''
    return templates.TemplateResponse("admin/admin_panel.html", {"request": request, "right": get_user_authorization_by_request(db, request=request)})


@router.get("/rights_management", response_class=HTMLResponse)
async def display_rights_management(request: Request, message: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''
    Function that return the list of user if it's not empty, othersize all the users in the limit size.
      
    :param message: [default=None] an mesage to the user
    :param skip: [default=0] number of skiped line
    :parm limit: [default=100] maximum line in the result
    :param db: the database session

    :authorisation ADMIN

    :return an template for the front
    '''
    users          = get_users_with_authorizations(db, skip=skip, limit=limit)
    authorizations = get_authorizations(db, skip=skip, limit=4)

    return templates.TemplateResponse("admin/rights_management.html", {"request": request, "users": users, "authorizations": authorizations, "message": message, "right": get_user_authorization_by_request(db, request=request)})


@router.post("/rights_management", response_class=HTMLResponse)
async def edit_rights_management(user_id_connect: str = Body(...), authorization: Union[Rights, None] = Body(default=None), db: Session = Depends(get_db)):
    '''
    Function that changes the authorization of a predefined user based on their id_connect (ex:e2100676), if the action in parameter is edit.
    
    :param user_id_connect: the user id connect that represent an user
    :param authorization: [default=None] the authorization to be applies
    :param db: the database session
    
    :authorisation ADMIN

    :raise HTTPException(400) if the user_id_connect if empty or if the user_id_connect is not valid
    :raise HTTPException(404) if there is a bad request

    :return an redirection to the GET /admin_panel/rights_management
    '''
    if user_id_connect == None:
        raise HTTPException(status_code=400, detail="Bad request: empty user_id_connect !")

    if not verif_id_connect(user_id_connect):
        raise HTTPException(status_code=400, detail="Bad request: user_id_connect not valid !")
    
    if authorization not in Rights._value2member_map_:
        raise HTTPException(status_code=404)
    
    user          = get_user_by_user_id_connect(db, user_id_connect=user_id_connect)
    authorization = get_authorization_by_name(db, authorization_name=authorization)

    update_user_authorization(db, user_id=user.id, authorization_id=authorization.id)
    return JSONResponse(content=jsonable_encoder({"message": f"{user_id_connect} Updated !"}))


@router.get("/cas_config", response_class=HTMLResponse)
async def cas_config(request: Request, db: Session = Depends(get_db)):
    '''
    Function that allows the display of the CAS configuration page

    :param request: the initial request
    :param db: the database session

    :authorisation ADMIN

    :return the html page 
    '''
    return templates.TemplateResponse("admin/cas_config.html", {"request": request, "right": get_user_authorization_by_request(db, request=request)})


@router.post("/cas_config")
async def cas_config(request: Request, cas_ip: str = Body(...), cas_port: str = Body(...), db: Session = Depends(get_db)):
    '''
    Function that changes the IP address and port of the CAS to be contacted
    
    :param cas_ip : the IP address of the CAS
    :param cas_port : the port address of the CAS
    :param request: the initial request
    :param db: the database session

    :authorisation ADMIN

    :raise HTTPException(400) if the ip or port are incorrect

    :return disconnects and redirects to the login page of the new case
    '''
    if not is_valid_ipv4_address(cas_ip) or not cas_port.isdigit():
        raise HTTPException(status_code=400, detail="IP or port incorrect !")

    # Delete the old CAS in the database
    remove_old_cas_add(db)

    # Change the cas addresse
    auth_r.cas_client.server_url = f'https://{cas_ip}:{cas_port}/cas/login'

    # Add new cas addresse in the database
    new_cas_add = CASCreate(cas_ip=cas_ip, cas_port=cas_port)
    create_add_cas(db, new_cas_add=new_cas_add)

    return RedirectResponse(status_code=303, url=request.url_for(name='logout'))
    

@router.get("/add_view", response_class=HTMLResponse)
async def add_room(request: Request, db: Session = Depends(get_db)):
    '''
    Function that allows you to add a room to the room set and 
    import a new ICS, to replace the old one. Then restart the 
    parser

    :param request: the initial request
    :param db: the database session

    :authorisation ADMIN
    '''
    return templates.TemplateResponse("admin/add_view.html", {"request": request, "right": get_user_authorization_by_request(db, request=request)})


@router.post("/add_view/add_ics")
async def add_ics(ics_file: UploadFile = File(...)):
    '''
    Function that import a new ICS, to replace the old one. Then restart the 
    parser.

    :param ics_file: the ics file to replace the old one
    '''
    ext = ics_file.filename.split('.')[-1]

    if (ics_file.content_type not in ["text/calendar"]) and (ext != "ics"):
        raise HTTPException(status_code=422, detail="Bad file format, needed xlsx file !")

    if not ics_file.file:
        raise HTTPException(status_code=422, detail="Empty file !")

    contents = ics_file.file.read()
   
    old_ics_file = open('api/parser/ics/ensibs.ics', 'wb')
    old_ics_file.write(contents)
        
    ics_file.file.close()
    old_ics_file.close()

    #parser()


@router.post("/add_view/create_room")
async def create_room(room: str = Body(...), nbr_place: int = Body(...)):
    '''
    Function that allows you to add a room to the set of 
    rooms. Then launch the parser

    :param request: the initial request
    :param room: the room to add
    '''
    if nbr_place < 0:
        raise HTTPException(status_code=422, detail="Incorrect number (> 0) !")

    rooms_file = open('api/parser/list_rooms.txt', 'r+') # r+ = read/write
    lines      = rooms_file.readlines()

    # verify if the room doesn't exist in the file
    for line in lines:
        if room in line:
            raise HTTPException(status_code=422, detail="The room already exist !")
   
    rooms_file.write(f"\n{room} ({nbr_place})")
    rooms_file.close()

    parser()