# Databricks notebook source
# MAGIC %sql
# MAGIC create or replace table hive_metastore.news_etl_group6.silver_articles as (
# MAGIC     select
# MAGIC         article_id,
# MAGIC         source_id,
# MAGIC         author,
# MAGIC         title,
# MAGIC         description,
# MAGIC         url,
# MAGIC         source,
# MAGIC         image,
# MAGIC         category,
# MAGIC         language,
# MAGIC         country,
# MAGIC         published_at,
# MAGIC         year(published_at) as published_year,
# MAGIC         month(published_at) as published_month,
# MAGIC         day(published_at) as published_day,
# MAGIC         hour(published_at) as published_hour,
# MAGIC         minute(published_at) as published_minute,
# MAGIC         second(published_at) as published_second,
# MAGIC         case when author is not null then 1 else 0 end as has_author,
# MAGIC         case when title like "%!%" or description like "%!%" then 1 else 0 end as has_shock_value 
# MAGIC     from hive_metastore.news_etl_group6.bronze_articles
# MAGIC     order by published_at desc);

# COMMAND ----------

# MAGIC %pip install great-expectations

# COMMAND ----------

from great_expectations.dataset import SparkDFDataset

# COMMAND ----------

# Tests
df = spark.read.table('hive_metastore.news_etl_group6.silver_articles')
ge_df = SparkDFDataset(df)
expect1 = ge_df.expect_column_values_to_not_be_null("article_id")
assert expect1.success
expect2 = ge_df.expect_column_values_to_be_in_set(column="has_author", value_set=[0,1])
assert expect2.success
expect3 = ge_df.expect_column_values_to_be_in_set(column="has_shock_value", value_set=[0,1])
assert expect3.success
