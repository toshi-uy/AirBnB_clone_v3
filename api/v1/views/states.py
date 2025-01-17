#!/usr/bin/python3
"""States module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'])
def all_states(state_id=None):
    """Returns all state objects handeling states id"""
    states = []
    for value in storage.all(State).values():
        states.append(value.to_dict())
    if not state_id:
        return jsonify(states)
    get_state = storage.get(State, state_id)
    if get_state is None:
        abort(404)
    return jsonify(get_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    """Deletes a state objects by id"""
    get_state = storage.get(State, state_id)
    if get_state is not None:
        storage.delete(get_state)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def creates_state():
    """Creates a state object"""
    get_states = request.get_json()
    if not get_states:
        abort(400, 'Not a JSON')
    elif 'name' not in get_states:
        abort(400, 'Missing name')
    new_obj = State(name=get_states['name'])
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id=None):
    """Updates a state objects by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    get_states = request.get_json()
    if not get_states:
        abort(400, 'Not a JSON')

    for key, value in get_states.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
