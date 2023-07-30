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
        return jsonify(states)
    return get_match(State, state_id)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """DELETE a state object base on its id"""
    return delete_match(State, state_id)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """POST a state object"""
    if not request.json:
        abort(400, description='Not a JSON')
    if "name" not in request.json:
        abort(400, description='Missing name')
    kwargs = request.get_json()
    return create_new(State, **kwargs)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """PUT a state object"""
    match_state = storage.get(State, state_id)
    if not match_state:
        abort(404)
    if not request.json:
        abort(400, description='Not a JSON')
    kwargs = request.get_json()
    return update_match(match_state, **kwargs)
