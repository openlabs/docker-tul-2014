import re

from flask import Flask, request
from fabric.api import local
from flask import render_template
from .tasks import _create_container, _create_nginx_proxy
app = Flask(__name__)

from docker import Client
c = Client(base_url='tcp://docker.openlabs.us:2375')
IMAGE = 'tryton_tul_demo'


def validate_name(name):
    return re.match(r'^[a-zA-Z\d-]{,63}$', name)


@app.route("/")
def home():
    name, setup_done = request.form.get('name'), False

    if request.method == 'POST' and validate_name(name):
        container = _create_container(name)
        port = c.port(container['id'], 8000)
        _create_nginx_proxy(name, port)
        flash('Your ERP is now setup')
        setup_done = True

    return render_template('home.html', name=name, setup_done=setup_done)


if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')
