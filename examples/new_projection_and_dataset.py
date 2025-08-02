from cordex_database import crud, schemas
from datetime import datetime

new_projection = schemas.ProjectionAttributesCreate(CORDEX_domain='EU', global_climate_model='bgl', regional_climate_model='rcm', experiment_id='rcp85',
                                                    ensemble='anEnsembe',creation_date=datetime(2006,1,1),starting_date=datetime(2006,1,1),ending_date=datetime(2100,12,31))


crud.ProjectionAttributes.add(new_projection=new_projection)

print()
