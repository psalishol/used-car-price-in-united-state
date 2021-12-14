from pyspark.sql import SparkSession
from pyspark.sql.types import *


# Making a sparksession
SPARK_SESSION = SparkSession \
    .builder \
    .appName("Preprocessing with Spark") \
    .getOrCreate()
    
    

# Defining a schema for the variables
SCHEMA = StructType([
    StructField("id", IntegerType(), nullable=False),
    StructField("region", StringType(), nullable=False),
    StructField("price", IntegerType(), nullable=False),
    StructField("manufacturer", StringType(), nullable=False),
    StructField("model", StringType(), nullable=False),
    StructField("condition", StringType(), nullable=False),
    StructField("cylinders", StringType(), nullable=False),
    StructField("fuel", StringType(), nullable=False),
    StructField("odometer", IntegerType(), nullable=False),
    StructField("transmission", StringType(), nullable=False),
    StructField("drive", StringType(), nullable=False),
    StructField("size", StringType(), nullable=False),
    StructField("type", StringType(), nullable=False),
    StructField("state", StringType(), nullable=False),
    StructField("lat", IntegerType(), nullable=False),
    StructField("long", IntegerType(), nullable=False),

])



if __name__ == '__main__':
    # Reading the data
    df = SPARK_SESSION.read.csv(
        r"..\data\external\vehicles.csv", header=True, schema=SCHEMA)
    print(df)
