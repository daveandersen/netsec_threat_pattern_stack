def create_country_code(tx, country_code, country_name):
    return tx.run(
        "MERGE (country: COUNTRY {country_code: $country_code, country_name: $country_name})",
        country_code=country_code, country_name=country_name
    )

def create_target_node(tx, target):
    return tx.run(
        "MERGE (target: TARGET {target: $target})",
        target=target
    )

def create_source_city(tx, source_city):
    return tx.run(
        "MERGE (source_city: source_CITY {source_city: $source_city})",
        source_city=source_city
    )

def create_target_country(tx, target_country):
    return tx.run(
        "MERGE (target_country: TARGET_COUNTRY {target_country: $target_country})",
        target_country=target_country
    )

def create_source_country(tx, source_country):
    return tx.run(
        "MERGE (source_country: SOURCE_COUNTRY {source_country: $source_country})",
        source_country=source_country
    )


def create_target_port(tx, target_port):
    return tx.run(
        "MERGE (target_port: TARGET_PORT {target_port: $target_port})",
        target_port=target_port
    )

def create_source_address(tx, source_address):
    return tx.run(
        "MERGE (source_address: SOURCE_ADDRESS {source_address: $source_address})",
        source_address=source_address
    )

def create_command(tx, command):
    return tx.run(
        "MERGE (command: COMMAND{command: $command})",
        command=command
    )
    
def create_threat_category(tx, threat_category):
    return tx.run(
        "MERGE (threat_category: THREAT_CATEGORY {threat_category: $threat_category})",
        threat_category = threat_category
    )
    
def create_threat_purpose(tx, threat_purpose):
    return tx.run(
        "MERGE (threat_purpose: THREAT_PURPOSE {threat_purpose: $threat_purpose})",
        threat_purpose = threat_purpose
    )
    
def create_threat_phase(tx, threat_phase):
    return tx.run(
        "MERGE (threat_phase: THREAT_PHASE {threat_phase: $threat_phase})",
        threat_phase = threat_phase
    )
    

def create_behavior(tx, behavior):
    return tx.run(
        "MERGE (behavior: BEHAVIOR {behavior: $behavior})",
        behavior = behavior
    )
    
def delete_behavior(tx):
    return tx.run ("""
        MATCH (n:BEHAVIOR)
        DETACH DELETE n
    """)
    
def create_mitre_tactic(tx, mitre_tactic):
    return tx.run(
        "MERGE (mitre_tactic:MITRE_TACTIC {mitre_tactic: $mitre_tactic})",
        mitre_tactic = mitre_tactic
    )
    
    

