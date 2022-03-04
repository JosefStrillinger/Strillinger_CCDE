import json
from flask_restful import Api, Resource
from model import Question, Millionaire, getRandomQuestion, getData, getQuests, get_question_by_id, change_question, add_question, delete_question, get_all_questions
from flask import Flask, jsonify, render_template, request, session


app = Flask(__name__)
app.secret_key='_5#y2L”F4Q8z\n\xec]/'
api = Api(app)

@app.route('/')
def start():
   session["difficulty"]=0
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
      if answer == (session["correct_answer"]+1):
         if session["difficulty"] == 4:
            #level auf 0, korrekte Antwort löschen; gewinner seite anzeigen
            session["difficulty"] = 0
            session.pop('correct_answer', None)
            return render_template("end.html", result=dict, text="Sie haben gewonnen!")
         session["difficulty"]+=1
      else:
         session["difficulty"] = 0
         return render_template("end.html", result=dict, text="Sie haben verloren!")

   q= getRandomQuestion(session["difficulty"], getQuests())
   
   session["correct_answer"] = q.correctAnswer
   return render_template("game.html",result=dict, level = session["difficulty"], question=q)

class Service(Resource):
   def get(self, id):
      return get_question_by_id(id)
        
    
   def put(self, id):
      if not get_question_by_id:
         return {"500: Frage mit ID: {} existiert bereits!".format(id)}
      data = request.get_json(force=True)['info']
      add_question(id, data)
      return {"200: Frage mit ID: {} wurde hinzugefügt!".format(id)}
      
    
   def patch(self, id):
      data=json.loads(request.json['info'])
      change_question(id, data)
      return {'message': 'object with id %d modified' % id}
     
   def delete(self, id):
      delete_question(id)
      return {'message':'%d deleted' % id}


#TODO All-Questions

class AllQuests(Resource):
    def get(self):
      get_all_questions



#TODO API-Routing
api.add_resource(Service, "/rest/<int:id>")
api.add_resource(AllQuests, "/all")


if __name__ == '__main__':
   app.debug = True
   app.run()