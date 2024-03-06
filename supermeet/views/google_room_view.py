from flask import abort, render_template

from .. import APP_STARTUP, CONFIG
from ..web import app


@app.route("/room/<room_id>/")
def google_room_view(room_id):
    if room_id not in CONFIG["rooms"]["google"]:
        abort(404)

    return render_template(
        "room_view.html",
        app_startup=APP_STARTUP,
        room=CONFIG["rooms"]["google"][room_id],
        room_id=room_id,
    )
