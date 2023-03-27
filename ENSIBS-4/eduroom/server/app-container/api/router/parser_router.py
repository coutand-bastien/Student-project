''' Routes for the readers '''
__name__      = "parser_router.py"
__author__    = "MARCHAND Robin"
__date__      = "12.11.22"


from fastapi import Depends, APIRouter, HTMLResponse
from starlette.requests import Request

from api.auth.HTTPSessionAuthentication import HTTPSessionAuthentication
from api.constants.rights import Rights
from api.router.dependencies import templates


router = APIRouter(
    prefix="/api",
    tags=["api"],
    dependencies=[Depends(HTTPSessionAuthentication([Rights.ADMIN, Rights.SUPERVISOR, Rights.READER]))],
    responses={404: {"description": "Not found"}},
)


@router.get("/salles")
async def salles(request : Request):
    """_summary_ : Display the list of rooms

    Args:
        request (Request): Request

    Returns:
        _type_: HTML
    """
    if not request.session.get('username', None):
        return HTMLResponse("<h1>Vous n'avez pas le droit d'accéder à cette page</h1>")
    return templates.TemplateResponse("salles.html", {"request": request, "rooms": list_unique_rooms_without_multi_rooms})