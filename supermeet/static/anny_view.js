room_info = null;


function update_display() {
    if (!room_info) {
        document.getElementById('supermeet').innerHTML = '<p>Warte auf Kalenderdaten ...</p>';
        return;
    }

    document.getElementById("room_name").innerHTML = room_info['name'];

    now = new Date(Date.now()).getTime()/1000;
    out = '';
    num_booked = 0;

    for (i in room_info['children']) {
        child = room_info['children'][i];

        current = get_current_event(child['events']);
        next = get_next_event(child['events']);

        if (current) {
            out += '<h2><span>' + child['name'] + '</span> ' + current['title'] + '</h2>';
            out += '<p>endet ' + time_until(current['end']) + '</p>';
            if (next) {
                out += '<p><span>' + next['title'] + '</span> startet ' + time_until(next['start']) + '</p>';
            }
            num_booked += 1;
        } else if (next) {
            out += '<h2><span>' + child['name'] + '</span> ' + next['title'] + '</h2>';
            out += '<p>startet ' + time_until(next['start']) + '</p>';
        } else {
            out += '<h2>' + child['name'] + '</h2>';
            out += '<p>Frei für mehr als 7 Tage</p>';
        }
    }

    if (num_booked == Object.keys(room_info['children']).length) {
        document.body.style.background = '#FF4400';
    } else if (num_booked > 0) {
        document.body.style.background = '#FFBF00';
    } else {
        document.body.style.background = '#008000';
    }

    document.getElementById('supermeet').innerHTML = out;
}
window.setInterval(update_display, 1000);


function fetch_events() {
    console.info('fetching events from ' + api_room_events);

    xhr_get(api_room_events, function(event) {
        room_info = JSON.parse(req.responseText);
    });
}
