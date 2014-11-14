# Trytond 3.2
#
# VERSION	3.2.0.1

FROM openlabs/tryton:3.2
MAINTAINER Prakash Pandey <prakash.pandey@openlabs.co.in>

RUN apt-get -y update
RUN apt-get -y -q install sqlite

RUN pip install "trytond_party>=3.2,<3.3"

RUN sqlite3 test_db
RUN trytond -i all -d test_db

# SET data_path to a volume on the server
VOLUME /var/lib/trytond
