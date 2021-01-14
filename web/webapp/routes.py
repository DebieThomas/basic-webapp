import time
import socket

import flask
from flask import g, redirect, url_for, request
from flask import current_app as app

from webapp import login_manager


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@app.context_processor
def inject_hostname():
    return dict(hostname=socket.gethostname())


@login_manager.unauthorized_handler
def unauthorized_handler():
    print("======> " + request.full_path)
    return redirect(url_for('auth_blueprint.login', next=request.full_path))
