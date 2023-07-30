#!/usr/bin/python3
"""Module for Review view"""
from api.v1.views import app_views
from api.v1.views import *
from models import storage
from models.review import Review
from models.place import Place
from flask import jsonify, make_response, request

view = Review
parent_view = Place


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=["GET"])
def get_reviews(place_id):
    """GET /place route"""
    return get_view_parent(parent_view, place_id, "reviews")


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """GET view"""
    return get_view(view, review_id)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """DELETE view"""
    return delete_view(view, review_id)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def post_review(place_id):
    """POST view"""
    required = ["user_id", "text"]
    return post_view(view, parent_view, place_id, required)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def put_review(review_id):
    """PUT view"""
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    return put_view(view, review_id, ignore)
