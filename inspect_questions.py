import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("--- ID 10 (Screening Test - Java) Questions ---")
cur.execute("SELECT id, question, question_type, correct_answer FROM assessment_questions WHERE assessment_id = 10 ORDER BY id;")
for q in cur.fetchall():
    print(f"[{q[0]}] ({q[2]}) {q[1][:80]}... => {q[3]}")

print("\n--- ID 15 (Technical Round 2 - Java) Questions ---")
cur.execute("SELECT id, question, question_type, correct_answer FROM assessment_questions WHERE assessment_id = 15 ORDER BY id;")
for q in cur.fetchall():
    print(f"[{q[0]}] ({q[2]}) {q[1][:80]}... => {q[3]}")

conn.close()
