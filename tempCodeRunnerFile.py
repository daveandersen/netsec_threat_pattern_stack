    session.write_transaction(create_command, threat['matching_syntax'])
                session.write_transaction(create_use_command_relationship, fields['source_address'], threat['matching_syntax'])

