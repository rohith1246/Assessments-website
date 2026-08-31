import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

uri = os.environ.get('DATABASE_URL', '')
if '&channel_binding=' in uri:
    uri = uri.split('&channel_binding=')[0]

print("Connecting to database...", flush=True)
conn = psycopg2.connect(uri, connect_timeout=15)
cur = conn.cursor()

migrations = [
    "ALTER TABLE assessment_questions ADD COLUMN IF NOT EXISTS question_type VARCHAR(20) DEFAULT 'mcq';",
    "ALTER TABLE assessment_questions ALTER COLUMN option_a DROP NOT NULL;",
    "ALTER TABLE assessment_questions ALTER COLUMN option_b DROP NOT NULL;",
    "ALTER TABLE assessment_questions ALTER COLUMN option_c DROP NOT NULL;",
    "ALTER TABLE assessment_questions ALTER COLUMN option_d DROP NOT NULL;",
    "ALTER TABLE assessment_questions ALTER COLUMN correct_answer TYPE TEXT;",
    "ALTER TABLE assessment_answers ALTER COLUMN selected_option TYPE TEXT;"
]

for sql in migrations:
    print(f"Executing: {sql}", flush=True)
    cur.execute(sql)

conn.commit()
print("[OK] Database migration applied successfully!", flush=True)
conn.close()
