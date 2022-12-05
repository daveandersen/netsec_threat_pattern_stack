def create_ip_commands_graph(tx):
    return tx.run ("""
        CALL gds.graph.project.cypher(
        'ipAndCommands',
        'MATCH (n) WHERE n:SOURCE_ADDRESS OR n:COMMAND RETURN id(n) AS id, labels(n) AS labels',
        'MATCH (n)-[r:USE]->(m) RETURN id(n) AS source, id(m) AS target, type(r) AS type')
        YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipCount AS rels
    """)

def create_ip_commands_graph_similarity(tx):
    return tx.run ("""
        CALL gds.nodeSimilarity.stream('ipAndCommands')
        YIELD node1, node2, similarity
        RETURN gds.util.asNode(node1).source_address AS IP1, gds.util.asNode(node2).source_address AS IP2, similarity
        ORDER BY similarity DESCENDING, IP1, IP2
    """) 

def create_ip_behave_graph(tx):
    return tx.run ("""
        CALL gds.graph.project.cypher(
        'ipAndBehavior',
        'MATCH (n) WHERE n:SOURCE_ADDRESS OR n:BEHAVIOR RETURN id(n) AS id, labels(n) AS labels',
        'MATCH (n)-[r:BEHAVE]->(m) RETURN id(n) AS source, id(m) AS target, type(r) AS type')
        YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipCount AS rels           
    """)

   
def create_ip_behave_graph_similarity(tx):
    return tx.run ("""
        CALL gds.nodeSimilarity.stream('ipAndBehavior')
        YIELD node1, node2, similarity
        RETURN gds.util.asNode(node1).source_address AS IP1, gds.util.asNode(node2).source_address AS IP2, similarity
        ORDER BY similarity DESCENDING, IP1, IP2
    """)

def delete_behavior(tx):
    return tx.run ("""
        MATCH (n:BEHAVIOR)
        DETACH DELETE n
    """)


