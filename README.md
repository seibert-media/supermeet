# supermeet

This is a small flask application which renders a room information screen
based on the availability in google calendar. Users can interact with
the booking by changing the end time or booking a new appointment.

Supermeet has been tested to run under python 3.10 and 3.11.

## License

Supermeet is licensed under [AGPL 3.0](LICENSE). The included font (Lato)
is licensed under the [SIL Open Font License](LICENSE_fonts).

## Installation

1. deploy the git repository onto your server
2. (Optional, but recommended) create and activate a python3 virtualenv
3. install the application by running `pip install -e /path/to/git/repo`
4. (Optional, but recommended) install `gunicorn`
5. deploy your service account json and `config.toml`
6. run supermeet

### Example systemd unit file

This example assumes you run a reverse proxy in front of the application,
and you have gunicorn installed.

```
[Unit]
Description=flask application supermeet
After=network.target

[Service]
Environment=APP_CONFIG=/opt/supermeet/config.toml
Environment=APP_SECRETS=/opt/supermeet/secrets.json
Environment=FLASK_SECRET=changeme
User=www-data
Group=www-data
ExecStart=/opt/supermeet/venv/bin/gunicorn -w 4 -b 127.0.0.1:4000 supermeet.web:app

[Install]
WantedBy=multi-user.target
```
