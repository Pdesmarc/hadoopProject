import requests
from kafka import KafkaProducer
import json
producer = KafkaProducer(bootstrap_servers='localhost:9092')

def get_tok():
	urlOAuth = 'https://as.api.iledefrance-mobilites.fr/api/oauth/token' 
	client_id='f2c9279f-772a-427b-a63f-d0205dc69557' 
	client_secret='b2c1b99a-c645-4825-8569-47d7f97cda26'
	data =dict(grant_type='client_credentials', scope='read-data', client_id=client_id, client_secret=client_secret)
	response = requests.post(urlOAuth, data=data) 
	print(response.json)
	if response.status_code != 200: 
		print('Status:', response.status_code, 'Erreur sur la requete; fin de programme')
		exit()
	jsonData = response.json() 
	return jsonData['access_token']

token = get_tok()
#token = '3IhXQ1T9h4DUHAwdPBK1o8S78gWFdSNnd13X2ed5zWrqgVzUu4hIrq'

url = 'https://traffic.api.iledefrance-mobilites.fr/v1/tr-unitaire/stop-monitoring'

paramsList = ['STIF:StopPoint:Q:41160:', 'STIF:StopPoint:Q:41233:']
headers = { 'Accept-Encoding' : 'gzip', 'Authorization' : 'Bearer ' + token }

for i in paramsList:
	response = requests.get(url, params={'MonitoringRef': i}, headers=headers)
	if response.status_code != 200:
		print('Status:', response.status_code, 'Erreur sur la requete; fin de programme')
		exit()
	jsonData = response.json()
	producer.send('ratp-api', json.dumps(jsonData))
	producer.flush()
