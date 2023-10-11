events = {};


function update_display() {
    if (!events) {
        document.getElementById('booked').innerHTML = '<p>Warte auf Kalenderdaten ...</p>';
        return;
    }

    now = new Date(Date.now()).getTime()/1000;
    booked = '';
    available = '';
    num_booked = 0;


    for (const[room, evts] of Object.entries(events)) {
        current = get_current_event(evts);
        next = get_next_event(evts);

        if (current) {
            ends = new Date(current['end']).getTime();

            booked += '<h2><span>' + room + '</span> ' + current['title'] + '</h2>';
            booked += '<p>endet ' + time_until(current['end']) + '</p>';
            if (next) {
                booked += '<p><span>' + next['title'] + '</span> startet ' + time_until(next['start']) + '</p>';
            }

            num_booked += 1;
        } else if (next) {
            available += '<h2><span>' + room + '</span> ' + next['title'] + '</h2>';
            available += '<p>startet ' + time_until(next['start']) + '</p>';
        } else {
            available += '<h2>' + room + '</h2>';
            available += '<p>Frei für mehr als 7 Tage</p>';
        }
    }

    if (num_booked == Object.keys(rooms).length) {
        document.body.style.background = '#FF4400';
    } else if (num_booked > 0) {
        document.body.style.background = '#FFBF00';
    } else {
        document.body.style.background = '#008000';
    }

    document.getElementById('booked').innerHTML = booked;
    document.getElementById('available').innerHTML = available;
}
window.setInterval(update_display, 1000);


function fetch_events(room_name) {
    console.info('fetching events for ' + room_name + ' from ' + rooms[room_name]);

    req = new XMLHttpRequest();
    req.open('GET', rooms[room_name]);
    req.setRequestHeader('Accept', 'application/json');
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.addEventListener('load', function(event) {
        events[room_name] = JSON.parse(req.responseText);
    });
    req.send();
}
