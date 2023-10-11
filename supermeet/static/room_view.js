events = null;


function update_display() {
    if (!events) {
        document.getElementById('supermeet').innerHTML = '<p>Warte auf Kalenderdaten ...</p>';
        return;
    }

    now = new Date(Date.now()).getTime()/1000;
    current = get_current_event(events);
    next = get_next_event(events);

    out = '';
    if (current) {
        ends = new Date(current['end']).getTime();

        out += '<h2>' + current['title'] + '</h2>';
        out += '<p>endet ' + time_until(current['end']) + '</p>';
        if (next) {
            out += '<p>' + next['title'] + ' ' + time_until(next['start']) + '</p>';
        }

        out += '<p class="buttons">';
        if ((ends - now) > 600) {
            out += '<a href="' + booking_link + '?end_now">Vorzeitig beenden</a>';
        }
        out += '<a href="' + booking_link + '">Buchung verändern</a>';
        out += '</p>';
    } else if (next) {
        out += '<h2>' + next['title'] + '</h2>';
        out += '<p>startet ' + time_until(next['start']) + '</p>';
    } else {
        out += '<p>Frei für mehr als 7 Tage</p>';
    }

    if (!current) {
        out += '<p class="buttons">';
        out += '<a href="' + booking_link + '">Raum buchen</a>';
        out += '</p>';
    }

    if (current) {
        document.body.style.background = '#FF4400';
    } else {
        document.body.style.background = '#008000';
    }

    document.getElementById('supermeet').innerHTML = out;
}
window.setInterval(update_display, 1000);


function fetch_events() {
    console.info('fetching events from ' + api_room_events);

    req = new XMLHttpRequest();
    req.open('GET', api_room_events);
    req.setRequestHeader('Accept', 'application/json');
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.addEventListener('load', function(event) {
        events = JSON.parse(req.responseText);
    });
    req.send();
}
