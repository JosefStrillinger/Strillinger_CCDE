import random
from random import randint

class Question:
    def __init__(self, level, question, answers, correctAnswer):
        self . _level = level
        self . _question = question
        self . _answers = answers
        self . _correctAnswer = correctAnswer
    def __str__(self):
        ret = str(self . _level) +" | "+self . _question+" | "+self . _answers+" | "
        return ret

def getData():
    questions = []
    file = open('millionaire.txt', 'r')
    lines = file.read()
    file.close()
    line = []
    line = lines.split("\n")
    for l in range(len(line)):
        parts = []
        parts = line[l].split("\t")
        answers = [parts[2], parts[3], parts[4], parts[5]]
        random.shuffle(answers)
        correct = parts[2]
        q = Question(parts[0], parts[1], answers, correct)     
        questions.append(q)
    return questions

def getQuestion(level, questions):
    questionsOfLevel = []
    for question in questions:
        if int(question.level) == level:
            questionsOfLevel.append(question)
    random = randint(0, len(questionsOfLevel) - 1)
    return questionsOfLevel[random]

