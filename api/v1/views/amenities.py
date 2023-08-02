#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.amenity import Amenity
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from api.v1.views import *

parent_cls = Amenity


@app_views.route(
    "/amenities",
    strict_slashes=False,
    methods=["GET"],
    defaults={"amenity_id": None},
)
@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=["GET"]
)
def get_amenity(amenity_id):
    """GET all amenity"""
    if not amenity_id:
        amenity = [
            amenity.to_dict() for amenity in storage.all(parent_cls).values()
        ]
        return jsonify(amenity)
    return get_match(parent_cls, amenity_id)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """DELETE a state object base on its id"""
    return delete_match(parent_cls, amenity_id)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    """POST an amenity object"""
    if not request.json:
        abort(400, description="Not a JSON")
    if "name" not in request.json:
        abort(400, description="Missing name")
    kwargs = request.get_json()
    return create_new(parent_cls, None, None, **kwargs)


@app_views.route(
    "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False
)
def update_amenity(amenity_id):
    """PUT a state object"""
    match_amenity = storage.get(parent_cls, amenity_id)
    if not match_amenity:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    kwargs = request.get_json()
    return update_match(match_amenity, **kwargs)
