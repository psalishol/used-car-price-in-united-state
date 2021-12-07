# Using Apache Spark for the preprocessing
from pyspark.sql import SparkSession
SPARK_SESSION = SparkSession.builder.appName("Spark builder").getOrCreate()

if __name__ == '__main__':
    print(SPARK_SESSION)

