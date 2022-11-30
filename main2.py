from pymongo import MongoClient
from neo4j import GraphDatabase
from Node import *
from NodeRelationship import *
from GetNodes import *
from elasticsearch7 import Elasticsearch


cluster = MongoClient("mongodb://localhost:27017")
db = cluster["netsec_project"]
collection = db['ssh_commands']

driver = GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "sgunetsec"))

es = Elasticsearch(HOST="http://localhost", PORT=9200)


with driver.session() as session:
    cursor = collection.find({})
    for document in cursor:
        fields = document['fields']
        request = document['request_']
        country = document['honeypot_country']
        attacker_location = document['geo_location']
        threats = document['threat']
        # print(threats)
        if(request == {}):
            request['description'] = "SSH Honeypot Cowrie"

        for threat in threats:
            print(fields['source_address'])
            # print(threat.get('matching_syntax') is None)
            if(threat.get('matching_syntax') is None):
                 session.write_transaction(create_command, threat['unknown_syntax'])
                 session.write_transaction(create_use_command_relationship, fields['source_address'], threat['unknown_syntax'])
            else:
                session.write_transaction(create_command, threat['matching_syntax'])
                session.write_transaction(create_use_command_relationship, fields['source_address'], threat['matching_syntax'])


        session.write_transaction(create_source_address, fields['source_address'])
        session.write_transaction(create_country_code, attacker_location['country_code'], attacker_location['country'])
        session.write_transaction(create_target_node, request['description'])
        session.write_transaction(create_target_port, fields['target_port'])
        session.write_transaction(create_source_address_and_country_relationship, fields['source_address'], attacker_location['country_code'])
        session.write_transaction(create_source_address_and_registered_country_relationship, fields['source_address'], attacker_location['country_code'])
        session.write_transaction(create_source_address_and_target_port_relationship, fields['source_address'], fields['target_port'])
        session.write_transaction(create_attack_relationship, fields['source_address'], request['description'])
    
    countries = get_country(session)
    i = 0
    for country in countries.data():
        print(country)
        es.index(index="country", doc_type="countries", id = i,document=country)
        i+=1

    # attack_relationships = get_attacks_relationship(session)
    # i = 0
    # for attack in attack_relationships.data():
    #     print(attack)
    #     es.index(index="attack", doc_type="attacks", id = i,document=attack)
    #     i+=1

driver.close()

# get all data from neo4j and then export to elasticsearch
        
