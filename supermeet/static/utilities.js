current_avatar = null;

function get_current_event(events) {
    now = new Date(Date.now()).getTime()/1000;

    for (i in events) {
        event = events[i];

        event_start = new Date(event['start']).getTime();
        event_end = new Date(event['end']).getTime();

        if (event_start <= now && event_end > now) {
            return event;
        }
    }
    return null;
}


function get_next_event(events) {
    now = new Date(Date.now()).getTime()/1000;
    next_event_time = 0;
    next_event = null;

    for (i in events) {
        event = events[i];

        event_start = new Date(event['start']).getTime();

        if (
            event_start > now &&
            (next_event_time == 0 || event_start < next_event_time)
        ) {
            next_event_time = event_start;
            next_event = event;
        }
    }
    return next_event;
}


function time_until(time) {
    now = new Date(Date.now()).getTime()/1000;
    until = new Date(time).getTime();

    diff = until - now;
    single = 'einer';

    if (diff > 86400) {
        value = parseInt(diff/86400);
        name = 'Tag';
        single = 'einem';
        if (value > 1) {
            name += 'e';
        }
    } else if (diff > 3600) {
        value = parseInt(diff/3600);
        name = 'Stunde';
    } else if (diff > 300) {
        value = parseInt(diff/60);
        name = 'Minute';
    } else {
        return 'gleich';
    }

    if (value > 1) {
        name += 'n';
    }

    switch (value) {
        case 1:
            value = single;
            break;
        case 2:
            value = 'zwei';
            break;
        case 3:
            value = 'drei';
            break;
        case 4:
            value = 'vier';
            break;
    }

    return 'in ' + value + ' ' + name;
}


function xhr_get(url, callback_func) {
    req = new XMLHttpRequest();
    req.timeout = 10000;
    req.open('GET', url);
    req.setRequestHeader('Accept', 'application/json');
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.addEventListener('load', function(event) {
        if (req.status != 200) {
            return;
        }

        callback_func(event);
    });
    req.send();
}


function _format_time(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}


function load_avatar(email) {
    if (current_avatar == email) {
        return;
    }

    current_avatar = email;

    if (!email) {
        document.getElementById('avatar').innerHTML = '';
        return;
    }

    console.info('got avatar request for ' + email);

    xhr_get('/api/avatar/' + email + '/', function(event) {
        if (req.responseText) {
            document.getElementById('avatar').innerHTML = '<img src="' + req.responseText + '">';
        } else {
            document.getElementById('avatar').innerHTML = '';
        }
    });
}


window.setInterval(function() {
    console.info('checking if GUI needs reloading because server has restarted');

    xhr_get('/api/app-startup-time/', function(event) {
        startup = parseInt(req.responseText);
        if (startup > 0 && app_startup < startup) {
            console.warn('startup time has changed, reloading GUI');
            window.location.reload();
        }
    });
}, 42000);


window.setInterval(function() {
    now = new Date(Date.now());
    document.getElementById('clock').innerHTML = _format_time(now.getHours()) + ":" + _format_time(now.getMinutes());
}, 5000);
