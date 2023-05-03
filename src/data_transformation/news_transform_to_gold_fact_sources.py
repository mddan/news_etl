# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC create or replace table hive_metastore.news_etl_group6.gold_dim_sources as ( 
# MAGIC   select 
# MAGIC     source_id,
# MAGIC     source as source_name,
# MAGIC     category as source_category,
# MAGIC     country as source_country_code,
# MAGIC     language as source_language_code,
# MAGIC     code as source_code,
# MAGIC     url as source_url,
# MAGIC     article_count as source_article_count
# MAGIC   from hive_metastore.news_etl_group6.silver_sources
# MAGIC );

# COMMAND ----------

# MAGIC %pip install great-expectations

# COMMAND ----------

from great_expectations.dataset import SparkDFDataset

# Test
df = spark.read.table('hive_metastore.news_etl_group6.gold_dim_sources')
ge_df = SparkDFDataset(df)
expect1 = ge_df.expect_column_values_to_not_be_null("source_id")
assert expect1.success
