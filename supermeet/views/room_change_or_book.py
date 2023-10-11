from datetime import datetime, timedelta, timezone

from flask import abort, redirect, render_template, request, url_for

from .. import CONFIG
from ..google import GoogleAPI
from ..web import app


@app.route('/room/<room_id>/update/', methods=['GET', 'POST'])
def room_change_or_book(room_id):
    if room_id not in CONFIG['rooms']['google']:
        abort(404)

    g = GoogleAPI()
    current_event = None
    next_event_date = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(
        days=14
    )
    now = datetime.utcnow().replace(tzinfo=timezone.utc)

    for event in g.get_room_events(CONFIG['rooms']['google'][room_id]['id']):
        start = datetime.fromisoformat(event['start']['dateTime'])
        end = datetime.fromisoformat(event['end']['dateTime'])

        if start <= now < end and not current_event:
            current_event = event

        if start > now and start < next_event_date:
            next_event_date = start

    if current_event:
        if 'end_now' in request.args:
            g.patch_room_event_end_time(
                CONFIG['rooms']['google'][room_id]['id'],
                current_event['id'],
                g._date(now),
            )
            return redirect(url_for('room_view', room_id=room_id))

    event_id = request.form.get('event_id')
    if current_event and event_id and current_event['id'] != event_id:
        abort(400)

    if request.method == 'POST':
        new_end = now + timedelta(minutes=int(request.form['input_minutes']))
        if event_id:
            g.patch_room_event_end_time(
                CONFIG['rooms']['google'][room_id]['id'],
                event_id,
                g._date(new_end),
            )
        else:
            g.create_event(
                CONFIG['rooms']['google'][room_id]['id'],
                request.form['input_title'],
                g._date(now),
                g._date(new_end),
            )
        return redirect(url_for('room_view', room_id=room_id))

    # limit this to 8 hours. If you need the room for longer, you have
    # to book in google calendar.
    minutes_until_next_event = min(
        int((next_event_date - now).total_seconds() / 60), 8 * 60
    )

    slider_value = 60
    if current_event:
        slider_value = int(
            (datetime.fromisoformat(event['end']['dateTime']) - now).total_seconds()
            / 60
        )

    if not event_id and current_event:
        event_id = current_event['id']

    return render_template(
        'room_change_or_book.html',
        current_event=current_event,
        event_id=event_id or '',
        minutes_until_next_event=minutes_until_next_event,
        room_id=room_id,
        room=CONFIG['rooms']['google'][room_id],
        slider_value=slider_value,
    )
