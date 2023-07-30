#!/usr/bin/python3
"""model for blue print view"""

from flask import Blueprint
from flask import jsonify, make_response, abort
from models import storage

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


def get_match(cls, id):
    """GET: get match by id"""
    state = storage.get(cls, id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


def delete_match(cls, id):
    """DELETE: delete match by id"""
    obj = storage.get(cls, id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


def create_new(cls, **kwargs):
    """POST: create new object"""
    obj = cls(**kwargs)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


def update_match(match_state, **kwargs):
    """PUT: update a state obj"""
    exempt = ['id', 'created_at', 'updated_at']
    for key, value in kwargs.items():
        if key not in exempt:
            setattr(match_state, key, value)
    storage.save()
    return make_response(jsonify(match_state.to_dict()), 200)


from api.v1.views.index import *
from api.v1.views.states import *
