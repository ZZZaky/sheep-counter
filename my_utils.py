import json
import os
from datetime import datetime
import pandas as pd

HISTORY_FILE = 'history.json'

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        # Если файл повреждён, возвращаем пустой список
        return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def add_record(image_path, sheep_count):
    history = load_history()
    record = {
        "id": len(history) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "image_path": image_path,
        "sheep_count": sheep_count
    }
    history.append(record)
    save_history(history)
    return record

def generate_excel_report(filename='report.xlsx'):
    history = load_history()
    df = pd.DataFrame(history)
    df.to_excel(filename, index=False)
    return filename
