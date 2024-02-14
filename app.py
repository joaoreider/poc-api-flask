from flask import Flask
from main import init_app
from os import environ


def create_app():
    app = Flask(__name__)
    init_app(app)
    return app