from datetime import datetime

from flask import abort, jsonify

from .. import CONFIG
from ..anny import AnnyAPI
from ..web import app


@app.route("/api/anny/<resource>/events/")
def api_anny_events(resource):
    if resource not in CONFIG["rooms"]["anny"]:
        abort(404)
    a = AnnyAPI()
    events = {}
    for e in a.get_events():
        if (
            str(e["relationships"]["resource"]["data"]["id"])
            not in CONFIG["rooms"]["anny"][resource]["resources"]
        ):
            continue
        description = e["attributes"]["description"]
        if description in ("Flex-Buchung",):
            description = e["attributes"]["note"].splitlines()[0]
        events[e["attributes"]["start_date"]] = {
            "end": datetime.fromisoformat(e["attributes"]["end_date"]).timestamp(),
            "id": e["id"],
            "start": datetime.fromisoformat(e["attributes"]["start_date"]).timestamp(),
            "title": description,
        }

    result = [v for k, v in sorted(events.items())]
    return jsonify(result)
