from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", "5000"))
