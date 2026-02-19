from flask import Flask, jsonify
from extensions import db, ma, migrate
from blueprints.users.routes import user_bp
from blueprints.destinations.routes import destinations_bp
from blueprints.activites.routes import activity_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate.init_app(app, db)

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(destinations_bp)
    app.register_blueprint(activity_bp)
    

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": error.description}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": error.description}), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Server Error", "message": "Server error"}), 500

    with app.app_context():
        db.create_all()

    return app  

app = create_app()