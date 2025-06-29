
# arise_memory.py
import re
import json
import os

MEMORY_FILE = "arise_brain.json"

# Ensure memory file exists
def initialize_memory():
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w') as f:
            json.dump({}, f)

def load_memory():
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def handle_memory_query(query):
    initialize_memory()
    brain = load_memory()

    # Remember command
    remember_match = re.search(r"remember that (.+?) is (.+)", query)
    if remember_match:
        key = remember_match.group(1).strip().lower()
        value = remember_match.group(2).strip()
        brain[key] = value
        save_memory(brain)
        return f"Okay, I will remember that {key} is {value}."

    # Retrieve command
    retrieve_match = re.search(r"(what|when|where|who) (.*)\??", query)
    if retrieve_match:
        for key in brain:
            if key in query:
                return f"You told me that {key} is {brain[key]}."

    # Show all memory
    if "what do you remember" in query:
        if not brain:
            return "I don’t remember anything yet."
        return "Here’s what I remember: " + "; ".join([f"{k} is {v}" for k, v in brain.items()])

    return None
