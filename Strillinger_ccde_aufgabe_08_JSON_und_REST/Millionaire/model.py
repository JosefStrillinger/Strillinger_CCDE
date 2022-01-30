from random import randint
import random

class Question:
    
    def __init__(self, level, question, answers, correctAnswer, id):
        self.level=level
        self.question=question
        self.answers=answers
        self.correctAnswer=correctAnswer
        self.id=id
    
    def __str__(self):      
       return str(self.level)+" "+" "+self.question+" | "+str(self.answers)+" | "+str(self.correctAnswer)
    
def getData(filename):
    f = open (filename,"r")
    f.readline()
    lines=f.readlines()
    questions=[]
    i = 1
    for item in lines:
        i+=1
        question=item.split("\t")
        answers=[question[2],question[3],question[4],question[5]]
        random.shuffle(answers)
        correct=answers.index(question[2])
        q1= Question(question[0],question[1],answers,correct, i)
        questions.append(q1)
    return questions
    
def getRandomQuestion(level, questions):
    levelQuestions = []
    for question in questions:
        if int(question.level) == level:
            levelQuestions.append(question)
    random = randint(0, len(levelQuestions) - 1)
    return levelQuestions[random]