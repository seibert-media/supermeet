events = null;


function update_display() {
    container = document.getElementById('supermeet');

    if (!events) {
        replace_children(container, [make_element('p', 'Warte auf Kalenderdaten ...')]);
        return;
    }

    now = new Date(Date.now()).getTime()/1000;
    current = get_current_event(events);
    next = get_next_event(events);

    out = [];
    avatar = ''
    if (current) {
        ends = new Date(current['end']).getTime();

        out.push(make_element('h2', current['title']));
        out.push(make_element('p', 'endet ' + time_until(current['end'])));
        if (next) {
            out.push(make_element_with_span('p', next['title'], 'startet ' + time_until(next['start'])));
        }

        buttons = make_element('div');
        buttons.className = 'buttons';
        if ((ends - now) > 600) {
            form = make_element('form');
            form.method = 'post';
            form.action = booking_link;
            for (const [name, value] of [['event_id', current['id']], ['end_now', '1']]) {
                hidden = make_element('input');
                hidden.type = 'hidden';
                hidden.name = name;
                hidden.value = value;
                form.append(hidden);
            }
            submit = make_element('input');
            submit.type = 'submit';
            submit.value = 'Vorzeitig beenden';
            form.append(submit);
            buttons.append(form);
        }
        link = make_element('a', 'Buchung verändern');
        link.href = booking_link;
        buttons.append(link);
        out.push(buttons);
        avatar = current['creator_avatar'];
    } else if (next) {
        out.push(make_element('h2', next['title']));
        out.push(make_element('p', 'startet ' + time_until(next['start'])));
        avatar = next['creator_avatar'];
    } else {
        out.push(make_element('p', 'Frei für mehr als 7 Tage'));
    }

    if (!current) {
        buttons = make_element('p');
        buttons.className = 'buttons';
        link = make_element('a', 'Raum buchen');
        link.href = booking_link;
        buttons.append(link);
        out.push(buttons);
    }

    if (current) {
        document.body.style.background = '#FF4400';
    } else {
        document.body.style.background = '#008000';
    }

    replace_children(container, out);
    load_avatar(avatar);
}
window.setInterval(update_display, 1000);


function fetch_events() {
    console.info('fetching events from ' + api_room_events);

    xhr_get(api_room_events, function(event) {
        events = JSON.parse(event.target.responseText);
    });
}
