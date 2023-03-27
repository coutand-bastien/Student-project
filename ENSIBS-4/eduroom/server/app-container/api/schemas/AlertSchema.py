''' Alert Schema for the roads '''
__name__      = "EmailSchema.py"
__author__    = "DAOUDI Elyes"
__date__      = "15.11.22"


from pydantic import BaseModel, Field


class AlertBase(BaseModel):
    ''' 
        Alert schema
    '''
    alert_name: str = Field (
        default="UPDATE_RIGHT_ALERT",
        description='Type of alerte to send by email'
    )


class AlertInDB(AlertBase):
    '''
        Alert schema for the db
    '''
    id: int = Field(
        description='ID in the database of the alert'
    )

    alert_description: str = Field(
        default="",
        description='Description of the alert mail'
    )
    
    class Config:
        orm_mode = True