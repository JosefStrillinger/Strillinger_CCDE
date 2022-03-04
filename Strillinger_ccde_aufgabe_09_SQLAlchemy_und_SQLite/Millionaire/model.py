#from distutils.log import info
import sqlite3
from random import randint
import random
from flask import Flask, jsonify, render_template, request, redirect, session, g
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from flask_restful import Resource, Api
from dataclasses import dataclass
from sqlalchemy import Column, Integer, Text, Float, DateTime, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
import json

Base = declarative_base()
metadata = Base.metadata

engine = create_engine('sqlite:///.\millionaire.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()
app = Flask(__name__)
api = Api(app)

class Millionaire(Base):
    __tablename__ = 'millionaire'
    
    id = Column(Integer, primary_key=True)
    difficulty = Column(Integer)
    question = Column(Text)
    correct_answer = Column(Text)
    answer2 = Column(Text)
    answer3 = Column(Text)
    answer4 = Column(Text)
    background_information = Column(Text)
    
    def serialize(self):
        return {
            "ID": self.id,
            "level": self.difficulty,
            "fragetext": self.question,
            "antwortmoeglichkeit": [self.correct_answer, self.answer2, self.answer3, self.answer4],
            "antwort": 0
        }
    

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
    

def getData():
    infos = Millionaire.query.all()
    #for x in infos:
    #    print(x.serialize())
    questions=[]
    i = 0
    for info in infos:
        # Millionaire mill = Millionaire.get(id)
        answers=[info.correct_answer,info.answer2,info.answer3,info.answer4]
        random.shuffle(answers)
        #correct=answers.index(infos[id].correct_answer)
        q1= Question(info.difficulty, info.question, answers, answers.index(info.correct_answer), info.id)#auf db umschreiben, danach ===> profit
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

quests = getData() 

def getQuests():
    return quests

#TODO Service Class

def get_question_by_id(id):
    data = Millionaire.query.get(id)
    if data == None:
        return {"ERROR"}
    return data.serialize()

def add_question(id, data):
    info = Millionaire(difficulty=data['difficulty'], question=data['question'], correct_answer=data['correct_answer'], answer2=data['answer2'], answer3=data['answer3'], answer4=data['answer4'], background_information=['background_information'])
    db_session.add(info)
    db_session.flush()
    return info.serialize()

def change_question(id, data):
    info = Millionaire.query.get(id)
    if info is None:
        return jsonify({'message':'object with id %d does not nexist' % id})
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
    return {"200: Frage mit ID: {} wurde geändert!".format(id)}

def delete_question(id):
    info = Millionaire.query.get(id)
    if info is None:
        return jsonify({'message':'object with id %d does not exist' % id})
    db_session.delete(info)
    db_session.flush()
    return True

def get_all_questions():
    infos = Millionaire.query.all()
    return infos.serialize()