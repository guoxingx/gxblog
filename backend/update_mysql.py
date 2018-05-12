#!/usr/bin/python

import os

from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


config_name = os.getenv('APP_CONFIG') or 'test'
mysql = config[config_name].SQLALCHEMY_DATABASE_URI


engine = create_engine(mysql)
session = Session(bind=engine)
try:
    session.execute('drop tables alembic_version')
    session.commit()
except Exception:
    pass

os.system('rm -rf migrations')
os.system('python manager.py db init')
os.system('python manager.py db migrate')
os.system('python manager.py db upgrade')
