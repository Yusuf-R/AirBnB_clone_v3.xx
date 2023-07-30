#!/usr/bin/python3
"""Module for State views"""
from api.v1.views import app_views
from api.v1.views import *
from models import storage
from models.state import State
from flask import jsonify, make_response, request

view = State


@app_views.route("/states", strict_slashes=False,
                 methods=["GET"], defaults={"state_id": None})
@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """GET"""
    if not state_id:
        list_views = [v.to_dict() for v in storage.all(view).values()]
        return jsonify(list_views)
    return get_view(view, state_id)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """DELETE"""
    return delete_view(view, state_id)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    """POST"""
    required = ["name"]
    return post_view(view, None, None, required)


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """PUT view"""
    ignore = ["id", "created_at", "updated_at"]
    return put_view(view, state_id, ignore)
