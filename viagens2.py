# # DEPRECATED! USE JUPYTER WHEN EXPERIMENTING SPARK

# same as viagens, but now using PySpark
import navigation as nav
import pandas as pd
import glob
import os
import zipfile
from unidecode import unidecode
from io import BytesIO

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import FloatType, BooleanType


# start a spark session
spark = SparkSession.builder.appName('ETL_ptransp').getOrCreate()
print(spark.version)

# path = "other_datasets\\ptransp_viagens\\*"
# files = glob.glob(path)
# dataframes = []

# # for file in files:
# with zipfile.ZipFile(files[-1], 'r') as ref:
#     datasets = ref.namelist()
#     last_csv = datasets[-1]
#     with ref.open(last_csv) as current:
#         df1 = pd.read_csv(current, encoding='latin1', sep=';', dtype='object')
#         spark_df = spark.createDataFrame(df1)

#         dataframes.append(spark_df)
#     print(f'Processed {last_csv} from {ref}: ok!')

# df = dataframes[0]
# for i in dataframes[1:]:
#     df = df.unionByName(df)

# df.printSchema()
# df.show(5)