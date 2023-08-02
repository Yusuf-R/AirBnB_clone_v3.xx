#!/usr/bin/python3
"""A place_amenities module"""

from flask import abort, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of amenities of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage_t = getenv("HBNB_TYPE_STORAGE")
    if storage_t == "db":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    elif storage_t == "file":
        return jsonify(
            [storage.get(Amenity, id).to_dict() for id in place.amenity_ids]
        )


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an amenity from a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage_t = getenv("HBNB_TYPE_STORAGE")
    if storage_t == "db":
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)
    elif storage_t == "file":
        if amenity in place.amenity_ids:
            place.amenity_ids.remove(amenity_id)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """Create an amenity and link to Place base on the place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage_t = getenv("HBNB_TYPE_STORAGE")
    if storage_t == "db":
        if amenity in place.amenieites:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
    elif storage == "file":
        if amenity in place.ameniity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
