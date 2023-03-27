''' Routes for the readers '''
__name__      = "reader_router.py"
__author__    = "COUTAND Bastien"
__date__      = "12.11.22"


from fastapi import Depends, APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from api.auth.HTTPSessionAuthentication import HTTPSessionAuthentication
from api.constants.rights import Rights
from api.router.dependencies import templates
from api.router.dependencies import get_db, get_user_authorization_by_request
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import FileResponse



router = APIRouter(
    prefix="/reader_panel",
    tags=["reader_panel"],
    dependencies=[Depends(HTTPSessionAuthentication([Rights.ADMIN, Rights.SUPERVISOR, Rights.READER]))],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def reader_panel(request: Request, db: Session = Depends(get_db)):
    '''
    The panel reader route. Use for the read the occupation of the rooms.

    @authorisation ADMIN, SUPERVISOR, READER

    @return an jsonObject for the front
    '''
    return templates.TemplateResponse("reader/reader_panel.html", {"request": request, "right": get_user_authorization_by_request(db, request=request)})

excel_path = "./api/parser/excels/output.xlsx"
list_rooms_path = "./api/parser/list_rooms.txt"

@router.get("/read_excel")
async def serve_excel():
    # (Generate excel using item.)
    # For now, return a fixed excel.
    headers = {'Content-Disposition': 'attachment; inline; filename="output.xlsx"', 'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
    return FileResponse(excel_path, headers=headers)

@router.get("/liste_salle")
async def liste_salle():
    headers = {'Content-Disposition': 'attachment; inline; filename="list_rooms.txt"', 'Content-Type': 'application/text'}
    return FileResponse(list_rooms_path)

