def create_source_address_and_country_relationship(tx, source_address, country_code):
    return tx.run ("""
        MATCH (source_address:SOURCE_ADDRESS {source_address: $source_address}), (country:COUNTRY {country_code: $country_code})
        MERGE (source_address)-[:LOCATED_IN]->(country)
    """, source_address=source_address, country_code=country_code
    )

def create_source_address_and_registered_country_relationship(tx, source_address, country_code):
    return tx.run("""
        MATCH(source_address:SOURCE_ADDRESS {source_address: $source_address}), (country:COUNTRY {country_code: $country_code})
        MERGE (source_address)-[:REGISTERED_IN]->(country)
    """, source_address=source_address, country_code=country_code
    )

def create_source_address_and_target_port_relationship(tx, source_address, target_port):
    return tx.run("""
        MATCH(source_address:SOURCE_ADDRESS {source_address: $source_address}), (target_port:TARGET_PORT {target_port: $target_port})
        MERGE (source_address)-[:AIMS_TO]->(target_port)
    """, source_address=source_address, target_port=target_port
    )

def create_attack_relationship(tx, source_address, target):
    return tx.run ("""
        MATCH (source_address:SOURCE_ADDRESS {source_address: $source_address}), (target:TARGET {target: $target})
        MERGE (source_address)-[:ATTACKS]->(target)
    """, source_address=source_address, target=target)

def create_use_command_relationship(tx, source_address, command):
    return tx.run ("""
        MATCH (source_address:SOURCE_ADDRESS {source_address: $source_address}), (command:COMMAND {command: $command})
        MERGE (source_address)-[:USE]->(command)
    """, source_address=source_address, command=command)
    
def create_threat_categorized_as_relationship(tx, command, threat_category):
    return tx.run ("""
        MATCH (command:COMMAND {command: $command}), (threat_category:THREAT_CATEGORY {threat_category: $threat_category})
        MERGE (command)-[:CATEGORIZED_AS]->(threat_category)
    """, command=command, threat_category=threat_category)
    
def create_behavior_relationship(tx, source_address, behavior):
    return tx.run ("""
        MATCH (source_address:SOURCE_ADDRESS {source_address: $source_address}), (behavior:BEHAVIOR {behavior: $behavior})
        MERGE (source_address)-[:BEHAVE]->(behavior)
    """, source_address=source_address, behavior=behavior)