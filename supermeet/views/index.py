from flask import render_template, url_for

from .. import CONFIG
from ..web import app


@app.route("/")
def index():
    rooms = []
    for identifier, multi in CONFIG.get("multi", {}).items():
        rooms.append((multi["name"], url_for("multi_view", multi_id=identifier)))

    for identifier, room in CONFIG["rooms"]["google"].items():
        rooms.append(
            (f'Google: {room["name"]}', url_for("room_view", room_id=identifier))
        )

    for identifier, room in CONFIG["rooms"]["anny"].items():
        rooms.append(
            (f'Anny: {room["name"]}', url_for("room_view", room_id=identifier))
        )

    return render_template("index.html", rooms=rooms)
