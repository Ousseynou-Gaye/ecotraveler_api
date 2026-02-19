# EcoTraveler API

API REST Flask pour planifier des voyages éco-responsables avec suggestions intelligentes basées sur l'IA Google Gemini.

##  Table des matières

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Structure du projet](#structure-du-projet)
- [Modèles de données](#modèles-de-données)
- [Documentation API](#documentation-api)
- [Exemples d'utilisation](#exemples-dutilisation)
- [Migrations de base de données](#migrations-de-base-de-données)
- [Gestion des erreurs](#gestion-des-erreurs)
---

##  Description

**EcoTraveler API** est une plateforme backend développée avec Flask qui aide les voyageurs à planifier leurs voyages de manière éco-responsable. L'API permet de gérer des destinations, créer des activités, sauvegarder des favoris, et surtout **obtenir des suggestions d'alternatives écologiques** grâce à l'intégration de l'IA **Google Gemini**.

---

##  Fonctionnalités

###  Gestion des utilisateurs
- Création d'utilisateurs avec validation des données
- Consultation des détails d'un utilisateur
- Gestion des destinations favorites par utilisateur
- Ajout et suppression de favoris

###  Gestion des destinations
- Consultation des destinations
- Association d'activités aux destinations

###  Gestion des activités
- Création d'activités (types : transport, loisir, repas)
- Validation des types d'activités
- Estimation des prix

###  Intelligence Artificielle (Google Gemini)
- **Endpoint principal** : Génération de plans de voyage éco-responsables
- Analyse contextuelle basée sur la destination
- Suggestions d'alternatives écologiques personnalisées pour chaque activité
- Explications détaillées de l'impact environnemental

---

##  Architecture

Le projet respecte les **meilleures pratiques Flask** :

###  Blueprints
- Séparation modulaire par domaine fonctionnel (users, destinations, activités)
- **Aucun code métier dans `app.py`**

###  Service Layer
- Isolation de la logique d'appel à l'API Gemini dans `services.py`
- Gestion centralisée des erreurs externes

###  Validation avec Marshmallow
- Validation systématique des données entrantes
- Contrôle des types, champs obligatoires, et formats

###  Sécurité
- Variables d'environnement avec `.env`
- **Aucune clé API dans le code**

###  Gestion des erreurs
- Error handlers pour renvoyer du JSON (404, 400, 500)
- Gestion spécifique des timeouts et erreurs Gemini

###  Base de données
- PostgreSQL avec SQLAlchemy
- Migrations avec Flask-Migrate

---

##  Prérequis

- **Python** 3.13.12
- **PostgreSQL** 12+
- **Clé API Google Gemini** ([obtenir une clé](https://ai.google.dev/))
- **pip** (gestionnaire de paquets Python)

---

##  Installation

### 1. Cloner le repository
```bash
git clone https://github.com/votre-username/ecotraveler-api.git
cd ecotraveler-api
```

### 2. Créer un environnement virtuel
```bash
python -m venv env
.\env\Scripts\Activate.ps1  # Windows powershell
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer PostgreSQL
```bash
# Créer la base de données via psql
psql -U postgres
CREATE DATABASE ecotravel;
\q
```

### 5. Configurer les variables d'environnement
Créez un fichier `.env` à la racine du projet (voir section [Configuration](#configuration))

### 6. Initialiser la base de données avec Flask-Migrate
```bash
# Initialiser les migrations (première fois uniquement)
flask db init

# Créer une migration
flask db migrate -m "Initial migration"

# Appliquer les migrations
flask db upgrade
```

### 7. Lancer l'application
```bash
python app.py
```

L'API sera accessible sur `http://localhost:5000`

---

##  Configuration

Créez un fichier `.env` à la racine du projet :

```env
# Base de données PostgreSQL
DATABASE_URL=postgresql://postgres:couple@localhost:5432/ecotravel

# Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=votre_cle_secrete_tres_securisee

# Google Gemini API
GEMINI_API_KEY=AIzaSyAqRHBd6ubCD9-SxtcrjcHWMXBiTE-WvBki

# Serveur (optionnel)
HOST=0.0.0.0
PORT=5000
DEBUG=True
```


### Obtenir une clé API Gemini
1. Rendez-vous sur [Google AI Studio](https://ai.google.dev/)
2. Créez un compte ou connectez-vous
3. Générez une clé API
4. Copiez-la dans votre fichier `.env`

---

## 📁 Structure du projet

```
PROJET FLASK/
│
├── app.py                      # Point d'entrée (Factory Pattern)
├── config.py                   # Configuration centralisée (.env)
├── extensions.py               # Initialisation SQLAlchemy, Marshmallow, Migrate
├── models.py                   # Modèles SQLAlchemy
├── services.py                 # Service Layer (appel API Gemini)
├── requirements.txt            # Dépendances Python
├── .env                        # Variables d'environnement (NON VERSIONNÉ)
├── README.md                   # Documentation
│
├── migrations/                 # Migrations Flask-Migrate
│   ├── versions/               # Fichiers de migration
│   └── ...
│
└── blueprints/                 # Blueprints modulaires
    │
    ├── users/                  # Module Utilisateurs
    │   ├── __init__.py
    │   ├── routes.py           # Routes utilisateurs
    │   └── schemas.py          # Validation Marshmallow
    │
    ├── destinations/           # Module Destinations
    │   ├── __init__.py
    │   ├── routes.py           # Routes destinations + IA
    │   └── schemas.py          # Validation Marshmallow
    │
    └── activites/              # Module Activités
        ├── __init__.py
        ├── routes.py           # Routes activités
        └── schemas.py          # Validation Marshmallow
```

### Description des fichiers principaux

| Fichier | Rôle |
|---------|------|
| `app.py` | Initialise Flask, enregistre les blueprints, configure les error handlers |
| `config.py` | Charge les variables d'environnement depuis `.env` |
| `extensions.py` | Initialise SQLAlchemy, Marshmallow, Flask-Migrate |
| `models.py` | Définit les modèles : User, Destination, Activity, users_favorites |
| `services.py` | Contient `GeminiService` pour l'intégration IA |
| `blueprints/` | Organisation modulaire par domaine (users, destinations, activites) |

---

##  Modèles de données

### User
```python
- id: int (PK)
- nom: str
- prenom: str
- email: str (unique)
- adresse: str
- favorites: relationship → [Destination]
```

### Destination
```python
- id: int (PK)
- city: str
- country: str
- description: text
```

### Activity
```python
- id: int (PK)
- name: str
- type: str (transport, loisir, repas)
- price_estimated: float
- destination_id: int (FK, nullable)
- destination: relationship → Destination
```

### users_favorites (Table d'association)
```python
- user_id: int (FK)
- destination_id: int (FK)
```

---

##  Documentation API

### Base URL
```
http://localhost:5000
```

---

##  Endpoints Utilisateurs

### Créer un utilisateur
```http
POST /users
Content-Type: application/json

{
  "nom": "Gaye",
  "prenom": "Ousseynou",
  "email": "ousseynou.gaye@gmail.com",
  "adresse": "Dakar, Sénégal"
}
```

**Réponse (201 Created)** :
```json
{
  "nom": "Gaye",
  "prenom": "Ousseynou",
  "email": "ousseynou.gaye@gmail.com",
  "adresse": "Dakar, Sénégal"
}
```

---

### Obtenir un utilisateur
```http
GET /users/{id}
```

**Réponse (200 OK)** :
```json
{
 "nom": "Gaye",
  "prenom": "Ousseynou",
  "email": "ousseynou.gaye@gmail.com",
  "adresse": "Dakar, Sénégal"
}
```

**Erreur (404)** :
```json
{
  "error": "Not Found",
  "message": "User not found"
}
```

---

### Ajouter une destination aux favoris
```http
POST /users/{user_id}/favorites
Content-Type: application/json

{
  "destination_id": 1
}
```

**Réponse (201 Created)** :
```json
{
  "message": "Destination added to favorites"
}
```

---

### Retirer une destination des favoris
```http
DELETE /users/{user_id}/favorites/{destination_id}
```

**Réponse (200 OK)** :
```json
{
  "message": "Destination retired from favorites"
}
```

**Erreur (400)** :
```json
{
  "error": "Bad Request",
  "message": "This destination is not in users favorites"
}
```

---

##  Endpoints Destinations

### Obtenir un plan éco-responsable (IA Gemini)
```http
POST /destinations/{destination_id}/eco-plan
Content-Type: application/json

{
  "activities": [
    {
      "name": "Louer une voiture",
      "type": "transport",
      "price_estimated": 25.000 
    },
    {
      "name": "Manger du mafé au fast-food",
      "type": "repas",
      "price_estimated": 3.000
    },
    {
      "name": "Visite en taxi",
      "type": "transport",
      "price_estimated": 15.000
    }
  ]
}
```

**Réponse (200 OK)** :
```json
{
  "destination": {
    "id": 1,
    "nom": "Mbour",
    "pays": "Sénégal",
    "description": "Ville culturelle, petite cote sénégalaise"
  },
  "activites_soumises": [
    {
      "name": "Louer une voiture",
      "type": "transport",
      "price_estimated": 15.000
    },
    {
      "name": "Manger du mafé au fast-food",
      "type": "repas",
      "price_estimated": 3.000
    }
  ],
  "suggestions_ecologiques": {
    "suggestions": [
      {
        "activite_originale": "Louer une voiture",
        "alternative_eco": "Utilisez un yango pour vos déplacements",
        "explication": "Les transports Yango sénégalais sont excellents et réduisent considérablement votre empreinte carbone",
        "impact_estime": "Moins d'exposition à l'émission de CO2"
      },
      {
        "activite_originale": "Manger au fast-food",
        "alternative_eco": "Privilégiez les restaurants locaux avec des produits de saison",
        "explication": "Soutien de l'économie locale, moins d'emballages, produits frais",
        "impact_estime": "-60% de déchets plastiques"
      }
    ]
  }
}
```

**Erreur (404)** :
```json
{
  "error": "Destination non trouvée"
}
```

**Erreur (500)** :
```json
{
  "error": "Service Gemini non disponible. Vérifiez votre clé API dans .env"
}
```

---

##  Endpoints Activités

### Créer une activité
```http
POST /activities
Content-Type: application/json

{
  "name": "Plongée",
  "type": "loisir",
  "price_estimated": 5.000
}
```

**Réponse (201 Created)** :
```json
{
 "name": "Plongée",
  "type": "loisir",
  "price_estimated": 5.000
}
```

**Erreur de validation (400)** :
```json
{
  "errors": {
    "type": [
      "Must be one of: transport, loisir, repas."
    ]
  }
}
```

---

### Obtenir une activité
```http
GET /activities/{id}
```

**Réponse (200 OK)** :
```json
{
 "name": "Plongée",
  "type": "loisir",
  "price_estimated": 5.000
}
```

---

##  Exemples d'utilisation

### Scénario complet : Créer un voyage éco-responsable

#### 1. Créer un utilisateur
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Fall",
    "prenom": "Sophie",
    "email": "sophie.fall@gmail.com",
    "adresse": "Rue 10, Médina"
  }'
```

#### 2. Ajouter une destination aux favoris
```bash
curl -X POST http://localhost:5000/users/1/favorites \
  -H "Content-Type: application/json" \
  -d '{"destination_id": 1}'
```

#### 3. Obtenir un plan éco-responsable avec Gemini
```bash
curl -X POST http://localhost:5000/destinations/1/eco-plan \
  -H "Content-Type: application/json" \
  -d '{
    "activities": [
      {
        "name": "Prendre le TER",
        "type": "transport",
        "price_estimated": 1.000
      },
      {
        "name": "Acheter de l'\''eau en bouteille plastique",
        "type": "loisir",
        "price_estimated": 2.000
      },
      {
        "name": "Manger au McDonald",
        "type": "repas",
        "price_estimated": 10.000
      }
    ]
  }'
```

---

##  Migrations de base de données

Le projet utilise **Flask-Migrate** (Alembic) pour gérer les changements de schéma.

### Commandes principales

#### Créer une migration
```bash
flask db migrate -m "Description de la migration"
```

#### Appliquer les migrations
```bash
flask db upgrade
```

#### Revenir en arrière
```bash
flask db downgrade
```

#### Voir l'historique
```bash
flask db history
```

### Workflow de migration

1. **Modifier `models.py`**
   ```python
   # Exemple : Ajouter un champ
   class User(db.Model):
       telephone: Mapped[str] = mapped_column(String(20))
   ```

2. **Créer la migration**
   ```bash
   flask db migrate -m "Add telephone field to User"
   ```

3. **Vérifier le fichier généré**
   ```
   migrations/versions/xxxxx_add_telephone_field_to_user.py
   ```

4. **Appliquer la migration**
   ```bash
   flask db upgrade
   ```

###  Problèmes courants

**Problème** : Ajout d'une colonne NOT NULL sur une table existante
```
ERREUR: la colonne contient des valeurs NULL
```

**Solution** : Rendre la colonne nullable temporairement
```python
destination_id: Mapped[int | None] = mapped_column(nullable=True)
```

---

##  Gestion des erreurs

L'API utilise des **error handlers personnalisés** pour renvoyer des réponses JSON structurées.

### Erreur 404 - Ressource non trouvée
```json
{
  "error": "Not Found",
  "message": "User not found"
}
```

### Erreur 400 - Requête invalide
```json
{
  "error": "Bad Request",
  "message": "This destination is not in users favorites"
}
```

### Erreur 500 - Erreur serveur
```json
{
  "error": "Server Error",
  "message": "Server error"
}
```

### Erreur de validation Marshmallow
```json
{
  "errors": {
    "email": ["Not a valid email address."],
    "type": ["Must be one of: transport, loisir, repas."]
  }
}
```

### Erreur Gemini API
```json
{
  "error": "Erreur lors du traitement",
  "details": "Erreur Gemini API: ..."
}
```


##  Dépendances

Fichier `requirements.txt` :

```txt
Flask==3.1.2
flask-sqlalchemy==3.1.1
flask-marshmallow==1.3.0
marshmallow==4.2.0
psycopg2-binary==2.9.11
python-dotenv==1.2.1
Flask-Migrate==4.0.7
google-generativeai==0.8.3
```

### Installation
```bash
pip install -r requirements.txt
```


##  Licence

Ce projet est un projet académique réalisé dans le cadre d'un examen de fin de semestre à ISI pour le cours de développement Flask.

---

##  Auteur

- **Ousseynou GAYE** - *Développement* - [VotreGitHub](https://github.com/votre-username)

---

## 🙏 Remerciements

- **Google Gemini** pour l'API d'intelligence artificielle
- **Flask** et sa communauté
- **SQLAlchemy** pour l'ORM
- **Marshmallow** pour la validation
- Tous les contributeurs open-source

---

##  Support

Pour toute question ou problème :
- Ouvrez une [issue](https://github.com/votre-username/ecotraveler-api/issues)
- Contactez : ousseynougaye1999@gmail.com
---

**Made with 💚 for sustainable travel** 
