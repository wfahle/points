import requests

url="http://127.0.0.1:5000/"
headers =  {"Content-Type":"application/json; charset=utf-8"}
res=requests.get(url+'clear')
payload={ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
res = requests.post(url+'transaction', data=payload, headers=headers)
payload= { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
res = requests.post(url+'transaction', data=payload, headers=headers)
payload= { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
res = requests.post(url+'transaction', data=payload, headers=headers)
payload= { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
res = requests.post(url+'transaction', data=payload, headers=headers)
payload= { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
res = requests.post(url+'transaction', data=payload, headers=headers)
print("transactions:")
res = requests.get(url+'transactions')
print(res.json())
print("points:")
res = requests.get(url+'points')
print(res.json())
print("totals:")
res = requests.get(url+'totals')
print(res.json())
payload={"points":5000}
print("spend:")
res = requests.post(url+'spend', data = payload, headers=headers)
print(res.json())
print("totals:")
res = requests.get(url+'totals')
print(res.json())
print("transactions:")
res = requests.get(url+'transactions')
print(res.json())
print("points:")
res = requests.get(url+'points')
print(res.json())
