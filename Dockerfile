# Trytond 3.2
#
# VERSION	3.2.0.1

FROM openlabs/tryton:3.2
MAINTAINER Prakash Pandey <prakash.pandey@openlabs.co.in>

RUN apt-get -y update
RUN apt-get install -y -q python-psycopg2

RUN pip install "trytond_party>=3.2,<3.3"

ADD trytond.conf /etc/trytond.conf

# SET data_path to a volume on the server
VOLUME /var/lib/trytond
