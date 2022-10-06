# Guide: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html

import boto3
import pandas as pd
import numpy as np

Access_key ="YOUR_KEY"
Secret_Access_key = "SECRET_KEY"   # Vous pouvez les obtenir en créant un compte AWS
client = boto3.client(
    'dynamodb',
    "eu-west-3",
    aws_access_key_id=Access_key,
    aws_secret_access_key=Secret_Access_key
    )
dynamodb = boto3.resource(
   'dynamodb',
    "eu-west-3",
    aws_access_key_id=Access_key,
    aws_secret_access_key=Secret_Access_key
)
billet_Table = dynamodb.Table("Billet")
vente_Table = dynamodb.Table("Vente")
spectacle_Table = dynamodb.Table("Spectacle")
salle_Table = dynamodb.Table("Salle")
concert_Table = dynamodb.Table("Concert")

billets = pd.read_csv("données_billet.csv", sep =';')
spectacle = pd.read_csv("données_specatacle.csv", sep =';')
salle = pd.read_csv("données_salle.csv", sep =';')
concert = pd.read_csv("données_concert.csv", sep =';')
vente =  pd.read_csv("données_vente.csv", sep =';')

# Insérer les données

csv = [billets, spectacle, salle, concert, vente]
tables= [billet_Table, spectacle_Table, salle_Table, concert_Table, vente_Table]
for i in range(len(csv)):
    for j in range(len(csv[i])):
        doc = dict(csv[i].loc[j,:])
        for value in doc:
            if not isinstance(doc[value],str):
                doc[value] = int(doc[value])
        tables[i].put_item(Item= doc)

# REQUETES

#a) Quels sont les dates du concert d’un artiste donné ?

Artiste = "Mireille Matthieu"

response = spectacle_Table.scan()
data = response['Items']
for spec in data:
    if spec["artist"] == Artiste:
        print(spec["date_debut"])

#b) Quels sont les noms des salles ayant la plus grande capacité ?

response = salle_Table.scan()
data = response['Items']
capacite = []
for salle in data:
    capacite.append(salle["capacite"])
index = np.argmax(capacite)
data[index]["nom"]

#c) Quels sont les artistes n’ayant jamais réalisé de concert à une salle donnée ?

salle_nom = "salle_0"

response = spectacle_Table.scan()
spectacle_data = response['Items']
response = salle_Table.scan()
salle_data = response['Items']

salle_id = [salle for salle in salle_data if salle["nom"] == salle_nom][0]["Salle_ID"]
artists = list(set([spectacle["artist"] for spectacle in spectacle_data]))

res = []
for artist in artists:
    spectacles = [spec for spec in spectacle_data if spec["artist"]==artist]
    salles = [spec["salle_id"] for spec in spectacles]
    if salle_id not in salles:
        res.append(artist)

#d) Quel sont les chanteurs ayant réalisé au moins un concert dans toutes les salles ?

response = spectacle_Table.scan()
data = response['Items']
salles = list(set([data[i]["salle_id"] for i in range(len(data))]))
artistes = list(set([data[i]["artist"] for i in range(len(data))]))
res = []
for artiste in artistes:
    tmp = salles
    for spec in data:
        if spec["salle_id"] in tmp:
            tmp.pop(tmp.index(spec["salle_id"]))
    if len(tmp) == 0:
        res.append(artiste)

#e) Quels sont les chanteurs et les identificateurs des concerts pour lesquels il ne reste aucun billet invendu ?

response = vente_Table.scan()
vente_data = response['Items']
response = billet_Table.scan()
billets_data = response['Items']
response = spectacle_Table.scan()
spectacle_data = response['Items']

all_id = [billets_data[i]["Billet_ID"] for i in range(len(billets_data))]
id_vendus = [vente_data[i]["Billet_ID"] for i in range(len(vente_data))]

res = []
for spe in spectacle_data:
    id = spe["Spectacle_ID"]
    if all_id.count(id)==id_vendus.count(id):
        res.append((id, spe["artist"]))

#f) Combien de billets d’une catégorie donnée ont été vendus par spectacles à une date donnée ?
date = "25/11/2021"
cat = 3A


response = spectacle_Table.scan()
spectacle_data = response['Items']
response = vente_Table.scan()
vente_data = response['Items']
response = billet_Table.scan()
billets_data = response['Items']
response = concert_Table.scan()
concerts_data = response['Items']


for spec in spectacle_data:
    concerts = [concert for concert in concerts_data if concert["spectacle_id"] == spec["Spectacle_ID"] and concert["date"]==date]
    concerts_id= [concert["Concert_ID"] for concert in concerts]
    billets = [i for i in billets_data if i["Concert_ID"] in concerts_id and i["categorie"] == cat]
    billets_id = [i["Billet_ID"] for i in billets]
    billets_vendus = [i for i in vente_data if i["Billet_ID"] in billets_id]
    print(spec["Spectacle_ID"], len(billets_vendus))