FROM python:3.7.4-alpine3.10 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:${PATH}"

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.0

RUN apk add --no-cache gcc python3-dev alpine-sdk libffi-dev openssl-dev musl-dev
RUN pip install "poetry==${POETRY_VERSION}"
RUN python -m venv /venv

COPY poetry.lock pyproject.toml /app/
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final

COPY --from=builder /venv /venv
COPY . /app/

CMD [ "variable-updater", "--config", "/app/config.example.yml" ]
