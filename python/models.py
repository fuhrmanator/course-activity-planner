from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.orm import mapper

from database import metadata, db_session


class Planning():
    query = db_session.query_property()

    def __init__(self, uuid, planning_txt, ics_fullpath, mbz_fullpath):
        self.uuid = uuid
        self.planning_txt = planning_txt
        self.ics_fullpath = ics_fullpath
        self.mbz_fullpath = mbz_fullpath

    def as_pub_dict(self):
        pub_dict = {
            'uuid': self.uuid,
            'planning_txt': self.planning_txt,
            }
        return pub_dict


plannings = Table(
    'plannings', metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String),
    Column('planning_txt', String),
    Column('ics_fullpath', String),
    Column('mbz_fullpath', String),
    Column('created_at', DateTime, default=datetime.now),
    Column('modified_at', DateTime, onupdate=datetime.now),
)

mapper(Planning, plannings)
