#!/usr/bin/python3
"""Module for User view"""
from api.v1.views import app_views
from api.v1.views import *
from models import storage
from models.user import User
from flask import jsonify, make_response, request

view = User


@app_views.route("/users", strict_slashes=False,
                 methods=["GET"], defaults={"user_id": None})
@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """GET view"""
    if not user_id:
        list_views = [v.to_dict() for v in storage.all(view).values()]
        return jsonify(list_views)
    return get_view(view, user_id)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """DELETE view"""
    return delete_view(view, user_id)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_user():
    """POST view"""
    required = ["email", "password"]
    return post_view(view, None, None, required)


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """PUT view"""
    ignore = ["id", "created_at", "updated_at", "email"]
    return put_view(view, user_id, ignore)
