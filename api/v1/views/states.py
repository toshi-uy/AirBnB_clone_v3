#!/usr/bin/python3
"""States module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State

@app_views.route('/states/', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'])
def all_states(state_id=None):
    """Returns all state objects handeling states id"""
    states = []
    for key, value in storage.all('State').items():
        states.append(list(value.to_dict()))
    if not state_id:
        return jsonify(states)
    get_state = storage.get(State, state_id)
    if get_state is None:
        abort(404)
    else:
        jsonify(get_state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete(state_id=None):
    """Deletes a state objects by id"""
    get_state = storage.get(State, state_id)
    if get_state is not None:
        for key, value in get_state.items():
            if state_id == value.id:
                storage.delete(value)
                storage.save()
                return make_response(jsonify({}), 200)
        abort(404)

@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create():
    """Deletes a state object"""
    get_states = request.get_json()
    if not get_states:
        abort(400, 'Not a JSON')
    elif "name" not in get_states:
        abort(400, 'Missing name')
    else:
        new_obj = State(get_states['name'])
        storage.new(new_obj)
        storage.save()
        return make_response(jsonify(new_obj.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'])
def update(state_id=None):
    """Updates a state objects by id"""
    get_states = request.get_json()
    if not get_states:
        abort(404, 'Not a JSON')
    elif state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        for key, value in get_states.items():
            setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
    else:
        abort(404)
