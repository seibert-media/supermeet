from flask import jsonify

from .. import CONFIG
from ..google import GoogleAPI
from ..web import app


@app.route("/api/avatar/<email>/")
def api_google_avatar(email):
    g = GoogleAPI()
    avatar = g.get_profile_picture_from_email(email)

    return avatar if avatar else ""
