#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {"Amenity": 0, "BaseModel": 0, "City": 0,
           "Place": 0, "Review": 0,"State": 0,
           "User": 0}


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
