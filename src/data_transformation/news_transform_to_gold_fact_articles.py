# Databricks notebook source
# MAGIC %sql
# MAGIC create or replace table hive_metastore.news_etl_group6.gold_fact_articles as (
# MAGIC     select
# MAGIC         article_id,
# MAGIC         source_id as article_source_id,
# MAGIC         country as article_country_code,
# MAGIC         language as article_language_code,
# MAGIC         author as article_author,
# MAGIC         title as article_title,
# MAGIC         description as article_description,
# MAGIC         url as article_url,
# MAGIC         image as article_image,
# MAGIC         published_at as article_published_dt,
# MAGIC         published_year as article_published_year,
# MAGIC         published_month as article_published_month,
# MAGIC         published_day as article_published_day,
# MAGIC         published_hour as article_published_hour,
# MAGIC         published_minute as article_published_minute,
# MAGIC         published_second as article_published_second,
# MAGIC         has_author as article_has_author,
# MAGIC         has_shock_value as article_has_shock_value 
# MAGIC     from hive_metastore.news_etl_group6.silver_articles);

# COMMAND ----------

# MAGIC %pip install great-expectations

# COMMAND ----------

from great_expectations.dataset import SparkDFDataset

# Test
df = spark.read.table('hive_metastore.news_etl_group6.gold_fact_articles')
ge_df = SparkDFDataset(df)
expect1 = ge_df.expect_column_values_to_not_be_null("article_id")
assert expect1.success
expect2 = ge_df.expect_column_values_to_be_in_set(column="article_has_author", value_set=[0,1])
assert expect2.success
expect3 = ge_df.expect_column_values_to_be_in_set(column="article_has_shock_value", value_set=[0,1])
assert expect3.success
