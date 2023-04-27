import datetime
import sqlalchemy
import secrets
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    created_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    apikey = sqlalchemy.Column(sqlalchemy.String, unique=True, default=secrets.token_urlsafe(25))
    session_key = sqlalchemy.Column(sqlalchemy.String, unique=True, default=secrets.token_urlsafe(25))
