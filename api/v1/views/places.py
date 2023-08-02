#!/usr/bin/python3
""" Place Module for HBNB project """
from models.place import Place
from models.city import City
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from api.v1.views import *

parent_cls = City
child_cls = Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def get_all_places(city_id):
    """GET all the place for a given city_id"""
    match_city = storage.get(parent_cls, city_id)
    if not match_city:
        abort(404)
    return jsonify([place.to_dict() for place in match_city.places])


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """GET a place object"""
    match_place = storage.get(child_cls, place_id)
    if not match_place:
        abort(404)
    return get_match(child_cls, place_id) 


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """DELETE a place object base on its id"""
    return delete_match(child_cls, place_id)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """POST a place object"""
    if not request.json:
        abort(400, description='Not a JSON')
    if "name" not in request.json:
        print("name is not found")
        abort(400, description='Missing name')
    if "user_id" not in request.json:
        abort(400, description='Missing user_id')
    kwargs = request.get_json()
    return create_new(parent_cls, child_cls, city_id, **kwargs)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """PUT a state object"""
    match_place = storage.get(child_cls, place_id)
    if not match_place:
        abort(404)
    if not request.json:
        abort(400, description='Not a JSON')
    kwargs = request.get_json()
    return update_match(match_place, **kwargs)
