import sqlite3
import random
import string

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # ຕារາງសម្រាប់រក្សាទុក Key
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_code TEXT UNIQUE,
            plan_type TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def generate_key_code(plan_type):
    # បង្កើត Key បែបស្វ័យប្រវត្តិ ឧ. YT-1_MONTH-XXXX
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=8))
    key_code = f"YT-{plan_type.upper()}-{random_part}"
    return key_code