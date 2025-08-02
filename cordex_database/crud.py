__version__='0.1.8'
__author__=['Ioannis Tsakmakis']
__date_created__='2025-06-30'
__last_updated__='2025-08-01'

from cordex_database import models, schemas, engine
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from geoalchemy2.functions import ST_GeomFromText, ST_Distance_Sphere
from aws_utils.aws_utils import KeyManagementService
from databases_companion.decorators import DatabaseDecorators, DTypeValidator
from databases_companion.enum_variables import TemporalResolution, AggregationFunction, ConfirmationStatus
import os, hashlib

data_base_decorators = DatabaseDecorators(SessionLocal=engine.SessionLocal, Session=Session)
data_type_validator = DTypeValidator()

def hash_user_sub(user_sub: str) -> str:
    return hashlib.sha256(user_sub.encode()).hexdigest()

class User:

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add(new_user: schemas.UsersCreate, db: Session = None):
        enc_user_sub = KeyManagementService().encrypt_data(new_user.user_sub, key_id=os.getenv('key_management_service_key'))
        user_sub_hash = hash_user_sub(new_user.user_sub)
        email_hash = hash_user_sub(new_user.email)
        new_user = models.Users(user_sub=enc_user_sub, user_hash=user_sub_hash, email=email_hash, confirmation_status=new_user.confirmation_status,
                                account_type=new_user.account_type, subscription_expires_in=new_user.subscription_expires_in)
        db.add(new_user)
    
    @staticmethod
    @data_type_validator.validate_str('user_sub')
    @data_base_decorators.session_handler_query
    def get_by_user_sub(user_sub: str, db: Session = None):
        user_sub_hash = hash_user_sub(user_sub)
        return db.execute(select(models.Users).filter_by(user_sub=user_sub_hash)).scalar()
    
    @staticmethod
    @data_type_validator.validate_str('email')
    @data_base_decorators.session_handler_query
    def get_by_email(email: str, db: Session = None):
        email_hash = hash_user_sub(email)
        return db.execute(select(models.Users).filter_by(email=email_hash)).scalar()
    
    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    @data_type_validator.validate_str('email')
    def update_configuration_status_by_email(email: str, status: ConfirmationStatus, db: Session = None):
        email_hash = hash_user_sub(email)
        db.execute(update(models.Users).where(models.Users.email==email_hash).values(configuration_status=status))

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
    def get_all_ids(db: Session = None):
        return db.execute(select(models.ProjectionAttributes.id)).scalars().all()

    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_str('global_climate_model','regional_climate_model','CORDEX_domain','experiment_id','ensemble')
    def get_by_gcm_rcm_CD_expID_ens(global_climate_model: str, regional_climate_model: str, CORDEX_domain: str, experiment_id: str, ensemble: str, db: Session = None):
        return db.execute(select(models.ProjectionAttributes).filter(models.ProjectionAttributes.global_climate_model==global_climate_model,
                                                                       models.ProjectionAttributes.regional_climate_model==regional_climate_model,
                                                                       models.ProjectionAttributes.CORDEX_domain==CORDEX_domain,
                                                                       models.ProjectionAttributes.experiment_id==experiment_id,
                                                                       models.ProjectionAttributes.ensemble==ensemble)).scalars().first()

class Locations:

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add(new_location: schemas.LocationsCreate, db: Session = None):
        new_location = models.Locations(longitude=new_location.longitude, latitude=new_location.latitude, elevation=new_location.elevation, geom=ST_GeomFromText(f'POINT({new_location.longitude} {new_location.latitude})', 4326))
        db.add(new_location)

    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('location_id')
    def get_by_id(location_id: int, db: Session = None):
        return db.execute(select(models.Locations).filter_by(id=location_id)).scalars().first()

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
    
    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_decimal('longitude','latitude')
    def check_registration_status(longitude: float, latitude: float, db: Session = None):
        return db.execute(select(models.Locations).filter(models.Locations.latitude==latitude,
                                                                  models.Locations.longitude==longitude)).scalars().first()

