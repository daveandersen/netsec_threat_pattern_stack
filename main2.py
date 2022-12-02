import json
from pymongo import MongoClient
from neo4j import GraphDatabase
from Node import *
from NodeRelationship import *
from GetNodes import *
from CypherQuery import *
from elasticsearch7 import Elasticsearch
from graphdatascience import GraphDataScience

cluster = MongoClient("mongodb://localhost:27017")
db = cluster["neo4j"]
collection = db['ssh_commands']

driver = GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "sgunetsec"))
# gds = GraphDataScience("bolt://localhost:7687", auth=("neo4j", "sgunetsec"))
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
        # print(fields['source_address'])
        if(request == {}):
            request['description'] = "SSH Honeypot Cowrie"
        
        behavior = []
        i = 0
        for threat in threats:
            if(threat.get('matching_syntax') is None):
                print("hellooo no matching syntax")
                behavior.append(threat['unknown_syntax'])
                session.execute_write(create_command, threat['unknown_syntax'])
                session.execute_write(create_use_command_relationship, fields['source_address'], threat['unknown_syntax'])
                es.index(index="unknown_command", doc_type="unknown_commands", id = i, document=threat['unknown_syntax'])

            else:
                behavior.append(threat['matching_syntax'])
                session.execute_write(create_command, threat['matching_syntax'])
                session.execute_write(create_use_command_relationship, fields['source_address'], threat['matching_syntax'])
                
                session.execute_write(create_threat_category, threat['threat_category'])
                session.execute_write(create_threat_categorized_as_relationship, threat['matching_syntax'], threat['threat_category'])
            i+=1

        print(hash(tuple(behavior)))
        session.execute_write(create_behavior, hash(tuple(behavior)))
        session.execute_write(create_behavior_relationship, fields['source_address'], hash(tuple(behavior)))
                
        session.execute_write(create_source_address, fields['source_address'])
        session.execute_write(create_country_code, attacker_location['country_code'], attacker_location['country'])
        session.execute_write(create_target_node, request['description'])
        session.execute_write(create_target_port, fields['target_port'])
        session.execute_write(create_source_address_and_country_relationship, fields['source_address'], attacker_location['country_code'])
        session.execute_write(create_source_address_and_registered_country_relationship, fields['source_address'], attacker_location['country_code'])
        session.execute_write(create_source_address_and_target_port_relationship, fields['source_address'], fields['target_port'])
        session.execute_write(create_attack_relationship, fields['source_address'], request['description'])
    
    countries = get_country(session)
    categories = get_threat_category(session)
    # overallRelationship = get_overall_relationship(session)
    # print(overallRelationship)

    i = 0
    for country in countries.data():
        # print(country)
        es.index(index="country", doc_type="countries", id = i,document=country)
        i+=1

    attack_relationships = get_attacks_relationship(session)
    i = 0
    for attack in attack_relationships.data():
        # print(attack)
        # print(attack['p'][0]['source_address'])
        attack_temp_object = {
            "relationship": attack['p'][1],
            "properties": {
              "source": attack['p'][0]['source_address'],
              "target": attack['p'][2]['target']
            }
        }
        # print(attack_temp_object)
        es.index(index="attack", doc_type="attacks", id = i,document=attack_temp_object)
        i+=1

    # create_ip_commands_graph(session)
    ip_commands_similarity = create_ip_commands_graph_similarity(session)
    # print(ip_commands_similarity.data())

    i = 0
    for similarity in ip_commands_similarity.data():
        # print(similarity)
        es.index(index="ip_commands_similarity", doc_type="ip_commands_similarities", id = i, document=similarity)
        i+=1
        
    ip_behave_similarity = create_ip_commands_graph_similarity(session)
    print(ip_behave_similarity.data())
    i = 0
    for similarity in ip_behave_similarity.data():
        # print(similarity)
        es.index(index="ip_behave_similarity", doc_type="ip_behave_similarities", id = i, document=similarity)
        i+=1
driver.close()

# get all data from neo4j and then export to elasticsearch
        
