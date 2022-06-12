from flask import Flask, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
import pymongo
import requests


#initialisation du server flask
app = Flask(__name__)

#configuration de la bdd avec mongo
#configuration et connection à la bdd
app.config["MONGO_URI"] = "mongodb://localhost:27017/projectapi"
mongo = PyMongo(app)

#définir une route pour voir si l'api fonctionne
@app.route('/postdata', methods=['POST'])
def create_users():
    currentCollection = mongo.db.data
    #receiving data
    level_0 = request.json['level_0']
    index = request.json['index']
    Player = request.json['Player']
    Position = request.json['Position']
    Age = request.json['Age']
    Teams = request.json['Teams']
    #hashed_password = generate_password_hash(password)
    currentCollection.insert_one({'level_0': level_0, 'index' : index,'Player' : Player, 'Position': Position, 'Age': Age, 'Teams':Teams})
    return jsonify({'level_0': level_0, 'index' : index, 'Player' : Player, 'Position': Position, 'Age': Age, 'Teams': Teams})
#methode get
@app.route('/allplayers', methods=['GET'])
def getAll():
    #log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
    board = list()
    currentCollection = mongo.db.data
    #contition avec boucle pour tout récupérer
    for i in currentCollection.find():
        board.append({'level_0': i['level_0'], 'index' : i['index'],'Player' : i['Player'], 'Position' : i['Position'], 'Age': i['Age'], 'Teams' : i['Teams']})
    return jsonify(board)

#nous allons vouloir faire une recherche par noms
@app.route('/allplayers/<Player>', methods=['GET'])
def get_name(Player):
    currentCollection = mongo.db.data
    data = currentCollection.find_one({"Player" : Player})
    #on retourne sous format json la donnée chercher
    return jsonify({'level_0': data['level_0'], 'index' : data['index'],'Player' : data['Player'],'Position' : data['Position'], 'Age' : data['Age'], 'Teams': data['Teams']})
#méthode qui permet de supprimer des données
@app.route('/deletedata/<Player>', methods=['DELETE'])
def delete_data(Player):
    currentCollection = mongo.db.data
    currentCollection.delete_one({'Player' : Player})
    #nous allon rediriger vers l'ensemble de nos données
    return redirect(url_for('getAll')) 

#méthode qui va nous permettre de pouvoir modifier certaine données
@app.route('/updatedata/<Player>', methods=['PUT'])
def update_data(Player):
    currentCollection = mongo.db.data
    #la requête que nous voulons
    updateLevel = request.json['level_0']
    updateIndex = request.json['index']
    updatePlayer = request.json['Player']
    updatePosition = request.json['Position']
    updateAge = request.json['Age']
    updateTeams = request.json['Teams']
    currentCollection.find_one({'Player' : Player})
    currentCollection.update_many({'Player' : Player}, {"$set" : { 'level_0' : updateLevel, 'index' : updateIndex,'Player' : updatePlayer, 'Position' : updatePosition, 'Age' : updateAge, 'Teams' : updateTeams}})
    #on renvoie les données sous format json
    return jsonify({'level_0': updateLevel, 'index' : updateIndex, 'Player' : updatePlayer, 'Position': updatePosition, 'Age': updateAge, 'Teams': updateTeams})
    #on redirige le résultat vers l'ensemble de nos données
    #return redirect(url_for('getAll'))
#méthode qui permet de paginer les resultats
@app.route('/allplayers/pagination/', methods=['GET'])
def pagination():
    collectionData = mongo.db.data
    #on pose une limite de résultat à pas dépassé
    #créer un décalage, à partir d'u'une chiffre d'index, on commence
    #à afficher les données
    pageNumber = int(request.args['PageNumber'])
    limit = int(request.args['limit'])
    starting_id = collectionData.find().sort('_id', pymongo.ASCENDING)
    #on commence de la pageNumber et on sort les 10 data comme prédéfini
    last_id = starting_id[pageNumber]['_id']
    query = collectionData.find({'_id' : {'$gte' : last_id}}).sort('_id', pymongo.ASCENDING).limit(limit)
    #tableau qui prend en compte les données
    print(query[0])
    output = []
    for i in query:
        output.append({'collectionData': i})
    return jsonify({'result' : str(output), 'prev_url' : '', 'next_url' : ''})
#test de l'api


#méthode qui permet de tester notre api
#condition pour dire que le server est lancé
if __name__ == "__main__":
    app.run(debug=True)