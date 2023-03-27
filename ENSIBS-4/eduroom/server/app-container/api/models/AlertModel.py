''' Email alert model '''
__name__      = "AlertModel.py"
__author__    = "COUTAND Bastien"
__date__      = "12.11.22"


from sqlalchemy import Column, String, Integer, Text

from api.database.database import Base


class AlertModel(Base):
    '''
        Alert model
    '''
    __tablename__ = 'alert'

    id                = Column(Integer, primary_key=True, index=True)
    alert_name        = Column(String(100), index=True, nullable=False)
    alert_description = Column(Text, nullable=False)