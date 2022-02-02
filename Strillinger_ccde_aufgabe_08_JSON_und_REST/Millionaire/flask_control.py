import json
from flask_restful import Api
from model import Question, getRandomQuestion, getData, Service, AllQuests, getQuests
from flask import Flask, render_template, session


app = Flask(__name__)
app.secret_key='_5#y2L”F4Q8z\n\xec]/'
api = Api(app)

@app.route('/')
def start():
   session["level"]=0
   return render_template("startseite.html")

@app.route('/questions')
def showQuests():
   return render_template("questions.html", questions = getQuests())

@app.route('/ran')
def ranQuest():
       return json.dumps(getRandomQuestion(1, getQuests()).serialize())

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

   q= getRandomQuestion(session["level"], getQuests())
   
   session["correct"] = q.correctAnswer
   return render_template("game.html",result=dict, level = session["level"], question=q)




#TODO API-Routing
api.add_resource(Service, "/rest/<int:id>")
api.add_resource(AllQuests, "/all")


if __name__ == '__main__':
   app.debug = True
   app.run()