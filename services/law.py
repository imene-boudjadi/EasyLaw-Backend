
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
    http_auth=('elastic', 'elastic'),  # Add your username and password here
)
# Fonction pour effectuer une recherche dans Elasticsearch
def search_laws(query):
    # Effectuer une recherche dans l'index 'laws' sur le champ 'sujet' avec la requête spécifiée
    res = es.search(index='laws', body={
        "query": {
            "match": {
                "sujet": query
            }
        }
    })
    return res['hits']['hits']

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
                    # "date": {"type": "text"},
                    "num_jarida": {"type": "text"},
                    # "date_jarida": {"type": "text"},
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
    # Commencez par la requête de base
    query = Law.query

    # Ajoutez les filtres un par un si les valeurs ne sont pas nulles
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

    # Exécutez la requête et retournez les résultats
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

