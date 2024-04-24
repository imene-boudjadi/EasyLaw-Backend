# app.py

from . import app, db
from flask import request, make_response , send_from_directory
from .services.services import signup, login, token_required, get_all_funds, create_fund
from .services.law import get_all_laws , get_all_laws_with_sum 
from flask import jsonify
from flask_cors import CORS
import os
from .routes.lawRoute import law_routes # Importez la fonction depuis le fichier lawRoutes.py
from .routes.userRoutes import user_routes 
from .routes.newsRoutes import news_routes
from .routes.ijtihadRoutes import ijtihad_routes 
CORS(app)


app.register_blueprint(user_routes, url_prefix='/')
app.register_blueprint(law_routes, url_prefix='/')
app.register_blueprint(news_routes, url_prefix='/')
app.register_blueprint(ijtihad_routes, url_prefix='/')
