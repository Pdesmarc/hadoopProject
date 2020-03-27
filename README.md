# Projet Hadoop

The goal of Hadoop project is to get in real time the average waiting time for each stations of the N line using: 
- RATP API
- Kafka
- SparkStreaming
- Tableau software

MS SIO 2019-2020 - CentraleSupélec

Team Members : 
DESMARCHELIER Pierre,
LY Stéphane,
NGBANGO Soulémanou,
RHERMINI Acheq

## Installation

### Hadoop stack 

Please follow this procedure to install HDP 3.0.1 Sandbox Through Docker on AWS : https://github.com/qge/hdp 

### Reproduce our environnement

You need to first launch your AWS EC2 instance. Once your instance is launched : 
```sh
$ ssh -i "EPATH/TO/YOUR/KEY.pem" ec2-user@YOUR-PUBLIC-DNS-ADRESS
```

Then you need to start the dockers:
```sh
# Start the docker daemons engine
$ sudo systemctl start docker

#Start the docker containing hadoop
$ sudo docker start <HDP-DOCKER-ID>

#Start the docker containing the proxy
$ sudo docker start <PROXY-DOCKER-ID>
```

Now you should be able to access into the Hadoop docker 
```sh
# Access the hadoop docker
$ docker exec -it <HDP-DOCKER-ID> /bin/bash
```

Once you are in the docker, please go inside the kafka_broker repository :
```sh
# Access the kafka_broker repository 
$ cd /usr/hdp/current/kafka-broker/
```
Then clone our repo : 
```sh
# Clone our git repo 
$ git clone https://github.com/Pdesmarc/hadoopProject.git
$ cd hadoopProjet/
```
###  Save to hdfs
The spark streaming script need to have an example file with the response of the RATP API in hdfs (user/root/). We provide in this repo the example file : test.json.
```sh
# Save to hdfs (/user/root/)
$ hdfs dfs -put test2.json /user/root
# To check if the file is in hdfs
$ hdfs dfs -ls /user/root/
```

 ## Kafka
 
 ### Run the producer python script
  You have nothing to do, the script will retrieve all the authorizations needed to do a request.
```sh
# Producer script
$ python app1-ratpProducer.py
```
### Launch the spark submit 
To launch the spark submit, you must to write this command : 
```sh
# Launch the spark submit 
$ spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.0 sparkstream_script.py
```
Once the producer and the spark submit are launched, spark streaming will automatically save the results in hdfs : /user/root/save_stream/ . The results are saved in parquet. 


## Tableau

To allow Tableau software  to connect HDFS, please install this plugins : https://www.cloudera.com/downloads/hdp.html

