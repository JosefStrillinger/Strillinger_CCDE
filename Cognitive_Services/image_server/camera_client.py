import base64

import requests
from io import BytesIO
from time import sleep
import datetime
#from picamera import PiCamera
import paho.mqtt.client as mqtt

host = "http://192.168.178.26:5000/file"
mqtt_ip = "raspberrypi"
mqtt_port = "2222"
username = "jstrillinger"
password = "Jstrillinger1"

client = mqtt.Client('raspberryPi')
channelSend = "foto/get/dev0"
channelPost = "foto/taken/dev0"

my_stream = BytesIO()
#camera = PiCamera()

def encode_base64(data):
    base64_encode_data = base64.b64encode(data)
    return base64_encode_data.decode('utf-8')

def decode_base64(filename, data):
    base64_decode_data = data.encode("utf-8")
    with open(filename, "wb") as file:
        decoded_data = base64.decodebytes(base64_decode_data)
        file.write(decoded_data)

def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("Message received: %s" % data)
    if data == "photo":
        enc = encode_base64(take_photo(channelPost))
        request_put(enc)
        print("Image captured successfully")
    else:
        print("Execution failed %s!" % data)
        
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connection established")
        return
    print("Connection failed")
    
def on_connect_fail(client, userdata, flags, rc, properties=None):
    print("Connection failed!")

def publish_mqtt(channel):
    client.subscribe(channel)
    
def take_photo(channel):
    #amera.capture(my_stream, "jpeg")
    publish_mqtt(channel, "foto_taken")
    return my_stream.getvalue()

def request_put(photo):    
    response = requests.put("%s/%s" % (host, "1"), data={
        "TITLE" : "Test",
        "DEVICE" : "RaspberryPi",
        "DATE" : datetime.datetime.now(),
        "PICTURE" : photo,
        "ETENSION" : "png",
        "DESCRIPTION" : "test on raspberry pi"  
    }).json()
    print(response)

def request_delete(id):
    response = requests.delete("%s/%s" % (host, "5")).json()
    print(response)

def request_get(id):
    response = requests.get("%s/%s" % (host, "10")).json()
    if "message" not in response:
        path="/tmp/%s.%s" % (response["ID"], response["EXTENSION"])
        decode_base64(path, response["PICTURE"])
        print("Picture saved in %s" % path)
    else:
        print(response)

if __name__ == '__main__':
    print("Connecting")
    client.on_connect=on_connect
    client.on_connect_fail=on_connect_fail
    client.username_pw_set(username, password)
    client.connect(mqtt_ip, port=mqtt_port)
    print("Subscribing")
    client.subscribe(channelSend)
    client.on_message=on_message
    client.loop_forever()
    print("Finished")