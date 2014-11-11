# -*- coding: utf-8 -*-
import getpass

from fabric.api import run, sudo, cd, hosts, env
from fabric.contrib.files import exists, upload_template

REPO_PATH = "git@github.com:prakashpp/tryton-unconference.git"
HOST = "maint.advocatetaxportal.com"
TRYTOND_CONF = {
    'DB_HOST': '',  # Determine from docker host IP
    'DB_PORT': 5432,
    'DB_USER': 'tryton',
    'DB_PASS': 'tryton',
    'ADMIN_PASS': 'admin',
}

env.use_ssh_config = True
env.forward_agent = True


@hosts('%s@%s' % (getpass.getuser(), HOST))
def setup_tryton():
    """Setup a new tryton container.

    This returns a tuple of host and dbname.
    """
    # fetch the docker host port
    TRYTOND_CONF['DB_HOST'] = run(
        "ip route | awk '/docker/ { print $NF }'"
    )

    with cd("tryton-unconference"):
        upload_template(
            'trytond.jinja',  # local template file
            'trytond.conf',
            TRYTOND_CONF,
            use_jinja=True, backup=False
        )

        # Build docker image
        sudo('sudo docker build --rm --no-cache -t trytond-demo .')

        # Start containers in detach mode
        sudo('docker run -d trytond-demo')
