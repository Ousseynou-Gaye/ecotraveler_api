from flask_sqlalchemy import SQLAlchemy  # pour le stockage
from flask_marshmallow import Marshmallow  # pour la séréalisation
from flask_migrate import Migrate  

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()