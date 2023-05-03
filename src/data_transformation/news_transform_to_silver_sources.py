# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC create or replace table hive_metastore.news_etl_group6.silver_sources as ( 
# MAGIC   with agg as (
# MAGIC       select source_id, count(*) as article_count
# MAGIC       from hive_metastore.news_etl_group6.silver_articles
# MAGIC       group by source_id
# MAGIC   )
# MAGIC   select a.*, agg.article_count
# MAGIC   from hive_metastore.news_etl_group6.bronze_sources a
# MAGIC   left join agg on a.source_id = agg.source_id
# MAGIC )

# COMMAND ----------

# MAGIC %pip install great-expectations

# COMMAND ----------

from great_expectations.dataset import SparkDFDataset

# Test
df = spark.read.table('hive_metastore.news_etl_group6.silver_sources')
ge_df = SparkDFDataset(df)
expect4 = ge_df.expect_column_values_to_be_of_type('article_count', 'LongType')
assert expect4.success
