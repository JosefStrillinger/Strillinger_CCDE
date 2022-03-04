
import requests


host='http://localhost:5000/rest/'

result= requests.get(host+"1").json()
print(result)

result = requests.delete(host+"1").json()
print(result)

result= requests.get(host+"1").json()
print(result)

result = requests.put(host + "500", data={"difficulty":1, "question":"Who is the greatest rapper of all time?","correct_answer":"Eminem","answer2":"Jay-Z","answer3":"Kendrik Lamar","answer4":"J. Cole","background_information":"JS"}).json()
print (result)

result = requests.patch(host + "500", data={"difficulty":1, "question":"Who is the greatest rapper of all time, lmao?","correct_answer":"Eminem","answer2":"Jay-Z","answer3":"Kendrik Lamar","answer4":"J. Cole","background_information":"JS"}).json()
print (result)


