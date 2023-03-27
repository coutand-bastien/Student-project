''' Alert user Schema for the roads '''
__name__      = "EmailSchema.py"
__author__    = "DAOUDI Elyes"
__date__      = "15.11.22"


from datetime import datetime
from pydantic import BaseModel, Field


class AlertUserBase(BaseModel):
    '''
        Alert user Schema
    '''
    id_user: int = Field(
        description='unique id for an user'
    )

    id_alert: int = Field(
        description='Type of alerte to send by email'
    )


class AlertUserCreate(AlertUserBase):
    '''
        AlertUser schema for the creation of an user in the database.
    '''
    pass


class AlertUserInDB(AlertUserBase):
    '''
        AlertUser schema for the db
    '''
    created_at: datetime = Field(
        default=datetime.utcnow,
        description='Date of the creation for an assignation betwenn an alert and an user'
    )

    class Config:
        orm_mode = True