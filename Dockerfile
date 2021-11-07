FROM python:latest

### Mandatory
#
RUN adduser player && chown -R player /app
#
USER player
#############

COPY . /app/

# Run a little script : the /bin/bash maintain the container running
CMD ["bash", "start.sh"]
