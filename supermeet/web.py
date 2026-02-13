import logging
from os import environ
from os.path import abspath, dirname

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

FLASK_ROOT = dirname(abspath(__file__))
PROJECT_ROOT = dirname(FLASK_ROOT)

app = Flask("supermeet")
app.secret_key = environ["FLASK_SECRET"]

if environ.get("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=environ["SENTRY_DSN"],
        send_default_pii=True,
        integrations=[
            FlaskIntegration(
                transaction_style="url",
            ),
        ],
    )

if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)


from .views import *
