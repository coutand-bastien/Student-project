''' User schema's for the roads '''
__name__      = "UserSchema.py"
__author__    = "COUTAND Bastien"
__date__      = "07.11.22"


from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    '''
        User Schema
    '''
    user_id_connect: str = Field(
        default="e2100676",
        description='unique id for an user'
    )


class UserCreate(UserBase):
    '''
        User schema for the creation of an user in the database.
    '''
    pass


class UserInDB(UserBase):
    '''
        User schema for the db
    '''
    id: int = Field(
        description='ID in the database of the user'
    )

    user_token_csrf: str = Field(
        description='token cssrf'
    )

    is_authentified: bool = Field(
        default=False,
        description='The user is authenticate or not'
    )

    created_at: datetime = Field(
        default=datetime.utcnow,
        description='Date of the creation for an user'
    )

    updated_at: datetime = Field(
        default=datetime.utcnow,
        description='Date of the update for an user'
    )

    right_id: int = Field(
        description='ID of the right in the database'
    )

    class Config:
        orm_mode = True