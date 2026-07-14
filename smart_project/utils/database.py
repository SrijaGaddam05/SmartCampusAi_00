"""
JSON-based database utility for SmartCampusAI.
Provides thread-safe load, save, insert, update, delete, and search functionality.
Auto-creates required files if missing.
"""
import os
import json
import threading
from typing import List, Dict, Any, Callable

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
DB_LOCK = threading.Lock()

# Ensure database directory exists
os.makedirs(DB_DIR, exist_ok=True)

def get_file_path(filename: str) -> str:
    """Return the absolute path of a JSON file in the database directory."""
    if not filename.endswith(".json"):
        filename = f"{filename}.json"
    return os.path.join(DB_DIR, filename)

def init_db_file(filename: str, default_data: Any) -> None:
    """Initialize a database file with default data if it doesn't exist."""
    path = get_file_path(filename)
    if not os.path.exists(path):
        with DB_LOCK:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=4)

# Initialize expected files with default structures
init_db_file("users", [])
init_db_file("activity", [])
init_db_file("settings", {"theme": "Dark", "notifications_enabled": True, "maintenance_mode": False})
# We also want to support storing student and faculty lists
init_db_file("students", [])
init_db_file("faculty", [])
init_db_file("attendance", [])
init_db_file("timetable", [])

def load_json(filename: str) -> Any:
    """Load and return the JSON data from the specified database file."""
    path = get_file_path(filename)
    # Ensure it exists
    if not os.path.exists(path):
        return [] if filename != "settings.json" else {}
        
    with DB_LOCK:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading {filename}: {e}")
            # Return empty structure as fallback
            return {} if "settings" in filename else []

def save_json(filename: str, data: Any) -> bool:
    """Save data to the specified database file in a pretty JSON format."""
    path = get_file_path(filename)
    with DB_LOCK:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except IOError as e:
            print(f"Error saving {filename}: {e}")
            return False

def insert(filename: str, item: Dict[str, Any]) -> bool:
    """Insert a new item (dict) into a JSON list database."""
    data = load_json(filename)
    if not isinstance(data, list):
        return False
    data.append(item)
    return save_json(filename, data)

def update(filename: str, key: str, value: Any, new_item: Dict[str, Any]) -> bool:
    """
    Update items in a JSON list database matching key=value with new_item properties.
    """
    data = load_json(filename)
    if not isinstance(data, list):
        # If it's a dict (like settings.json), perform a dictionary merge update
        if isinstance(data, dict):
            data.update(new_item)
            return save_json(filename, data)
        return False
        
    updated = False
    for i, item in enumerate(data):
        if item.get(key) == value:
            data[i].update(new_item)
            updated = True
            
    if updated:
        return save_json(filename, data)
    return False

def delete(filename: str, key: str, value: Any) -> bool:
    """Delete items in a JSON list database matching key=value."""
    data = load_json(filename)
    if not isinstance(data, list):
        return False
        
    initial_length = len(data)
    filtered_data = [item for item in data if item.get(key) != value]
    
    if len(filtered_data) < initial_length:
        return save_json(filename, filtered_data)
    return False

def search(filename: str, key: str, value: Any) -> List[Dict[str, Any]]:
    """Search for items in a JSON database matching key=value."""
    data = load_json(filename)
    if not isinstance(data, list):
        return []
        
    # Handle string comparison case-insensitive search if relevant, otherwise strict match
    results = []
    for item in data:
        item_val = item.get(key)
        if isinstance(item_val, str) and isinstance(value, str):
            if item_val.lower() == value.lower():
                results.append(item)
        elif item_val == value:
            results.append(item)
    return results
