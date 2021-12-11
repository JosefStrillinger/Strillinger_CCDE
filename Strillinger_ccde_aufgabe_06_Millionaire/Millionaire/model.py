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
