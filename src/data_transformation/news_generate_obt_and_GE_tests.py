# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC create or replace table hive_metastore.news_etl_group6.gold_obt as ( 
# MAGIC   select 
# MAGIC     article_id,
# MAGIC     article_source_id,
# MAGIC     article_country_code,
# MAGIC     article_language_code,
# MAGIC     article_author,
# MAGIC     article_title,
# MAGIC     article_description,
# MAGIC     article_url,
# MAGIC     article_image,
# MAGIC     article_published_dt,
# MAGIC     article_published_year,
# MAGIC     article_published_month,
# MAGIC     article_published_day,
# MAGIC     article_published_hour,
# MAGIC     article_published_minute,
# MAGIC     article_published_second,
# MAGIC     article_has_author,
# MAGIC     article_has_shock_value,
# MAGIC     source_name,
# MAGIC     source_category,
# MAGIC     source_code,
# MAGIC     source_url,
# MAGIC     source_article_count,
# MAGIC     country_name,
# MAGIC     language_name
# MAGIC   from hive_metastore.news_etl_group6.gold_fact_articles a
# MAGIC   left join hive_metastore.news_etl_group6.gold_dim_sources b on a.article_source_id = b.source_id
# MAGIC   left join hive_metastore.news_etl_group6.gold_dim_countries c on a.article_country_code = c.country_code
# MAGIC   left join hive_metastore.news_etl_group6.gold_dim_languages d on a.article_language_code = d.language_code
# MAGIC );

# COMMAND ----------

# MAGIC %pip install great-expectations

# COMMAND ----------

import pandas as pd

df = spark.read.table("hive_metastore.news_etl_group6.bronze_articles").toPandas()
total_article_count = len(df)

# COMMAND ----------

from great_expectations.dataset import SparkDFDataset

# COMMAND ----------

# Final OBT tests
obt_df = spark.read.table('hive_metastore.news_etl_group6.gold_obt')
ge_obt_df = SparkDFDataset(obt_df)
expect1 = ge_obt_df.expect_column_values_to_not_be_null("article_id")
assert expect1.success
expect2 = ge_obt_df.expect_table_row_count_to_equal(total_article_count)
assert expect2.success
expect3 = ge_obt_df.expect_column_values_to_be_in_set(column="article_has_author", value_set=[0,1])
assert expect3.success
expect4 = ge_obt_df.expect_column_values_to_be_of_type('source_article_count', 'LongType')
assert expect4.success
expect5 = ge_obt_df.expect_column_values_to_be_of_type('country_name', 'StringType')
assert expect5.success

# COMMAND ----------

# diagnostics...

# COMMAND ----------

# %sql
# select article_has_author, count(*) from hive_metastore.news_etl_group6.gold_obt group by article_has_author

# COMMAND ----------

# obt_spark = df = spark.read.table("hive_metastore.news_etl_group6.gold_obt")
# obt_spark.printSchema()
# # print(obt_spark.schema("article_id").dataType)
# print(obt_spark.schema.simpleString)
