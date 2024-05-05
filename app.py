# app.py
from .services.services import *
from . import app, db
from flask import request, make_response , send_from_directory
from flask import jsonify
from flask_cors import CORS
import os
from .routes.adminRoutes import moderator_routes
from .routes.userRoutes import user_routes

from flask_migrate import Migrate

CORS(app)

app.register_blueprint(user_routes, url_prefix='/')
app.register_blueprint(moderator_routes, url_prefix='/')


migrate = Migrate(app, db)
