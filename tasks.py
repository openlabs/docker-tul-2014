from fabric.api import local
from celery import Celery
from flask import render_template
from docker import Client

app = Celery('tasks', broker='redis://localhost')
client = Client(base_url='unix:///var/run/docker.sock', version='1.3')

IMAGE = 'tul:2014'


@app.task
def _create_container(name):
    """
    Create a container with the name
    """
    container = client.create_container(
        image=IMAGE,
        hostname='%s.docker.openlabs.us' % name,
        name=name
    )
    print container
    print client.start(container.get('Id'), port_bindings={8000: None})
    return container


@app.task
def _create_nginx_proxy(name, port):
    """
    Create an nginx proxy for the given upstream
    """
    nginx_conf = render_template('nginx_conf.jinja', name=name, port=port)
    with open('/etc/nginx/sites-enabled/%s.conf' % name, 'w') as f:
        f.write(nginx_conf)
    local('service nginx reload')

