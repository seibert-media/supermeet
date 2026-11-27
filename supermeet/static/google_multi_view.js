events = {};


function update_display() {
    if (Object.keys(events).length == 0) {
        replace_children(document.getElementById('supermeet'), [make_element('p', 'Warte auf Kalenderdaten ...')]);
        return;
    }

    free = [];
    occupied = [];

    for (const[room, evts] of Object.entries(events)) {
        current = get_current_event(evts);
        next = get_next_event(evts);
        tmp = [];

        if (current) {
            tmp.push(make_element_with_span('h2', room, current['title']));
            tmp.push(make_element('p', 'endet ' + time_until(current['end'])));
            if (next) {
                tmp.push(make_element_with_span('p', next['title'], 'startet ' + time_until(next['start'])));
            }
            occupied.push({sort_key: new Date(current['end']).getTime(), content: tmp});
        } else if (next) {
            tmp.push(make_element_with_span('h2', room, next['title']));
            tmp.push(make_element('p', 'startet ' + time_until(next['start'])));
            free.push({sort_key: new Date(next['start']).getTime(), content: tmp});
        } else {
            tmp.push(make_element('h2', room));
            tmp.push(make_element('p', 'Frei für mehr als 7 Tage'));
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

    real_content = [];
    for (const item of free.concat(occupied)) {
        real_content.push(...item.content);
    }

    replace_children(document.getElementById('supermeet'), real_content);
}
window.setInterval(update_display, 1000);


function fetch_events(room_name) {
    console.info('fetching events for ' + room_name + ' from ' + rooms[room_name]);

    xhr_get(rooms[room_name], function(event) {
        events[room_name] = JSON.parse(req.responseText);
    });
}
