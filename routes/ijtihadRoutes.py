from flask import Blueprint, jsonify, request
from ..services.ijtihad import get_all_qrar, get_all_qrarat_mahkama, get_details_qrarMahkama, get_all_sujets, get_unique_years, get_all_qrarat_with_details

ijtihad_routes = Blueprint('ijtihad_routes', __name__)

@ijtihad_routes.route('/qrar', methods=['GET'])
def get_all_qrar_route():
    qrar = get_all_qrar()
    serialized_qrar = []

    for q in qrar:
        serialized_q = {
            'raqmQarar': q.raqmQarar,
            'dataQarar': q.dataQarar,
            'sujetQarar': q.sujetQarar,
            'principe': q.principe 
            
        }
        serialized_qrar.append(serialized_q)

    return jsonify(serialized_qrar)


@ijtihad_routes.route('/qraratMahkama', methods=['GET'])
def get_all_qrarat_Mahkama_route():
    MahkamaQrar = get_all_qrarat_mahkama()
    serialized_qrarMahkama = []

    for q in MahkamaQrar:
        serialized_q = {
            'idQrarMahkama': q.idQrarMahkama,
            'refLegale': q.refLegale,
            'motsClés': q.motsClés,
            'parties': q.parties,
            'repMahkama': q.repMahkama,
            'OperatDecision': q.OperatDecision,
            'raqmQararOrigin': q.raqmQararOrigin,
            'raqmQarar': q.raqmQarar,
            'dataQarar': q.dataQarar,
            'sujetQarar': q.sujetQarar,
            'principe': q.principe  
        }
        serialized_qrarMahkama.append(serialized_q)

    return jsonify(serialized_qrarMahkama)


@ijtihad_routes.route('/DetailsqrarMahkama/<int:raqmQarar>', methods=['GET'])
def get_Details_qrarMahkama_route(raqmQarar):
    qrarMahkama = get_details_qrarMahkama(raqmQarar)
    
    if qrarMahkama:
        serialized_qrarMahkama = {
            'idQrarMahkama': qrarMahkama.idQrarMahkama,
            'refLegale': qrarMahkama.refLegale,
            'motsClés': qrarMahkama.motsClés,
            'parties': qrarMahkama.parties,
            'repMahkama': qrarMahkama.repMahkama,
            'OperatDecision': qrarMahkama.OperatDecision,
            'raqmQararOrigin': qrarMahkama.raqmQararOrigin,
            'raqmQarar': qrarMahkama.raqmQarar,
            'dataQarar': qrarMahkama.dataQarar,
            'sujetQarar': qrarMahkama.sujetQarar,
            'principe': qrarMahkama.principe  
        }
        return jsonify(serialized_qrarMahkama)
    else:
        return jsonify({'message': 'QrarMahkama not found'}), 404

@ijtihad_routes.route('/sujetsQarar', methods=['GET'])
def get_all_sujets_route():
    sujets = get_all_sujets()
    serialized_sujets = []

    for sujet in sujets:
        serialized_sujet = {
            'Nomsujet': sujet.Nomsujet      
        }
        serialized_sujets.append(serialized_sujet)

    return jsonify(serialized_sujets)


@ijtihad_routes.route('/yearsQarar', methods=['GET'])
def get_unique_years_route():
    years = get_unique_years()
    serialized_years = []
    for year in years:
        serialized_year = {
            'year': year      
        }
        serialized_years.append(serialized_year)

    return jsonify(serialized_years)



@ijtihad_routes.route('/qraratwihDetails', methods=['GET'])
def get_all_qrarat_with_details_route():
    Qrarat = get_all_qrarat_with_details()
    serialized_qrarat = []

    for q in Qrarat:
        serialized_qrar = {
            'raqmQarar': q.raqmQarar,
            'dataQarar': q.dataQarar,
            'sujetQarar': q.sujetQarar,
            'principe': q.principe,
            'commission' : q.commission   
        }
        serialized_qrarat.append(serialized_qrar)

    return jsonify(serialized_qrarat)
