FROM ghcr.io/astral-sh/uv:0.11-python3.14-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt update && apt install --no-install-recommends -y \
    build-essential \
    libpq-dev tree

WORKDIR /app
COPY ./pyproject.toml ./uv.lock ./


RUN uv sync --frozen --no-install-project --all-groups
COPY /src /app/src

RUN uv sync --frozen --all-groups

# Start runtime image,
FROM ghcr.io/astral-sh/uv:0.11-python3.14-trixie-slim

# Create user bag-amsterdam-api with the same UID as github actions runner.
RUN groupadd --system --gid 999  bag-amsterdam-api  && useradd --system --gid 999 \
    --uid 1001 --create-home bag-amsterdam-api
RUN apt update && apt install --no-install-recommends -y \
    curl \
    libpq5

WORKDIR /app
# Copy python build artifacts from builder image
RUN chown bag-amsterdam-api:bag-amsterdam-api /app
COPY --from=builder --chown=bag-amsterdam-api:bag-amsterdam-api /app /app
USER bag-amsterdam-api

# Have some defaults so the container is easier to start
ENV DJANGO_SETTINGS_MODULE=bag_amsterdam_api.settings \
    DJANGO_DEBUG=false \
    UWSGI_HTTP_SOCKET=:8000 \
    UWSGI_MODULE=bag_amsterdam_api.wsgi \
    UWSGI_CALLABLE=application \
    UWSGI_MASTER=1

RUN uv run src/manage.py collectstatic --noinput
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT []
EXPOSE 8000

CMD ["uv", "run", "gunicorn", "bag_amsterdam_api.wsgi", "--host", "0.0.0.0", "--port", "8000"]
