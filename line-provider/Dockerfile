FROM python:3.10.12-slim-buster as base
RUN apt-get update \
    && apt-get install -y --no-install-recommends\
    xz-utils
WORKDIR /app
COPY ../Pipfile ../Pipfile.lock ./
RUN python -m venv --copies /venv
RUN . /venv/bin/activate && pip install pipenv && pipenv install --deploy

FROM python:3.10.12-slim-buster as prod
WORKDIR /app
COPY --from=base /venv /venv/
ENV PATH /venv/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
COPY . ./
