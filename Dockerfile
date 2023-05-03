FROM python:3.8.16-slim

WORKDIR /src

COPY /src .

RUN pip install -r requirements.txt

ENV PYTHONPATH=/src

CMD ["python", "data_ingestion/producer/mediastack_kafka_producer.py"]

