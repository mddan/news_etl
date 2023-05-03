# Databricks notebook source
# %sql
# -- Delta load to bronze_articles
# create or replace table hive_metastore.news_etl_group6.delta_articles as (
#   select distinct
#     hash(url) as article_id,
#     hash(concat(source, category, country, language)) as source_id,
#     author,
#     title,
#     description,
#     url,
#     source,
#     image,
#     category,
#     language,
#     country,
#     published_at,
#     batch_timestamp
#   from hive_metastore.news_etl_group6.new_sample2 -- replace with mediastack_headlines when deployed
#   order by published_at asc)
#   ;

# COMMAND ----------

# %sql
# insert into hive_metastore.news_etl_group6.bronze_articles
# select * from hive_metastore.news_etl_group6.delta_articles
# where article_id not in (select distinct article_id from hive_metastore.news_etl_group6.bronze_articles);

# COMMAND ----------

# Extract delta_dim_table (hit source API)

# Import libraries
import http.client, urllib.parse
import json
import pandas as pd

# Get search list and search string for source API
df = spark.read.table("hive_metastore.news_etl_group6.delta_articles").toPandas()
search_list = set(df['source'])
search_list = list(search_list)[0:400] # shortened list for initial load 
search_string = '"' + '" "'.join(search_list) + '"'

# Hit source API and extract source df
conn = http.client.HTTPConnection('api.mediastack.com')
params_source = urllib.parse.urlencode({
    'access_key': '145068c938076e8c65d8ab6f1805e6b5',
    'search' : search_string,
    'limit' : 100
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

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC create or replace table hive_metastore.news_etl_group6.delta_sources as
# MAGIC   select distinct
# MAGIC     hash(concat(name, category, country, language)) as source_id,
# MAGIC     name,
# MAGIC     category,
# MAGIC     country,
# MAGIC     language,
# MAGIC     code,
# MAGIC     url
# MAGIC   from hive_metastore.news_etl_group6.landing_sources

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC create or replace table hive_metastore.news_etl_group6.article_jn_delta_sources as (
# MAGIC   select distinct
# MAGIC     a.source_id,
# MAGIC     a.source,
# MAGIC     a.category,
# MAGIC     a.country,
# MAGIC     a.language,
# MAGIC     b.code,
# MAGIC     b.url
# MAGIC   from hive_metastore.news_etl_group6.bronze_articles a
# MAGIC   left join hive_metastore.news_etl_group6.delta_sources b on a.source_id = b.source_id
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC create or replace table hive_metastore.news_etl_group6.bronze_sources as (
# MAGIC   select * from hive_metastore.news_etl_group6.article_jn_delta_sources
# MAGIC )
