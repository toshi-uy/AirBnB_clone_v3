#!/usr/bin/python3
"""Amenitys module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def all_amenities(amenity_id=None):
    """Returns all amenity objects handeling amenities id"""
    amenities = []
    for value in storage.all(Amenity).values():
        amenities.append(value.to_dict())
    if not amenity_id:
        return jsonify(amenities)
    get_amenity = storage.get(Amenity, amenity_id)
    if get_amenity is None:
        abort(404)
    return jsonify(get_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """Deletes a amenity objects by id"""
    get_amenity = storage.get(Amenity, amenity_id)
    if get_amenity is not None:
        storage.delete(get_amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def creates_amenity():
    """Creates a amenity object"""
    get_amenities = request.get_json()
    if not get_amenities:
        abort(400, 'Not a JSON')
    elif 'name' not in get_amenities:
        abort(400, 'Missing name')
    new_obj = Amenity(name=get_amenities['name'])
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id=None):
    """Updates a amenity objects by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    
    get_amenities = request.get_json()
    if not get_amenities:
        abort(400, 'Not a JSON')
    
    for key, value in get_amenities.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
