ARG PYTHON_VERSION=3.9-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL=postgresql://postgres:lOpLRRyuOrdsOqTHrRAFzSKRWuIIfEIh@postgres.railway.internal:5432/railway

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --deploy --system
COPY . /code

EXPOSE 8000

CMD ["gunicorn","--bind",":8000","--workers","2","FRESHOWBAND.wsgi"]