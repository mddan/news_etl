import json
import requests
from confluent_kafka.cimpl import Producer
import ccloud_lib
import os
import datetime


if __name__ == '__main__':
    
    #Topic 
    topic = os.environ.get('KAFKA_TOPIC')

    conf = {'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVERS'), 
            'security.protocol': 'SASL_SSL', 
            'sasl.mechanisms': 'PLAIN', 
            'sasl.username': os.environ.get('KAFKA_SASL_USERNAME'), 
            'sasl.password': os.environ.get('KAFKA_SASL_PASSWORD'), 
            'compression.type': 'lz4', 
            'batch.size': '10000', 
            'request.timeout.ms': '120000', 
            'queue.buffering.max.messages': '200000'}

    # Pop the Schema Registry configuration parameters from the configuration dictionary
    producer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)

    # Create Producer instance
    producer = Producer(producer_conf)

    # Create topic if needed
    ccloud_lib.create_topic(conf, topic)

    delivered_records = 0

    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or
    # permanently failed delivery (after retries).
    def acked(err, msg):
        global delivered_records
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            delivered_records += 1
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))
            
    # Define the API endpoint and parameters
    api_endpoint = 'http://api.mediastack.com/v1/news'
    mediastack_access_key = os.environ.get('MEDIASTACK_ACCESS_KEY')
    params = {'access_key': mediastack_access_key, 'countries': 'us', 
              'languages': 'en', 'limit': 100, 'sort': 'published_desc'}

    # # Query the API and retrieve the news headlines
    response = requests.get(api_endpoint, params=params)
    headlines = json.loads(response.text)
    batch_timestamp = str(datetime.datetime.now())

    # # Write the headlines to the Kafka topic
    for headline in headlines['data']:
        headline['batch_timestamp'] = batch_timestamp
        # Produce the message to the Kafka topic
        producer.produce(topic, key=None, value=json.dumps(headline), on_delivery=acked)
        producer.poll(0)
        
    producer.flush()
    print("{} messages were produced to topic {}!".format(delivered_records, topic))