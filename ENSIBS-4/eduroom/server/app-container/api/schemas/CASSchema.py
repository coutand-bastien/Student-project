''' CAS schema's for the roads '''
__name__      = "CASSchema.py"
__author__    = "COUTAND Bastien"
__date__      = "07.12.22"


from datetime import datetime
from pydantic import BaseModel, Field


class CASBase(BaseModel):
    '''
        CAS Schema
    '''
    cas_ip: str = Field(
        description='ip for the CAS'
    )

    cas_port: int = Field(
        description='port for the CAS'
    )


class CASCreate(CASBase):
    '''
        CAS schema for the creation of an CAS in the database.
    '''
    pass


class CASInDB(CASBase):
    '''
        CAS schema for the db
    '''
    id: int = Field(
        description='ID in the database of the CAS'
    )

    created_at: datetime = Field(
        default=datetime.utcnow,
        description='Date of the creation for an CAS'
    )

    class Config:
        orm_mode = True