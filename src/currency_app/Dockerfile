FROM diliplakshya/python3.10.12-alpine3.18-poetry
WORKDIR /currency/
COPY pyproject.toml poetry.lock /currency/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV PYTHONPATH "/alfbot/"
RUN apk update && apk add poetry && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /currency/
RUN chmod +x ./currency-entrypoint.sh
ENTRYPOINT ["./currency-entrypoint.sh"]

