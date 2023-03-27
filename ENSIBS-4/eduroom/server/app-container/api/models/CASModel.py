''' CAS model for the database '''
__name__      = "CASModel.py"
__author__    = "COUTAND Bastien"
__date__      = "07.12.22"


from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime

from api.database.database import Base


class CASModel(Base):
    '''
        CAS model
    '''
    __tablename__ = 'server_auth'
    
    id         = Column(Integer, primary_key=True, index=True)
    cas_ip     = Column(String(100), unique=False, nullable=False)
    cas_port   = Column(Integer, unique=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)