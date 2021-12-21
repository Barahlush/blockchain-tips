
from pony.orm import Database, Required, Optional
from flask_login import UserMixin
from datetime import datetime

db = Database()


class User(db.Entity, UserMixin):
    login = Required(str, unique=True)
    password = Required(str)
    name = Required(str)
    surname = Required(str)
    eth_address = Required(str, unique=True)
    photo_url = Optional(str)
    last_login = Optional(datetime)
    hash = Optional(str, unique=True)
