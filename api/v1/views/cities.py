#!/usr/bin/python3
"""Module for City view"""
from api.v1.views import app_views
from api.v1.views import *
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, make_response, request

view = City
parent_view = State


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=["GET"])
def get_cities(state_id):
    """GET /state route"""
    return get_view_parent(parent_view, state_id, "cities")


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """GET view"""
    return get_view(view, city_id)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """DELETE view"""
    return delete_view(view, city_id)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def post_city(state_id):
    """POST view"""
    required = ["name"]
    return post_view(view, parent_view, state_id, required)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """PUT view"""
    ignore = ["id", "state_id", "created_at", "updated_at"]
    return put_view(view, city_id, ignore)
