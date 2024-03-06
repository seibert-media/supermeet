events = null;


function update_display() {
    if (!events) {
        document.getElementById('supermeet').innerHTML = '<p>Warte auf Kalenderdaten ...</p>';
        return;
    }

    now = new Date(Date.now()).getTime()/1000;
    out = '';

    for (i in events) {
        event = events[i];

        event_start = new Date(event['start']).getTime();
        event_end = new Date(event['end']).getTime();

        if (event_start <= now && event_end > now) {
            out += '<h2>' + event['title'] + '</h2>';
            out += '<p>endet ' + time_until(event['end']) + '</p>';
        }
    }

    if (out) {
        document.body.style.background = '#FF4400';
    } else {
        document.body.style.background = '#008000';
        out += "<h2>Alle Plätze verfügbar</h2>";
    }

    document.getElementById('supermeet').innerHTML = out;
}
window.setInterval(update_display, 1000);


function fetch_events() {
    console.info('fetching events from ' + api_room_events);

    xhr_get(api_room_events, function(event) {
        events = JSON.parse(req.responseText);
    });
}
