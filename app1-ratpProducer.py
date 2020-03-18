import requests
from kafka import KafkaProducer
import json
import csv
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def get_tok():
	urlOAuth = 'https://as.api.iledefrance-mobilites.fr/api/oauth/token' 
	client_id='a636e4c2-afae-4905-afe5-84b7c326f362' 
	client_secret='5ad70c24-431c-4ad4-b16f-0b5de340bfcd'
	data =dict(grant_type='client_credentials', scope='read-data', client_id=client_id, client_secret=client_secret)
	response = requests.post(urlOAuth, data=data) 
	print(response.json)
	if response.status_code != 200: 
		print('Status:', response.status_code, 'Erreur sur la requete token; fin de programme')
		exit()
	jsonData = response.json() 
	return jsonData['access_token']

token = get_tok()
#token = '3IhXQ1T9h4DUHAwdPBK1o8S78gWFdSNnd13X2ed5zWrqgVzUu4hIrq'

url = 'https://traffic.api.iledefrance-mobilites.fr/v1/tr-unitaire/stop-monitoring'

paramsList = []

with open('/usr/hdp/current/kafka-broker/hadoopProject/references.csv') as csv_file:
	csv_reader = csv.DictReader(csv_file, delimiter=';')
	for row in csv_reader:
		paramsList.append(row['MonitoringRef_ZDE'])



headers = { 'Accept-Encoding' : 'gzip', 'Authorization' : 'Bearer ' + token }
for i  in range(479):
    for i in paramsList:
        response = requests.get(url, params={'MonitoringRef': i}, headers=headers)
	if response.status_code != 200:
            print('Status:', response.status_code, 'Erreur sur la requete response; fin de programme')
            exit()
	jsonData = response.json()
	producer.send('ratp-api', json.dumps(jsonData))
	producer.flush()
    time.sleep(180)
