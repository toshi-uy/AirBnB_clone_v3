#!/usr/bin/python3
"""Users module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_users():
    """Returns all user objects handeling users id"""
    users = []
    for value in storage.all(User).values():
        users.append(value.to_dict())
    return jsonify(users), 200


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def one_user(user_id=None):
    """Returns a user by user id"""
    get_user = storage.get(User, user_id)
    if get_user is None:
        abort(404)
    return jsonify(get_user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user objects by id"""
    get_user = storage.get(User, user_id)
    if get_user is not None:
        storage.delete(get_user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def creates_user():
    """Creates a user object"""
    get_users = request.get_json()
    if not get_users:
        abort(400, 'Not a JSON')
    elif 'name' not in get_users:
        abort(400, 'Missing name')
    elif 'password' not in get_users:
        abort(400, 'Missing password')
    elif 'email' not in get_users:
        abort(400, 'Missing email')
    new_obj = User(email=get_users['email'], password=get_users['password'])
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id=None):
    """Updates a user objects by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    get_users = request.get_json()
    if not get_users:
        abort(400, 'Not a JSON')

    for key, value in get_users.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
