''' User model for the database '''
__name__      = "UserModel.py"
__author__    = "COUTAND Bastien"
__date__      = "12.11.22"


from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey

from api.database.database import Base


class UserModel(Base):
    '''
        User model
    '''
    __tablename__ = 'user'
    
    id               = Column(Integer, primary_key=True, index=True)
    user_id_connect  = Column(String(100), unique=True, nullable=False)
    user_email       = Column(String(100), unique=True, nullable=True)
    user_token_csrf  = Column(String(100), unique=True, nullable=True)
    is_authentified  = Column(Boolean, default=False, nullable=False)
    created_at       = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)    
    authorization_id = Column(Integer, ForeignKey('authorization.id'))