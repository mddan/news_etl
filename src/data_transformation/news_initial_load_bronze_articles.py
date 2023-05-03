# Databricks notebook source
# MAGIC %sql
# MAGIC -- Initial load of articles
# MAGIC create or replace table hive_metastore.news_etl_group6.delta_articles as
# MAGIC   select distinct 
# MAGIC     hash(url) as article_id,
# MAGIC     hash(concat(source, category, country, language)) as source_id,
# MAGIC     author,
# MAGIC     title,
# MAGIC     description,
# MAGIC     url,
# MAGIC     source,
# MAGIC     image,
# MAGIC     category,
# MAGIC     language,
# MAGIC     country,
# MAGIC     published_at
# MAGIC   from mediastack_headlines -- hive_metastore.news_etl_group6.new_sample1 -- replace with mediastack_headlines when deployed
# MAGIC   order by published_at asc
# MAGIC   limit 10000
# MAGIC   ;
# MAGIC
# MAGIC create or replace table hive_metastore.news_etl_group6.bronze_articles as
# MAGIC   select *
# MAGIC   from hive_metastore.news_etl_group6.delta_articles;
