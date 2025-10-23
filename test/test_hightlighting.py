
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from chat.database_client.vector_database import VectorDatabase

db = VectorDatabase()

db.clear_database()

transcript = (
        "Alice discussed her experience with QualAI in detail. "
        "She mentioned it improved her workflow drastically. "
        "Later, Bob talked about unrelated topics like his holiday. "
        "Finally, Alice suggested adding offline support to QualAI."
    )

highlights = [
    {"start": 0, "end": 53, "priority": 1},    # positive (high)
    {"start": 53, "end": 105, "priority": 0},  # negative (low)
    {"start": 105, "end": 159, "priority": -1} # excluded
]

db.store_entries(transcript, "test", highlights)

print("Search 1: QualAI workflows")
print(db.search_priority(" workflows"))

print("Search 2: Offline support")
print(db.search_priority("Offline support ti QualAI"))

db.close_driver()

