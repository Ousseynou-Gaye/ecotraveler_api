import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY non trouvée dans le fichier .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def get_eco_alternatives(self, destination_description, activities):
        """
        Génère des alternatives écologiques pour des activités
        """
        # Construction de la liste des activités
        activities_text = "\n".join([
            f"- {activity['name']} (type: {activity['type']})"
            for activity in activities
        ])
        
        # Prompt pour Gemini
        prompt = f"""
Tu es un conseiller en voyage éco-responsable. 

Destination : {destination_description}

Activités prévues par le voyageur :
{activities_text}

Pour CHAQUE activité, suggère une alternative plus écologique.

Réponds UNIQUEMENT avec un JSON valide au format suivant (sans balises markdown) :
{{
    "suggestions": [
        {{
            "activite_originale": "nom exact de l'activité",
            "alternative_eco": "ta suggestion écologique",
            "explication": "pourquoi c'est mieux pour l'environnement",
            "impact_estime": "estimation de réduction d'impact (ex: -50% CO2)"
        }}
    ]
}}
"""
        
        try:
            response = self.model.generate_content(
                prompt,
                request_options={"timeout": 30}
                )
            return response.text
        except TimeoutError:
            raise Exception("Gemini API timeout après 30 secondes")
        except Exception as e:
            raise Exception(f"Erreur Gemini API: {str(e)}")