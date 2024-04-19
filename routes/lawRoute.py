from flask import Blueprint, jsonify , request, make_response, send_from_directory
import os
from ..services.law import get_all_laws , get_all_unique_wizara

law_routes = Blueprint('law_routes', __name__)

@law_routes.route('/laws', methods=['GET'])
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
            "page_jarida": law.page_jarida
        }
        serialized_laws.append(serialized_law)

    return jsonify(serialized_laws)

@law_routes.route('/laws/wizara', methods=['GET'])  # New route to get unique wizara values
def get_unique_wizara_route():
    unique_wizara = get_all_unique_wizara()  # Call get_all_unique_wizara method
    return jsonify(unique_wizara)  # Return unique wizara values as JSON

UPLOAD_FOLDER = 'uploads'  # Dossier de téléchargement
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@law_routes.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Aucun fichier trouvé', 400
    
    file = request.files['file']

    if file.filename == '':
        return 'Nom de fichier vide', 400
    
    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return 'Fichier téléchargé avec succès', 200

@law_routes.route('/upload/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)