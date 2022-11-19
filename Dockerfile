FROM python:3.10-alpine3.15
ENV PYTHONUNBUFFERED 1
ENV ENV docker
STOPSIGNAL SIGINT
RUN apk update && apk add --no-cache git bash yarn curl
RUN curl -sSL install.python-poetry.org | POETRY_HOME=/opt/poetry python -
ENV PATH /opt/poetry/bin:$PATH
WORKDIR /logviewer2
ENTRYPOINT [ "/logviewer2/.docker/entry_point.sh" ]
CMD ["poetry", "run", "webd"]