
from flask import request
from ..models.models import  Law 
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
# import jwt
# from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
from .. import db
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['http://localhost:9200'],  # Include the port in the host URL
    http_auth=('elastic', 'elastic'), 
)
# Fonction pour effectuer une recherche dans Elasticsearch
def search_laws(query):
    # Initialiser une liste pour stocker les résultats
    all_results = []

    # Liste des champs sur lesquels effectuer la recherche
    fields = ["sujet", "wizara", "type", "num", "num_jarida", "page_jarida"]
 
    # Effectuer une recherche pour chaque champ
    for field in fields:
        res = es.search(index='laws', body={
            "query": {
                "match": {
                    field: query
                }
            }
        })
        # Ajouter les résultats à la liste
        all_results.extend(res['hits']['hits'])

    # Retourner les résultats avec l'identifiant de la loi inclus
    return [{"idLaw": hit["_id"], **hit["_source"]} for hit in all_results]


def index_laws():
    laws = Law.query.all()
    # Check if the 'laws' index exists
    if not es.indices.exists(index='laws'):
        # Define the index mapping
        index_mapping = {
            "mappings": {
                "properties": {
                    "wizara": {"type": "text"},
                    "sujet": {"type": "text"},
                    "type": {"type": "text"},
                    "num": {"type": "text"},
                    "date_jarida": {"type": "text"},
                    # "date": {"type": "text"},
                    "num_jarida": {"type": "text"},                   
                    "page_jarida": {"type": "text"}
                }
            }
        }
        # Create the 'laws' index with the defined mapping
        es.indices.create(index='laws', body=index_mapping)

    # Index each law into Elasticsearch
    for law in laws:
        es.index(index='laws', id=law.idLaw, body={
            "wizara": law.wizara,
            "sujet": law.sujet,
            "type": law.type,
            "num": law.num,
            # "date": law.date,
            "num_jarida": law.num_jarida,
            # "date_jarida": law.date_jarida,
            "page_jarida": law.page_jarida
        })

def filter_laws(wizara=None, law_type=None,  num_jarida=None, date_jarida=None, page_jarida=None):
    query = Law.query

    if wizara:
        query = query.filter(Law.wizara == wizara)
    if law_type:
       query = query.filter(Law.type.like(f"%{law_type}%"))
    if num_jarida:
        query = query.filter(Law.num_jarida == num_jarida)
    if date_jarida:
        query = query.filter(Law.date_jarida == date_jarida)
    if page_jarida:
        query = query.filter(Law.page_jarida == page_jarida)

    laws = query.all()
    return laws

def get_all_laws():
    laws = Law.query.all()

    return laws

def get_all_unique_wizara():
    unique_wizara = Law.query.with_entities(Law.wizara).distinct().all()
    unique_wizara = [w[0] for w in unique_wizara]  # Extracting wizara values from tuples

    return unique_wizara

def get_all_laws_with_sum():
    laws = Law.query.all()

    total_sum = db.session.query(func.sum(Law.idLaw)).scalar()

    return {
        "data": laws,
        "sum": total_sum
    }

def get_law_by_id(law_id):
    # Récupérer la loi par son ID
    law = Law.query.get(law_id)

    # Vérifier si la loi existe
    if law is None:
        return jsonify({'success': False, 'message': 'Law not found'}), 404

    # Construire le JSON à retourner
    law_json = {
        'id': law.idLaw,
        'wizara': law.wizara,
        'sujet': law.sujet,
        'type': law.type,
        'num': law.num,
        'date_jarida': law.date_jarida,
        'num_jarida': law.num_jarida,
        'page_jarida': law.page_jarida
    }

    return jsonify({'success': True, 'law': law_json}), 200