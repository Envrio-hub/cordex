from cordex_database import crud, schemas

new_user = schemas.UsersBaseCreate(aws_user_name='4aaac506-6eb0-4db7-a60e-6077b4f9189d',email='admin@envrio.org',account_type='academic',subscription_expires_in='2100-12-31T23:55:00')

crud.User.add(new_user=new_user)