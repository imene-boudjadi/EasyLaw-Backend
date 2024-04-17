# app.py

from . import app, db
from flask import request, make_response , send_from_directory
from .services.services import signup, login, token_required, get_all_funds, create_fund
from .services.law import get_all_laws , get_all_laws_with_sum 
from flask import jsonify
from flask_cors import CORS
import os


CORS(app)

@app.route("/signup", methods=["POST"])
def signup_route():
    data = request.json
    response, status_code = signup(data)
    return make_response(response, status_code)

@app.route("/login", methods=["POST"])
def login_route():
    auth = request.json
    response, status_code = login(auth)
    return make_response(response, status_code)

@app.route("/funds", methods=["GET"])
@token_required
def get_all_funds_route(current_user):
    response_data = get_all_funds(current_user)
    return make_response(response_data)

@app.route("/funds", methods=["POST"])
@token_required
def create_fund_route(current_user):
    data = request.json
    response_data = create_fund(data, current_user)
    return make_response(response_data)




@app.route('/laws', methods=['GET'])
def get_all_laws_route():
    laws = get_all_laws()  
    serialized_laws = []

    for law in laws:
        serialized_law = {
            "idLaw": law.idLaw,
            "wizara": law.wizara,
            "sujet": law.sujet,
            "type": law.type,
            "num": law.num,
            "date": law.date,
            "num_jarida": law.num_jarida,
            "date_jarida": law.date_jarida,
            "page_jarida":law.page_jarida
        }
        serialized_laws.append(serialized_law)

    return jsonify(serialized_laws)



UPLOAD_FOLDER = 'uploads'  # Dossier de téléchargement
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Aucun fichier trouvé', 400
    
    file = request.files['file']

    if file.filename == '':
        return 'Nom de fichier vide', 400
    
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Fichier téléchargé avec succès', 200



@app.route('/upload/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)