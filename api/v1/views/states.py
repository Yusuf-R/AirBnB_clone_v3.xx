#!/usr/bin/python3
""" State Module for HBNB project """
from api.v1.views import app_views
from api.v1.views import *
from models import storage
from models.state import State
from flask import jsonify 

view = State

@app_views.route('/states', strict_slashes=False, methods=['GET'], defaults= {"state_id" : None})
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states(state_id):
    """ GET all states """
    if not state_id:
        states = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(states)
    return get_view(view, state_id)

@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """DELETE State with spaecific ID"""
    return delete_view(view, state_id)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    """Create new State """
    required = ["name"]
    return post_view(view, None, None, required)


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """Edit State info"""
    info = ["id", "created_at", "updated_at"]
    return put_view(view, state_id, info)
