#!/usr/bin/python3
"""model for blue print view"""

from flask import Blueprint
from flask import jsonify, make_response, abort
from models import storage
from models.user import User

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


def get_match(cls, id):
    """GET: get match by id"""
    obj = storage.get(cls, id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


def delete_match(cls, id):
    """DELETE: delete match by id"""
    obj = storage.get(cls, id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


def create_new(p_cls, ch_cls, p_id, **kwargs):
    """POST: create new object"""
    if ch_cls is None and p_id is None:
        obj = p_cls(**kwargs)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 201)
    elif "user_id" in kwargs and "text" not in kwargs:
        user_obj = storage.get(User, kwargs["user_id"])
        if user_obj is None:
            abort(404)
        obj = storage.get(p_cls, p_id)
        if obj is None:
            abort(404)
        obj_list = [place.to_dict() for place in obj.places]
        key = p_cls.__name__.lower() + "_id"
        kwargs[key] = p_id
        obj = ch_cls(**kwargs)
        obj.save()
        obj_list.append(obj.to_dict())
        return make_response(jsonify(obj_list), 201)
    elif "user_id" in kwargs and "text" in kwargs:
        user_obj = storage.get(User, kwargs["user_id"])
        if user_obj is None:
            abort(404)
        obj = storage.get(p_cls, p_id)
        if obj is None:
            abort(404)
        obj_list = [review.to_dict() for review in obj.reviews]
        key_placeID = (
            p_cls.__name__.lower() + "_id"
        )  # this will give is place_id
        kwargs[key_placeID] = p_id
        obj = ch_cls(**kwargs)
        obj.save()
        obj_list.append(obj.to_dict())
        return make_response(jsonify(obj_list), 201)
    else:
        obj = storage.get(p_cls, p_id)
        if obj is None:
            abort(400)
        obj_list = [city.to_dict() for city in obj.cities]
        key = p_cls.__name__.lower() + "_id"
        kwargs[key] = p_id
        obj = ch_cls(**kwargs)
        obj.save()
        # storage.new(obj)
        # storage.save()
        # this also can be done by calling obj.save()
        obj_list.append(obj.to_dict())
        return make_response(jsonify(obj_list), 201)


def update_match(match_obj, **kwargs):
    """PUT: update a state obj"""
    exempt = [
        "id",
        "created_at",
        "updated_at",
        "state_id",
        "email",
        "place_id",
        "user_id",
    ]
    for key, value in kwargs.items():
        if key not in exempt:
            setattr(match_obj, key, value)
    storage.save()
    return make_response(jsonify(match_obj.to_dict()), 200)


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
