from flask import Blueprint, request, jsonify, abort
from models import User, Destination
from extensions import db
from .schemas import UserSchema, FavoriteSchema

user_bp = Blueprint("users", __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
favorite_schema = FavoriteSchema()


@user_bp.route("/users", methods=["POST"])
def create_user():
    data = user_schema.load(request.json)
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(404, description="User not found")
    return user_schema.jsonify(user)


@user_bp.route("/users/<int:id>/favorites", methods=["POST"])
def add_favorite(id):
    user = User.query.get(id)
    if not user:
        abort(404, description="User not found")

    data = favorite_schema.load(request.json)
    destination = Destination.query.get(data["destination_id"])
    if not destination:
        abort(404, description="Destination not found")

    user.favorites.append(destination)
    db.session.commit()
    return jsonify({"message": "Destination added to favorites"}), 201

@user_bp.route("/users/<int:user_id>/favorites/<int:destination_id>", methods=["DELETE"])
def remove_favorite(user_id, destination_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    destination = Destination.query.get(destination_id)
    if not destination:
        abort(404, description="Destination not found")

    if destination not in user.favorites:
        abort(400, description="This destination is not in users favorites")

    user.favorites.remove(destination)
    db.session.commit()

    return jsonify({"message": "Destination retired from farorites"}), 200


@user_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
        user = User.query.get(id)
        if not user:
            abort(404, description="User not found")
        
        data = user_schema.load(request.json, partial=True)
        for key, value in data.items():
            setattr(user, key, value)
        
        db.session.commit()
        return user_schema.jsonify(user), 200

@user_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
        user = User.query.get(id)
        if not user:
            abort(404, description="User not found")
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200