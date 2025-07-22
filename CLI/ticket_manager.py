import json
import re
from datetime import datetime

def load_unanswered_kb(file_path="../unanswered_kb.json"):  # Adjusted default path
    """Load the unanswered questions knowledge base."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def generate_ticket_id(existing_ids, prefix="BEWHOOP", digits=7):
    """Generate a unique ticket ID."""
    numbers = [
        int(re.search(rf"{prefix}(\\d+)", t).group(1))
        for t in existing_ids if re.match(rf"{prefix}\\d+", t)
    ]
    next_number = max(numbers) + 1 if numbers else 1
    return f"{prefix}{str(next_number).zfill(digits)}"

def save_unanswered_ver_1(question, user_contact, category=None, audience=None, tags=None, file_path="../unanswered_kb.json"):  # Adjusted default path
    """Save an unanswered question to the knowledge base."""
    data = load_unanswered_kb(file_path)
    existing_ids = [entry["ticket_id"] for entry in data]

    ticket_id = generate_ticket_id(existing_ids)

    new_entry = {
        "ticket_id": ticket_id,
        "question": question,
        "answer": "",
        "user_contact": user_contact,
        "category": category or "Uncategorized",
        "audience": audience or [],
        "tags": tags or [],
        "status": "unanswered",
        "created": datetime.now().strftime("%Y-%m-%d")
    }

    data.append(new_entry)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return ticket_id

def save_unanswered_question_v2(question, user_contact, file_path="../unanswered_questions_v2.json"):  # Adjusted default path
    """Save an unanswered question to an alternate database."""
    entry = {
        "question": question,
        "email": user_contact.get("email"),
        "whatsapp": user_contact.get("whatsapp"),
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return f"TICKET-{len(data):04d}"