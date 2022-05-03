import datetime
import json
import os
from urllib import response
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
import sqlite3
from sqlalchemy.sql.expression import func

from sqlalchemy import Column, Integer, Text, DateTime, create_engine, LargeBinary, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import time
from ids import comp_vision_key as subscription_key

from dataclasses import dataclass

from camera_client import decode_base64

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
api = Api(app)

Base = declarative_base()
metadata = Base.metadata
engine = create_engine(r'sqlite:///D:\Apps\SQLite\images.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property

class Image(Base):
    __tablename__ = "Images"
    
    ID = Column(Integer, primary_key=True)
    TITLE = Column(Text, nullable=False)
    DEVICE = Column(Text, nullable=False)
    DATE = Column(DateTime, nullable=False)
    PICTURE = Column(Text, nullable=False)
    EXTENSIONS = Column(Text, nullable=False)
    DESCRIPTION = Column(Text)
    ANALYSIS = Column(Text)
    RECOGNITION = Column(Text)
    
    
    def serialize(self):
        return{
            "ID" : str(self.ID),
            "TITLE" : self.TITLE,
            "DEVICE" : self.DEVICE,
            "DATE" : str(self.DATE),
            "PICTURE" : self.PICTURE,
            "EXTENSIONS" : self.EXTENSIONS,
            "DESCRIPTION" : self.DESCRIPTION        
        }
    

def CognitiveServices():
    def analyseImage(self, path):
        endpoint = "germanywestcentral"
        credentials = CognitiveServicesCredentials(subscription_key)
        client = ComputerVisionClient(endpoint="https://"+endpoint+".api.cognitive.microsoft.com/", credentials=credentials)
        image_analysis = client.analyze_image_in_stream((open(path, "rb")),visual_features=[VisualFeatureTypes.tags])
        info = []
        for tag in image_analysis.tags:
            info.append(str(tag))
        analysis = client.describe_image_in_stream(open(path, "rb"),3,"en")
        for caption in analysis.contents:
            info.append(caption.text)
            info.append(caption.confidence)
        return json.dumps(info)
    def recognize_image(self, path):
        endpoint = "germanywestcentral"
        credentials = CognitiveServicesCredentials(subscription_key)
        client = ComputerVisionClient(endpoint="https://"+endpoint+".api.cognitive.microsoft.com/", credentials=credentials)
        numbrtOfCharsInOperationId = 360
        rawHttpResponse = client.read_in_stream(open(path, "rb"), language="en", raw=True)
        operationLocation = rawHttpResponse.headers["Operation-Location"]
        idLocation = len(operationLocation)-numbrtOfCharsInOperationId
        operationId = operationLocation[idLocation:]
        time.sleep(10)
        info = []
        result = client.get_read_result(operationId)
        info.append(result)
        if result.status == OperationStatusCodes.succeeded:
            for line in result.analyze_result.read_results[0].lines:
                info.append(line.txt)
                info.append(line.bounding_box)
        return json.dumps(info)
           
def file_check(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
class File(Resource):
    def get(self, id):
        image = Image.query.get(id)
        if not image:
            return jsonify({"message" : "does not exist"})
        return image.serialize()
    def delete(self, id):
        image = Image.query.get(id)
        if not image:
            return jsonify({"message" : "file with this id does not exist %s" %id})
        db_session.delete(image)
        db_session.flush()
        return jsonify({"message" : "%s deleted" %id})
    def put(self, id):
        services = CognitiveServices()
        if request.form["EXTENSION"] not in ALLOWED_EXTENSIONS:
            return jsonify({"message" : "extension is wrong"})
        analysis = ""
        recognition = ""
        path = "img/%s.%s"%(str(id), request.form["EXTENSION"])
        if request.form["SERVICE"] == "analysis":
            decode_base64(path, request.form["PICTURE"])
            analysis = json.dumps(services.analyseImage(path))
        elif request.form["SERVICE"] == "recognition":
            recognition = json.dumps(services.recognizeImage(path))
        else:
            response = "no or unknown service"
        image = Image(TITLE=request.form["TITLE"], DEVICE=request.form["DEVICE"], DATE=datetime.datetime.strptime(request.form["DATE"], '%Y-%m-%d %H:%M:%S.%f'), PICTURE=request.form["PICTURE"], EXTENSIONS=request.form["EXTENSIONS"], DESCRIPTION=request.form["DESCRIPTION"], ANALYSIS=analysis, RECOGNITION=recognition)
        db_session.add(image)
        db_session.flush()
        return jsonify({"message" : "file saved","analysis":analysis, "recognition":recognition})

api.add_resource(File, "/file/<string:id>")

@app.route("/search/<string:name>")
def search(name):
    res = Image.query.filter(or_(Image.name.contains(name), Image.desc.contains(name))).all()
    return jsonify(res)

def createDB():
    Base.metadata.create_all(bind = engine)
    
if __name__ == '__main__':
    createDB()
    app.run(debug=True, host="0.0.0.0")