import os
from dotenv import load_dotenv  

load_dotenv()  #Pour chercher le fichier .env et charger les variables d'environnements locales

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")