import requests
import json

import ids

url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat=47.2627&lon=11.3945&appid=%s' % ids.openweathermap_key
url2 = 'http://api.openweathermap.org/data/2.5/weather?q=Innsbruck&appid=%s&units=metric' % ids.openweathermap_key

if __name__ == '__main__':
    responsePollution = requests.get(url).json()
    responseWeather = requests.get(url2).json()
    '''
    print(response)
    # Formatierte Ausgabe
    print(json.dumps(response, indent=4, sort_keys=False))
    #Schreiben in eine Datei
    with open('/tmp/data.json', 'w') as outfile:
        json.dump(response, outfile)

    #Laden von JSON aus einer Datei
    with open('/tmp/data.json') as json_file:
        data = json.load(json_file)
    print (data)


    # Einfache Abfragen
    longitude = response["coord"]["lon"]
    print (longitude)

    description = response["weather"][0]["description"]
    print(description)
    '''
    '''print(json.dumps(responsePollution, indent=4, sort_keys=False))'''
    co = str(responsePollution['list'][0]['components']['co'])
    no2 = str(responsePollution['list'][0]["components"]["no2"])
    o3 = str(responsePollution['list'][0]["components"]["o3"])
    pm10 = responsePollution['list'][0]["components"]["pm10"]
    
    print("Kohlenstoffmonoxid: ")
    print(co)
    print("\nStickstoffdioxid: ")
    print(no2)
    print("\nFeinstaub: ")
    print(pm10)
    print("\nOzon: ")
    print(o3)
    
    print("--------------------------------------------------------------")
    '''print(json.dumps(responseWeather, indent=4, sort_keys=False))'''
    
    temp = responseWeather['main']['temp']
    tempFeel = responseWeather['main']['feels_like']
    humidity = responseWeather['main']['humidity']
    
    print("\nTemperatur: ")
    print(temp)
    print("\nGefühlt: ")
    print(tempFeel)
    print("\nLuftfeuchtigkeit: ")
    print(humidity)
    
    
    
    