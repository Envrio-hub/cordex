__version__='0.1.0'
__author__=['Ioannis Tsakmakis']
__date_created__='2025-06-30'
__last_updated__='2025-06-30'

from pydantic import BaseModel, condecimal
from databases_companion.enum_variables import AccountType
from typing import Annotated
from decimal import Decimal
from datetime import datetime

# Base Models
class UsersBase(BaseModel):
    aws_user_name: str
    email: str
    account_type: AccountType
    subscription_expires_in: datetime

class ProjectedParametersBase(BaseModel):
    longitude: Annotated[Decimal, condecimal(max_digits=10, decimal_places=6)]
    latitude: Annotated[Decimal, condecimal(max_digits=10, decimal_places=6)]
    global_model: str
    regional_model: str
    rcp_scenario: str
    parameter: str

# Create Models
class UsersBaseCreate(UsersBase):
    pass
