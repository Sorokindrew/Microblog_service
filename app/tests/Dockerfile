FROM python:3.7
RUN apt-get update && apt-get install -y python3-dev supervisor nginx \
    && rm -rf /var/lib/apt/lists/*

ENV DB_URL='postgres_test'

COPY ./app/tests/requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY ../../app/src/ /app/src/
COPY ../../app/tests/ /app/tests/
COPY ./pytest.ini /app/

WORKDIR /app/

CMD ["pytest", "-v", "-s", "tests"]
