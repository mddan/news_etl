# COMMAND ----------

dbutils.fs.mkdirs("/mnt/delta/mediastack_headlines")

# COMMAND ----------

dbutils.fs.mkdirs("/mnt/checkpoints/mediastack_headlines")

# COMMAND ----------

dbutils.fs.rm("dbfs:/mnt/checkpoints/mediastack_headlines", True)


# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE mediastack_headlines
# MAGIC USING DELTA
# MAGIC LOCATION "/mnt/delta/mediastack_headlines"