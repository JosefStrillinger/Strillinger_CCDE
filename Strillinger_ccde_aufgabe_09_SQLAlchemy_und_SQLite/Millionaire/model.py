from distutils.log import info
from random import randint
import random
from flask import Flask, request, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from sqlalchemy import create_engine
from flask_restful import Resource, Api
from dataclasses import dataclass
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()
metadata = Base.metadata

engine = create_engine('sqlite:///millionaire.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.queary = db_session.query_property()
app = Flask(__name__)
api = Api(app)

class Millionaire(Base):
    __tablename__ = 'millionaire'
    
    id: int
    difficulty: int
    question: str
    correct_answer: str
    answer2: str
    answer3: str
    answer4: str
    background_information: str

    id = Column(Integer, primary_key=True)
    difficulty = Column(Integer)
    question = Column(Text)
    correct_answer = Column(Text)
    answer2 = Column(Text)
    answer3 = Column(Text)
    answer4 = Column(Text)
    background_information = Column(Text)

class MillionaireREST(Resource):
    def get(self, id):
        info = Millionaire.queary.get(id)
        return jsonify(info)
    def put(self, id):
        data = request.get_json(force=True)['info']
        print(data)
        info = Millionaire(difficulty=data['difficulty'], question=data['question'], correct_answer=data['correct_answer'], answer2=data['answer2'], answer3=data['answer3'], answer4=data['answer4'], background_information=['background_information'])
        db_session.add(info)
        db_session.flush()
        return jsonify(info)
    def delete(self, id):
        info = Millionaire.queary.get(id)
        if info is None:
            return jsonify({'message':'object with id %d does not exist' % id})
        db_session.delete(info)
        db_session.flush()
        return jsonify({'message':'%d deleted' % id})
    def patch(self, id):
        info = Millionaire.queary.get(id)

class Question:
    
    def __init__(self, level, question, answers, correctAnswer, id):
        self.level=level
        self.question=question
        self.answers=answers
        self.correctAnswer=correctAnswer
        self.id=id
    
    def __str__(self):      
       return str(self.level)+" "+" "+self.question+" | "+str(self.answers)+" | "+str(self.correctAnswer)+" | " +str(self.id)
   
    def serialize(self):
        return {'id': self.id, 'question':self.question, 'level':self.level, 'answers':self.answers, 'correctAnswer': self.correctAnswer }
    

def getData(filename):
    f = open (filename,"r")
    f.readline()
    lines=f.readlines()
    questions=[]
    i = 0
    for item in lines:     
        question=item.split("\t")
        answers=[question[2],question[3],question[4],question[5]]
        random.shuffle(answers)
        correct=answers.index(question[2])
        q1= Question(question[0],question[1],answers,correct, i)
        questions.append(q1)
        i+=1
    return questions
    
def getRandomQuestion(level, questions):
    levelQuestions = []
    for question in questions:
        if int(question.level) == level:
            levelQuestions.append(question)
    random = randint(0, len(levelQuestions) - 1)
    return levelQuestions[random]

quests = getData("millionaire.txt") 

def getQuests():
    return quests

#TODO Service Class

class Service(Resource):
    def get(self, id):
        info = Millionaire.queary.get(id)
        return jsonify(info)
    
    def put(self, id):
        data = request.get_json(force=True)['info']
        print(data)
        info = Millionaire(difficulty=data['difficulty'], question=data['question'], correct_answer=data['correct_answer'], answer2=data['answer2'], answer3=data['answer3'], answer4=data['answer4'], background_information=['background_information'])
        db_session.add(info)
        db_session.flush()
        return jsonify(info)
    
    def patch(self, id):
        info = Millionaire.queary.get(id)
        if info is None:
            return jsonify({'message':'object with id %d does not nexist' % id})
        data=json.loads(request.json['info'])
        if 'difficulty' in data:
            info.difficulty = data['difficulty']
        if 'question' in data:
            info.question = data['question']
        if 'correct_answer' in data:
            info.correct_answer = data['correct_answer']
        if 'answer2' in data:
            info.answer2 = data['answer2']
        if 'answer3' in data:
            info.answer3 = data['answer3']
        if 'answer4' in data:
            info.answer4 = data['answer4']
        if 'background_information' in data:
            info.background_information = data['background_information']
        db_session.add(info)
        db_session.flush()
        return jsonify({'message': 'object with id %d modified' % id})
    
    def delete(self, id):
        info = Millionaire.queary.get(id)
        if info is None:
            return jsonify({'message':'object with id %d does not exist' % id})
        db_session.delete(info)
        db_session.flush()
        return jsonify({'message':'%d deleted' % id})


#TODO All-Questions

class AllQuests(Resource):
    def get(self):
        message = []
        for qu in quests:
            message.append(qu.serialize())
        return {"data" : message}
    
    
