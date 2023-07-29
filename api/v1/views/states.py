#!/usr/bin/python3
""" State Module for HBNB project """
from models.state import State
from flask import jsonify, abort 
from api.v1.views import app_views
from models import storage  

@app_views.route('/states', strict_slashes=False, methods=['GET'], defaults= {"state_id" : None})
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def states(state_id):
    """ GET all states """
    if not state_id:
        states = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(states)

    all_state = storage.all(State)
    key = "{}.{}".format(State.__name__, state_id)
    if key in all_state:
        match_state = [all_state[key].to_dict() if key in all_state else None]
        if match_state:
            return jsonify(match_state[0])
        abort(404)
