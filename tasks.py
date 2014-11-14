from celery import Celery
from docker import Client

app = Celery('tasks', broker='redis://localhost')
client = Client(base_url='tcp://docker.openlabs.us:2375')


@app.task
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


@app.task
def _create_nginx_proxy(name, port):
    """
    Create an nginx proxy for the given upstream
    """
    nginx_conf = render_template('nginx_conf.jinja', name=name, port=port)
    with open('/etc/nginx/sites-enabled/%s.conf' % name, 'w') as f:
        f.write(nginx_conf)
    local('service nginx reload')

