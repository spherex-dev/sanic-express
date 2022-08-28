FROM python:3.10.6-slim-bullseye
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && mkdir /data
ADD src /sanic-express
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]