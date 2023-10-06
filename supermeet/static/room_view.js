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
            out += '<p>Nächster Termin ' + time_until(next['start']) + '</p>';
        }

        if ((ends - now) > 600) {
            out += '<p class="buttons"><button onclick="cancel_event(\'' + current['id'] + '\');">Vorzeitig beenden</button></p>';
        }
    } else if (next) {
        out += '<h2>' + next['title'] + '</h2>';
        out += '<p>startet ' + time_until(next['start']) + '</p>';
    } else {
        out += '<p>Frei für mehr als 7 Tage</p>';
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

function cancel_event(event_id) {
    console.warn('cancelling event with id ' + event_id);

    params = JSON.stringify({
        event_id: event_id,
        until: new Date().toISOString()
    })

    req = new XMLHttpRequest();
    req.open('POST', api_event_cancel);
    req.setRequestHeader('Accept', 'application/json');
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.addEventListener('load', function(event) {
        console.debug(req.responseText);
        result = JSON.parse(req.responseText);

        if (result['status'] == 'ok') {
            fetch_events();
        }
    });
    req.send(params);
}
