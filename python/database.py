from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, create_session

engine = None
metadata = MetaData()

db_session = scoped_session(
    lambda: create_session(autocommit=False, autoflush=False, bind=engine))


def init_engine(uri):
    global engine
    engine = create_engine(uri, convert_unicode=True, pool_recycle=60)
    return engine


def init_db():
    global engine
    metadata.create_all(bind=engine)


def clear_db():
    global engine
    for tbl in reversed(metadata.sorted_tables):
        engine.execute(tbl.delete())
