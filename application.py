from flask import Flask, request
from fabric.api import local
from flask import render_template
app = Flask(__name__)

from docker import Client
c = Client(base_url='tcp://docker.openlabs.us:2375')
IMAGE = 'tryton_tul_demo'


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


def _create_container(name):
    """
    Create a container with the name
    """
    container = c.create_container(
        image=IMAGE,
        hostname='%s.docker.openlabs.us' % name,
        name=name
    )
    print container
    return container


def _create_nginx_proxy(name, port):
    """
    Create an nginx proxy for the given upstream
    """
    nginx_conf = render_template('nginx_conf.jinja', name=name, port=port)
    with open('/etc/nginx/sites-enabled/%s.conf' % name, 'w') as f:
        f.write(nginx_conf)
    local('service nginx reload')


if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')
