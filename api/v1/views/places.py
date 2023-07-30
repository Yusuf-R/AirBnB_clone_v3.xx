#!/usr/bin/python3
"""Module for Place view"""
from api.v1.views import app_views
from api.v1.views import *
from models import storage
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from flask import jsonify, make_response, request

view = Place
parent_view = City


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=["GET"])
def get_places(city_id):
    """GET /city route"""
    return get_view_parent(parent_view, city_id, "places")


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """GET view"""
    return get_view(view, place_id)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """DELETE view"""
    return delete_view(view, place_id)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def post_place(city_id):
    """POST view"""
    required = ["name", "user_id"]
    return post_view(view, parent_view, city_id, required)


@app_views.route("/places/<place_id>", methods=["PUT"])
def put_place(place_id):
    """PUT view"""
    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
    return put_view(view, place_id, ignore)


@app_views.route("/places_search", methods=["POST"])
def place_search():
    """
    retrieves all Place objects
    depending of the JSON in the body of the request
    """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    sc = {"states", "cities"}
    places = []
    if not len(data) or all([len(v) == 0 for k, v in data.items() if k in sc]):
        places = storage.all(view).values()

    if len(data.get("cities", [])):
        cities = [storage.get(parent_view, id) for id in data["cities"]]
        [[places.append(place) for place in city.places]
         for city in cities if city]

    if len(data.get("states", [])):
        states = [storage.get(State, id) for id in data["states"]]
        [[[places.append(place) for place in city.places]
         for city in state.cities] for state in states if state]

    places = list(set(places))
    if len(data.get("amenities", [])):
        amenities = [storage.get(Amenity, id) for id in data["amenities"]]
        places = [place for place in places
                  if all([a in place.amenities for a in amenities])]

    return jsonify([place.to_dict() for place in places])
