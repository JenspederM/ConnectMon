FROM python:3.8-alpine as BUILD

# Configure Poetry
ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install dependencies
RUN apk add --no-cache --virtual \
    curl \
    libffi-dev \
    build-base \
    && rm -rf /var/cache/apk/*

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install --upgrade pip setuptools wheel \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install

# Run your app
COPY ./connectmon /connectmon

# Build the final image
CMD [ "poetry", "run", "python", "-m", "connectmon" ]