#!/usr/bin/env python3

from os import environ
from os.path import abspath, dirname, join

ROOT = dirname(abspath(__file__))

environ.setdefault('APP_CONFIG', join(ROOT, 'config.toml'))
environ.setdefault('APP_SECRETS', join(ROOT, 'serviceaccount.json'))
environ.setdefault('FLASK_SECRET', 'just-for-testing')

from supermeet.web import app

app.run(debug=True)
