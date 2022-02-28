
import requests


host='http://localhost:5000/rest/'

result= requests.get(host+"1").json()
print(result)

result = requests.delete(host+"1").json()
print(result)

result= requests.get(host+"1").json()
print(result)

result = requests.put(host + "500", data={"level":1, "question":"Who is the greatest rapper of all time?","answers": ["Eminem","Jay-Z","Kendrik Lamar","J. Cole"],"correct":"Eminem"}).json()
print (result)

result = requests.patch(host + "500", data={"level":1, "question":"Who is the greatest rapper of all time, lmao?","answers": ["Eminem","Jay-Z","Kendrik Lamar","J. Cole"],"correct":"Eminem"}).json()
print (result)


