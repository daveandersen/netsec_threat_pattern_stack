# def create_target_node(tx, target_name, target_country, target_address, target_port, target_protocol):
#     return tx.run(
#         "MERGE (target:TARGET {target_name: $target_name, target_country: $target_country, target_address: $target_address, target_port: $target_port, target_protocol: $target_protocol})",
#         target_name=target_name, target_country=target_country, target_address=target_address,target_port=target_port, target_protocol=target_protocol
#     )

# def create_source_node(tx, source_address, source_country, source_port, source_protocol):
#     return tx.run(
#         "MERGE (source:SOURCE {source_address: $source_address, source_country: $source_country, source_port: $source_port, source_protocol: $source_protocol})",
#         source_address=source_address, source_country=source_country, source_port=source_port, source_protocol=source_protocol
#     )

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

