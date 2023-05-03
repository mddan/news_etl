# Databricks notebook source
# Extract delta_dim_table (hit source API)

# Import libraries
import http.client, urllib.parse
import json
import pandas as pd

# Get search list and search string for source API
df = spark.read.table("hive_metastore.news_etl_group6.delta_articles").toPandas()
set_limit = 100
search_list = set(df['source'])
search_list = list(search_list)[0:400] # shortened list
search_string = '"' + '" "'.join(search_list) + '"'
if len(search_list) == 0:
    search_string = "abc" # default search string when delta is zero, therefore no new soruce in search list
    set_limit = 1

mediastack_api_key = <YOUR_MEDIASTACK_API_KEY>
# Hit source API and extract source df
conn = http.client.HTTPConnection('api.mediastack.com')
params_source = urllib.parse.urlencode({
    'access_key': mediastack_api_key,
    'search' : search_string,
    'limit' : set_limit
    })
conn.request('GET', '/v1/sources?{}'.format(params_source))
response_source = conn.getresponse()
response_source_read = response_source.read()
df_source = pd.json_normalize(json.loads(response_source_read)['data'])

# Convert pandas table to spark table
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("pandas to spark").getOrCreate()
df_source_spark = spark.createDataFrame(df_source)
df_source_spark.write.mode("overwrite").saveAsTable("hive_metastore.news_etl_group6.landing_sources")

