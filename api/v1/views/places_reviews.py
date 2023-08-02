#!/usr/bin/python3
""" Place_Review Module for HBNB project """
from models.place import Place
from models.review import Review
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from api.v1.views import *

parent_cls = Place
child_cls = Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def get_all_reviews(place_id):
    """GET all the reveiew for a given place_id"""
    match_place = storage.get(parent_cls, place_id)
    if not match_place:
        abort(404)
    return jsonify([review.to_dict() for review in match_place.reviews])


@app_views.route('/review/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """GET a review object"""
    match_review = storage.get(child_cls, review_id)
    if not match_review:
        abort(404)
    return get_match(child_cls, review_id) 


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """DELETE a review object base on its id"""
    return delete_match(child_cls, review_id)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """POST a review to a place object"""
    if not request.json:
        abort(400, description='Not a JSON')
    if "text" not in request.json:
        abort(400, description='Missing text')
    if "user_id" not in request.json:
        abort(400, description='Missing user_id')
    kwargs = request.get_json()
    return create_new(parent_cls, child_cls, place_id, **kwargs)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """PUT a state object"""
    match_review = storage.get(child_cls, review_id)
    if not match_review:
        abort(404)
    if not request.json:
        abort(400, description='Not a JSON')
    kwargs = request.get_json()
    return update_match(match_review, **kwargs)
