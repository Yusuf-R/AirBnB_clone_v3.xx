#!/usr/bin/python3
""" State Module for HBNB project """
from models.state import State
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage  
from api.v1.views import *


@app_views.route('/states',
                 strict_slashes=False,
                 methods=['GET'],
                 defaults={"state_id": None}
                 )
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def states(state_id):
    """GET all states"""
    if not state_id:
        states = [state.to_dict() for state in storage.all(State).values()]
        return make_response(jsonify(states))
   
    return get_match(State, state_id)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """DELETE a state object base on its id"""
    return delete_match(State, state_id)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """POST a state object"""
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    kwargs = request.get_json()
    return create_new(State, **kwargs)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """PUT a state object"""
    if not request.is_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    match_state = storage.get(State, state_id)
    if not match_state:
        abort(404)
    kwargs = request.get_json()
    return update_match(match_state, **kwargs)
