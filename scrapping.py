from bs4 import BeautifulSoup
import pandas as pd
import requests
from pymongo import MongoClient

#!/usr/bin/env python
# coding: utf-8


#url 
url='https://www.basketball-reference.com/leagues/NBA_2021_per_'
page=requests.get(url)
page





#utilisation de soup
soup=BeautifulSoup(page.content, 'html.parser')
print(soup.prettify)






#première extraction des données
url='https://www.basketball-reference.com/leagues/NBA_2021_per_game.html'
page=requests.get(url)
soup=BeautifulSoup(page.content, 'html.parser')
tableau=soup.find_all('tr', {'class':'full_table'})
print(tableau)





joueur = []
#on prend la première données des tr présent
for j in tableau[1].find_all('td'):
    print(j)
    joueur.append(j.text)
print(joueur)





#permet de renvoyer un tableau de tableau de tout les joueurs ainsi que leurs stats
joueurs=[]
for i in range(len(tableau)):
    joueur=[]
    for j in tableau[i].find_all('td'):
        joueur.append(j.text)
    joueurs.append(joueur)
print(joueurs)





#scraper le nom des colones 
#utilisation de split et suppression de certain caractère
head= soup.find(class_='thead')
column_head=[head.text for item in head][0]
spliter = column_head.split('\n')[2:-1]
print(spliter)





df= pd.DataFrame(joueurs, columns=['Player', 'Pos', 'Age', 'Tm']).set_index('Player')
df.head()





#faire différentes section pour pouvoir faire une simple dataframe par la suite
#créer un tableau qui contiendra toutes ces données
player_info = []
player_position=[]
player_Age=[]
player_Team=[]

Player=[x.text for x in soup.find_all('td', {'data-stat':'player'})]
Position =[x.text for x in soup.find_all('td', {'class':'center'})]
Age=[x.text for x in soup.find_all('td', {'data-stat':'age'})]
Teams=[x.text for x in soup.find_all('td', {'data-stat':'team_id'})]
#boucle qui permet d'itérer
for i in Player:
   player_info.append(i)
   
for j in Position:
   player_position.append(j)
   
for x in Age:
   player_Age.append(x)
   
for z in Teams:
   player_Team.append(z)
   
print(len(player_position))





di = {'Player':player_info, 'Position':player_position, 'Age':player_Age, 'Teams':player_Team}
df = pd.DataFrame(di)
df





#trouver la moyenne d'age des basketteurs
#convertir le type de la colonne age en int
df['Age']=df['Age'].astype(str).astype(int)
df.info()
df['Age'].mean()
print('------------------------------------------')
#donner une descitpion exhaustive de ces données
df['Age'].describe()





#créer un fichier csv pour analyser les données et faire un éventuel reporting
df.to_csv(r'nabadata.csv', index=False)





#connection à la bdd
client=MongoClient('mongodb://localhost:27017')
#vérifier si la connextion à la chaîne de connexion fonctionne bien
client.list_database_names()





db = client['projectapi']
#vérifier toutes les collection présentes dans cette bdd
db.list_collection_names()





#se connecter à notre collection
collection = db['data']
#convertir toutes nos données de notre dataframe sous liste format JSON pour qu'elles soient accepter dans notre 
#collection mongo
df.reset_index(inplace=True)
data_dict = df.to_dict("records")
data_dict



#insérer toutes nos données de notre dataframe dans notre collection
insert_data = collection.insert_many(data_dict)
insert_data


