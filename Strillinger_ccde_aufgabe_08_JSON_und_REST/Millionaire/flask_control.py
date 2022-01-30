from model import Question, getRandomQuestion, getData
from flask import Flask, render_template, session


app = Flask(__name__)
app.secret_key='_5#y2L”F4Q8z\n\xec]/'

@app.route('/')
def start():
   session["level"]=0
   return render_template("startseite.html")

@app.route('/questions')
def showQuests():
   return render_template("questions.html", questions = getData("millionaire.txt"))

@app.route('/game')
@app.route('/game/<int:answer>')
def game(answer = -1):
   if answer != -1:
      if answer == (session["correct"]+1):
         if session["level"] == 4:
            #level auf 0, korrekte Antwort löschen; gewinner seite anzeigen
            session["level"] = 0
            session.pop('correct', None)
            return render_template("end.html", result=dict, text="Sie haben gewonnen!")
         session["level"]+=1
      else:
         session["level"] = 0
         return render_template("end.html", result=dict, text="Sie haben verloren!")

   q= getRandomQuestion(session["level"], getData("millionaire.txt"))
   
   session["correct"] = q.correctAnswer
   return render_template("game.html",result=dict, level = session["level"], question=q)

if __name__ == '__main__':
   app.debug = True
   app.run()