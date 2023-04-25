import datetime
import sqlalchemy
import secrets
from .db_session import SqlAlchemyBase


def generate_apikey():
    return secrets.token_urlsafe(25)


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    created_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    apikey = sqlalchemy.Column(sqlalchemy.String, unique=True, default=generate_apikey())
    session_key = sqlalchemy.Column(sqlalchemy.String, unique=True, default=generate_apikey())
