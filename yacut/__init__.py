from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from yacut.settings import Config

app = Flask(
    __name__,
    static_folder='../static',
    template_folder='../templates'
)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import views, views_api, models, forms