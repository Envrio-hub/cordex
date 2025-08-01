__version__='0.1.0'
__author__=['Ioannis Tsakmakis']
__date_created__='2025-06-30'
__last_updated__='2025-06-30'

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from aws_utils.aws_utils import SecretsManager
from dotenv import load_dotenv
from envrio_logger.logger import alchemy
import os


# Load environemntal variables
load_dotenv()

# Access database configuration info
db_conf = SecretsManager().get_secret(secret_name=os.getenv('db_name'))

# Creating sqlalchemy engine
try:
    engine = create_engine(url=f'{db_conf['DBAPI']}://{db_conf['username']}:{db_conf['password']}@{db_conf['host-ip']}/{os.getenv('db_name')}',
                           pool_size=30, max_overflow=5, pool_recycle=72000)
except Exception as e:
    alchemy.error(f"Error occured during engine creation: {str(e)}")

SessionLocal = scoped_session(sessionmaker(bind=engine))

class Base(DeclarativeBase):
    pass