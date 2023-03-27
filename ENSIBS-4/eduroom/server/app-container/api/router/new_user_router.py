''' Routes for the new users '''
__name__      = "new_user_router.py"
__author__    = "COUTAND Bastien"
__date__      = "12.11.22"


from fastapi import Depends, APIRouter

from api.auth.HTTPSessionAuthentication import HTTPSessionAuthentication
from api.constants.rights import Rights


router = APIRouter(
    prefix="/new_user_panel",
    tags=["new_user_panel"],
    dependencies=[Depends(HTTPSessionAuthentication([Rights.ADMIN, Rights.SUPERVISOR, Rights.READER, Rights.NEW_USER]))],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def new_user_panel():
    '''
    The panel new user route. Use for the user who have no rights.

    @authorisation ADMIN, SUPERVISOR, READER, NEW_USER
    
    @return an jsonObject for the front
    '''
    return {"Message": "Hello new user"}