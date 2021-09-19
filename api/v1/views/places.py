#!/usr/bin/python3
"""Places module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City


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

@app_views.route('places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def one_place(place_id=None):
    """Returns a place by place id"""
    get_place = storage.get(Place, place_id)
    if get_place is None:
        abort(404)
    return jsonify(get_place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'])
def delete_place(place_id=None):
    """Deletes a city objects by id"""
    get_place = storage.get(Place, place_id)
    if get_place is not None:
        storage.delete(get_place)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def creates_city(state_id=None):
    """Creates a city object"""
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    get_cities = request.get_json()
    if not get_cities:
        abort(400, 'Not a JSON')
    elif 'name' not in get_cities:
        abort(400, 'Missing name')
    new_obj = City(name=get_cities['name'], state_id=states.id)
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id=None):
    """Updates a city objects by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    get_cities = request.get_json()
    if not get_cities:
        abort(400, 'Not a JSON')
    
    for key, value in get_cities.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
