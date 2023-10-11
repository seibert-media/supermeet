try:
    from tomllib import loads as toml_load
except ImportError:
    from rtoml import load as toml_load

from datetime import datetime
from os import environ

with open(environ["APP_CONFIG"]) as c:
    CONFIG = toml_load(c.read())

# this is used by the clients to determine if the display has to be
# refreshed
APP_STARTUP = int(datetime.utcnow().timestamp())
