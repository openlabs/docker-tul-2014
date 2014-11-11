# Trytond 3.2
#
# VERSION	3.2.0.1

FROM openlabs/tryton:3.2
MAINTAINER Prakash Pandey <prakash.pandey@openlabs.co.in>

RUN apt-get -y update

RUN pip install "trytond_party>=3.2,<3.3"

ADD trytond.conf /etc/trytond.conf

# SET data_path to a volume on the server
VOLUME /var/lib/trytond

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/trytond"]
