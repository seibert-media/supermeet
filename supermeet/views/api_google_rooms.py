from flask import jsonify, url_for

from .. import CONFIG
from ..web import app


@app.route("/api/rooms/")
def api_google_rooms():
    rooms = []

    for identifier, room in CONFIG["rooms"]["google"].items():
        rooms.append(
            {
                "name": room["name"],
                "id": room["id"],
                "urls": {
                    "events": url_for("api_room_events", room_id=identifier),
                },
            }
        )
    return jsonify(rooms)
