#!/usr/bin/python3
"""Module for Blueprint"""
from flask import Blueprint, make_response, jsonify
from models.user import User


def get_view(view, view_id):
    """GET view"""
    obj_v = storage.get(view, view_id)
    if not obj_v:
        abort(404)
    return jsonify(obj_v.to_dict())


def get_view_parent(view_parent, view_parent_id, view_child):
    """GET view parent"""
    parent = storage.get(view_parent, view_parent_id)
    if not parent:
        abort(404)
    return jsonify([v.to_dict() for v in getattr(parent, view_child)])


def delete_view(view, view_id):
    """DELETE view"""
    obj_v = storage.get(view, view_id)
    if not obj_v:
        abort(404)
    storage.delete(obj_v)
    storage.save()
    return make_response(jsonify({}), 200)


def post_view(view, view_parent, view_parent_id, required):
    """POST /model api route"""
    if view_parent:
        parent = storage.get(view_parent, view_parent_id)
        if not parent:
            abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for req in required:
        if req not in data.keys():
            message = "Missing " + req
            return make_response(jsonify({'error': message}), 400)
    if "user_id" in required:
        if not storage.get(User, data.get("user_id")):
            abort(404)
    if view_parent:
        data[view_parent.__name__.lower() + '_id'] = view_parent_id
    obj_v = view(**data)
    obj_v.save()
    return make_response(jsonify(obj_v.to_dict()), 201)


def put_view(view, view_id, ignore):
    """PUT view"""
    obj_v = storage.get(view, view_id)
    if not obj_v:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for k, v in data.items():
        if k not in ignore:
            setattr(obj_v, k, v)
    obj_v.save()
    return make_response(jsonify(obj_v.to_dict()), 200)

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.states import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
