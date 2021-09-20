#!/usr/bin/python3
"""Reviews module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities1(place_id):
    """Returns all amenities from a place object"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    amenities = []
    for value in places.amenities:
        if value.place_id == place_id:
            amenities.append(value.to_dict())
    return jsonify(amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Deletes an amenity objects by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities or amenity_id not in place.amenity_ids:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def creates_amenity(place_id, amenity_id):
    """ Creates an amenity object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(400)
    if amenity not in place.amenities or amenity_id not in place.amenity_ids:
        new_obj = Amenity(place_id=place_id, amenity_id=amenity_id)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201
    return jsonify(amenity.to_dict()), 200
