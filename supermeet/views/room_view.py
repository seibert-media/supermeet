from flask import abort, render_template

from .. import CONFIG
from ..web import app


@app.route('/room/<room_id>/')
def room_view(room_id):
    if room_id not in CONFIG['rooms']['google']:
        abort(404)

    return render_template(
        'room_view.html', room_id=room_id, room=CONFIG['rooms']['google'][room_id]
    )
