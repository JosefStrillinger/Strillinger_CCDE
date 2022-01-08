import random

class Question:
    def __init__(self, level, question, answer1, answer2, answer3, answer4, correctAnswer):
        self . _level = level
        self . _question = question
        self . _answer1 = answer1
        self . _answer2 = answer2
        self . _answer3 = answer3
        self . _answer4 = answer4
        self . _correctAnswer = correctAnswer
    def __str__(self):
        ret = self . _level +" | "+self . _question+" | "+self . _answer1+" | "+self . _answer2+" | "+self . _answer3+" | "+self . _answer4+" | "
        return ret

def getData(questions):
    file = open('millionaire.txt', 'r')
    lines = file.read()
    file.close()
    line = []
    line = lines.split("\n")
    for l in range(len(line)):
        parts = []
        parts = line[l].split("\t")
        question = [parts[0], parts[1], parts[2],
                    parts[3], parts[4], parts[5], parts[2]]
        questions.append(question)

def randomizeAnswer():
    rand1 = random.randint(2,5)
    rand2 = random.randint(2,5)
    while rand2 == rand1:
        rand2 = random.randint(2,5)
    rand3 = random.randint(2,5)
    while rand3 == rand1 or rand3 == rand2:
        rand3 = random.randint(2,5)
    rand4 = random.randint(2,5)
    while rand4 == rand1 or rand4 == rand2 or rand4 == rand3:
        rand4 = random.randint(2,5)
    return rand1, rand2, rand3, rand4

def getQuestion(rand, questions):
    ans1, ans2, ans3, ans4 = randomizeAnswer()
    question = Question(questions[rand][0], questions[rand][1], questions[rand][ans1],
                        questions[rand][ans2], questions[rand][ans3], questions[rand][ans4], questions[rand][6])
    return question