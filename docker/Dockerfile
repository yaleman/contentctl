FROM python:3.12-slim

RUN apt-get update && apt-get -y install git && apt-get clean

ADD contentctl /app/contentctl
ADD README.md /app/README.md
ADD pyproject.toml /app/
RUN ls /app/
RUN python -m pip install /app/
RUN mkdir /data/

WORKDIR /data/
ENTRYPOINT [ "contentctl" ]