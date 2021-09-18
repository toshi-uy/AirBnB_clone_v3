#!/usr/bin/python3
"""States module"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State

@app_views.route('/states/', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'])
def all_states(state_id=None):
    """Returns all state objects."""
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
