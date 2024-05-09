from chargily_pay import ChargilyClient
from sqlalchemy.exc import SQLAlchemyError
from flask import request, jsonify
from chargily_pay.settings import CHARGILIY_TEST_URL
from dotenv import load_dotenv
from chargily_pay.entity import Checkout
from .. import db
from ..models.models import Users, PlanTarifications, AbonementServices, AccessTokens, Payements

import hashlib
import hmac
import json
from datetime import datetime
from datetime import timedelta
import jwt


load_dotenv()
key="test_pk_3F71yThlwOzng2F5pIKaoW8Btt0oRU7G8a3tpMKx"
secret="test_sk_lsJW3aHT6LDlvsafXHOMEHYJQMkKGOgSLNdVkD9k"

chargily = ChargilyClient(key, secret, CHARGILIY_TEST_URL)



def subscribe(data):
    try:
        # Extract user_id and plan_id from the request data
        data = request.json
        user_id = data.get("user_id")
        plan_id = data.get("plan_id")

        # Retrieve user and plan objects from the database
        user = Users.query.get(user_id)
        plan = PlanTarifications.query.get(plan_id)

        # Check if both user and plan exist
        if user is None or plan is None:
            return jsonify({"error": "User or plan not found"}), 404


        # Retrieve service from the plan
        service = plan.service
    
    
        # Check if the user is already subscribed to the service
        existing_subscription = AbonementServices.query\
            .join(PlanTarifications, PlanTarifications.id == AbonementServices.plan_id)\
            .join(AccessTokens, AccessTokens.id == AbonementServices.access_token_id)\
            .filter(PlanTarifications.service_id == service.id,
                    AccessTokens.acteur_id == user_id,
                    AbonementServices.status == "Active")\
            .first()

        if existing_subscription:
            return jsonify({"error": "User is already subscribed to this service"}), 400

        # Create checkout using chargily
        checkout = chargily.create_checkout(
            Checkout(
                items=[{"price": plan.price_id, "quantity": 1}],
                customer_id=user.customer_id,
                success_url="https://example.com/success",
                failure_url="https://example.com/failure",
            )
        )

        
        
        # Create AbonementServices object
        abonement = AbonementServices(
            plan_id=plan.id, 
            checkout_id=checkout["id"],
            access_token_id=None,
            status="Pending",
            service_id=service.id
        )

        db.session.add(abonement)
        db.session.flush()  
        # Create payment record
        payment = Payements(
            abonement_id=abonement.id,  
            acteur_id=user_id,
            moyen_payment="ccp",
        )

        db.session.add(payment)
        db.session.commit()

        # Redirect to the checkout URL
        return jsonify({"message": checkout["checkout_url"]}), 302
    
    except SQLAlchemyError as e:
        # Rollback changes and handle database errors
        db.session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    
    except Exception as e:
        # Handle other exceptions
        return jsonify({"error": str(e)}), 500


def get_invoices_by_user(user_id):
    try:
        invoices = AbonementServices.query.filter_by(acteur_id=user_id).all()

        serialized_invoices = []
        for invoice in invoices:
            serialized_invoice = {
                "id": invoice.id,
                "nom": invoice.plan.nom,  
                "date_paiement": invoice.date_abonement.strftime("%Y-%m-%d %H:%M:%S"),  
                "moyen_payment": invoice.moyen_payment,
                "price": invoice.plan.tarif,
            }
            serialized_invoices.append(serialized_invoice)

        return jsonify(serialized_invoices), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_subscriptions_by_user(user_id):
    try:
        subscriptions = AbonementServices.query.filter_by(acteur_id=user_id).all()

        serialized_subscriptions = []
        for subscription in subscriptions:
            serialized_subscription = {
                "id": subscription.id,  
                "durree": subscription.plan.durree, 
                "date_paiement": subscription.date_abonement.strftime("%Y-%m-%d %H:%M:%S"), 
                "moyen_payment": subscription.moyen_payment,
                "status": subscription.status,
            }
            serialized_subscriptions.append(serialized_subscription)

        return jsonify(serialized_subscriptions), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def generate_access_token(user_id, service_id, expires_in_days=30):
    secret_key="secret"
    payload = {
        "user_id": user_id,
        "service_id": service_id,
        "exp": datetime.utcnow() + timedelta(days=expires_in_days)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    print(token)
    return token




def handleWebhook(request):
    try:
        signature = request.headers.get('signature')
        payload = request.data.decode('utf-8')

        if not signature:
            return "Signature missing", 400

        computed_signature = hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(signature, computed_signature):
            return "Signature mismatch", 403

        event = json.loads(payload)
        checkout = None

        if event['type'] == 'checkout.paid':
            checkout = event['data']
            abonement = AbonementServices.query.filter_by(checkout_id=checkout['id']).first()
            payment = Payements.query.filter_by(abonement_id=abonement.id).first()
            if abonement:
                abonement.status = "Active"
                db.session.commit()

                if payment:
                    payment.moyen_payment = checkout["payment_method"]
                    db.session.commit()
                else:
                    return "Payment not found", 404
                access_token = generate_access_token(payment.acteur_id, abonement.service_id,abonement.plan.durree) 
                
                access_token_obj = AccessTokens(
                    acteur_id=payment.acteur_id,
                    service_id=abonement.service_id,
                    expires=datetime.utcnow() + timedelta(days=abonement.plan.durree),  
                    token=access_token  
                )
                
                db.session.add(access_token_obj)
                db.session.commit()

                abonement.access_token_id = access_token_obj.id
                db.session.commit()
            else:
                return "Abonement not found", 404
        else:
            checkout = event['data']
            abonement = AbonementServices.query.filter_by(checkout_id=checkout['id']).first()
            payment = Payements.query.filter_by(abonement_id=abonement.id).first()
            if abonement:
                db.session.delete(abonement)
                db.session.commit()
            if payment:
                db.session.delete(payment)
                db.session.commit()
            else:
                return "Abonement not found", 404

        return "Webhook received!", 200

    except Exception as e:
        return str(e), 500


