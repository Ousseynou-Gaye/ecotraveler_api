from flask import Blueprint, request, jsonify, abort
from models import Activity
from extensions import db
from .schemas import ActivitySchema

activity_bp = Blueprint("activities", __name__)
activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)

@activity_bp.route("/activities", methods=["POST"])
def create_activity():
    data = activity_schema.load(request.json)
    activity = Activity(**data)
    db.session.add(activity)
    db.session.commit()
    return activity_schema.jsonify(activity), 201

@activity_bp.route("/activities/<int:id>", methods=["GET"])
def get_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        abort(404, description="Activity not found")
    return activity_schema.jsonify(activity)