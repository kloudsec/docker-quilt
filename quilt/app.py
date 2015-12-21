import os
from cfg import SQL_URI
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from werkzeug.wsgi import SharedDataMiddleware


app = Flask(__name__)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                    {'/media/': os.path.join(os.path.dirname(__file__), 'media')})
db = create_engine(SQL_URI,
                   poolclass=StaticPool,
                   connect_args={'check_same_thread': False}
                   )
Base = declarative_base()
Session = sessionmaker(bind=db)
session = Session()


def save(o):
    session.add(o)
    session.commit()


def delete(o):
    session.delete(o)
    session.commit()
