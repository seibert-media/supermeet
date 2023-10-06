from flask import abort, render_template

from .. import CONFIG
from ..web import app


@app.route('/multi/<multi_id>/')
def multi_view(multi_id):
    if multi_id not in CONFIG['multi']:
        abort(404)

    rooms = [
        {
            'name': CONFIG['rooms']['google'][room]['name'],
            'id': room,
        }
        for room in CONFIG['multi'][multi_id]['rooms']
    ]

    return render_template(
        'multi_view.html',
        multi=CONFIG['multi'][multi_id],
        rooms=rooms,
    )
