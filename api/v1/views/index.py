#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {"amenities": 'Amenity', "cities": 'City',
           "places": 'Place', "reviews": 'Review', "states": 'State',
           "users": 'User'}


@app_views.route("/status")
def status():
    """ Returns a 'status ok' json """
    return jsonify({'status': 'OK'})

@app_views.route("/stats")
def counting():
    """ Returns number of each objects by type """
    for key, value in classes.items():
        count = storage.count(value)
        classes[key] = count
        return jsonify(classes)
