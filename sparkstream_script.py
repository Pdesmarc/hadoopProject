import pyspark.sql.types as T
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from hdfs import InsecureClient
from py4j.java_gateway import java_import
import time

if __name__ == '__main__':
	spark = SparkSession.builder.appName("HadoopProject").enableHiveSupport().getOrCreate() 

	#On instancie notre stream en souscrivant au topic ratp-api
	kafkaStream = spark.readStream.format("kafka").option("kafka.bootstrap.servers","sandbox-hdp.hortonworks.com:9092").option("subscribe","ratp-api").load() #.option("startingOffsets", "earliest")


	#On vient recuperer la requete example pour recuperer le schema global
	json_example = spark.read.json("hdfs:///user/root/test.json",multiLine=True)
	schema_json=json_example.schema
	#json_example.printSchema()

	#On recupere les colonnes voulues des messages du producer : value corresponds a la reponse, et timestamp a l'heure ou a ete effectue la requete
	df = kafkaStream.selectExpr("CAST(value as STRING)", "CAST(timestamp as TIMESTAMP)")

	#Selection de la partie du json qui nous interesse
	df = df.select(F.from_json(F.col("value"), schema_json).alias("test"), "timestamp").select("test.Siri.ServiceDelivery.StopMonitoringDelivery.MonitoredStopVisit","timestamp").select(F.explode("MonitoredStopVisit"), "timestamp").select(F.explode("col"),"timestamp").select("col.MonitoredVehicleJourney","timestamp", "col.MonitoringRef")
	#df.printSchema()

	#Selectionne des colonnes qui nous interesse
	df = df.select("MonitoredVehicleJourney.DestinationName","MonitoredVehicleJourney.LineRef","MonitoredVehicleJourney.TrainNumbers.TrainNumberRef", "MonitoredVehicleJourney.MonitoredCall.ExpectedArrivalTime", "MonitoredVehicleJourney.MonitoredCall.StopPointName", "timestamp", "MonitoringRef")

	#On renomme et on met toutes les donnees au meme niveau
	df= df.withColumn("Destination", F.explode("DestinationName")).withColumn("TrainNumber", F.explode("TrainNumberRef")).withColumn("StopName", F.explode("StopPointName")).drop("DestinationName","TrainNumberRef", "StopPointName")

	#Pour une meilleure visualisation, on met les dans dans un ordre precis
	df = df.select("timestamp",F.col("TrainNumber.value").alias("TrainNumber"),F.col("StopName.value").alias("StopName"),F.col("MonitoringRef.value").alias("MonitoringRef"), "ExpectedArrivalTime", F.col("Destination.value").alias("Destination"),F.col("LineRef.value").alias("LineRef"))

	#Nettoyage et filtrage des donnees sur la ligne N, sur les heures erronees et sur les possibilites de duplicat
	df = df.filter(F.col("LineRef") == "STIF:Line::C01736:").na.drop(subset = ['ExpectedArrivalTime']).dropDuplicates(["TrainNumber", "StopName"])

	#Formattage de la donnee necessaire pour les calculs
	df=df.withColumn('ExpectedArrivalTimeFormat',F.unix_timestamp('ExpectedArrivalTime', "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")).drop('ExpectedArrivalTime')



	#On definit arbitrairement un watermark de 5 minutes, et on regroupe par station avec une fenetre d'1h comme demande avec un intervalle glissant de 5 minutes pour avoir le resultat heure par heure
	df = df.withWatermark("timestamp", "5 minutes").groupBy(F.window("timestamp", "60 minutes", "2 minutes"), "StopName", "MonitoringRef")

	#On definit le temps d'attente moyen par : 1h divise par le nombre de train passe a la station l'heure precedent
	df = df.agg(F.count("TrainNumber").alias("NumberOfTrain"), F.format_number(60./ F.count("TrainNumber"), 2).cast("long").alias("AverageWaitingTime"))


	query = df.select("StopName", "MonitoringRef", "window", "NumberOfTrain", "AverageWaitingTime").writeStream.format("console").option("truncate", False).outputMode("append").format("parquet").option("checkpointLocation", "stream_checkpoint").option("path", "stream_save").start()
	query.awaitTermination()
