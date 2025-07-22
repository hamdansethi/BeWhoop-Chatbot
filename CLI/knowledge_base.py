import json

def load_knowledge_base(file_path="../bewhoop_kb.json"):  # Adjusted default path
    """Load the knowledge base from a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)