from model import Question, getData, getQuestion
from flask import Flask, render_template, session


app = Flask(__name__)
app.secret_key='_5#y2L”F4Q8z\n\xec]/'
@app.route('/')
def start():
   session["level"]=0
   return render_template("startseite.html")

@app.route('/quest')
def showQuests():
   questions = []
   return render_template("questions.html", getData())

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

   questions = getData()
   q=getQuestion(session["level"], questions)
   return render_template("game.html", level = session["level"])

if __name__ == '__main__':
   app.debug = True
   app.run()