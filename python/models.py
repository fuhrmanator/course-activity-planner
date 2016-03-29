from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.orm import mapper

from database import metadata, db_session


class Planning():
    query = db_session.query_property()

    def __init__(self, uuid, user_id, planning_txt, ics_fullpath,
                 mbz_fullpath, name, year, semester, group):
        self.uuid = uuid
        self.user_id = user_id
        self.planning_txt = planning_txt
        self.ics_fullpath = ics_fullpath
        self.mbz_fullpath = mbz_fullpath
        self.name = name
        self.year = year
        self.semester = semester
        self.group = group

    def as_pub_dict(self):
        pub_dict = {
            'uuid': self.uuid,
            'planning_txt': self.planning_txt,
            'name': self.name,
            'year': self.year,
            'semester': self.semester,
            'group': self.group,
            'created_at': self.created_at,
            }
        return pub_dict


plannings = Table(
    'plannings', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', String),
    Column('uuid', String),
    Column('planning_txt', String),
    Column('ics_fullpath', String),
    Column('mbz_fullpath', String),
    Column('name', String),     # LOG-121
    Column('year', String),     # 2016
    Column('semester', String),  # 02
    Column('group', String),    # 06
    Column('created_at', DateTime, default=datetime.now),
    Column('modified_at', DateTime, onupdate=datetime.now),
)

mapper(Planning, plannings)
