#!/usr/bin/python3
"""States module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models import place
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id=None):
    """Returns all places from a city object"""
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    places = []
    for value in cities.places:
        places.append(value.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def one_place(place_id=None):
    """Returns a place by place id"""
    get_place = storage.get(Place, place_id)
    if get_place is None:
        abort(404)
    return jsonify(get_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id=None):
    """Deletes a city objects by id"""
    get_place = storage.get(Place, place_id)
    if get_place is not None:
        storage.delete(get_place)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def creates_place(city_id=None):
    """Creates a place object"""
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    get_places = request.get_json()
    if not get_places:
        abort(400, 'Not a JSON')
    elif 'user_id' not in get_places:
        abort(400, 'Missing user_id')
    elif 'name' not in get_places:
        abort(400, 'Missing name')

    user = storage.get(User, get_places['user_id'])
    if not user:
        abort(404)
    new_obj = Place(name=get_places['name'], city_id=cities.id,
                    user_id=user.id)
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id=None):
    """Updates a place objects by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    get_places = request.get_json()
    if not get_places:
        abort(400, 'Not a JSON')

    for key, value in get_places.items():
        if key not in ["id", "user_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """ Gets all places object"""
    get_place = request.get_json()
    if not get_place:
        abort(400, 'Not a JSON')

    storage.new(get_place)
    storage.save()
    return jsonify(get_place.to_dict()), 201
