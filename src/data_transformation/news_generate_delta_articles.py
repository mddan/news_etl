# Databricks notebook source
# MAGIC %sql
# MAGIC -- Delta load to bronze_articles
# MAGIC create or replace table hive_metastore.news_etl_group6.delta_articles as (
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
# MAGIC   from mediastack_headlines --hive_metastore.news_etl_group6.new_sample2 -- replace with mediastack_headlines when deployed
# MAGIC   where hash(url) not in (select distinct article_id from hive_metastore.news_etl_group6.bronze_articles) -- only pull delta from existing bronze_articles
# MAGIC   order by published_at asc)
# MAGIC   ;

# COMMAND ----------

# MAGIC %sql select count(*) as cnt from hive_metastore.news_etl_group6.delta_articles

# COMMAND ----------

# %sql
# select distinct
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
#     published_at
# from mediastack_headlines

# COMMAND ----------

# %sql
# select * from hive_metastore.news_etl_group6.bronze_articles

# COMMAND ----------

# %sql
# select distinct
#     hash(url) as article_id
# from mediastack_headlines
# order by article_id asc

# COMMAND ----------

# %sql
# select distinct
#   count(distinct hash(url)) cnt
# from mediastack_headlines

# COMMAND ----------

# %sql
# select distinct article_id from hive_metastore.news_etl_group6.bronze_articles order by article_id asc

# COMMAND ----------

# %sql
# select count(distinct article_id) from hive_metastore.news_etl_group6.bronze_articles

# COMMAND ----------

# %sql
# select distinct
#   count(*) cnt
# from mediastack_headlines
