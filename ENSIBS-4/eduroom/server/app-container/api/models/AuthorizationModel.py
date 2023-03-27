''' Right model for the database '''
__name__      = "AuthorizationModel.py"
__author__    = "COUTAND Bastien"
__date__      = "19.10.22"


from uuid import UUID
from sqlalchemy import Column, String, Integer, Text

from api.database.database import Base


class AuthorizationModel(Base):
    '''
        Authorization model
    '''
    __tablename__ = 'authorization'

    id                        = Column(Integer, primary_key=True, index=True)
    authorization_name        = Column(String(100), index=True, nullable=False)
    authorization_description = Column(Text, nullable=False)