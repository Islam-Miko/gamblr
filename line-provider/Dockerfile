FROM python:3.10.12-slim-buster as base
RUN apt-get update \
    && apt-get install -y --no-install-recommends\
    xz-utils
WORKDIR /app
COPY requirements.txt req.txt
RUN python -m venv --copies /venv
RUN . /venv/bin/activate && pip install -r req.txt

FROM python:3.10.12-slim-buster as prod
WORKDIR /app
COPY --from=base /venv /venv/
ENV PATH /venv/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
COPY . ./
