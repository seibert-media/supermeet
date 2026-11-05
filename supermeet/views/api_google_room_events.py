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
            organizer_email = e.get("organizer", {}).get("email")
            if organizer_email:
                organizer_profile = g.get_profile_from_email(organizer_email)
            else:
                organizer_profile = {}

            is_confidential = e.get("visibility") in ("private", "confidential")
            if CONFIG["rooms"]["google"][room_id].get("force_anonymize", False):
                title = "Belegt"
            elif e.get("summary") and not is_confidential:
                title = e["summary"]
            elif e.get("organizer", {}).get("displayName"):
                title = e["organizer"]["displayName"]
            elif organizer_profile and organizer_profile.get("name"):
                title = organizer_profile["name"]
            elif organizer_email:
                title = organizer_email
            else:
                title = "Belegt"

            if e["start"].get("dateTime"):
                start = int(datetime.fromisoformat(e["start"]["dateTime"]).timestamp())
            elif e["start"].get("date"):
                start = int(datetime.fromisoformat(e["start"]["date"]).timestamp())
            else:
                raise ValueError(f"could not figure out start time: {e['start']!r}")

            if e["end"].get("dateTime"):
                end = int(datetime.fromisoformat(e["end"]["dateTime"]).timestamp())
            elif e["end"].get("date"):
                end = int(datetime.fromisoformat(e["end"]["date"]).timestamp())
            else:
                raise ValueError(f"could not figure out end time: {e['end']!r}")

            events[start] = {
                "creator": organizer_email,
                "creator_avatar": organizer_profile.get("avatar"),
                "end": end,
                "id": e["id"],
                "start": start,
                "title": title.strip(),
            }
        except KeyError:
            app.logger.exception(
                f"{room_id}: could not add event '{e.get('id')}' to list of events"
            )

    result = [v for k, v in sorted(events.items())]
    return jsonify(result)
