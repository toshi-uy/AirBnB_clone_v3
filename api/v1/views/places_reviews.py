#!/usr/bin/python3
"""Reviews module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id=None):
    """Returns all reviews from a place object"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    reviews = []
    for value in places.reviews:
        reviews.append(value.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def one_review(review_id=None):
    """Returns a review by review id"""
    get_review = storage.get(Review, review_id)
    if get_review is None:
        abort(404)
    return jsonify(get_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id=None):
    """Deletes a review objects by id"""
    get_review = storage.get(Review, review_id)
    if get_review is not None:
        storage.delete(get_review)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def creates_review(place_id=None):
    """Creates a review object"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    get_reviews = request.get_json()
    if not get_reviews:
        abort(400, 'Not a JSON')
    elif 'name' not in get_reviews:
        abort(400, 'Missing name')
    new_obj = Review(name=get_reviews['name'], place_id=places.id)
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id=None):
    """Updates a review objects by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    get_reviews = request.get_json()
    if not get_reviews:
        abort(400, 'Not a JSON')

    for key, value in get_reviews.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
