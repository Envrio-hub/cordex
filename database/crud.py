__version__='0.1.0'
__author__=['Ioannis Tsakmakis']
__date_created__='2025-06-30'
__last_updated__='2025-06-30'

from database import models, schemas, engine
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from aws_utils.aws_utils import KeyManagementService
from databases_companion.decorators import DatabaseDecorators, DTypeValidator

data_base_decorators = DatabaseDecorators(SessionLocal=engine.SessionLocal, Session=Session)
data_type_validator = DTypeValidator()

class User:

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add(new_user: schemas.UsersBaseCreate, db: Session = None):
        new_user = models.Users(aws_user_name=new_user.aws_user_name, email=new_user.email, account_type=new_user.account_type, subscription_expires_in=new_user.subscription_expires_in)
        db.add(new_user)
    
    @staticmethod
    @data_type_validator.validate_str('aws_user_name')
    @data_base_decorators.session_handler_query
    def get_by_name(name: str, db: Session = None):
        return db.execute(select(models.Users).filter_by(aws_user_name=name)).scalar()
    
    @staticmethod
    @data_type_validator.validate_int('user_id')
    @data_base_decorators.session_handler_query
    def get_by_name(user_id: int, db: Session = None):
        return db.execute(select(models.Users).filter_by(id=user_id)).scalar()
    
    @staticmethod
    @data_type_validator.validate_str('email')
    @data_base_decorators.session_handler_query
    def get_by_email(email: str, db: Session = None):
        return db.execute(select(models.Users).filter_by(email=email)).scalar()