#!/usr/bin/python3
"""App file"""
from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close(self):
    """method to close session"""
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """ 404 handler """
    status = {"error": "Not found"}
    return make_response(jsonify(status), 404)

if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", "5000"), threaded=True)
