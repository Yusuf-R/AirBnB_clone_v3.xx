#!/usr/bin/python3
""" City Module for HBNB project """
from models.state import State
from models.city import City
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from api.v1.views import *

parent_cls = State
child_cls = City


@app_views.route(
    "/states/<state_id>/cities", strict_slashes=False, methods=["GET"]
)
def get_all_cities(state_id):
    """GET all the cities for a given state_id"""
    match_state = storage.get(parent_cls, state_id)
    if not match_state:
        abort(404)
    return jsonify([city.to_dict() for city in match_state.cities])


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    """GET a city object"""
    match_city = storage.get(child_cls, city_id)
    if not match_city:
        abort(404)
    return get_match(child_cls, city_id)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """DELETE a city object base on its id"""
    return delete_match(child_cls, city_id)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """POST a city object"""
    if not request.json:
        abort(400, description="Not a JSON")
    if "name" not in request.json:
        abort(400, description="Missing name")
    kwargs = request.get_json()
    print("Hooray")
    return create_new(parent_cls, child_cls, state_id, **kwargs)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """PUT a state object"""
    match_city = storage.get(child_cls, city_id)
    if not match_city:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    kwargs = request.get_json()
    return update_match(match_city, **kwargs)
