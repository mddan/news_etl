# Databricks notebook source
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
