import requests
import json

import ids

url = 'http://api.openweathermap.org/data/2.5/weather?q=Innsbruck&appid=%s&units=metric' % ids.openweathermap_key

if __name__ == '__main__':
    response = requests.get(url).json()
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