# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC insert into hive_metastore.news_etl_group6.bronze_articles
# MAGIC select * from hive_metastore.news_etl_group6.delta_articles
# MAGIC where article_id not in (select distinct article_id from hive_metastore.news_etl_group6.bronze_articles);
