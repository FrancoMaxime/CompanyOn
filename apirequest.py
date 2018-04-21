import requests
import json

url = 'https://techofficeopendata.azurewebsites.net/api/Data?MaxRow=1'
headers = {}
headers['accept'] = 'application/json'
headers['Authorization'] = '093fb7e2-9387-41ee-babe-08d59f923971'
r = requests.get(url, headers=headers)
test = json.loads(r.text)
print test[0]
