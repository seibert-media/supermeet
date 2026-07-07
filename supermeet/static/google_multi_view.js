events = {};


function update_display() {
    if (!events) {
        document.getElementById('booked').innerHTML = '<p>Warte auf Kalenderdaten ...</p>';
        return;
    }

    free = [];
    occupied = [];

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
            occupied.push({sort_key: new Date(current['end']).getTime(), content: tmp});
        } else if (next) {
            tmp += '<h2><span>' + room + '</span> ' + next['title'] + '</h2>';
            tmp += '<p>startet ' + time_until(next['start']) + '</p>';
            free.push({sort_key: new Date(next['start']).getTime(), content: tmp});
        } else {
            tmp += '<h2>' + room + '</h2>';
            tmp += '<p>Frei für mehr als 7 Tage</p>';
            free.push({sort_key: Infinity, content: tmp});
        }
    }

    if (occupied.length == Object.keys(rooms).length) {
        document.body.style.background = '#FF4400';
    } else if (occupied.length > 0) {
        document.body.style.background = '#FFBF00';
    } else {
        document.body.style.background = '#008000';
    }

    free.sort((a, b) => b.sort_key - a.sort_key);
    occupied.sort((a, b) => a.sort_key - b.sort_key);

    real_content = '';
    for (const item of free.concat(occupied)) {
        real_content += item.content;
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
