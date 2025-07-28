__version__='0.1.6'
__author__=['Ioannis Tsakmakis']
__date_created__='2025-06-30'
__last_updated__='2025-07-28'

from pydantic import BaseModel, condecimal
from databases_companion.enum_variables import AccountType, AggregationFunction, TemporalResolution
from typing import Annotated, Optional
from decimal import Decimal
from datetime import datetime


# Base Models
class UsersBase(BaseModel):
    aws_user_name: str
    email: str
    account_type: AccountType
    subscription_expires_in: datetime

class ProjectionAttributesBase(BaseModel):
    CORDEX_domain: str
    global_climate_model: str
    regional_climate_model: str
    experiment_id: str
    ensemble: str
    creation_date: datetime
    starting_date: Optional[datetime] = None
    ending_date: Optional[datetime] = None

class LocationsBase(BaseModel):
    longitude: Annotated[Decimal, condecimal(max_digits=10, decimal_places=6)]
    latitude: Annotated[Decimal, condecimal(max_digits=10, decimal_places=6)]
    elevation: Optional[int] = None

class VariablesBase(BaseModel):
    standard_name: str
    long_name: str
    units: str

class DataProductsBase(BaseModel):
    variable_id: int
    short_name: str
    aggregation_function: AggregationFunction
    temporal_resolution: TemporalResolution
    spatial_resulution: Optional[str] = None

class DataMappingBase(BaseModel):
    projection_id: int
    location_id: int
    data_product_id: int

# Create Models
class UsersCreate(UsersBase):
    pass

class ProjectionAttributesCreate(ProjectionAttributesBase):
    pass

class LocationsCreate(LocationsBase):
    pass

class VariablesCreate(VariablesBase):
    pass

class DataProductsCreate(DataProductsBase):
    pass

class DataMappingCreate(DataMappingBase):
    pass