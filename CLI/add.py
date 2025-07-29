import json
from vector_store import add_question_to_vector_store

def load_json_and_add(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    result = add_question_to_vector_store(data)
    print(f"✅ Added to vector store with ID: {result}")


if __name__ == "__main__":
    load_json_and_add("../unanswered/BEWHOOP000000001.json") 
