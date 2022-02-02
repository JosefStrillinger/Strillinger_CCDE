from random import randint
import random
from flask import request

from flask_restful import Resource

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
        for qu in quests:
            if qu.id == id:
                return {"Result" : qu.serialize()}
        return {"Result" : "Abfrage hat nicht funktioniert"}
    
    def put(self, id):
        qu = Question(request.form['level'], request.form['question'], request.form['answers'], request.form['correct'], id)
        quests.append(qu)
        return {"Result": "Erfolgreich hinzugefügt!"}
    
    def patch(self, id):
        qu = Question(request.form['level'], request.form['question'], request.form['answers'], request.form['correct'], id)
        print(qu)
        for q in quests:
            if q.id == id:
                quests[quests.index(q)]=qu
                return{"Result": "Efolgreich geändert!"}
        return{"Result":"Nicht erfolgreich geändert!"}
    
    def delete(self, id):
        for qu in quests:
            if qu.id==id:
                quests.pop(quests.index(qu))
                return {"Result" : "Erfolgreich gelöscht!"}
        return {"Result":"Nicht erfolgreich gelöscht!"}


#TODO All-Questions

class AllQuests(Resource):
    def get(self):
        message = []
        for qu in quests:
            message.append(qu.serialize())
        return {"data" : message}
    
    
