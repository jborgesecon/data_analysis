# # DEPRECATED! USE JUPYTER WHEN EXPERIMENTING SPARK

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestApp") \
    .master("local[*]") \
    .getOrCreate()

print(spark.version)