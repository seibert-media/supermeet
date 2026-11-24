from datetime import UTC, datetime
from os import environ
from tomllib import loads as toml_load

with open(environ["APP_CONFIG"]) as c:
    CONFIG = toml_load(c.read())

# this is used by the clients to determine if the display has to be
# refreshed
APP_STARTUP = int(datetime.now(UTC).timestamp())
