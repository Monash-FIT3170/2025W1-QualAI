import sys
import os

# Ensure backend modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from backend.chat.text_transformer.neo4j_interactor import Neo4JInteractor

# --- Connect to Neo4j ---
neo4j = Neo4JInteractor()

# --- 1) Query by subject: find all relationships for a given entity ---
subject_query = """
MATCH (s:Entity)-[r]->(o:Entity)
WHERE s.name = $subject
RETURN s.name AS subject, type(r) AS predicate, o.name AS object
"""
subject_params = {"subject": "Alice"}

subject_results = neo4j.run_cypher_query(subject_query, subject_params)

print("Query results by subject (Alice):")
for row in subject_results:
    print(f"{row['subject']} -[{row['predicate']}]-> {row['object']}")

# --- 2) Query by predicate: find all entity pairs connected by a specific relationship ---
predicate_query = """
MATCH (s:Entity)-[r]->(o:Entity)
WHERE type(r) = $predicate
RETURN s.name AS subject, type(r) AS predicate, o.name AS object
"""
predicate_params = {"predicate": "LOVES"}

predicate_results = neo4j.run_cypher_query(predicate_query, predicate_params)

print("\nQuery results by predicate (LOVES):")
for row in predicate_results:
    print(f"{row['subject']} -[{row['predicate']}]-> {row['object']}")
