from flask import request
from ..models.models import Qrar, QrarMahkama, sujet, QrarMajliss, Classe, Chambre, Takyif
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
# import jwt
# from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func, literal
from .. import db
from random import shuffle


try:
    es = Elasticsearch(
        ['http://localhost:9200'],  # Include the port in the host URL
        http_auth=('elastic','elastic'),  # Add your username and password here
    )
except Exception as e:
    print("Erreur lors de la connexion à Elasticsearch:", e)

def get_all_qrar():
    qrar = Qrar.query.all()
    return qrar


def get_all_qrarat_mahkama():
    # join entre la table "قرار_المحكمة" et la table "قرار" pour avoir toutes les informations
    qrarat_mahkama = db.session.query(
        QrarMahkama.idQrarMahkama,  # columns from QrarMahkama
        QrarMahkama.refLegale,
        QrarMahkama.motsClés,
        QrarMahkama.parties,
        QrarMahkama.repMahkama,
        QrarMahkama.OperatDecision,
        QrarMahkama.raqmQararOrigin,
        Qrar.raqmQarar,  # columns from Qrar
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe
    ).join(
        Qrar, QrarMahkama.raqmQararOrigin == Qrar.raqmQarar
    ).all()

    return qrarat_mahkama

def get_all_qrarat_majliss():
    qrarat_majliss = db.session.query(
        QrarMajliss.id_qarar_majliss,
        QrarMajliss.chambre,
        QrarMajliss.classe,
        QrarMajliss.takyif,
        QrarMajliss.num_qarar,
        Qrar.raqmQarar,
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe
    ).join(
        QrarMajliss, QrarMajliss.num_qarar == Qrar.raqmQarar
    ).all()

    return qrarat_majliss

##################################################################################
def get_all_qrarat_with_details():
    # jointure entre QrarMajliss et Qrar
    qrarat_with_details_1 = db.session.query(
        Qrar.raqmQarar,
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe,
        literal("المحكمة العليا").label("commission")   
    ).join(
        QrarMahkama, QrarMahkama.raqmQararOrigin == Qrar.raqmQarar
    ).all()
    #  jointure entre QrarMahkama et Qrar
    qrarat_with_details_2 = db.session.query(
        Qrar.raqmQarar,
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe,
        literal("مجلس الدولة").label("commission") 
    ).join(
        QrarMajliss, QrarMajliss.num_qarar == Qrar.raqmQarar
    ).all()

    # Fusionner les résultats des deux jointures
    qrarat_with_details = qrarat_with_details_1 + qrarat_with_details_2
    # Mélanger les éléments de la liste
    # shuffle(qrarat_with_details)

    return qrarat_with_details


##################################################################################

def get_details_qrarMahkama(raqmQarar):
    qrar_mahkama = db.session.query(
        QrarMahkama.idQrarMahkama,
        QrarMahkama.refLegale,
        QrarMahkama.motsClés,
        QrarMahkama.parties,
        QrarMahkama.repMahkama,
        QrarMahkama.OperatDecision,
        QrarMahkama.raqmQararOrigin,
        Qrar.raqmQarar,
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe
    ).join(
        Qrar, QrarMahkama.raqmQararOrigin == Qrar.raqmQarar
    ).filter(Qrar.raqmQarar == raqmQarar).first()
    return qrar_mahkama


def get_details_qrarMajliss(raqmQarar):
    qrar_majliss = db.session.query(
        QrarMajliss.id_qarar_majliss,
        QrarMajliss.chambre,
        QrarMajliss.classe,
        QrarMajliss.takyif,
        QrarMajliss.num_qarar,
        Qrar.raqmQarar,
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe
    ).join(
        Qrar, QrarMajliss.num_qarar == Qrar.raqmQarar
    ).filter(Qrar.raqmQarar == raqmQarar).first()
    return qrar_majliss


def get_all_sujets():
    sujets = sujet.query.all()
    return sujets

def get_unique_years():
    unique_years = db.session.query(func.extract('year', Qrar.dataQarar)).distinct().all()
    years = [year[0] for year in unique_years if year[0] is not None]  # Filter les valeurs vides
    return years

def get_all_classes():
    classes = Classe.query.all()
    return classes

def get_all_chambres():
    chambres = Chambre.query.all()
    return chambres


def get_all_takyif():
    takyifs = Takyif.query.all()
    return takyifs

def search_qrar(query):
    res = es.search(index='qrar', body={
        "query": {
            "match": {
                "principe": query
            }
        }
    })
    return res['hits']['hits']

def index_qrar():
    qrars = Qrar.query.all()
    if not es.indices.exists(index='qrar'):
        index_mapping = {
            "mappings": {
                "properties": {
                    "sujetQarar": {"type": "text"},
                    "principe": {"type": "text"},
                    
                }
            }
        }
        es.indices.create(index='qrar', body=index_mapping)

    for qrar in qrars:
        es.index(index='qrar', id=qrar.raqmQarar, body={
            "sujetQarar": qrar.sujetQarar,
            "principe": qrar.principe,
           
        })