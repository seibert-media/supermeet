events = {};


function update_display() {
    if (!events) {
        document.getElementById('booked').innerHTML = '<p>Warte auf Kalenderdaten ...</p>';
        return;
    }

    now = new Date(Date.now()).getTime()/1000;
    content = {};
    num_booked = 0;

    for (const[room, evts] of Object.entries(events)) {
        current = get_current_event(evts);
        next = get_next_event(evts);
        tmp = '';

        if (current) {
            tmp += '<h2><span>' + room + '</span> ' + current['title'] + '</h2>';
            tmp += '<p>endet ' + time_until(current['end']) + '</p>';
            if (next) {
                tmp += '<p><span>' + next['title'] + '</span> startet ' + time_until(next['start']) + '</p>';
            }
            content[current['end'].toString() + room] = tmp;
            num_booked += 1;
        } else if (next) {
            tmp += '<h2><span>' + room + '</span> ' + next['title'] + '</h2>';
            tmp += '<p>startet ' + time_until(next['start']) + '</p>';
            content[next['start'].toString() + room] = tmp;
        } else {
            tmp += '<h2>' + room + '</h2>';
            tmp += '<p>Frei für mehr als 7 Tage</p>';
            content[room] = tmp;
        }
    }

    if (num_booked == Object.keys(rooms).length) {
        document.body.style.background = '#FF4400';
    } else if (num_booked > 0) {
        document.body.style.background = '#FFBF00';
    } else {
        document.body.style.background = '#008000';
    }

    real_content = '';
    keys = Object.keys(content);
    keys.sort()
    for (const k of keys) {
        real_content += content[k];
    }

    document.getElementById('supermeet').innerHTML = real_content;
}
window.setInterval(update_display, 1000);


function fetch_events(room_name) {
    console.info('fetching events for ' + room_name + ' from ' + rooms[room_name]);

    xhr_get(rooms[room_name], function(event) {
        events[room_name] = JSON.parse(req.responseText);
    });
}
