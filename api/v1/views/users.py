#!/usr/bin/python3
""" User Module for HBNB project """
from models.user import User
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from api.v1.views import *

parent_cls = User


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['GET'],
                 defaults={"user_id": None}
                 )
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """GET all user"""
    if not user_id:
        user = [user.to_dict() for user in storage.all(parent_cls).values()]
        return jsonify(user)
    return get_match(parent_cls, user_id)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """DELETE a state object base on its id"""
    return delete_match(parent_cls, user_id)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """POST an user object"""
    if not request.json:
        abort(400, description='Not a JSON')
    if "email" not in request.json:
        abort(400, description='Missing email')
    if "password" not in request.json:
        abort(400, description='Missing password')
    kwargs = request.get_json()
    return create_new(parent_cls, None, None, **kwargs)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """PUT a state object"""
    match_user = storage.get(parent_cls, user_id)
    if not match_user:
        abort(404)
    if not request.json:
        abort(400, description='Not a JSON')
    kwargs = request.get_json()
    return update_match(match_user, **kwargs)
