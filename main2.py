from pymongo import MongoClient
from neo4j import GraphDatabase
from Node import *
from NodeRelationship import *
from GetNodes import *

cluster = MongoClient("mongodb://localhost:27017")
db = cluster["netsec_project"]
collection = db['ssh_commands']

driver = GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "sgunetsec"))

with driver.session() as session:
    cursor = collection.find({})
    for document in cursor:
        fields = document['fields']
        request = document['request_']
        country = document['honeypot_country']
        attacker_location = document['geo_location']
        threat = document['threat']

        session.write_transaction(create_source_address, fields['source_address'])
        session.write_transaction(create_country_code, attacker_location['country_code'], attacker_location['country'])
        session.write_transaction(create_target_node, request['description'])
        session.write_transaction(create_target_port, fields['target_port'])
        session.write_transaction(create_source_address_and_country_relationship, fields['source_address'], attacker_location['country_code'])
        session.write_transaction(create_source_address_and_registered_country_relationship, fields['source_address'], attacker_location['country_code'])
        session.write_transaction(create_source_address_and_target_port_relationship, fields['source_address'], fields['target_port'])
        session.write_transaction(create_attack_relationship, fields['source_address'], request['description'])

    placeholder = session.read_transaction(get_country)
    print(placeholder.data())
    print(placeholder.single())
driver.close()

# get all data from neo4j and then export to elasticsearch
        
