# Databricks notebook source
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
