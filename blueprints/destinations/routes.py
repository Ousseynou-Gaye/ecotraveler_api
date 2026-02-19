from flask import Blueprint, request, jsonify
from models import  Destination  
from .schemas import DestinationSchema
from extensions import db
from services import GeminiService
from blueprints.activites.schemas import EcoPlanRequestSchema
from marshmallow import ValidationError
import json
import re

destinations_bp = Blueprint('destinations', __name__)
destination_schema = DestinationSchema()
destinations_schema = DestinationSchema(many=True)


@destinations_bp.route('/destinations', methods=['POST'])
def create_destination():
    data = destination_schema.load(request.json)
    destination = Destination(
        city=data['city'],
        country=data['country'],
        description=data.get('description')
    )
    db.session.add(destination)
    db.session.commit()
    return destination_schema.jsonify(destination), 201

@destinations_bp.route('/destinations', methods=['GET'])
def get_destinations():
    country = request.args.get('country')
    
    if country:
        destinations = Destination.query.filter_by(country=country).all()
    else:
        destinations = Destination.query.all()
    
    return destinations_schema.jsonify(destinations), 200

# Initialiser le service Gemini
try:
    gemini_service = GeminiService()
except ValueError as e:
    print(f"ERREUR : {e}")
    gemini_service = None

@destinations_bp.route('/destinations/<int:destination_id>/eco-plan', methods=['POST'])
def get_eco_plan(destination_id):
    """
    Endpoint pour obtenir des suggestions écologiques
    """
    # Vérifier que Gemini est configuré
    if not gemini_service:
        return jsonify({
            "error": "Service Gemini non disponible. Vérifiez votre clé API dans .env"
        }), 500
    
    try:
        # 1. Valider les données avec Marshmallow
        schema = EcoPlanRequestSchema()
        data = schema.load(request.json)
        
        # 2. Récupérer la destination dans la DB
        destination = Destination.query.get(destination_id)
        if not destination:
            return jsonify({"error": "Destination non trouvée"}), 404
        
        # 3. Appeler Gemini
        activities = data['activities']
        gemini_response = gemini_service.get_eco_alternatives(
            destination.description,
            activities
        )
        
        # 4. Parser la réponse JSON
        # Nettoyer les éventuelles balises markdown
        cleaned_response = re.sub(r'```json\n?|\n?```', '', gemini_response).strip()
        
        try:
            suggestions = json.loads(cleaned_response)
        except json.JSONDecodeError:
            # Si Gemini ne retourne pas du JSON, on retourne le texte brut
            suggestions = {
                "raw_response": gemini_response,
                "note": "Réponse non parsée (format inattendu)"
            }
        
        # 5. Retourner la réponse formatée
        return jsonify({
            "destination": {
                "id": destination.id,
                "city": destination.city,
                "country": destination.country,
                "description": destination.description
            },
            "activites_soumises": activities,
            "suggestions_ecologiques": suggestions
        }), 200
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    except Exception as e:
        return jsonify({
            "error": "Erreur lors du traitement",
            "details": str(e)
        }), 500