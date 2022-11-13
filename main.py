from pymongo import MongoClient
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config

# Connecting to MongoDB
cluster = MongoClient("mongodb://localhost:27017")
db = cluster["Neo4j_DB"]
collection = db['NBA']

# MongoDB Connecting to Neo4j
config.DATABASE_URL = 'bolt://neo4j:sgunetsec@localhost:7687/neo4j'

class Player(StructuredNode):
    name = StringProperty(unique_index=True)
    coach = RelationshipFrom('Coach', 'COACH')

class Coach(StructuredNode):
    name = StringProperty(unique_index=True)
    player = RelationshipTo('Player', 'PLAYER')

# cursor = collection.find({})
# for document in cursor:
#     print(document['n'])
#     id_name = document['n']['properties']['name']
#     if(document['n']['labels'][0] == 'PLAYER'):
#         Player(name=id_name).save()
#     if(document['n']['labels'][0] == 'COACH'):
#         Coach(name=id_name).save()

# lebronJames = Player.nodes.first(name="LeBron James")
# frankVogel = Coach.nodes.first(name="Frank Vogel")

# We can save relationship to the variable so we can send it to ES
# lebronFrank = lebronJames.coach.connect(frankVogel)

from elasticsearch7 import Elasticsearch

# Neo4j Connecting to Elasticsearch
es = Elasticsearch(HOST="http://localhost", PORT=9200)

#Insert data to Elasticsearch
i = 0
for player in Player.nodes:
    objectPlayer = {"name": player.name}
    es.index(index="player", doc_type="players", id=i, document=objectPlayer)
    i+=1


i = 0
for coach in Coach.nodes:
    objectCoach = {"name": coach.name}
    es.index(index="coach", doc_type="coaches", id=i, body=objectCoach)
    i+=1

#Getting data from Elasticsearch
# player1 = es.get(index="player", doc_type="players", id= 0)
# coach1 = es.get(index="coach", doc_type="coaches", id= 0)

# print(player1)
# print(coach1)
    

