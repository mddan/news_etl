# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

TOPIC = dbutils.secrets.get("NewsEtlSecretBucket", "KafkaTopic")
KAFKA_BROKER = dbutils.secrets.get("NewsEtlSecretBucket", "KafkaBroker")
confluentApiKey = dbutils.secrets.get("NewsEtlSecretBucket", "ConfluentApiKey")
confluentSecret = dbutils.secrets.get("NewsEtlSecretBucket", "ConfluentApiSecret")
deltaTablePath = <YOUR_DELTA_TABLE_PATH>
checkpointPath = <YOUR_DELTA_CHECKPOINT_PATH>

# Define the schema for the incoming data
json_schema = StructType([
    StructField("author", StringType(), True),
    StructField("title", StringType(), True),
    StructField("description", StringType(), True),
    StructField("url", StringType(), True),
    StructField("source", StringType(), True),
    StructField("image", StringType(), True),
    StructField("category", StringType(), True),
    StructField("language", StringType(), True),
    StructField("country", StringType(), True),
    StructField("published_at", StringType(), True),
    StructField("batch_timestamp", StringType(), True)
])

# Define the streaming DataFrame to read from Kafka 
raw_kafka_events = (spark.readStream
    .format("kafka")
    .option("subscribe", TOPIC)
    .option("kafka.bootstrap.servers", KAFKA_BROKER)
    .option("kafka.security.protocol", "SASL_SSL")
    .option("kafka.sasl.jaas.config", "kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username='{}' password='{}';".format(confluentApiKey, confluentSecret))
    .option("kafka.ssl.endpoint.identification.algorithm", "https")
    .option("kafka.sasl.mechanism", "PLAIN")
    .option("failOnDataLoss", "false")
    .option("max.poll.records", "10000")
    .option("startingOffsets", "earliest")
    .option("checkpointLocation", checkpointPath) \
    .load()
    )


# Parse JSON messages using the json_schema
parsed_df = raw_kafka_events.selectExpr("CAST(value AS STRING)") \
  .select(from_json(col("value"), json_schema).alias("data")) \
  .select("data.*")


# Write the parsed_df to the Delta table with checkpointing
parsed_df.writeStream \
  .format("delta") \
  .option("startingOffsets", "latest") \
  .option("mergeSchema", "true") \
  .option("checkpointLocation", checkpointPath) \
  .outputMode("append") \
  .start(deltaTablePath) 





