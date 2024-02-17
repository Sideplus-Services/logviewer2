FROM python:3.12.2-bookworm
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  OAUTHLIB_INSECURE_TRANSPORT=1
ENV ENV docker
STOPSIGNAL SIGINT
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt update && apt install -y git bash yarn curl gcc build-essential yarn
RUN curl -sSL install.python-poetry.org | POETRY_HOME=/opt/poetry python -
ENV PATH /opt/poetry/bin:$PATH
WORKDIR /logviewer2
COPY . .
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
RUN yarn install --frozen-lockfile
LABEL org.opencontainers.image.source=https://github.com/Sideplus-Services/logviewer2
LABEL infra=modmail
CMD ["poetry", "run", "web"]
