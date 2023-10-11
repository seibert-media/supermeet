from .. import APP_STARTUP
from ..web import app


@app.route('/api/app-startup-time/')
def app_startup_time():
    return str(APP_STARTUP)
