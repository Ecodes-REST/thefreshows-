ARG PYTHON_VERSION=3.9-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
 

RUN mkdir -p /code
# Set the working directory to the subdirectory that contains the manage.py file
WORKDIR /home/e_mollz/FRESHOWBAND/

# Run makemigrations and migrate commands
RUN python manage.py makemigrations
RUN python manage.py migrate

RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --deploy --system
COPY . /code

EXPOSE 8000

ENV DATABASE_URL=postgresql://postgres:lOpLRRyuOrdsOqTHrRAFzSKRWuIIfEIh@postgres.railway.internal:5432/railway

CMD ["gunicorn","--bind",":8000","--workers","2","FRESHOWBAND.wsgi"]