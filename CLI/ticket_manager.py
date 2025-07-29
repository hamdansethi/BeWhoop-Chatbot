import json
import re
import os
from datetime import datetime, timezone

UNANSWERED_DIR = "../unanswered"  # Folder to store individual unanswered files
TICKET_PREFIX = "BEWHOOP"
TICKET_DIGITS = 9

def ensure_unanswered_dir():
    """Ensure the unanswered folder exists."""
    os.makedirs(UNANSWERED_DIR, exist_ok=True)

def get_existing_ticket_ids():
    """Scan existing files in the unanswered directory to get ticket IDs."""
    ensure_unanswered_dir()
    files = os.listdir(UNANSWERED_DIR)
    ticket_ids = [
        re.match(rf"^{TICKET_PREFIX}(\d{{{TICKET_DIGITS}}})\.json$", f)
        for f in files
    ]
    return [
        f"{TICKET_PREFIX}{m.group(1)}"
        for m in ticket_ids if m is not None
    ]

def generate_ticket_id(existing_ids):
    """Generate a new unique ticket ID like BEWHOOP000000001."""
    numbers = [
        int(re.search(rf"{TICKET_PREFIX}(\d+)", t).group(1))
        for t in existing_ids
    ]
    next_number = max(numbers) + 1 if numbers else 1
    return f"{TICKET_PREFIX}{str(next_number).zfill(TICKET_DIGITS)}"

def save_unanswered_question_individual(
    question,
    user_contact,
    category=None,
    audience=None,
    tags=None
):
    """Save each unanswered question in its own JSON file under the 'unanswered' folder."""

    existing_ids = get_existing_ticket_ids()
    ticket_id = generate_ticket_id(existing_ids)

    entry = {
        "ticket_id": ticket_id,
        "question": question,
        "answer": "",
        "user_contact": user_contact,
        "category": category or "Uncategorized",
        "audience": audience or [],
        "tags": tags or [],
        "status": "unanswered",
        "created": datetime.now(timezone.utc).isoformat()
    }

    # Save as a separate file
    file_path = os.path.join(UNANSWERED_DIR, f"{ticket_id}.json")
    with open(file_path, "w") as f:
        json.dump(entry, f, indent=2)

    return ticket_id

# ticket = save_unanswered_question_individual(
#     question="How do I reset my password?",
#     user_contact={"email": "user@example.com", "whatsapp": "+123456789"},
#     category="Account",
#     audience=["Vendors"],
#     tags=["reset", "password"]
# )

# print(ticket)

