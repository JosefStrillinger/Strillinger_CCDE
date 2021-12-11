from model import Question
import random

questions = []


def getData():
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


def getQuestion(rand):
    ans1, ans2, ans3, ans4 = randomizeAnswer()
    question = Question(questions[rand][0], questions[rand][1], questions[rand][ans1],
                        questions[rand][ans2], questions[rand][ans3], questions[rand][ans4], questions[rand][6])
    return question


getData()

score = 0
isRunning = 1
level1 = 60
level2 = 66
level3 = 50
level4 = 15
currentlevel = 40
substractor = 40

while isRunning == 1:
    rand = random.randint(currentlevel-substractor, currentlevel)
    q = getQuestion(rand)
    print(q)
    answer = input("Your answer: ")
    if answer == questions[rand][6]:
        print("Correct\n")
        score += 1
        if score == 10:
            print("Congratulations, you did it!!!\nYou really won!\nPresitge, that is!\nYou're welcome\n\n\nNow, go away\n")
            isRunning = 0
        else:
            match score:
                case 2:
                    currentlevel += level1
                    substractor = level1
                case 4:
                    currentlevel += level2
                    substractor = level2
                case 6:
                    currentlevel += level3
                    substractor = level3
                case 8:
                    currentlevel += level4
                    substractor = level4
    else:
        print("False\nYou really aren't good at this, are you?\n\n")
        score = 0
        currentlevel = 40
        substractor = 40
