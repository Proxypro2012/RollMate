BASE_URL = "http://localhost:5000"
import requests

url = str(BASE_URL+"/change-group-by-group")

payload = {
    'groupId': 'KIAHSTIWA30',
    'newGroup': 'E',
    'oldGroup': 'I'
}

response = requests.post(url, json=payload)
print(response.text)