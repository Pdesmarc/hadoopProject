import requests
from kafka import KafkaProducer
import json
producer = KafkaProducer(bootstrap_servers='localhost:9092')

def get_tok():
	urlOAuth = 'https://as.api.iledefrance-mobilites.fr/api/oauth/token' 
	client_id='a636e4c2-afae-4905-afe5-84b7c326f362' 
	client_secret='5ad70c24-431c-4ad4-b16f-0b5de340bfcd'
	data =dict(grant_type='client_credentials', scope='read-data', client_id=client_id, client_secret=client_secret)
	response = requests.post(urlOAuth, data=data) 
	print(response.json)
	if response.status_code != 200: 
		print('Status:', response.status_code, 'Erreur sur la requete; fin de programme')
		exit()
	jsonData = response.json() 
	return jsonData['access_token']

token = get_tok()


url = 'https://traffic.api.iledefrance-mobilites.fr/v1/tr-global/estimated-timetable'

headers = { 'Accept-Encoding' : 'gzip', 'Authorization' : 'Bearer ' + token }
response = requests.get(url,headers=headers)
if response.status_code != 200:
	print('Status:', response.status_code, 'Erreur sur la requete; fin de programme')
	exit()
jsonData = response.json()
print(jsonData)
producer.send('sio-topic', json.dumps(jsonData))
producer.flush()
