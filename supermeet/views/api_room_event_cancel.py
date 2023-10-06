from flask import abort, jsonify, request

from .. import CONFIG
from ..google import GoogleAPI
from ..web import app


@app.route('/api/rooms/google/<room_id>/event/update/', methods=['POST'])
def api_room_event_cancel(room_id):
    if room_id not in CONFIG['rooms']['google']:
        abort(404)

    event_id = request.json.get('event_id')
    until = request.json.get('until')

    if not event_id or not until:
        abort(400)

    try:
        g = GoogleAPI()
        g.patch_room_event_end_time(
            CONFIG['rooms']['google'][room_id]['id'],
            event_id,
            until,
        )
        return jsonify({'status': 'ok'})
    except Exception as e:
        return (
            jsonify(
                {
                    'status': 'error',
                    'msg': repr(e),
                }
            ),
            500,
        )
