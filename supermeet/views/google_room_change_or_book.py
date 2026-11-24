import logging
from datetime import UTC, datetime, timedelta

from flask import abort, redirect, render_template, request, url_for

from .. import CONFIG
from ..google import GoogleAPI
from ..web import app

logger = logging.getLogger(__name__)


@app.route("/room/<room_id>/update/", methods=["GET", "POST"])
def google_room_change_or_book(room_id):
    if room_id not in CONFIG["rooms"]["google"]:
        abort(404)

    g = GoogleAPI()
    current_event = None
    next_event_date = datetime.now(UTC) + timedelta(days=14)
    now = datetime.now(UTC)

    for event in g.get_room_events(CONFIG["rooms"]["google"][room_id]["id"]):
        start = datetime.fromisoformat(event["start"]["dateTime"])
        end = datetime.fromisoformat(event["end"]["dateTime"])

        if start <= now < end and not current_event:
            current_event = event

        if start > now and start < next_event_date:
            next_event_date = start

    # limit this to 8 hours. If you need the room for longer, you have
    # to book in google calendar.
    minutes_until_next_event = min(
        int((next_event_date - now).total_seconds() / 60), 8 * 60
    )

    event_id = request.form.get("event_id")

    if request.method == "POST":
        # only ever change the event which is currently running, and only
        # create a new one if the room is free
        if current_event and event_id != current_event["id"]:
            abort(400)
        if not current_event and event_id:
            abort(400)

        if "end_now" in request.form:
            if not current_event:
                abort(400)
            minutes = 0
        else:
            try:
                minutes = int(request.form["input_minutes"])
            except (KeyError, ValueError):
                abort(400)
            minutes = max(0, min(minutes, minutes_until_next_event))

        new_end = now + timedelta(minutes=minutes)
        if current_event:
            try:
                g.patch_room_event_end_time(
                    CONFIG["rooms"]["google"][room_id]["id"],
                    current_event["id"],
                    g._date(new_end),
                )
            except Exception:
                logger.exception(
                    f"failed changing end time for event {current_event['id']} in calendar {room_id}"
                )
        else:
            try:
                g.create_event(
                    CONFIG["rooms"]["google"][room_id]["id"],
                    request.form["input_title"],
                    g._date(now),
                    g._date(new_end),
                )
            except Exception:
                logger.exception(f"failed creating event in calendar {room_id}")
        return redirect(url_for("room_view", room_id=room_id))

    slider_value = 60
    if current_event:
        slider_value = int(
            (
                datetime.fromisoformat(current_event["end"]["dateTime"]) - now
            ).total_seconds()
            / 60
        )

    if not event_id and current_event:
        event_id = current_event["id"]

    return render_template(
        "room_change_or_book.html",
        current_event=current_event,
        event_id=event_id or "",
        minutes_until_next_event=minutes_until_next_event,
        room_id=room_id,
        room=CONFIG["rooms"]["google"][room_id],
        slider_value=slider_value,
    )
