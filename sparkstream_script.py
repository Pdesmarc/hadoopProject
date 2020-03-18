from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.window import Window
if __name__ == '__main__':
    spark = SparkSession.builder.appName("tpspark").enableHiveSupport().getOrCreate()
    
    df = spark.readStream.format("kafka").option("kafka.bootstrap.servers","localhost:9092").option("startingOffsets", "earliest").option("subscribe","ratp-api").load()
    df = df.selectExpr("CAST(value as STRING)")
    df.printSchema()
    df2 = df.select(df.value=='LineRef', df.value=='AimedArrivalTime',df.value=='AimedDepartureTime', df.value=='ExpectedArrivalTime', df.value=='ExpectedDepartureTime')
    
    query = df2.writeStream.format("console").option("truncate","false").start()
    query= query.awaitTermination()
