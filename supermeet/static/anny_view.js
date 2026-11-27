room_info = null;


function update_display() {
    container = document.getElementById('supermeet');

    if (!room_info) {
        replace_children(container, [make_element('p', 'Warte auf Kalenderdaten ...')]);
        return;
    }

    document.getElementById("room_name").textContent = room_info['name'];

    // the description is maintained as html in anny by its admins
    description = make_element('div');
    description.innerHTML = room_info['description'];
    out = [description];
    num_booked = 0;

    for (i in room_info['children']) {
        child = room_info['children'][i];

        current = get_current_event(child['events']);
        next = get_next_event(child['events']);

        if (current) {
            out.push(make_element_with_span('h2', child['name'], current['title']));
            out.push(make_element('p', 'endet ' + time_until(current['end'])));
            if (next) {
                out.push(make_element_with_span('p', next['title'], 'startet ' + time_until(next['start'])));
            }
            num_booked += 1;
        } else if (next) {
            out.push(make_element_with_span('h2', child['name'], next['title']));
            out.push(make_element('p', 'startet ' + time_until(next['start'])));
        } else {
            out.push(make_element('h2', child['name']));
            out.push(make_element('p', 'Frei für mehr als 7 Tage'));
        }
    }

    if (num_booked == Object.keys(room_info['children']).length) {
        document.body.style.background = '#FF4400';
    } else if (num_booked > 0) {
        document.body.style.background = '#FFBF00';
    } else {
        document.body.style.background = '#008000';
    }

    replace_children(container, out);
}
window.setInterval(update_display, 1000);


function fetch_events() {
    console.info('fetching events from ' + api_room_events);

    xhr_get(api_room_events, function(event) {
        room_info = JSON.parse(event.target.responseText);
    });
}
