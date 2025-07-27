from __future__ import annotations

__version__='0.1.7'
__author__=['Ioannis Tsakmakis']
__date_created__='2025-06-30'
__last_updated__='2025-07-26'

from cordex_database.engine import Base
from sqlalchemy import Index, UniqueConstraint, ForeignKey, Integer, String, DateTime, Numeric, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from databases_companion.enum_variables import AccountType, TemporalResolution, AggregationFunction
from datetime import datetime


# Users
class Users(Base):
    __tablename__='users'

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    aws_user_name: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String(500), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(SQLAlchemyEnum(AccountType), nullable=False)
    subscription_expires_in: Mapped[datetime] = mapped_column(DateTime, nullable=False)

class ProjectionAttributes(Base):
    __tablename__ = 'projection_attributes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    CORDEX_domain: Mapped[str] = mapped_column(String(50), nullable=False)
    global_climate_model: Mapped[str] = mapped_column(String(50), nullable=False)
    regional_climate_model: Mapped[str] = mapped_column(String(50), nullable=False)
    experiment_id: Mapped[str] = mapped_column(String(50), nullable=False)
    ensemble: Mapped[str] = mapped_column(String(50), nullable=False)
    creation_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    starting_date: Mapped[datetime]= mapped_column(DateTime, nullable=True)
    ending_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

class Locations(Base):
    __tablename__ = 'locations'

    id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True)
    longitude: Mapped[float] = mapped_column(Numeric(10,6), nullable=False)
    latitude: Mapped[float] = mapped_column(Numeric(10,6), nullable=False)
    elevation: Mapped[int]= mapped_column(Integer, nullable=True)
    geom: Mapped[Geometry] = mapped_column(Geometry("POINT", srid=4326), nullable=False)

    __table_args__ = (
        UniqueConstraint("longitude", "latitude", name="uq_lon_lat"),
    )

# Add a spatial index (only works with MySQL spatial support)
idx_geom = Index("idx_geom", Locations.geom, mysql_using="SPATIAL")  # MySQL requires 'SPATIAL'

class Variables(Base):
    __tablename__ = 'variables'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    standard_name: Mapped[str] = mapped_column(String(50), nullable=False)
    long_name: Mapped[str] = mapped_column(String(200))
    units: Mapped[str] = mapped_column(String(40), nullable=False)

class DataProducts(Base):
    __tablename__='data_products'

    id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True)
    variable_id: Mapped[int] = mapped_column(Integer, ForeignKey(Variables.id), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=False)
    aggregation_function: Mapped[AggregationFunction] = mapped_column(SQLAlchemyEnum(AggregationFunction), nullable=False)
    termporal_resolution: Mapped[TemporalResolution] = mapped_column(SQLAlchemyEnum(TemporalResolution), nullable=False)
    spatial_resolution: Mapped[str] = mapped_column(String(20), nullable=True)

class DataMapping(Base):
    __tablename__ = 'data_mapping'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey(Locations.id), nullable=False)
    variable_id: Mapped[int] = mapped_column(Integer, ForeignKey(Variables.id), nullable=False)
    projection_id: Mapped[int] = mapped_column(Integer, ForeignKey(ProjectionAttributes.id), nullable=False)

    __table_args__ = (
        UniqueConstraint("location_id", "variable_id", "projection_id", name="uq_loc_var_proj"),
    )

    # Relationships (for ORM-style access)
    location = relationship("Locations")
    variable = relationship("Variables")
    projection = relationship("ProjectionAttributes")