class Variables:

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add(new_variable: schemas.VariablesCreate, db: Session = None):
        new_variable = models.Variables(standard_name=new_variable.standard_name, long_name=new_variable.long_name, units=new_variable.units)
        db.add(new_variable)

    @staticmethod
    @data_base_decorators.session_handler_query
    def get_all_ids(db: Session = None):
        return db.execute(select(models.Variables.id)).scalars().all()
    
    @staticmethod
    @data_base_decorators.session_handler_query
    def get_all_variables(db: Session = None):
        return db.execute(select(models.Variables)).scalars().all()

    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('variable_id')
    def get_by_variable_id(variable_id: int, db: Session = None):
        return db.execute(select(models.Variables).filter_by(id=variable_id)).scalars().first()

    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_str('standard_name')
    def get_by_standard_name(standard_name: str, db: Session = None):
        return db.execute(select(models.Variables).filter_by(standard_name=standard_name)).scalars().first()
    
    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    @data_type_validator.validate_str('standard_name')
    def delete_by_standard_name(standard_name: str, db: Session = None):
        result = db.execute(select(models.Variables).filter_by(standard_name=standard_name)).scalars().first()
        if result:
            db.delete(result)

class DataProducts:

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add(new_data_product: schemas.DataProductsCreate, db: Session = None):
        new_data_product = models.DataProducts(variable_id=new_data_product.variable_id, short_name=new_data_product.short_name, aggregation_function=new_data_product.aggregation_function,
                                               temporal_resolution=new_data_product.temporal_resolution, spatial_resolution=new_data_product.spatial_resolution)
        db.add(new_data_product)

    @staticmethod
    @data_base_decorators.session_handler_query
    def get_all_data_products(db: Session = None):
        return db.execute(select(models.DataProducts)).scalars().all()
    
    @staticmethod
    @data_base_decorators.session_handler_query
    def get_all_ids(db: Session = None):
        return db.execute(select(models.DataProducts.id)).scalars().all()

    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('variable_id')
    def get_by_variable_id(variable_id: int, db: Session = None):
        return db.execute(select(models.DataProducts).filter_by(variable_id=variable_id)).scalars().all()
    
    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('variable_id')
    @data_type_validator.validate_str('short_name')
    def get_by_variable_id_and_short_name(variable_id: int, short_name: str, db: Session = None):
        return db.execute(select(models.DataProducts).filter(models.DataProducts.variable_id==variable_id,
                                                             models.DataProducts.short_name==short_name)).scalars().first()
    
    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('variable_id')
    @data_type_validator.validate_str('short_name','spatial_resolution')
    def get_by_all(variable_id: int, short_name: str, aggregation_function: AggregationFunction, temporal_resolution:TemporalResolution, spatial_resolution: str, db: Session = None):
        return db.execute(select(models.DataProducts).filter(models.DataProducts.variable_id==variable_id,
                                                            models.DataProducts.short_name==short_name,
                                                            models.DataProducts.aggregation_function==aggregation_function,
                                                            models.DataProducts.temporal_resolution==temporal_resolution,
                                                            models.DataProducts.spatial_resolution==spatial_resolution)).scalars().first()

class DataMapping:

    @staticmethod
    @data_base_decorators.session_handler_add_delete_update
    def add_new_entry(new_netry: schemas.DataMappingCreate, db: Session = None):
        new_netry = models.DataMapping(projection_id=new_netry.projection_id, location_id=new_netry.location_id, data_product_id=new_netry.data_product_id)
        db.add(new_netry)

    @staticmethod
    @data_base_decorators.session_handler_query
    def get_all_ids(db: Session = None):
        return db.execute(select(models.DataMapping.id)).scalars().all()

    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('id')
    def get_by_id(id: int, db: Session = None):
        return db.execute(select(models.DataMapping).filter_by(id=id)).scalars()
    
    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('projection_id','location_id','data_product_id')
    def get_by_location_projection_variable_id(projection_id: int, location_id: int, data_product_id: int, db: Session = None):
        return db.execute(select(models.DataMapping).filter(models.DataMapping.location_id==location_id,
                                                            models.DataMapping.projection_id==projection_id,
                                                            models.DataMapping.data_product_id==data_product_id)).scalars().first()


    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('projection_id','data_product_id')
    def get_by_projection_and_data_product_id(projection_id: int, data_product_id: int, db: Session = None):
        return db.execute(select(models.DataMapping).filter(models.DataMapping.projection_id==projection_id,
                                                            models.DataMapping.data_product_id==data_product_id)).scalars().all()

    @staticmethod
    @data_base_decorators.session_handler_query
    @data_type_validator.validate_int('projection_id')
    def get_by_projection_id(projection_id: int, db: Session = None):
        return db.execute(select(models.DataMapping).filter_by(projection_id=projection_id)).scalars().all()

