import os
import re

from flask import Flask, request, flash
from fabric.api import local
from flask import render_template
from tasks import _create_container, _create_nginx_proxy, client
app = Flask(__name__)


def validate_name(name):
    if not re.match(r'^[a-zA-Z\d-]{,63}$', name):
        flash("Please enter a valid domain name")
        return False
    if os.path.exists("/etc/nginx/sites-enabled/demo-%s.conf" % name):
        flash("Instance with this name is already running!")
        return False
    return True


@app.route("/", methods=['GET', 'POST'])
def home():
    name, setup_done = request.form.get('name'), False

    if request.method == 'POST' and validate_name(name):
        container = _create_container(name)
        port = client.port(container['Id'], 8000)[0]
        _create_nginx_proxy(name, port['HostPort'])
        flash('Your ERP is now setup')
        setup_done = True

    return render_template('home.html', name=name, setup_done=setup_done)


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "development key"
    app.run('0.0.0.0')
