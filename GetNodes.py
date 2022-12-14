def get_target_node(tx):
    return tx.run(
        "MATCH (n:TARGET) RETURN n"
    ) 

def get_country(tx):
 return tx.run(
        "MATCH (n:COUNTRY) RETURN n"
    )
 
def get_threat_category(tx):
    return tx.run(
        "MATCH (n:THREAT_CATEGORY) RETURN n"
    ) 

def get_target_port(tx):
 return tx.run(
        "MATCH (n:TARGET_PORT) RETURN n"
    ) 

def get_source_address(tx):
 return tx.run(
        "MATCH (n:SOURCE_ADDRESS) RETURN n"
    )

def get_aims_to_relationship(tx):
 return tx.run(
        "MATCH p=()-[r:AIMS_TO]->() RETURN p"
    )

def get_attacks_relationship(tx):
 return tx.run(
        "MATCH p=()-[r:ATTACKS]->() RETURN p"
    )

def get_registered_in_relationship(tx):
 return tx.run(
        "MATCH p=()-[r:LOCATED_IN]->() RETURN p"
    )

def get_registered_in_relationship(tx):
 return tx.run(
        "MATCH p=()-[r:REGISTERED_IN]->() RETURN p"
    )
 
def get_threat_behaviour_categorization(tx):
    return tx.run(
        "MATCH p=()-[r:USE]-()-[q:CATEGORIZED_AS]-()-[a:FOR]-()-[b:IN_PHASE]->() RETURN p"
    )


def get_overall_relationship(tx):
 return tx.run(
        "MATCH p=()-->() RETURN p"
    )


