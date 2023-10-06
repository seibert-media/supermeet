import logging
from os import environ
from os.path import abspath, dirname

from flask import Flask

FLASK_ROOT = dirname(abspath(__file__))
PROJECT_ROOT = dirname(FLASK_ROOT)

app = Flask('supermeet')
app.secret_key = environ['FLASK_SECRET']

if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)


from .views import *
