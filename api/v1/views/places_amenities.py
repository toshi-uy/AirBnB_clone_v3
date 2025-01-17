#!/usr/bin/python3
"""Reviews module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from os import environ
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_place_amenities(place_id):
    """Returns all amenities from a place object"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    amenities = []
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        for value in places.amenities:
            amenities.append(value.to_dict())
    else:
        for value in places.amenity_ids:
            amenities.append(storage.get(Amenity, value).to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an amenity objects by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def creates_place_amenity(place_id, amenity_id):
    """ Creates an amenity object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
