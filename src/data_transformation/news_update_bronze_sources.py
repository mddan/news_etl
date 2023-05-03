# Databricks notebook source
# MAGIC %sql
# MAGIC -- Stack up old sources with EMPTY source-related fields with new sources with EMPTY source-related fields. While deduping
# MAGIC create or replace table hive_metastore.news_etl_group6.append_sources_missing_fields as (
# MAGIC   select * from hive_metastore.news_etl_group6.bronze_sources where code is null
# MAGIC   union
# MAGIC   select * from hive_metastore.news_etl_group6.article_jn_delta_sources where code is null
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Stack up old sources with FULL source-related fields with new sources with FULL source-related fields. While deduping
# MAGIC create or replace table hive_metastore.news_etl_group6.append_sources_full_fields as (
# MAGIC   select * from hive_metastore.news_etl_group6.bronze_sources where code is not null
# MAGIC   union
# MAGIC   select * from hive_metastore.news_etl_group6.article_jn_delta_sources where code is not null
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Insert missing_fields delta to full_fields table, PRIORITIZING sources with filled source-related fields over sources that have empty sources-related fields
# MAGIC insert into hive_metastore.news_etl_group6.append_sources_full_fields
# MAGIC select * from hive_metastore.news_etl_group6.append_sources_missing_fields
# MAGIC where source_id not in (select source_id from hive_metastore.news_etl_group6.append_sources_full_fields);

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Update the old bronze_sources table with new bronze_sources table
# MAGIC create or replace table hive_metastore.news_etl_group6.bronze_sources as (
# MAGIC   select * from hive_metastore.news_etl_group6.append_sources_full_fields
# MAGIC )
