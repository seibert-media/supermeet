try:
    from tomllib import loads as toml_load
except ImportError:
    from rtoml import load as toml_load

from os import environ

with open(environ['APP_CONFIG']) as c:
    CONFIG = toml_load(c.read())
