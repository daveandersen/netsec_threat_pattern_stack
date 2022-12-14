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
es = Elasticsearch(HOST="http://localhost", PORT=9200)

with driver.session() as session:
    cursor = collection.find({})
    delete_behavior(session)
    
    i = 0
    for document in cursor:
        fields = document['fields']
        request = document['request_']
        country = document['honeypot_country']
        attacker_location = document['geo_location']
        threats = document['threat']

        if(request == {}):
            request['description'] = "SSH Honeypot Cowrie"
        
        behavior = []

        for threat in threats:

            if(threat.get('matching_syntax') is None):
                behavior.append(threat['unknown_syntax'])
                session.execute_write(create_command, threat['unknown_syntax'])
                session.execute_write(create_use_command_relationship, fields['source_address'], threat['unknown_syntax'])
                es.index(index="unknown_command", doc_type="unknown_commands", id = i, document=threat)
                i+=1
            else:
                behavior.append(threat['matching_syntax'])
                session.execute_write(create_command, threat['matching_syntax'])
                session.execute_write(create_use_command_relationship, fields['source_address'], threat['matching_syntax'])
                #Start threat pattern behavior categorization
                session.execute_write(create_threat_category, threat['threat_category'])
                session.execute_write(create_threat_purpose, threat['threat_purpose'])
                session.execute_write(create_threat_phase, threat['threat_phase'])
                session.execute_write(create_mitre_tactic, threat['mitre_tactic'])
                session.execute_write(create_threat_categorized_as_relationship, threat['matching_syntax'], threat['threat_category'])
                session.execute_write(create_threat_for_relationship, threat['threat_category'], threat['threat_purpose'])
                session.execute_write(create_threat_in_phase_relationship, threat['threat_purpose'], threat['threat_phase'])
                session.execute_write(create_threat_use_tactic_relationship, fields['source_address'], threat['mitre_tactic'])
                behavior_category_temp = {
                    "source_address": fields['source_address'],
                    "command": threat['matching_syntax'],
                    "threat_category": threat['threat_category'],
                    "threat_purpose": threat['threat_purpose'],
                    "threat_phase": threat['threat_phase']
                }
                hashedID = hash(str(i)+fields['source_address'])
                print(hashedID)
                print(behavior_category_temp)
                print("\n")
                es.index(index="threat_behavior", doc_type="threat_behaviors", id = i, document=behavior_category_temp)
                es.index(index="threat", doc_type="threats", id = i, document=threat)    
                i+=1
                  
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

        es.index(index="country", doc_type="countries", id = i,document=country)
        i+=1
        
    # threat_behaviour_categories = get_threat_behaviour_categorization(session)
    # i = 0
    # for behavior_category in threat_behaviour_categories.data():
    #     behavior_category_temp = {
    #         "source_address": behavior_category['p'][0]['source_address'],
    #         "command": behavior_category['p'][2]['command'],
    #         "threat_category": behavior_category['p'][4]['threat_category'],
    #         "threat_purpose": behavior_category['p'][6]['threat_purpose'],
    #         "threat_phase": behavior_category['p'][8]['threat_phase']
    #     }
    #     es.index(index="threat_behavior", doc_type="threat_behaviors", id = i, document=behavior_category_temp)
    #     i+=1

    attack_relationships = get_attacks_relationship(session)
    i = 0
    for attack in attack_relationships.data():
        attack_temp_object = {
            "relationship": attack['p'][1],
            "properties": {
              "source": attack['p'][0]['source_address'],
              "target": attack['p'][2]['target']
            }
        }

        es.index(index="attack", doc_type="attacks", id = i,document=attack_temp_object)
        i+=1

    create_ip_commands_graph(session)
    ip_commands_similarity = create_ip_commands_graph_similarity(session)


    i = 0
    for similarity1 in ip_commands_similarity.data():
        es.index(index="ip_commands_similarity", doc_type="ip_commands_similarities", id = i, document=similarity1)
        i+=1
    
    create_ip_behave_graph(session)    
    ip_behave_similarity = create_ip_behave_graph_similarity(session)
    i = 0
    for similarity2 in ip_behave_similarity.data():
        es.index(index="ip_behave_similarity", doc_type="ip_behave_similarities", id = i, document=similarity2)
        i+=1
driver.close()

# get all data from neo4j and then export to elasticsearch
        
