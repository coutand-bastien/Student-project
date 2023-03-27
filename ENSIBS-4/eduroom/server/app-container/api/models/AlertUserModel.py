''' Link betwenn User model and Email Alert model '''
__name__      = "AlertUserModel.py"
__author__    = "COUTAND Bastien"
__date__      = "12.11.22"


from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, DateTime

from api.database.database import Base


class AlertUserModel(Base):
    '''
        AlertUserModel model
    '''
    __tablename__ = 'alert_user'

    id_user    = Column(Integer, ForeignKey('user.id'), primary_key=True, autoincrement=True)
    id_alert   = Column(Integer, ForeignKey('alert.id'), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)