#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """ Returns a 'status ok' json """
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats():
    """ Returns number of each objects by type """
    objects = {"amenities": storage.count("Amenity"),
               "cities": storage.count("City"),
               "places": storage.count("Place"),
               "reviews": storage.count("Review"),
               "states": storage.count("State"),
               "users": storage.count("User")}
    return jsonify(objects)
