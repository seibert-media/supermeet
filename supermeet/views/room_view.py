from flask import abort, render_template

from .. import APP_STARTUP, CONFIG
from ..web import app


@app.route("/room/<room_id>/")
def room_view(room_id):
    room_type = None
    if room_id in CONFIG["rooms"]["google"]:
        room_type = "google"
    elif room_id in CONFIG["rooms"]["anny"]:
        room_type = "anny"

    if not room_type:
        abort(404)

    return render_template(
        "room_view.html",
        app_startup=APP_STARTUP,
        room=CONFIG["rooms"][room_type][room_id],
        room_id=room_id,
        room_type=room_type,
    )
