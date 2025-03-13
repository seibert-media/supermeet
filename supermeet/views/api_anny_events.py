from datetime import datetime

from flask import abort, jsonify

from .. import CONFIG
from ..anny import anny_api
from ..web import app


@app.route("/api/anny/<resource>/details/")
def api_anny_details(resource):
    if resource not in CONFIG["rooms"]["anny"]:
        abort(404)
    events = {}
    resources = anny_api.get_resources()

    if CONFIG["rooms"]["anny"][resource] not in resources:
        app.logger.error(
            f"configured anny room {resource} ({CONFIG['rooms']['anny'][resource]}) not found in anny api result!"
        )
        abort(404)

    result = {
        "name": resources[CONFIG["rooms"]["anny"][resource]]["name"],
        "description": resources[CONFIG["rooms"]["anny"][resource]]["description"],
        "children": {
            child_id: {
                "name": child_name,
                "events": [],
            }
            for child_id, child_name in resources[CONFIG["rooms"]["anny"][resource]][
                "children"
            ].items()
        },
    }

    child_events = {
        child_id: {}
        for child_id in resources[CONFIG["rooms"]["anny"][resource]]["children"]
    }

    for e in anny_api.get_events(
        resources=list(resources[CONFIG["rooms"]["anny"][resource]]["children"])
    ):
        try:
            resource_id = int(e["relationships"]["resource"]["data"]["id"])
        except KeyError:
            continue

        if resource_id not in child_events:
            continue

        description = e["attributes"]["description"]
        if description in ("Flex-Buchung",):
            description = e["attributes"]["note"].splitlines()[0]

        if e["attributes"].get("is_series_master"):
            # ignore parent of series bookings
            continue

        child_events[resource_id][e["attributes"]["start_date"]] = {
            "end": int(datetime.fromisoformat(e["attributes"]["end_date"]).timestamp()),
            "id": e["id"],
            "start": int(datetime.fromisoformat(e["attributes"]["start_date"]).timestamp()),
            "title": description,
        }

    for child_id, events in child_events.items():
        result["children"][child_id]["events"] = [v for k, v in sorted(events.items())]

    return jsonify(result)
