#!/usr/bin/python3
"""States module"""
from flask.json import jsonify
from api.v1.views import app_views
from flask import Flask, Request
from models import storage

@app_views.route('/api/v1/states', methods=['GET'])
def all_states():
    """Returns all state objects."""
    states = []
    for key, value in storage.all('State').items():
        states.append(value.to_dict())
    return jsonify(states)
