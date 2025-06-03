import os
import json
from datetime import datetime

HISTORY_DIR = 'history'
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

def save_history(history_type, data):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{history_type}_{timestamp}.json'
    with open(os.path.join(HISTORY_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

def list_history(history_type):
    files = [f for f in os.listdir(HISTORY_DIR) if f.startswith(history_type)]
    return sorted(files, reverse=True)

def load_history(filename):
    with open(os.path.join(HISTORY_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)
