from __future__ import annotations

__version__='0.1.0'
__author__=['Ioannis Tsakmakis']
__date_created__='2025-06-30'
__last_updated__='2025-06-30'

from database.engine import Base
from sqlalchemy import Index, Integer, String, DateTime, Numeric, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column
from databases_companion.enum_variables import AccountType
from datetime import datetime

# Users
class Users(Base):
    __tablename__='users'

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    aws_user_name: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String(500), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(SQLAlchemyEnum(AccountType), nullable=False)
    subscription_expires_in: Mapped[datetime] = mapped_column(DateTime, nullable=False)

class VariablesMetadata(Base):
    __tablename__ = 'variables_metadata'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    longitude: Mapped[float] = mapped_column(Numeric(10,6), nullable=False)
    latitude: Mapped[float] = mapped_column(Numeric(10,6), nullable=False)
    global_model: Mapped[str] = mapped_column(String(50), nullable=False)
    regional_model: Mapped[str] = mapped_column(String(50), nullable=False)
    rcp_scenario: Mapped[str] = mapped_column(String(50), nullable=False)
    ensemble: Mapped[str] = mapped_column(String(50), nullable=False)
    variable: Mapped[str] = mapped_column(String(50), nullable=False)

    __table_args__ = (
        Index('idx_coordinates', 'longitude', 'latitude'),
    )