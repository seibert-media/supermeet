from datetime import datetime

from flask import abort, jsonify

from .. import CONFIG
from ..google import GoogleAPI
from ..web import app


@app.route("/api/rooms/google/<room_id>/events/")
def api_room_events(room_id):
    if room_id not in CONFIG["rooms"]["google"]:
        abort(404)
    g = GoogleAPI()
    events = {}
    for e in g.get_room_events(CONFIG["rooms"]["google"][room_id]["id"]):
        events[e["start"]["dateTime"]] = {
            "title": e["summary"].strip(),
            "description": e.get("description"),
            "start": datetime.fromisoformat(e["start"]["dateTime"]).timestamp(),
            "end": datetime.fromisoformat(e["end"]["dateTime"]).timestamp(),
            "id": e["id"],
        }

    result = [v for k, v in sorted(events.items())]
    return jsonify(result)
