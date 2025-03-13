from datetime import datetime

from flask import abort, jsonify

from .. import CONFIG
from ..google import GoogleAPI
from ..web import app


@app.route("/api/rooms/google/<room_id>/events/")
def api_google_room_events(room_id):
    if room_id not in CONFIG["rooms"]["google"]:
        abort(404)
    g = GoogleAPI()
    events = {}
    for e in g.get_room_events(CONFIG["rooms"]["google"][room_id]["id"]):
        try:
            is_confidential = e.get("visibility") in ("private", "confidential")
            if e.get("summary") and not is_confidential:
                title = e["summary"]
            elif e["organizer"].get("displayName"):
                title = e["organizer"]["displayName"]
            else:
                title = e["organizer"]["email"]
            events[e["start"]["dateTime"]] = {
                "creator": e["organizer"]["email"],
                "description": e.get("description") if not is_confidential else "",
                "end": int(datetime.fromisoformat(e["end"]["dateTime"]).timestamp()),
                "id": e["id"],
                "start": int(datetime.fromisoformat(e["start"]["dateTime"]).timestamp()),
                "title": title.strip(),
            }
        except KeyError as e:
            app.logger.exception(
                "could not add event '{e.get(\"id\")}' to list of events"
            )

    result = [v for k, v in sorted(events.items())]
    return jsonify(result)
