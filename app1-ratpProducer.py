import requests
from kafka import KafkaProducer
import json
producer = KafkaProducer(bootstrap_servers='localhost:9092')

def get_tok():
	urlOAuth = 'https://as.api.iledefrance-mobilites.fr/api/oauth/token' 
	client_id='cd42b13f-9cd0-4204-9f8a-2f5976cf8c71' 
	client_secret='f0c32a8c-7f4b-48e8-8db9-f2bcb07b0c0a'
	data =dict(grant_type='client_credentials', scope='read-data', client_id=client_id, client_secret=client_secret)
	response = requests.post(urlOAuth, data=data) 
	print(response.json)
	if response.status_code != 200: 
		print('Status:', response.status_code, 'Erreur sur la requete; fin de programme')
		exit()
	jsonData = response.json() 
	return jsonData['access_token']

token = get_tok()
token = '3IhXQ1T9h4DUHAwdPBK1o8S78gWFdSNnd13X2ed5zWrqgVzUu4hIrq'

url = 'https://traffic.api.iledefrance-mobilites.fr/v1/tr-unitaire/stop-monitoring'

params = dict(MonitoringRef='STIF:StopPoint:Q:22388:')
headers = { 'Accept-Encoding' : 'gzip', 'Authorization' : 'Bearer ' + token }

response = requests.get(url,params=params, headers=headers)
if response.status_code != 200:
	print('Status:', response.status_code, 'Erreur sur la requete; fin de programme')
	exit()
jsonData = response.json()
print(jsonData)
producer.send('sio-topic', json.dumps(jsonData))
producer.flush()
