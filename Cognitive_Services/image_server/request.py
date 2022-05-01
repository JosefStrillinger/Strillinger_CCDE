import json
from pygame import encode_string
import requests
import datetime
import base64

host = "http://192.168.178.26:5000/file"
encoded_string = ""
def encode_base64(data):
    base64_encode_data = base64.b64encode(data)
    return base64_encode_data.decode('utf-8')

def decode_base64(filename, data):
    base64_decode_data = data.encode("utf-8")
    with open(filename, "wb") as file:
        decoded_data = base64.decodebytes(base64_decode_data)
        file.write(decoded_data)

with open("image_server/img/elon-musk.jpg","rb") as image_file:
    encode_base64 = encode_base64(image_file.read())

response = requests.put("%s/%s" % (host, "1"), data={
    "TITLE":"Test",
    "DEVICE": "PC",
    "DATE": datetime.datetime.now(),
    "PICTURE":encode_string,
    "EXTENSION":"jpg",
    "DESCRIPTION":"test services",
    "SERVICE":"analysis"
}).json()
print(json.dumps(response, indent=4))

response = requests.put("%s/%s" % (host, "1"), data={
    "TITLE":"Test",
    "DEVICE": "PC",
    "DATE": datetime.datetime.now(),
    "PICTURE":encode_string,
    "EXTENSION":"jpg",
    "DESCRIPTION":"test services",
    "SERVICE":"recognition"
}).json()
print(json.dumps(response, indent=4))