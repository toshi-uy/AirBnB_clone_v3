#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {"Amenity": 'Amenity', "BaseModel": 'BaseModel', "City": 'City',
           "Place": 'Place', "Review": 'Review',"State": 'State',
           "User": 'User'}


@app_views.route("/status")
def status():
    """ Returns a 'status ok' json """
    return jsonify({'status': 'OK'})

@app_views.route("/stats")
def counting():
    """ Returns number of each objects by type """
    objects = {"amenities": storage.count("Amenity"),
               "cities": storage.count("City"),
               "places": storage.count("Place"),
               "reviews": storage.count("Review"),
               "states": storage.count("State"),
               "users": storage.count("User")}
    return jsonify(objects)