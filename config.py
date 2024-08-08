from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()
migrate = Migrate()

bcrypt = Bcrypt()

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///distributex.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_COMPACT = False
