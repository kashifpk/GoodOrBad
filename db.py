from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from os.path import abspath, dirname, join, exists

conn_str = "sqlite:///gob.db"

import migrations


def setup_db():
    "Creates database tables. Called if the database is not setup"

    import models
    #if not exists(join(dirname(abspath(__file__)), 'gob.db')):
    engine = create_engine(conn_str, echo=True)

    migrations.rev1(models.Base.metadata, engine)
    models.Base.metadata.bind = engine
    models.Base.metadata.create_all()
    
    return True

    #return False


def get_db_session():
    "Returns database session object"

    engine = create_engine(conn_str, echo=True)
    Session = sessionmaker(bind=engine)

    return Session()
