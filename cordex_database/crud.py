__version__='0.1.1'
__author__=['Ioannis Tsakmakis']
__date_created__='2025-06-30'
__last_updated__='2025-07-22'

from database import models, schemas, engine
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from geoalchemy2.functions import ST_GeomFromText, ST_Distance_Sphere
from aws_utils.aws_utils import KeyManagementService
from databases_companion.decorators import DatabaseDecorators, DTypeValidator

data_base_decorators = DatabaseDecorators(SessionLocal=engine.SessionLocal, Session=Session)
data_type_validator = DTypeValidator()

class User:

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add(new_user: schemas.UsersCreate, db: Session = None):
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

class ProjectionAttributes():

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add(new_projection: schemas.ProjectionAttributesCreate, db: Session = None):
        new_projection = models.ProjectionAttributes(CORDEX_domain= new_projection.CORDEX_domain, global_climate_model= new_projection.global_climate_model,
                                                     regional_climate_model=new_projection.regional_climate_model, experiment_id=new_projection.experiment_id,
                                                     ensemble=new_projection.ensemble, creation_date=new_projection.creation_date,
                                                     starting_date=new_projection.starting_date, ending_date=new_projection.ending_date)
        db.add(new_projection)

    @staticmethod
    @data_base_decorators.session_handler_query
    def get_all(db: Session = None):
        return db.execute(select(models.ProjectionAttributes)).scalars().all()

    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_str('global_climate_model','regional_climate_model','CORDEX_domain','experiment_id','ensemble')
    def get_by_gcm_rcm_CD_expID_ens(global_climate_model: str, regional_climatte_model: str, CORDEX_domain: str, experiment_id: str, ensemble: str, db: Session = None):
        result = db.execute(select(models.ProjectionAttributes).filter(models.ProjectionAttributes.global_climate_model==global_climate_model,
                                                                       models.ProjectionAttributes.regional_climate_model==regional_climatte_model,
                                                                       models.ProjectionAttributes.CORDEX_domain==CORDEX_domain,
                                                                       models.ProjectionAttributes.experiment_id==experiment_id,
                                                                       models.ProjectionAttributes.ensemble==ensemble)).scalars()
        if result:
            return result

class Locations:

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add(new_location: schemas.LocationsCreate, db: Session = None):
        new_location = models.Locations(longitude=new_location.longitude, latitude=new_location.latitude, elevation=new_location.elevation, geom=ST_GeomFromText(f'POINT({new_location.longitude} {new_location.latitude})', 4326))
        db.add(new_location)

    @staticmethod
    @data_type_validator.validate_decimal('longitude', 'latitude')
    def find_nearest(lon_query: float, lat_query: float, db: Session = None):
        nearest = (
            db.query(
                Locations,
                ST_Distance_Sphere(
                    models.Locations.geom,
                    ST_GeomFromText(f'POINT({lon_query} {lat_query})', 4326)
                ).label("distance")
            )
            .order_by("distance")
            .first()
        )
        return nearest

class Variables:

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add(new_variable: schemas.VariablesCreate, db: Session = None):
        new_variable = models.Variables(projection_id=new_variable.projection_id, standard_name=new_variable.standard_name, long_name=new_variable.long_name, units=new_variable.units)
        db.add(new_variable)

    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_str('standard_name')
    def get_by_standard_name(standard_name: str, db: Session = None):
        return db.execute(select(models.Variables).filter_by(standard_name=standard_name)).scalars().all()
    
    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('projection_id')
    def get_by_projection_id(projection_id: int, db: Session = None):
        return db.execute(select(models.Variables).filter_by(projection_id=projection_id)).scalars().all()
    
    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    @data_type_validator.validate_str('standard_name')
    def delete_by_standard_name(standard_name: str, db: Session = None):
        result = db.execute(select(models.Variables).filter_by(standard_name=standard_name)).scalars().all()
        if result:
            db.delete(result)

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    @data_type_validator.validate_int('projection_id')
    def delete_by_projection_id(projection_id: int, db: Session = None):
        result = db.execute(select(models.Variables).filter_by(projection_id=projection_id)).scalars().all()
        if result:
            db.delete(result)

class DataMapping:

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add_new_entry(new_netry: schemas.DataMappingCreate, db: Session = None):
        new_netry = models.DataMapping(location_id=new_netry.location_id, variable_id=new_netry.variable_id, projection_id=new_netry.projection_id)
        db.add(new_netry)

    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('id')
    def get_by_id(id: int, db: Session = None):
        return db.execute(select(models.DataMapping).filter_by(id=id)).scalars()
    
    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_str('standard_name')
    def get_by_standard_name(standard_name: str, db: Session = None):
        variable_id = db.execute(select(models.Variables).filter_by(standard_name=standard_name)).scalars()
        return db.execute(select(models.DataMapping).filter_by(variable_id=variable_id)).scalars()
    
    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('projection_id')
    def get_by_projection_id(projection_id: int, db: Session = None):
        return db.execute(select(models.DataMapping).filter_by(projection_id=projection_id)).scalars().all()

