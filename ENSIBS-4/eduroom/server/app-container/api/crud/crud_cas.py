''' CRUD operation on cas in the database '''
__name__      = "crud_cas.py"
__author__    = "COUTAND Bastien"
__date__      = "07.12.22"


from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.models.CASModel import CASModel
from api.schemas.CASSchema import CASCreate


def there_is_cas(db: Session) -> int:
    '''
    Function that count the number of row in db [only one]

    :param db: the database session

    :raise HTTPException(501) if the request failed in bdd

    :return number of row
    '''
    try:
        res = db.query(CASModel).count()

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_alert_by_name function --> {exception}")
        raise HTTPException(status_code=501, detail="[ERROR]\tInternal error on get_alert_by_name function !")

    return res


def get_cas(db: Session):
    '''
    Function that retrieves a cas addresse from the database

    :param db: the database session

    :raise HTTPException(501) if the request failed in bdd

    :return an CASModel
    '''
    try:
        res = db.query(CASModel)[0]

    except Exception as exception:
        print(f"[ERROR]\tInternal error on get_cas function --> {exception}")
        raise HTTPException(status_code=501, detail="[ERROR]\tInternal error on get_cas function !")

    return res


def create_add_cas(db: Session, new_cas_add: CASCreate):
    '''
    Function that create and cas addresse with an ip and a port

    :param db: the database session
    :param new_cas_add: the cas addresse to create
    
    :raise HTTPException(501) if the request failed in bdd

    :return the new CASMODEL in the database
    '''
    try:
        db_cas = CASModel(cas_ip=new_cas_add.cas_ip, cas_port=new_cas_add.cas_port)
        db.add(db_cas)
        db.commit()
        db.refresh(db_cas)
     
    except Exception as exception:
        print(f"[ERROR]\tInternal error on create_add_cas function --> {exception}")
        raise HTTPException(status_code=501, detail="[ERROR]\tInternal error on create_add_cas function !")


def remove_old_cas_add(db: Session):
    '''
    Function that remove the cas in the database

    :param db: the database session
    
    :raise HTTPException(501) if the request failed in bdd
    '''
    try:
        db.query(CASModel).delete()
        db.commit()
     
    except Exception as exception:
        print(f"[ERROR]\tInternal error on remove_old_cas_add function --> {exception}")
        raise HTTPException(status_code=501, detail="[ERROR]\tInternal error on remove_old_cas_add function !")