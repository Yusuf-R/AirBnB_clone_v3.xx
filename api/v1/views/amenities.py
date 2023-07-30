#!/usr/bin/python3
"""Module for Amenity views"""
from api.v1.views import app_views
from api.v1.views import *
from models import storage
from models.amenity import Amenity
from flask import jsonify, make_response, request

view = Amenity


@app_views.route("/amenities", strict_slashes=False,
                 methods=["GET"], defaults={"amenity_id": None})
@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """GET"""
    if not amenity_id:
        list_views = [v.to_dict() for v in storage.all(view).values()]
        return jsonify(list_views)
    return get_view(view, amenity_id)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """DELETE"""
    return delete_view(view, amenity_id)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenity():
    """POST"""
    required = ["name"]
    return post_view(view, None, None, required)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """PUT view"""
    ignore = ["id", "created_at", "updated_at"]
    return put_view(view, amenity_id, ignore)
